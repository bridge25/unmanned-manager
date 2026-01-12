# Team JARVIS Template - Release Notes

## v1.0.0 (2026-01-13)

### 🎉 Initial Release

팀원들(수강, 대웅)이 Tony님의 JARVIS 시스템을 사용할 수 있도록 제공하는 템플릿입니다.

---

## 🆕 주요 기능

### 1. 💬 댓글 기반 프로젝트 트래킹 (NEW!)

**MindCollab CLI에 `--author` 옵션 추가**

```bash
# JARVIS가 작성하는 댓글
mc comment N45 "작업 시작합니다" --author "JARVIS"

# Tony님이 작성하는 댓글 (기본값)
mc comment N45 "이 부분 수정해줘"
```

**효과:**
- Tony ↔ JARVIS 대화 구분 가능
- 브리핑 시 노드 댓글을 통해 입체적 현황 파악
- 작업 진행 상황 리얼타임 트래킹

**자비스 행동 규칙:**
- 작업 시작 시: 댓글로 시작 알림
- 진행 중 체크포인트: 단계별 완료 현황 기록
- 블로커 발견 시: 즉시 댓글로 알림
- 작업 완료 시: 결과물 요약 기록

### 2. 🪟 Windows 호환성

**PowerShell 초기화 스크립트 (`init-jarvis.ps1`)**
- UTF-8 인코딩 자동 처리
- 디렉토리 자동 생성
- 개인 프로필 템플릿 생성
- Git 초기화

**Line Ending 자동 변환 (`.gitattributes`)**
- Windows: CRLF (로컬)
- Repository: LF (저장)
- Git이 자동으로 변환하여 Mac-Windows 간 충돌 방지

### 3. 📚 상세한 사용 가이드

**README.md 완전 재작성:**
- Windows 사용자 우선 설명
- 3분 빠른 시작 가이드
- PowerShell 명령어 예시
- 인코딩 문제 해결 방법
- 팀 협업 규칙

---

## 🚀 빠른 시작 (Windows)

### 1️⃣ 템플릿 다운로드

```powershell
# PowerShell 열기 (Windows + X → Windows PowerShell)
cd $HOME\Desktop
git clone https://github.com/bridge25/unmanned-manager.git
cd unmanned-manager\team-jarvis-template
```

### 2️⃣ 자신의 폴더로 복사

```powershell
# 수강
Copy-Item -Path . -Destination "$HOME\Desktop\sookang-jarvis" -Recurse
cd $HOME\Desktop\sookang-jarvis

# 대웅
Copy-Item -Path . -Destination "$HOME\Desktop\daewoong-jarvis" -Recurse
cd $HOME\Desktop\daewoong-jarvis
```

### 3️⃣ 초기화 실행

```powershell
# PowerShell 실행 정책 설정 (최초 1회만)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 초기화 실행
.\init-jarvis.ps1

# 프롬프트에서 이름 입력
```

### 4️⃣ MindCollab CLI 설치

```powershell
# Node.js 설치 확인
node --version

# MindCollab CLI 설치
npm install -g @mindcollab/cli

# 로그인
mc auth login --code SOOKANG-MC-2026  # 수강
mc auth login --code DAEWOONG-MC-2026 # 대웅
```

### 5️⃣ 프로젝트 선택

```powershell
mc init
# 참여 중인 프로젝트 선택 (Prezento, 사주.io 등)
```

### 6️⃣ Claude Code로 시작

```powershell
code .
# Claude Code에서 "와썹" 입력
```

---

## 📋 필수 파일 수정

### ✅ 수정 필요한 파일

| 파일 | 설명 |
|------|------|
| `current/profile.md` | **수정 필수** - 개인 정보 입력 |
| `current/projects.md` | **수정 필수** - 담당 프로젝트 목록 |
| `current/todo.md` | **수정 필수** - 개인 할 일 |

### ❌ 그대로 사용하는 파일

| 파일 | 설명 |
|------|------|
| `CLAUDE.md` | 세션 규칙 (와썹 브리핑 등) |
| `GUIDE.md` | 자비스 프로토콜 |
| `PM-GUIDE.md` | PM 오케스트레이션 |
| `current/pm-context.md` | PM 관리 컨텍스트 |

---

## 💬 댓글 사용 예시

### 작업 흐름

```bash
# 1. 작업 시작
mc comment N45 "Prezento 에디터 개선 작업 시작합니다" --author "JARVIS"

# 2. 진행 중 체크포인트
mc comment N45 "Step 1 (텍스트 입력) 완료. Step 2 (이미지 업로드) 진행 중" --author "JARVIS"

# 3. 블로커 발견
mc comment N45 "⚠️ 블로커: GLM API 크레딧 부족. Tony님 확인 필요" --author "JARVIS"

# 4. Tony님 응답
mc comment N45 "크레딧 충전했어. 계속 진행해줘"

# 5. 작업 완료
mc comment N45 "완료했습니다. 결과물: 에디터 기능 3개 구현, 테스트 통과" --author "JARVIS"

# 6. 노드 완료 처리
mc done N45 --pr
```

---

## ⚠️ 주의사항

