# 블로그 관리 API 미니 프로젝트 계획서

## 1. 프로젝트 개요

- **프로젝트명:** 게시판 Management API
- **목표:** FastAPI로 회원, 게시글, 댓글 CRUD API를 구현하고, 별도의 OpenAI LLM API 연동 기능을 추가한다.
- **난이도 기준:** 입문 수준의 구조를 사용한다. 각 기능은 `router → service → scheme`으로 분리하고 `pytest`로 API를 테스트한다.
- **LLM 범위:** LLM은 User, Post, Comment 데이터와 연결하지 않는다. 사용자의 질문을 OpenAI LLM API로 전달하고 답변만 반환하는 독립 채팅 API이다.
- **개인 실행 방식:** 각 팀원은 자신의 이니셜 실행 파일에서 담당 router만 등록해 실행·테스트한다. 모든 기능을 합친 최종 실행 파일은 팀장이 `app/main.py`에 작성한다.

## 2. 역할 분담

| 담당 | 기능 | 담당 파일 | 작업 브랜치 |
| --- | --- | --- | --- |
| 윤기화(팀장) | 프로젝트 기본 구조, GitHub 관리, OpenAI LLM API, 최종 통합 | `chat_router.py`, `chat_scheme.py`, `chat_service.py`, `chat_config.py`, `ygh.py`, `test_chat_router.py`, `main.py` | `feature/chat` |
| 장상옥 | User CRUD | `user_router.py`, `user_scheme.py`, `user_service.py`, `jso.py`, `test_user_router.py` | `feature/users` |
| 손영민 | Post CRUD | `post_router.py`, `post_scheme.py`, `post_service.py`, `sym.py`, `test_post_router.py` | `feature/posts` |
| 권오현 | Comment CRUD | `comment_router.py`, `comment_scheme.py`, `comment_service.py`, `koh.py`, `test_comment_router.py` | `feature/comments` |

`app/main.py`는 모든 router를 등록하는 공동 파일이다. 충돌을 줄이기 위해 각 담당자는 자신의 기능 파일과 개인 실행 파일만 수정하고, 최종 router 등록과 통합 테스트는 팀장이 진행한다.

## 3. 파일 구조 및 경로

```text
team1blog/
├── .gitignore                   # .env, .venv/, __pycache__/ 등 Git 제외
├── requirements.txt             # fastapi, uvicorn, pydantic, python-dotenv, google-genai, pytest, httpx
├── project_plan.md              # 프로젝트 설계 계획서
├── README.md                    # 최종 실행 방법 및 API 설명
├── app/
│   ├── __init__.py
│   ├── main.py                  # 팀장이 모든 router를 최종 등록
│   ├── ykw.py                   # 윤기화 LLM API 개인 실행 파일
│   ├── jso.py                   # 장상옥 User CRUD 개인 실행 파일
│   ├── sym.py                   # 손영민 Post CRUD 개인 실행 파일
│   ├── koh.py                   # 권오현 Comment CRUD 개인 실행 파일
│   ├── core/
│   │   └── chat_config.py       # .env 로드
│   ├── routers/
│   │   ├── user_router.py       # /users API
│   │   ├── post_router.py       # /posts API
│   │   ├── comment_router.py    # /comments API
│   │   └── chat_router.py       # /chat/gemini API
│   ├── schemes/
│   │   ├── user_scheme.py       # User 요청/응답 Pydantic 모델
│   │   ├── post_scheme.py       # Post 요청/응답 Pydantic 모델
│   │   ├── comment_scheme.py    # Comment 요청/응답 Pydantic 모델
│   │   └── chat_scheme.py       # LLM 요청/응답 Pydantic 모델
│   └── services/
│       ├── user_service.py      # User 메모리 데이터 및 CRUD 로직
│       ├── post_service.py      # Post 메모리 데이터 및 CRUD 로직
│       ├── comment_service.py   # Comment 메모리 데이터 및 CRUD 로직
│       └── chat_service.py      # google-genai 호출 로직
└── tests/
    ├── test_user_router.py
    ├── test_post_router.py
    ├── test_comment_router.py
    └── test_chat_router.py
```

