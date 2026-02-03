import random
import string
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import User, PhoneVerification
from schemas import PhoneSendRequest, PhoneVerifyRequest, MessageResponse, TokenResponse
from sms_service import send_verification_sms
from utils import create_access_token
from config import settings

router = APIRouter(prefix="/api/auth", tags=["인증"])


def generate_code(length: int) -> str:
    """랜덤 숫자 코드 생성"""
    return "".join(random.choices(string.digits, k=length))


# ===== 전화번호 인증 코드 전송 =====
@router.post("/phone/send", response_model=MessageResponse)
def send_phone(request: PhoneSendRequest, db: Session = Depends(get_db)):
    phone_number = request.phone_number

    # 최근 1분 내 발급한 코드가 있으면 재발급 제한 (스팸 방지)
    recent = (
        db.query(PhoneVerification)
        .filter(PhoneVerification.phone_number == phone_number)
        .order_by(PhoneVerification.created_at.desc())
        .first()
    )
    if recent and recent.created_at + timedelta(minutes=1) > datetime.utcnow():
        raise HTTPException(status_code=400, detail="잠깐 후에 다시 시도해주세요. (1분 쿨다운)")

    # 인증 코드 생성
    code = generate_code(settings.VERIFICATION_CODE_LENGTH)

    # DB에 저장
    verification = PhoneVerification(
        phone_number=phone_number,
        code=code,
        expires_at=datetime.utcnow() + timedelta(minutes=settings.VERIFICATION_EXPIRE_MINUTES),
        is_used=False,
        attempts=0,
    )
    db.add(verification)
    db.commit()

    # SMS 전송
    success = send_verification_sms(phone_number, code)
    if not success:
        db.rollback()
        raise HTTPException(status_code=500, detail="SMS 전송에 실패했습니다. 잠깐 후에 다시 시도해주세요.")

    return {"message": "인증 코드가 전송되었습니다."}


# ===== 전화번호 인증 코드 검증 =====
@router.post("/phone/verify", response_model=TokenResponse)
def verify_phone(request: PhoneVerifyRequest, db: Session = Depends(get_db)):
    phone_number = request.phone_number
    code = request.code

    # 최신 인증 코드 조회
    verification = (
        db.query(PhoneVerification)
        .filter(PhoneVerification.phone_number == phone_number, PhoneVerification.is_used == False)
        .order_by(PhoneVerification.created_at.desc())
        .first()
    )

    if not verification:
        raise HTTPException(status_code=400, detail="발급된 인증 코드가 없습니다.")

    # 최대 시도 횟수 초과
    if verification.attempts >= settings.MAX_VERIFICATION_ATTEMPTS:
        raise HTTPException(status_code=400, detail="시도 횟수가 초과되었습니다. 코드를 다시 발급받아주세요.")

    # 만료 확인
    if verification.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="인증 코드가 만료되었습니다. 다시 발급받아주세요.")

    # 코드 일치 확인
    if verification.code != code:
        verification.attempts += 1
        db.commit()
        remaining = settings.MAX_VERIFICATION_ATTEMPTS - verification.attempts
        raise HTTPException(status_code=400, detail=f"코드가 일치하지 않습니다. 남은 시도 횟수: {remaining}")

    # ✅ 코드 일치 → 인증 완료
    verification.is_used = True
    db.commit()

    # 유저가 없으면 새로 생성
    user = db.query(User).filter(User.phone_number == phone_number).first()
    if not user:
        user = User(phone_number=phone_number, is_verified=True)
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        user.is_verified = True
        db.commit()

    # JWT 토큰 생성 및 반환
    token = create_access_token(data={"phone_number": phone_number, "user_id": user.id})

    return {
        "access_token": token,
        "token_type": "bearer",
        "message": "전화번호 인증이 완료되었습니다."
    }
