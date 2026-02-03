from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


# ===== 사용자 테이블 =====
class User(Base):
    __tablename__ = "users"

    id            = Column(Integer, primary_key=True, index=True, autoincrement=True)
    phone_number  = Column(String, unique=True, index=True, nullable=False)
    student_id    = Column(String(20), unique=True, index=True, nullable=True)  # 학번 (인증 후 등록)
    is_verified   = Column(Boolean, default=False)                              # 전화번호 인증 완료 여부
    created_at    = Column(DateTime, default=datetime.utcnow)

    # 관계
    lotto_entries = relationship("LottoEntry", back_populates="user")


# ===== 전화번호 인증 테이블 =====
class PhoneVerification(Base):
    __tablename__ = "phone_verifications"

    id           = Column(Integer, primary_key=True, index=True, autoincrement=True)
    phone_number = Column(String, index=True, nullable=False)
    code         = Column(String, nullable=False)
    expires_at   = Column(DateTime, nullable=False)
    is_used      = Column(Boolean, default=False)
    attempts     = Column(Integer, default=0)
    created_at   = Column(DateTime, default=datetime.utcnow)


# ===== 로또 회차 설정 테이블 =====
class LottoDrawConfig(Base):
    __tablename__ = "lotto_draw_config"

    id               = Column(Integer, primary_key=True, index=True, autoincrement=True)
    draw_id          = Column(Integer, unique=True, index=True, nullable=False)
    number_count     = Column(Integer, nullable=False, default=7)
    number_range_min = Column(Integer, nullable=False, default=1)
    number_range_max = Column(Integer, nullable=False, default=45)
    created_at       = Column(DateTime, default=datetime.utcnow)

    # 관계
    entries = relationship("LottoEntry", back_populates="config")


# ===== 로또 참여 테이블 =====
class LottoEntry(Base):
    __tablename__ = "lotto_entries"

    id               = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id          = Column(Integer, ForeignKey("users.id"), nullable=False)
    draw_id          = Column(Integer, ForeignKey("lotto_draw_config.draw_id"), nullable=False)
    selected_numbers = Column(String, nullable=False)   # "3,7,12,25,33,40,45" 형태로 저장
    submitted_at     = Column(DateTime, default=datetime.utcnow)

    # 관계
    user   = relationship("User", back_populates="lotto_entries")
    config = relationship("LottoDrawConfig", back_populates="entries")


# ===== 로또 당첨 테이블 =====
# 당첨자를 기록하는 테이블 → 다음 회차 참여 제한에 사용
class LottoWinner(Base):
    __tablename__ = "lotto_winners"

    id          = Column(Integer, primary_key=True, index=True, autoincrement=True)
    draw_id     = Column(Integer, ForeignKey("lotto_draw_config.draw_id"), nullable=False)  # 당첨된 회차
    user_id     = Column(Integer, ForeignKey("users.id"), nullable=False)                   # 당첨된 유저
    student_id  = Column(String(20), nullable=False)                                        # 당첨된 학번
    announced_at = Column(DateTime, default=datetime.utcnow)                                # 당첨 발표 시간