### 1. 인코딩 문제 (Windows)

- ✅ **모든 파일은 UTF-8 인코딩**으로 저장됩니다
- ✅ Git이 자동으로 줄바꿈 변환 (Windows: CRLF ↔ Repo: LF)
- ❌ 메모장 대신 **VS Code 사용** 권장

### 2. TodoWrite는 영어로

Claude Code의 TodoWrite 기능은 한글 사용 시 크래시 발생:

```bash
❌ 잘못: "프레젠토 배포 확인"
✅ 올바름: "Check Prezento deployment"
```

### 3. --author 옵션 필수

JARVIS가 작성하는 댓글은 반드시 `--author "JARVIS"` 추가:

```bash
# ✅ 올바름
mc comment N45 "작업 완료" --author "JARVIS"

# ❌ 잘못 (Tony로 표시됨)
mc comment N45 "작업 완료"
```

### 4. "와썹" = 브리핑 시작

- "와썹"은 인사가 아님
- 세션 시작 시 브리핑 트리거 명령어
- 브리핑에서 노드 댓글 확인 자동 실행

---

## 🧑‍🤝‍🧑 팀 협업 워크플로우

### 1. Tony님이 노드 생성 & 할당

```bash
mc add "Prezento 랜딩 개선" --type task --assignee sookang --priority high
# → N78 생성됨
```

### 2. 팀원이 작업 시작

```bash
mc start N78
# → Git 브랜치 자동 생성
# → 상태: backlog → in_progress

mc comment N78 "작업 시작합니다" --author "JARVIS"
```

### 3. 진행 중 댓글로 소통

```bash
# JARVIS가 체크포인트 기록
mc comment N78 "Step 1 완료. Step 2 진행 중" --author "JARVIS"

# Tony님이 피드백
mc comment N78 "이 부분은 디자인 수정 필요해"

# JARVIS가 응답
mc comment N78 "알겠습니다. 디자인 수정했습니다" --author "JARVIS"
```

### 4. 작업 완료 & PR

```bash
mc done N78 --pr
# → PR 자동 생성
# → 상태: in_progress → done
```

---

## 🔧 MindCollab CLI 퀵 레퍼런스

```bash
# 인증
mc auth login --code YOUR-CODE
mc init                        # 프로젝트 선택

# 노드 관리
mc tasks                       # 할 일 목록
mc show N45                    # 노드 상세 정보
mc start N45                   # 작업 시작 (브랜치 생성)
mc done N45 --pr               # 완료 + PR 생성

# 댓글
mc comment N45 "내용" --author "JARVIS"  # 댓글 작성
mc comments N45                           # 댓글 목록

# 상태 변경
mc edit N45 --status blocked   # 블로커 발생
mc edit N45 --priority high    # 우선순위 변경

# 프로젝트 현황
mc status                      # 프로젝트 전체 현황
```

---

## 🐛 문제 해결

### PowerShell 실행 정책 오류

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Git 명령어 없음

https://git-scm.com/download/win 에서 Git for Windows 설치

### Node.js 없음

https://nodejs.org 에서 LTS 버전 설치

### mc 명령어 인식 안됨

```powershell
# PowerShell 재시작 후
npm install -g @mindcollab/cli
```

### 한글이 깨져요

- VS Code에서 파일 저장 시 **UTF-8** 인코딩 확인
- 메모장 사용 금지 (인코딩 문제 발생)

---

## 📞 도움 받기

- **Tony님께 질문**: MindCollab 댓글로 `@Tony` 멘션
- **JARVIS에게 질문**: Claude Code에서 직접 대화
- **MindCollab 웹**: https://mindcollab-web-production.up.railway.app

---

## 🔄 업데이트 방법

Tony님이 템플릿을 업데이트하면:

```powershell
# Windows PowerShell
cd $HOME\Desktop\unmanned-manager
git pull origin main

# 최신 파일 복사 (주의: 개인 파일은 백업 후)
Copy-Item -Path team-jarvis-template\CLAUDE.md -Destination $HOME\Desktop\my-jarvis\
Copy-Item -Path team-jarvis-template\GUIDE.md -Destination $HOME\Desktop\my-jarvis\
Copy-Item -Path team-jarvis-template\current\pm-context.md -Destination $HOME\Desktop\my-jarvis\current\
```

---

## 📚 추가 리소스

- **자비스 프로토콜**: `GUIDE.md` 참조
- **PM 오케스트레이션**: `PM-GUIDE.md` 참조
- **세션 규칙**: `CLAUDE.md` 참조
- **MindCollab 웹**: https://mindcollab-web-production.up.railway.app

---

## 🎯 다음 단계

1. ✅ 템플릿 다운로드 & 초기화
2. ✅ MindCollab CLI 설치 & 로그인
3. ✅ 프로젝트 선택 & Claude Code 시작
4. 📝 `current/profile.md` 개인화
5. 📝 `current/projects.md` 프로젝트 목록 작성
6. 💬 첫 작업 노드에 댓글로 진행 상황 기록
7. 🚀 Tony님과 댓글로 협업 시작!

---

**이제 자신만의 JARVIS로 Tony님과 협업하세요! 🚀**
