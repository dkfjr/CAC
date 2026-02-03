import hashlib
import hmac
import random
import string
from datetime import datetime, timezone

import requests
from config import settings


def _generate_signature(api_secret: str, date: str, salt: str) -> str:
    """HMAC-SHA256 Signature 생성"""
    data = date + salt
    signature = hmac.new(
        api_secret.encode("utf-8"),
        data.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()
    return signature


def _generate_salt(length: int = 16) -> str:
    """랜덤 salt 생성"""
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def send_verification_sms(phone_number: str, code: str) -> bool:
    """
    CoolSMS 공식 API를 통해 인증 코드 SMS 전송
    URL: https://api.coolsms.co.kr/messages/v4/send
    인증: HMAC-SHA256
    """
    url = "https://api.coolsms.co.kr/messages/v4/send"

    date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    salt = _generate_salt()
    signature = _generate_signature(settings.COOLSMS_API_SECRET, date, salt)

    headers = {
        "Authorization": f"HMAC-SHA256 apiKey={settings.COOLSMS_API_KEY}, date={date}, salt={salt}, signature={signature}",
        "Content-Type": "application/json",
    }

    payload = {
        "message": {
            "to": phone_number,
            "from": settings.COOLSMS_SENDER,
            "text": f"[조또]\n 인증 코드: {code}",
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        result = response.json()

        if response.status_code == 200:
            print(f"SMS 전송 성공: {result}")
            return True
        else:
            print(f"SMS 전송 실패 ({response.status_code}): {result}")
            return False

    except Exception as e:
        print(f"SMS 전송 오류: {e}")
        return False
