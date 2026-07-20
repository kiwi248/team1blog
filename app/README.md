# FastAPI 블로그 댓글 CRUD

이 `app` 폴더는 회원, 게시글, 댓글과 Chat 기능으로 구성되는 블로그 API의
애플리케이션 코드가 들어 있는 곳이다. 권오현(`port`)의 담당 기능은 댓글
생성·조회·수정·삭제이며, 실제 데이터베이스 대신 실행 중인 Python 리스트를
사용한다.

## 폴더와 파일의 역할

### `core`

- `chat_config.py`: Gemini API 키와 Chat 기능에 필요한 외부 API 설정을 관리한다.
  Comment 기능에서는 이 파일을 사용하지 않는다.

### `schemes`

Pydantic 모델로 요청과 응답 데이터의 형식을 정의한다.

- `chat_scheme.py`: Chat 요청과 응답 형식
- `comment_scheme.py`: Comment 생성·수정·응답 형식과 입력값 검증
- `post_scheme.py`: Post 요청과 응답 형식
- `user_scheme.py`: User 요청과 응답 형식

### `services`

데이터를 저장하거나 조회하는 실제 처리 로직을 담당한다.

- `chat_service.py`: Gemini API 호출 처리
- `comment_service.py`: 리스트 기반 댓글 CRUD 처리
- `post_service.py`: 게시글 CRUD 처리
- `user_service.py`: 회원 CRUD 처리

### `routers`

HTTP Method와 API 경로를 정하고 해당 Service 함수를 호출한다.

- `chat_router.py`: Chat API
- `comment_router.py`: Comment API
- `post_router.py`: Post API
- `user_router.py`: User API

### `port.py`

권오현의 개인 실행 파일이다. `comment_router`만 FastAPI 앱에 연결한다.

댓글 요청은 다음 순서로 처리된다.

```text
클라이언트
→ port.py
→ routers/comment_router.py
→ services/comment_service.py
→ fake_db
→ CommentResponse
```

`schemes/comment_scheme.py`는 이 과정에서 요청과 응답 데이터가 약속된 형식인지
검사한다.

## 댓글 데이터

댓글은 다음 정보를 갖는다.

| 필드 | 자료형 | 설명 |
|---|---|---|
| `comment_id` | int | 자동으로 발급되는 댓글 번호 |
| `post_id` | int | 댓글이 작성된 게시글 번호 |
| `user_id` | int | 댓글 작성자 번호 |
| `content` | str | 댓글 내용 |

댓글 생성 시 `post_id`는 요청 본문이 아니라 URL 경로에서 받는다.

## 댓글 API

| 기능 | Method | 경로 | 성공 코드 |
|---|---|---|---:|
| 댓글 생성 | POST | `/posts/{post_id}/comments` | 201 |
| 전체 댓글 조회 | GET | `/comments` | 200 |
| 게시글별 댓글 조회 | GET | `/posts/{post_id}/comments` | 200 |
| 댓글 한 개 조회 | GET | `/comments/{comment_id}` | 200 |
| 댓글 수정 | PUT | `/comments/{comment_id}` | 200 |
| 댓글 삭제 | DELETE | `/comments/{comment_id}` | 200 |

## 실행 및 Swagger 테스트

필요한 패키지가 없다면 먼저 설치한다.

```bash
python -m pip install fastapi uvicorn
```

프로젝트 최상위 폴더에서 다음 명령으로 개인 앱을 실행한다.

```bash
uvicorn app.port:app --reload
```

브라우저에서 `http://127.0.0.1:8000/docs`로 이동하면 Swagger 화면에서 API를
직접 실행할 수 있다.

### 1. 댓글 생성

`POST /posts/1/comments`를 열고 다음 요청을 전송한다.

```json
{
  "user_id": 2,
  "content": "좋은 글입니다."
}
```

성공하면 `201`과 함께 다음 형식의 댓글이 반환된다.

```json
{
  "comment_id": 1,
  "post_id": 1,
  "user_id": 2,
  "content": "좋은 글입니다."
}
```

### 2. 조회

다음 API를 차례로 실행한다.

```text
GET /comments
GET /comments/1
GET /posts/1/comments
```

### 3. 수정

`PUT /comments/1`에 다음 요청을 보낸다.

```json
{
  "content": "수정된 댓글입니다."
}
```

### 4. 삭제

`DELETE /comments/1`을 실행한다. 삭제된 댓글이 응답으로 반환된다. 이후
`GET /comments/1`을 실행하면 `404`가 반환되어야 한다.

## 상태 코드

- `200`: 조회·수정·삭제 성공
- `201`: 생성 성공
- `404`: 요청한 댓글을 찾을 수 없음
- `422`: 필수값 누락 또는 입력 형식 오류

## 현재 제한사항

- 서버 메모리의 `fake_db`를 사용하므로 서버를 다시 시작하면 댓글이 사라진다.
- User와 Post 데이터의 실제 존재 여부는 검사하지 않는다.
- 로그인, 작성자 인증 및 댓글 수정 권한 검사는 구현하지 않는다.