`domains` 폴더는 이번 프로젝트에서 사용하지 않는다.

## 4. 공통 CRUD 규칙

- 요청과 응답 모델은 `schemes`에서 Pydantic `BaseModel`로 정의한다.
- 생성은 `POST`, 전체 조회는 `GET`, 단건 조회는 `GET /{id}`, 수정은 `PUT /{id}`, 삭제는 `DELETE /{id}`를 사용한다.
- ID 이름은 `user_id`, `post_id`, `comment_id`로 통일한다.
- 존재하지 않는 ID는 `404 Not Found`를 반환한다.
- 필수 값 누락이나 잘못된 타입은 FastAPI 기본 검증 오류 `422 Unprocessable Entity`를 반환한다.
- 생성 성공은 `201 Created`, 조회·수정·삭제 성공은 `200 OK`를 사용한다.
- 삭제 성공 시 공통 응답 형식은 `{"message":"삭제되었습니다.","id":1}`로 한다.
- 각 service는 자신만의 `fake_db` 리스트와 ID 카운터를 관리한다.
- 각 service는 다른 service를 import하거나 참조하지 않는다.
- User의 `password`는 입력에는 포함하지만 출력에는 포함하지 않는다.
- 경로명은 소문자와 복수형을 사용한다: `/users`, `/posts`, `/comments`.
- Comment 생성 시 `post_id`는 URL 경로로 받고, `user_id`와 `content`는 요청 본문으로 받는다.

## 5. CRUD API 입력·출력 형식

### 5-1. User 관리 (`/users`)

| 기능 | Method / 경로 | 입력 형식 | 성공 출력 형식 |
| --- | --- | --- | --- |
| 등록 | `POST /users` | `{"username":"장상옥","email":"sangok@example.com","password":"1234","bio":"FastAPI를 공부하고 있습니다."}` | `{"user_id":1,"username":"장상옥","email":"sangok@example.com","bio":"FastAPI를 공부하고 있습니다."}` |
| 전체 조회 | `GET /users` | 없음 | `[{User 객체}, ...]` |
| 단건 조회 | `GET /users/{user_id}` | 경로 `user_id: int` | `User 객체` |
| 수정 | `PUT /users/{user_id}` | `{"username":"장상옥","email":"new@example.com","password":"5678","bio":"수정된 소개"}` | 수정된 `User 객체` |
| 삭제 | `DELETE /users/{user_id}` | 경로 `user_id: int` | `{"message":"삭제되었습니다.","id":1}` |

#### User 입력·출력 기준

- `user_id`: 서버에서 자동 생성
- `username`: 필수 문자열
- `email`: 필수 문자열
- `password`: 필수 문자열, 응답에서 제외
- `bio`: 선택 문자열 또는 `null`

#### User 개인 실행

```bash
uvicorn app.jso:app --reload
```

### 5-2. Post 관리 (`/posts`)

| 기능 | Method / 경로 | 입력 형식 | 성공 출력 형식 |
| --- | --- | --- | --- |
| 등록 | `POST /posts` | `{"user_id":1,"title":"첫 번째 블로그 글","content":"FastAPI를 이용해 블로그 API를 만들었습니다."}` | `{"post_id":1,"user_id":1,"title":"첫 번째 블로그 글","content":"FastAPI를 이용해 블로그 API를 만들었습니다."}` |
| 전체 조회 | `GET /posts` | 없음 | `[{Post 객체}, ...]` |
| 단건 조회 | `GET /posts/{post_id}` | 경로 `post_id: int` | `Post 객체` |
| 수정 | `PUT /posts/{post_id}` | `{"user_id":1,"title":"수정된 제목","content":"수정된 내용"}` | 수정된 `Post 객체` |
| 삭제 | `DELETE /posts/{post_id}` | 경로 `post_id: int` | `{"message":"삭제되었습니다.","id":1}` |

