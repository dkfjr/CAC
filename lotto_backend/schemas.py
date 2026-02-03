from pydantic import BaseModel, field_validator
from typing import List


# ===== 전화번호 인증 =====
class PhoneSendRequest(BaseModel):
    phone_number: str

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, v):
        # 숫자만, 010으로 시작, 10~11자리
        if not v.isdigit():
            raise ValueError("전화번호는 숫자만 입력 가능합니다.")
        if not v.startswith("01"):
            raise ValueError("올바르지 않은 전화번호입니다.")
        if len(v) < 10 or len(v) > 11:
            raise ValueError("전화번호 길이가 올바르지 않습니다.")
        return v

class PhoneVerifyRequest(BaseModel):
    phone_number: str
    code: str                                # 인증 코드


# ===== 학번 등록 =====
class StudentRegisterRequest(BaseModel):
    student_id: str

    @field_validator("student_id")
    @classmethod
    def validate_student_id(cls, v):
        # 학번은 숫자만, 길이 제한 (예: 9~10자리)
        if not v.isdigit():
            raise ValueError("학번은 숫자만 입력 가능합니다.")
        if len(v) < 5 or len(v) > 15:
            raise ValueError("학번 길이가 올바르지 않습니다.")
        return v


# ===== 로또 참여 =====
class LottoEntryRequest(BaseModel):
    draw_id: int                             # 참여할 회차
    numbers: List[int]                       # 선택한 번호 리스트

    @field_validator("numbers")
    @classmethod
    def validate_numbers(cls, v):
        # 중복 번호 확인
        if len(v) != len(set(v)):
            raise ValueError("중복된 번호가 있습니다.")
        return v


# ===== 공통 응답 =====
class MessageResponse(BaseModel):
    message: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    message: str

class LottoConfigResponse(BaseModel):
    draw_id: int
    number_count: int
    number_range_min: int
    number_range_max: int

class LottoEntryResponse(BaseModel):
    entry_id: int
    draw_id: int
    numbers: List[int]
    message: str


# ===== 당첨자 관련 =====
class WinnerRegisterRequest(BaseModel):
    draw_id: int        # 당첨된 회차
    student_id: str     # 당첨된 학번

class WinnerResponse(BaseModel):
    draw_id: int
    student_id: str
    message: str
