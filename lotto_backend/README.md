# 로또 백엔드 API

## 폴더 구조
```
lotto_backend/
├── .env                  ← 환경변수 (SMTP 비밀번호 등)
├── requirements.txt      ← 패키지 목록
├── config.py             ← 설정 관리
├── database.py           ← DB 연결
├── models.py             ← 테이블 정의
├── schemas.py            ← 요청/응답 형태 정의
├── utils.py              ← JWT 토큰 유틸
├── email_service.py      ← 이메일 전송
├── main.py               ← 앱 진입점 (여기서 실행)
├── init_data.py          ← 초기 회차 데이터 생성
└── routers/
    ├── __init__.py
    ├── auth.py           ← 이메일 인증 API
    ├── user.py           ← 학번 등록 API
    └── lotto.py          ← 로또 참여 API
```

## 실행 순서

### Step 1. 패키지 설치
```bash
pip install -r requirements.txt
pip install pydantic-settings
```

### Step 2. .env 파일 수정
- SMTP_USER, SMTP_PASSWORD에 Gmail 앱 비밀번호 입력

### Step 3. 초기 데이터 생성
```bash
python init_data.py
```

### Step 4. 서버 실행
```bash
uvicorn main:app --reload
```
→ http://127.0.0.1:8000 에서 확인 가능
→ http://127.0.0.1:8000/docs 에서 Swagger UI로 API 테스트 가능

---

## API 정리

| 단계 | 메서드 | URL | 설명 |
|------|--------|-----|------|
| 이메일 전송 | POST | /api/auth/email/send | 인증 코드 이메일 전송 |
| 이메일 검증 | POST | /api/auth/email/verify | 코드 검증 → JWT 반환 |
| 학번 중복 확인 | GET | /api/user/check-duplicate?student_id=xxx | 학번 중복 여부 |
| 학번 등록 | POST | /api/user/register | 학번 저장 (JWT 필수) |
| 회차 설정 조회 | GET | /api/lotto/config?draw_id=1 | 번호 개수/범위 조회 |
| 로또 참여 | POST | /api/lotto/entry | 번호 선택 제출 (JWT 필수) |
| 내 참여 조회 | GET | /api/lotto/my-entry?draw_id=1 | 내 제출 번호 조회 |

## 번호 개수 변경 방법
init_data.py 또는 DB에서 lotto_draw_config의 number_count 값만 바꾸면 됨.
코드 수정 불필요.
