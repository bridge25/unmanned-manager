# 🎛️ /pm 오케스트레이션 가이드

> 여러 프로젝트를 병렬로 관리하는 PM(Project Manager) 기능

---

## 개념

```
┌─────────────────────────────────────────────────────────────┐
│  PM (당신)                                                   │
│  ├── /pm project1 "테스트 실행해줘"                          │
│  ├── /pm project2 "빌드 상태 확인"                           │
│  └── /pm project3 "README 업데이트"                          │
│                                                             │
│  각 프로젝트의 Worker Claude가 작업 실행                      │
│  결과를 PM에게 리포트                                        │
└─────────────────────────────────────────────────────────────┘
```

**핵심**: 여러 tmux 세션에서 Claude Code가 실행되고, PM이 지시를 위임

---

## 사전 준비

### 1. tmux 세션 생성

```bash
# 프로젝트별 세션 생성
tmux new -s project1 -d
tmux new -s project2 -d
tmux new -s myapp -d

# 세션 목록 확인
tmux ls
```

### 2. 각 세션에서 Claude Code 시작

```bash
# 각 세션에 Claude 시작 명령 전송
tmux send-keys -t project1 "cd /path/to/project1 && claude" Enter
tmux send-keys -t project2 "cd /path/to/project2 && claude" Enter
tmux send-keys -t myapp "cd /path/to/myapp && claude" Enter
```

### 3. 프로젝트 등록

`CLAUDE.md`에 프로젝트 매핑 추가:

```markdown
## 등록된 프로젝트

| 세션명 | 폴더 | 별칭 |
|--------|------|------|
| project1 | my-project-1 | p1 |
| project2 | my-project-2 | p2 |
| myapp | my-application | app |
```

---

## 사용법

### 기본 문법

```
/pm <세션명> <지시>
```

### 예시

```
/pm project1 테스트 실행해줘
/pm myapp git status 확인
/pm project2 README 첫 10줄 보여줘
```

### 별칭 사용

```
/pm p1 빌드해줘
/pm app 배포 상태 확인
```

---

## 동작 원리

```
1. PM Claude가 /pm 명령 감지
2. tmux send-keys로 Worker 세션에 명령 전송
3. Worker Claude가 작업 실행
4. 결과를 .jarvis/results/에 저장
5. PM이 결과 파일 읽어서 응답
```

### 핵심 파일

```
.claude/hooks/jarvis/
├── tmux_orchestrator.py    # 세션 관리
├── pm_executor.py          # 명령 실행
└── orchestrator_ipc.py     # 프로세스 간 통신
```

---

## tmux 필수 명령어

| 작업 | 명령어 |
|------|--------|
| 새 세션 생성 | `tmux new -s 이름` |
| 백그라운드 세션 | `tmux new -s 이름 -d` |
| 세션 목록 | `tmux ls` |
| 세션 접속 | `tmux attach -t 이름` |
| 세션 분리 | `Ctrl+B` → `D` |
| 세션 종료 | `tmux kill-session -t 이름` |
| 명령 전송 | `tmux send-keys -t 이름 "명령" Enter` |

---

## 스크립트 사용법

### 세션 관리

```bash
cd .claude/hooks/jarvis

# 세션 목록 보기
python3 tmux_orchestrator.py list

# Claude 시작 (--dangerously-skip-permissions 모드)
python3 tmux_orchestrator.py start-claude project1

# 모든 세션에 Claude 시작
python3 tmux_orchestrator.py start-claude-all

# 세션 생성
python3 tmux_orchestrator.py create project1

# 세션 종료
python3 tmux_orchestrator.py kill project1
```

---

## 팁

### 1. 결과 디렉토리 설정

Worker에게 결과 저장 위치를 명시:

```
/pm project1 작업 완료 후 결과를 /path/to/.jarvis/results/에 저장해줘
```

### 2. 병렬 작업

여러 프로젝트에 동시 지시:

```
/pm project1 테스트 실행
/pm project2 빌드 실행
/pm myapp 린트 검사
```

### 3. 세션 모니터링

별도 터미널에서 세션 접속하여 진행 상황 확인:

```bash
tmux attach -t project1
# 보기만 하고 분리: Ctrl+B → D
```

---

## Windows (WSL2)

Windows에서는 WSL2 안에서 동일하게 사용:

```bash
# WSL 시작
wsl

# 프로젝트 경로 (Windows 경로 변환)
cd /mnt/c/Users/이름/projects/myproject

# 이후 동일
tmux new -s myproject
claude
```

자세한 내용: [WINDOWS-SETUP.md](./WINDOWS-SETUP.md)

---

## 문제 해결

### 세션이 응답 없음

```bash
# 세션 상태 확인
tmux ls

# 세션 강제 종료 후 재시작
tmux kill-session -t 세션명
tmux new -s 세션명
```

### 결과가 안 돌아옴

1. Worker 세션에 직접 접속하여 상태 확인
2. `.jarvis/results/` 폴더 권한 확인
3. Worker Claude가 실행 중인지 확인

### tmux 명령 실패

```bash
# Enter 키 분리 필수 (중요!)
tmux send-keys -t 세션 "명령" Enter && sleep 0.5 && tmux send-keys -t 세션 Enter
```

---

*PM Orchestration Guide v1.0*
