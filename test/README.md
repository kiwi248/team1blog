# Comment 테스트 안내

댓글 기능은 입력 데이터, 처리 로직, HTTP API를 따로 확인할 수 있도록 세 계층으로
나누어 테스트한다.

## 파일 구성

- `conftest.py`: 공통 `TestClient`와 테스트 데이터 초기화 설정
- `test_comment_scheme.py`: Pydantic 입력값 검증 테스트
- `test_comment_service.py`: 댓글 CRUD 처리 로직 테스트
- `test_comment_router.py`: 실제 HTTP 경로, 상태 코드와 JSON 응답 테스트

각 테스트 전후에는 `fake_db`와 댓글 ID가 초기화된다. 따라서 테스트 실행 순서와
관계없이 항상 같은 결과를 얻을 수 있다.

## 테스트 계층의 차이

### Scheme 테스트

HTTP 요청을 보내지 않고 Pydantic 모델을 직접 생성한다. 필수값, 자료형, 양수 ID,
빈 댓글과 공백 제거 규칙을 확인한다.

### Service 테스트

FastAPI Router를 거치지 않고 Service 함수를 직접 호출한다. 댓글 생성, 조회, 수정,
삭제와 `404` 처리를 확인한다.

### Router 테스트

FastAPI의 `TestClient`로 실제 API에 HTTP 요청을 보낸다. Router부터 Service와
`fake_db`까지 연결된 전체 흐름, 상태 코드와 JSON 응답을 확인한다.

실패한 계층으로 문제 위치를 좁힐 수 있다.

```text
Scheme 실패 → 입력 데이터 검증 문제
Service 실패 → 댓글 CRUD 처리 문제
Router만 실패 → API 경로, 상태 코드 또는 응답 설정 문제
```

## 실행 방법

필요한 테스트 패키지가 없다면 먼저 설치한다.

```bash
python -m pip install pytest httpx
```

프로젝트 최상위 폴더에서 실행한다.

전체 댓글 테스트:

```bash
pytest test -v
```

계층별 테스트:

```bash
pytest test/test_comment_scheme.py -v
pytest test/test_comment_service.py -v
pytest test/test_comment_router.py -v
```

테스트 하나만 실행:

```bash
pytest test/test_comment_router.py::test_create_comment_api_returns_201 -v
```

## 주요 상태 코드

- `200`: 조회·수정·삭제 성공
- `201`: 댓글 생성 성공
- `404`: 댓글을 찾을 수 없음
- `422`: 필수값 누락 또는 입력값 형식 오류
