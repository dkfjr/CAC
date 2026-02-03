from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routers import auth, user, lotto

# FastAPI 앱 생성
app = FastAPI(title="로또 백엔드 API", version="1.0.0")

# ===== CORS 설정 (프론트엔드 연결용) =====
origins = [
    "http://chosun-lotto-app.s3-website.ap-northeast-2.amazonaws.com",  # 프론트엔드 S3
    "http://localhost:3000",   # 로컬 개발용
    "http://127.0.0.1:3000",  # 로컬 개발용
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== 앱 시작 시 테이블 자동 생성 =====
Base.metadata.create_all(bind=engine)

# ===== 라우터 등록 =====
app.include_router(auth.router)    # /api/auth/...
app.include_router(user.router)    # /api/user/...
app.include_router(lotto.router)   # /api/lotto/...


# ===== 기본 확인 엔드포인트 =====
@app.get("/")
def read_root():
    return {"message": "로또 백엔드 API 정상 작동 중입니다."}
