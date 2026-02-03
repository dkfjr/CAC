from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# SQLite는 check_same_thread=False가 필요 (비동기 방지)
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)

# DB 세션 생성기
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모든 테이블의 기본 클래스
Base = declarative_base()


# FastAPI에서 사용하는 DB 세션 의존성
# 요청마다 세션을 생성하고, 요청 끝나면 자동 닫힘
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
