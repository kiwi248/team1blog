# FastAPI Post CRUD

FastAPI로 블로그 게시글 API를 구현하며 Router, Scheme, Service의 역할을 학습하는 프로젝트입니다.

실제 데이터베이스 대신 Python 리스트를 임시 저장소로 사용합니다. 따라서 서버를 종료하고 다시 실행하면 저장된 게시글이 초기화됩니다.

## 학습 목표

- FastAPI로 게시글 API를 구성합니다.
- Pydantic으로 요청과 응답 데이터 형식을 정의합니다.
- Router, Scheme, Service의 역할을 구분합니다.
- 게시글 생성, 조회, 수정, 삭제 기능을 구현합니다.
- 존재하지 않는 게시글 요청에 `404` 오류를 반환합니다.
- 필수 입력값이 잘못된 경우 `422` 오류가 발생하는지 확인합니다.
- FastAPI `TestClient`와 pytest로 Router를 테스트합니다.

## 기능 구조

```text
요청
  ↓
Post Router
  ↓
Post Service
  ↓
Python 리스트
  ↓
응답
```

- **Scheme**: 요청 데이터와 응답 데이터의 형식을 검사합니다.
- **Service**: 게시글을 생성, 조회, 수정, 삭제합니다.
- **Router**: HTTP Method와 URL을 Service 함수에 연결합니다.
- **Test**: Router에 요청을 보내 상태 코드와 응답을 확인합니다.

## 폴더 구조

```text
team1blog/
├─ app/
│  ├─ routers/
│  │  └─ post_router.py
│  ├─ schemes/
│  │  └─ post_scheme.py
│  ├─ services/
│  │  └─ post_service.py
│  ├─ requirements.txt
│  └─ sym.py
├─ test/
│  └─ test_post_router.py
└─ README.md
```

## 파일별 역할

| 파일 | 역할 |
|---|---|
| `app/schemes/post_scheme.py` | 게시글 생성, 수정, 응답 형식 정의 |
| `app/services/post_service.py` | 리스트를 이용한 게시글 데이터 처리 |
| `app/routers/post_router.py` | Post API 경로와 오류 처리 |
| `app/sym.py` | Post Router를 연결하는 개인 실행 앱 |
| `test/test_post_router.py` | Post Router 테스트 |

## 실행 준비

프로젝트 최상위 폴더에서 가상환경을 생성합니다.

```powershell
python -m venv .venv
```

PowerShell에서 가상환경을 활성화합니다.

```powershell
.\.venv\Scripts\Activate.ps1
```

필요한 패키지를 설치합니다.

```powershell
python -m pip install --upgrade pip
python -m pip install fastapi uvicorn pytest httpx
```

설치 여부는 다음 명령으로 확인할 수 있습니다.

```powershell
python -c "import fastapi, uvicorn, pytest; print('ready')"
```

## 서버 실행

프로젝트 최상위 폴더에서 다음 명령을 실행합니다.

```powershell
python -m uvicorn app.sym:app --reload
```

서버가 실행되면 Swagger UI에서 API를 확인할 수 있습니다.

```text
http://127.0.0.1:8000/docs
```

## 학습 확인 항목

- 가상환경을 활성화할 수 있습니다.
- Uvicorn으로 Post 앱을 실행할 수 있습니다.
- Swagger UI에서 게시글을 생성할 수 있습니다.
- 생성된 게시글을 번호로 조회할 수 있습니다.
- 게시글의 제목과 내용을 수정할 수 있습니다.
- 게시글을 삭제할 수 있습니다.
- `404`와 `422` 상태 코드의 의미를 설명할 수 있습니다.
- pytest로 Router 테스트를 실행할 수 있습니다.