#### Post 입력·출력 기준

- `post_id`: 서버에서 자동 생성
- `user_id`: 작성자 식별값
- `title`: 필수 문자열
- `content`: 필수 문자열
- 초기 버전에서는 User service의 실제 존재 여부를 검사하지 않는다.

#### Post 개인 실행

```bash
uvicorn app.sym:app --reload
```

### 5-3. Comment 관리 (`/comments`)

| 기능 | Method / 경로 | 입력 형식 | 성공 출력 형식 |
| --- | --- | --- | --- |
| 등록 | `POST /posts/{post_id}/comments` | `{"user_id":2,"content":"좋은 글입니다."}` | `{"comment_id":1,"post_id":1,"user_id":2,"content":"좋은 글입니다."}` |
| 전체 조회 | `GET /comments` | 없음 | `[{Comment 객체}, ...]` |
| 게시글별 조회 | `GET /posts/{post_id}/comments` | 경로 `post_id: int` | `[{Comment 객체}, ...]` |
| 단건 조회 | `GET /comments/{comment_id}` | 경로 `comment_id: int` | `Comment 객체` |
| 수정 | `PUT /comments/{comment_id}` | `{"user_id":2,"content":"수정된 댓글입니다."}` | 수정된 `Comment 객체` |
| 삭제 | `DELETE /comments/{comment_id}` | 경로 `comment_id: int` | `{"message":"삭제되었습니다.","id":1}` |

#### Comment 입력·출력 기준

- `comment_id`: 서버에서 자동 생성
- `post_id`: 등록 시 URL 경로에서 입력
- `user_id`: 댓글 작성자 식별값
- `content`: 필수 문자열
- 초기 버전에서는 User 또는 Post service의 실제 존재 여부를 검사하지 않는다.

#### Comment 개인 실행

```bash
uvicorn app.koh:app --reload
```

## 6. OpenAI LLM API 입력·출력 형식

### 채팅 (`/chat/chatgpt`)

| 기능 | Method / 경로 | 입력 형식 | 성공 출력 형식 |
| --- | --- | --- | --- |
| 질문 전송 | `POST /chat/gemini` | `{"user_id":"id01","prompt":"FastAPI가 무엇인지 설명해줘."}` | `{"answer":"FastAPI는 Python으로 API 서버를 만들 수 있는 웹 프레임워크입니다."}` |

- `user_id`: 요청 사용자 식별용 문자열
- `prompt`: OpenAI LLM에 전달할 질문
- `answer`: OpenAI LLM가 생성한 답변
- OpenAI LLM API 키와 모델명은 `.env`에서 불러온다.
- User, Post, Comment 데이터와 연결하지 않는다.

#### LLM 개인 실행

```bash
uvicorn app.ykw:app --reload
```

## 7. 개인 실행 파일 규칙

각 팀원은 자신의 router만 등록한 실행 파일을 작성한다.

### `app/jso.py`

```python
from fastapi import FastAPI
from app.routers.user_router import user_router

app = FastAPI(title="User CRUD")
app.include_router(user_router)
```

### `app/sym.py`

```python
from fastapi import FastAPI
from app.routers.post_router import post_router

app = FastAPI(title="Post CRUD")
app.include_router(post_router)
```

### `app/koh.py`

```python
from fastapi import FastAPI
from app.routers.comment_router import comment_router

app = FastAPI(title="Comment CRUD")
app.include_router(comment_router)
```

### `app/ygh.py`

```python
from fastapi import FastAPI
from app.core import chat_config
from app.routers.chat_router import chat_router

app = FastAPI(title="OpenAI LLM")
app.include_router(chat_router)
```

## 8. 테스트 계획

각 팀원은 담당 기능의 CRUD 또는 LLM API 테스트 파일을 직접 작성하고 실행한다.

