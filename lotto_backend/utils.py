from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from config import settings

# Authorization: Bearer <token> 형태로 토큰을 받는 설정
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """JWT 토큰 생성"""
    to_encode = data.copy()

    # 만료 시간 설정
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> dict:
    """JWT 토큰 복호화"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 토큰입니다."
        )


def get_current_user_phone(token: str = Depends(oauth2_scheme)) -> str:
    """
    API에서 사용하는 의존성 (Dependency)
    요청 헤더의 토큰에서 전화번호를 자동으로 추출
    사용법: def some_api(phone: str = Depends(get_current_user_phone))
    """
    payload = decode_token(token)
    phone_number = payload.get("phone_number")
    if not phone_number:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="토큰에 전화번호 정보가 없습니다."
        )
    return phone_number
