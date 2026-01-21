# JARVIS SDK

> Worker용 Python SDK for MindCollab IPC v2.1

Claude Code Worker에서 PM(Project Manager)에게 작업 상태를 실시간으로 전달하는 SDK입니다.

## 특징

- **Context Manager 지원**: `with` 문으로 자동 에러 처리
- **Fail-open 모드**: API 실패해도 작업 계속 진행 (outbox 저장)
- **Windows/Mac/Linux 호환**: 표준 라이브러리만 사용
- **Zero Dependencies**: 외부 패키지 불필요

## 설치

### 방법 1: 직접 복사 (권장)

```bash
# 프로젝트에 jarvis_sdk 폴더 복사
cp -r packages/jarvis-sdk your-project/jarvis_sdk
```

### 방법 2: pip 설치 (로컬)

```bash
cd packages/jarvis-sdk
pip install -e .
```

## 환경변수 설정

### Windows (PowerShell)

```powershell
$env:JARVIS_API_KEY = "<팀내_공유_키_사용>"
$env:JARVIS_API_URL = "https://mindcollab-web-production.up.railway.app/api"
$env:JARVIS_WORKER_ID = "your-worker-name"
```

### Windows (CMD)

```cmd
set JARVIS_API_KEY=<팀내_공유_키_사용>
set JARVIS_API_URL=https://mindcollab-web-production.up.railway.app/api
set JARVIS_WORKER_ID=your-worker-name
```

### Mac/Linux (bash)

```bash
export JARVIS_API_KEY="<팀내_공유_키_사용>"
export JARVIS_API_URL="https://mindcollab-web-production.up.railway.app/api"
export JARVIS_WORKER_ID="your-worker-name"
```

## 사용법

### 기본 사용 (Context Manager)

```python
from jarvis_sdk import JarvisTask

with JarvisTask(
    task_id="my_task_001",
    node_id="N148",           # MindCollab 노드 ID (선택)
    worker_id="haedong"       # 기본값: 환경변수 JARVIS_WORKER_ID
) as task:
    # 1. 작업 시작 알림
    task.start("데이터 처리 시작")

    # 2. 진행 중 로그 (선택)
    task.log("50% 완료", level="info")

    # 3. 작업 완료
    task.complete(
        result={"processed": 100, "failed": 0},
        summary="데이터 100건 처리 완료"
    )

# 예외 발생 시 자동으로 task.blocked() 호출됨
```

### 직접 호출

```python
from jarvis_sdk import JarvisTask

task = JarvisTask("my_task", worker_id="worker1")
task.start("작업 시작")

try:
    # 작업 수행
    result = do_something()
    task.complete({"data": result}, summary="성공")
except Exception as e:
    task.blocked(reason=str(e), blocker_type="error")
```

### 이벤트 타입

| 이벤트 | 메서드 | 설명 |
|--------|--------|------|
| `task_started` | `task.start()` | 작업 시작 |
| `task_completed` | `task.complete()` | 작업 완료 |
| `task_blocked` | `task.blocked()` | 블로커 발생 |
| `task_log` | `task.log()` | 진행 로그 |

### 블로커 타입

```python
task.blocked(
    reason="API 응답 없음",
    blocker_type="external"  # error, dependency, input_needed, external
)
```

## Fail-open 동작

API 호출 실패 시:
1. `.jarvis/outbox/pending/`에 이벤트 저장
2. 작업은 계속 진행 (예외 발생 안 함)
3. 나중에 재전송 가능

```python
# strict=True로 설정하면 API 실패 시 예외 발생
task = JarvisTask("my_task", strict=True)
```

## 파일 구조

```
jarvis_sdk/
├── __init__.py      # 패키지 진입점
├── client.py        # API 클라이언트 (재시도, outbox)
├── config.py        # 설정 관리
├── task.py          # JarvisTask 메인 클래스
├── py.typed         # 타입 힌트 마커
└── test_sdk.py      # 테스트
```

## 테스트

```bash
cd packages/jarvis-sdk
python -m pytest test_sdk.py -v
```

## 아키텍처

```
Worker Claude
     │
     │ JARVIS SDK (이 패키지)
     ▼
MindCollab API ─────► Supabase ──► Push Daemon
                                       │
                                       ├──► [사람] tmux display-message
                                       └──► [Claude PM] inbox.jsonl
```

## 라이선스

MIT License
