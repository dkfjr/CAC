"""
초기 데이터 세팅 스크립트
실행: python init_data.py

lotto_draw_config 테이블에 테스트용 회차 데이터를 미리 넣습니다.
"""

from database import SessionLocal, engine
from models import Base, LottoDrawConfig

# 테이블 생성 (아직 안 만들었으면 생성)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# 회차 1 생성: 1~45 중 7개 선택
config = LottoDrawConfig(
    draw_id=1,
    number_count=7,
    number_range_min=1,
    number_range_max=45,
)
db.add(config)
db.commit()

print("✅ 회차 1 생성 완료 (1~45 중 7개 선택)")

# 예시: 회차 2 생성 - 번호를 5개로 줄인 경우
config2 = LottoDrawConfig(
    draw_id=2,
    number_count=5,           # 5개로 줄임
    number_range_min=1,
    number_range_max=45,
)
db.add(config2)
db.commit()

print("✅ 회차 2 생성 완료 (1~45 중 5개 선택)")

db.close()
print("\n초기 데이터 세팅 완료!")
