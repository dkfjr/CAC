import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import settings


def send_verification_email(email: str, code: str):
    """
    이메일로 인증 코드 전송
    Gmail SMTP 사용 (개발용)
    - Gmail은 '앱 비밀번호'를 사용해야 함
      → Gmail 설정 > 보안 > 2단계 인증 활성화 후 앱 비밀번호 생성
    """
    subject = "로또 참여 이메일 인증"
    body = f"""
    <h2>이메일 인증 코드</h2>
    <p>아래 코드를 입력하여 인증을 완료해주세요.</p>
    <h3 style="color: blue; font-size: 28px;">{code}</h3>
    <p>이 코드는 <strong>{settings.VERIFICATION_EXPIRE_MINUTES}분</strong> 후 만료됩니다.</p>
    """

    # 이메일 메시지 구성
    msg = MIMEMultipart()
    msg["From"] = settings.SMTP_USER
    msg["To"] = email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    # SMTP 연결 및 전송
    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()                                          # 암호화
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)  # 로그인
            server.sendmail(settings.SMTP_USER, email, msg.as_string())
        return True
    except Exception as e:
        print(f"이메일 전송 실패: {e}")
        return False
