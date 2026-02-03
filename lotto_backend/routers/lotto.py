from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import User, LottoDrawConfig, LottoEntry, LottoWinner
from schemas import (
    LottoEntryRequest, LottoConfigResponse, LottoEntryResponse,
    MessageResponse, WinnerRegisterRequest, WinnerResponse
)
from utils import get_current_user_phone

router = APIRouter(prefix="/api/lotto", tags=["로또"])


# ===== 현재 회차 설정값 조회 =====
@router.get("/config", response_model=LottoConfigResponse)
def get_lotto_config(draw_id: int, db: Session = Depends(get_db)):
    """특정 회차의 번호 개수, 범위 등 설정값 조회"""
    config = db.query(LottoDrawConfig).filter(LottoDrawConfig.draw_id == draw_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="해당 회차가 존재하지 않습니다.")

    return {
        "draw_id": config.draw_id,
        "number_count": config.number_count,
        "number_range_min": config.number_range_min,
        "number_range_max": config.number_range_max,
    }


# ===== 로또 번호 제출 =====
@router.post("/entry", response_model=LottoEntryResponse)
def submit_lotto_entry(
    request: LottoEntryRequest,
    phone_number: str = Depends(get_current_user_phone),
    db: Session = Depends(get_db)
):
    # 1. 현재 유저 조회
    user = db.query(User).filter(User.phone_number == phone_number).first()
    if not user:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

    # 2. 학번 등록 완료 여부
    if not user.student_id:
        raise HTTPException(status_code=400, detail="학번을 먼저 등록해주세요.")

    # 3. 회차 설정값 조회
    config = db.query(LottoDrawConfig).filter(LottoDrawConfig.draw_id == request.draw_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="해당 회차가 존재하지 않습니다.")

    # 4. 이전 회차에서 당첨된 학번인지 확인 (당첨자는 다음 회차 참여 불가)
    previous_winner = (
        db.query(LottoWinner)
        .filter(
            LottoWinner.student_id == user.student_id,
            LottoWinner.draw_id == request.draw_id - 1   # 바로 직전 회차 당첨 여부
        )
        .first()
    )
    if previous_winner:
        raise HTTPException(
            status_code=400,
            detail=f"회차 {request.draw_id - 1}에서 당첨되었으므로, 이번 회차({request.draw_id})에는 참여할 수 없습니다."
        )

    # 5. 번호 개수 검증
    if len(request.numbers) != config.number_count:
        raise HTTPException(
            status_code=400,
            detail=f"번호는 정확히 {config.number_count}개를 선택해야 합니다."
        )

    # 6. 번호 범위 검증
    for num in request.numbers:
        if num < config.number_range_min or num > config.number_range_max:
            raise HTTPException(
                status_code=400,
                detail=f"번호는 {config.number_range_min}~{config.number_range_max} 범위 내에서 선택해야 합니다."
            )

    # 7. 같은 회차에 이미 참여한 경우 확인
    existing_entry = (
        db.query(LottoEntry)
        .filter(LottoEntry.user_id == user.id, LottoEntry.draw_id == request.draw_id)
        .first()
    )
    if existing_entry:
        raise HTTPException(status_code=400, detail="이 회차에 이미 참여하였습니다.")

    # ✅ 모든 검증 통과 → 저장
    numbers_str = ",".join(str(n) for n in sorted(request.numbers))

    entry = LottoEntry(
        user_id=user.id,
        draw_id=request.draw_id,
        selected_numbers=numbers_str,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)

    return {
        "entry_id": entry.id,
        "draw_id": entry.draw_id,
        "numbers": [int(n) for n in entry.selected_numbers.split(",")],
        "message": "로또 참여가 완료되었습니다!"
    }


# ===== 내 참여 기록 조회 =====
@router.get("/my-entry", response_model=LottoEntryResponse)
def get_my_entry(
    draw_id: int,
    phone_number: str = Depends(get_current_user_phone),
    db: Session = Depends(get_db)
):
    """특정 회차에서 내가 제출한 번호 조회"""
    user = db.query(User).filter(User.phone_number == phone_number).first()
    if not user:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

    entry = (
        db.query(LottoEntry)
        .filter(LottoEntry.user_id == user.id, LottoEntry.draw_id == draw_id)
        .first()
    )
    if not entry:
        raise HTTPException(status_code=404, detail="해당 회차의 참여 기록이 없습니다.")

    return {
        "entry_id": entry.id,
        "draw_id": entry.draw_id,
        "numbers": [int(n) for n in entry.selected_numbers.split(",")],
        "message": "참여 기록 조회 완료"
    }


# ===== 당첨자 등록 (관리자용) =====
# 당첨 발표 후 관리자가 당첨자 학번을 등록하는 엔드포인트
# → 등록되면 해당 학번은 다음 회차 참여 불가
@router.post("/winner", response_model=WinnerResponse)
def register_winner(request: WinnerRegisterRequest, db: Session = Depends(get_db)):
    """당첨자 등록 (학번 + 회차)"""

    # 회차 확인
    config = db.query(LottoDrawConfig).filter(LottoDrawConfig.draw_id == request.draw_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="해당 회차가 존재하지 않습니다.")

    # 이미 같은 회차에서 같은 학번이 당첨된 경우
    existing = (
        db.query(LottoWinner)
        .filter(LottoWinner.draw_id == request.draw_id, LottoWinner.student_id == request.student_id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="이미 등록된 당첨자입니다.")

    # 학번으로 유저 조회
    user = db.query(User).filter(User.student_id == request.student_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="해당 학번의 유저가 존재하지 않습니다.")

    # 당첨자 저장
    winner = LottoWinner(
        draw_id=request.draw_id,
        user_id=user.id,
        student_id=request.student_id,
    )
    db.add(winner)
    db.commit()

    return {
        "draw_id": request.draw_id,
        "student_id": request.student_id,
        "message": f"회차 {request.draw_id} 당첨자 등록 완료. 다음 회차({request.draw_id + 1})에는 참여할 수 없습니다."
    }


# ===== 당첨자 목록 조회 =====
@router.get("/winners", response_model=list[WinnerResponse])
def get_winners(draw_id: int, db: Session = Depends(get_db)):
    """특정 회차의 당첨자 목록 조회"""
    winners = db.query(LottoWinner).filter(LottoWinner.draw_id == draw_id).all()

    return [
        {
            "draw_id": w.draw_id,
            "student_id": w.student_id,
            "message": f"회차 {w.draw_id} 당첨자"
        }
        for w in winners
    ]
