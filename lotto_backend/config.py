from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # DB
    DATABASE_URL: str = "sqlite:///./lotto.db"

    # JWT
    SECRET_KEY: str = "your_secret_key_change_this_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # CoolSMS
    COOLSMS_API_KEY: str = ""
    COOLSMS_API_SECRET: str = ""
    COOLSMS_SENDER: str = ""

    # 인증 코드
    VERIFICATION_CODE_LENGTH: int = 6
    VERIFICATION_EXPIRE_MINUTES: int = 10
    MAX_VERIFICATION_ATTEMPTS: int = 5

    def __init__(self):
        import os
        self.DATABASE_URL = os.getenv("DATABASE_URL", self.DATABASE_URL)
        self.SECRET_KEY = os.getenv("SECRET_KEY", self.SECRET_KEY)
        self.ALGORITHM = os.getenv("ALGORITHM", self.ALGORITHM)
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", self.ACCESS_TOKEN_EXPIRE_MINUTES))
        self.COOLSMS_API_KEY = os.getenv("COOLSMS_API_KEY", self.COOLSMS_API_KEY)
        self.COOLSMS_API_SECRET = os.getenv("COOLSMS_API_SECRET", self.COOLSMS_API_SECRET)
        self.COOLSMS_SENDER = os.getenv("COOLSMS_SENDER", self.COOLSMS_SENDER)
        self.VERIFICATION_CODE_LENGTH = int(os.getenv("VERIFICATION_CODE_LENGTH", self.VERIFICATION_CODE_LENGTH))
        self.VERIFICATION_EXPIRE_MINUTES = int(os.getenv("VERIFICATION_EXPIRE_MINUTES", self.VERIFICATION_EXPIRE_MINUTES))
        self.MAX_VERIFICATION_ATTEMPTS = int(os.getenv("MAX_VERIFICATION_ATTEMPTS", self.MAX_VERIFICATION_ATTEMPTS))

# 전역 설정 객체 (다른 파일에서 from config import settings로 사용)
settings = Settings()