| 담당 | 테스트 파일 | 필수 테스트 |
| --- | --- | --- |
| 장상옥 | `tests/test_user_router.py` | 생성, 전체 조회, 단건 조회, 수정, 삭제, 404, 422, 비밀번호 미노출 |
| 손영민 | `tests/test_post_router.py` | 생성, 전체 조회, 단건 조회, 수정, 삭제, 404, 422 |
| 권오현 | `tests/test_comment_router.py` | 생성, 전체 조회, 게시글별 조회, 단건 조회, 수정, 삭제, 404, 422 |
| 윤기화 | `tests/test_chat_router.py` | 정상 응답, 빈 `user_id`, 빈 `prompt`, Mock 응답 |

테스트 파일은 각자의 개인 실행 파일에서 `app`을 불러온다.

```python
from fastapi.testclient import TestClient
from app.jso import app

client = TestClient(app)
```

담당 테스트 실행:

```bash
pytest tests/test_user_router.py -v
pytest tests/test_post_router.py -v
pytest tests/test_comment_router.py -v
pytest tests/test_chat_router.py -v
```

전체 테스트 실행:

```bash
pytest -v
```

GitHub에 Push하기 전에 담당 테스트와 전체 테스트가 모두 통과해야 한다.

## 9. GitHub 작업 규칙

### 브랜치

```text
main
feature/chat
feature/users
feature/posts
feature/comments
```

### 작업 시작

```bash
git switch main
git pull origin main
git switch -c feature/users
```

이미 브랜치가 있다면:

```bash
git switch feature/users
```

### 작업 순서

```text
scheme 작성
→ service 작성
→ router 작성
→ 개인 실행 파일 작성
→ Uvicorn 및 Swagger 확인
→ test 파일 작성
→ 담당 테스트 실행
→ 전체 테스트 실행
→ Commit
→ Push
→ Pull Request 생성
```

### Push 예시

```bash
git add app/schemes/user_scheme.py
git add app/services/user_service.py
git add app/routers/user_router.py
git add app/jso.py
git add tests/test_user_router.py

git commit -m "feat: User CRUD 및 테스트 구현"
git push -u origin feature/users
```

### Pull Request

- `base`: `main`
- `compare`: 자신의 `feature/*` 브랜치
- 담당 파일, 구현 기능, 테스트 결과를 Pull Request 설명에 작성한다.
- 팀장은 Pull Request를 검토한 뒤 `main`에 병합한다.

## 10. 최종 통합

모든 팀원의 Pull Request가 병합되면 팀장이 `app/main.py`에 전체 router를 등록한다.

```python
from fastapi import FastAPI
from app.core import chat_config
from app.routers.user_router import user_router
from app.routers.post_router import post_router
from app.routers.comment_router import comment_router
from app.routers.chat_router import chat_router

app = FastAPI(title="Blog Management API")

app.include_router(user_router)
app.include_router(post_router)
app.include_router(comment_router)
app.include_router(chat_router)
```

최종 실행:

```bash
uvicorn app.main:app --reload
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

최종 통합 후 팀장이 수행할 작업:

1. 모든 router가 정상 등록되었는지 확인한다.
2. 중복 경로와 import 오류를 확인한다.
3. `pytest -v`로 전체 테스트를 실행한다.
4. Swagger에서 User, Post, Comment, Chat API를 확인한다.
5. 필요하면 테스트가 `app.main`을 사용하도록 수정한다.
6. README에 설치, 실행, 테스트, API 경로를 작성한다.

## 11. 완료 기준

- User CRUD 5개 기능이 정상 동작한다.
- Post CRUD 5개 기능이 정상 동작한다.
- Comment CRUD와 게시글별 댓글 조회가 정상 동작한다.
- Gemini 독립 채팅 API가 정상 동작한다.
- 각 팀원의 담당 테스트가 통과한다.
- 최종 전체 테스트가 통과한다.
- `.env`와 가상환경 파일이 GitHub에 포함되지 않는다.
- 모든 기능이 `app/main.py`에 통합된다.
- README와 프로젝트 계획서가 GitHub에 포함된다.
