from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import StudentRegisterRequest, MessageResponse
from utils import get_current_user_phone

router = APIRouter(prefix="/api/user", tags=["사용자"])


# ===== 학번 중복 확인 =====
@router.get("/check-duplicate", response_model=MessageResponse)
def check_duplicate_student(student_id: str, db: Session = Depends(get_db)):
    """학번이 이미 등록되어 있는지 확인 (GET 파라미터로 받음)"""
    existing = db.query(User).filter(User.student_id == student_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="이미 등록된 학번입니다.")
    return {"message": "사용 가능한 학번입니다."}


# ===== 학번 등록 =====
@router.post("/register", response_model=MessageResponse)
def register_student(
    request: StudentRegisterRequest,
    phone_number: str = Depends(get_current_user_phone),   # JWT에서 전화번호 자동 추출
    db: Session = Depends(get_db)
):
    """
    학번 등록
    - JWT 토큰이 유효한 경우에만 접근 가능
    - 전화번호 인증 완료된 유저만 등록 가능
    """
    # 현재 유저 조회
    user = db.query(User).filter(User.phone_number == phone_number).first()
    if not user:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

    # 전화번호 인증 완료 여부 확인
    if not user.is_verified:
        raise HTTPException(status_code=400, detail="전화번호 인증을 먼저 완료해주세요.")

    # 이미 학번이 등록된 경우
    if user.student_id is not None:
        raise HTTPException(status_code=400, detail="학번이 이미 등록되어 있습니다.")

    # 학번 중복 확인
    existing = db.query(User).filter(User.student_id == request.student_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="이미 등록된 학번입니다.")

    # 학번 저장
    user.student_id = request.student_id
    db.commit()

    return {"message": "학번이 등록되었습니다."}
