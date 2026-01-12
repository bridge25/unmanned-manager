# Team JARVIS Template

> Tony님의 JARVIS 시스템을 팀원들이 사용할 수 있도록 제공하는 템플릿

---

## 🎯 이 템플릿은 누구를 위한 것인가?

- **수강**: 기획, 홍보, 리서치 담당 (Windows)
- **대웅**: 개발 담당 (Windows)
- **또는 Tony님의 팀에 합류하는 새 멤버**

---

## 🚀 빠른 시작 (3분)

### 🪟 Windows 사용자 (수강, 대웅)

#### 1️⃣ 템플릿 다운로드

```powershell
# PowerShell 열기 (Windows + X → Windows PowerShell)
# unmanned-manager 레포 clone
cd $HOME\Desktop
git clone https://github.com/bridge25/unmanned-manager.git
cd unmanned-manager\team-jarvis-template
```

#### 2️⃣ 자신의 폴더로 복사

```powershell
# 수강
Copy-Item -Path . -Destination "$HOME\Desktop\sookang-jarvis" -Recurse
cd $HOME\Desktop\sookang-jarvis

# 대웅
Copy-Item -Path . -Destination "$HOME\Desktop\daewoong-jarvis" -Recurse
cd $HOME\Desktop\daewoong-jarvis
```

#### 3️⃣ 초기화 스크립트 실행

```powershell
# PowerShell 실행 정책 설정 (최초 1회만)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 초기화 실행
.\init-jarvis.ps1

# 프롬프트 나오면 이름 입력 (예: sookang 또는 daewoong)
```

#### 4️⃣ MindCollab CLI 설치

```powershell
# Node.js 설치 확인 (없으면 https://nodejs.org 에서 설치)
node --version

# MindCollab CLI 설치
npm install -g @mindcollab/cli

# 로그인
# 수강
mc auth login --code SOOKANG-MC-2026

# 대웅
mc auth login --code DAEWOONG-MC-2026
```

#### 5️⃣ 프로젝트 선택

```powershell
mc init

# 참여 중인 프로젝트 선택
# 예: Prezento, 사주.io, PartyGram 등
```

#### 6️⃣ Claude Code로 열기

```powershell
# VS Code 또는 Cursor에서 폴더 열기
code .

# Claude Code에서 첫 대화 시작
"와썹"
```

---

### 🍎 macOS 사용자 (Tony님)

#### 1️⃣ 템플릿 복사

```bash
# unmanned-manager 레포에서 복사
cp -r dist/unmanned-manager/team-jarvis-template ~/Desktop/my-jarvis
cd ~/Desktop/my-jarvis
```

#### 2️⃣ 초기화 스크립트 실행

```bash
chmod +x init-jarvis.sh
./init-jarvis.sh
```

#### 3️⃣ MindCollab 로그인 & 프로젝트 선택

```bash
mc auth login --code TONY-MC-2026
mc init
```

---

## 💬 댓글 기반 트래킹 사용법

### 기본 사용

```bash
# 작업 시작 시
mc comment N45 "작업 시작합니다." --author "JARVIS"

# 진행 중
mc comment N45 "Step 1 완료. Step 2 진행 중" --author "JARVIS"

# 완료
mc comment N45 "완료했습니다. 결과물: ..." --author "JARVIS"

# 블로커 발견 시
mc comment N45 "⚠️ 블로커: API 크레딧 부족. Tony님 확인 필요" --author "JARVIS"
```

### Tony님과 대화

```bash
# Tony님이 댓글을 남김
mc comment N45 "이 부분 수정해줘"

# 댓글 확인
mc comments N45

# JARVIS가 응답
mc comment N45 "알겠습니다. 수정했습니다." --author "JARVIS"
```

---

## 📋 주요 파일 설명

| 파일 | 설명 | 수정 필요 |
|------|------|-----------|
| **CLAUDE.md** | 세션 규칙 (와썹 브리핑 등) | ❌ 그대로 사용 |
| **GUIDE.md** | 자비스 프로토콜 | ❌ 그대로 사용 |
| **PM-GUIDE.md** | PM 오케스트레이션 가이드 | ❌ 그대로 사용 |
| **current/profile.md** | 개인 프로필 | ✅ **수정 필수** |
| **current/projects.md** | 담당 프로젝트 | ✅ **수정 필수** |
| **current/todo.md** | 할 일 | ✅ **수정 필수** |
| **current/pm-context.md** | PM 관리 컨텍스트 | ❌ 그대로 사용 |

---

## 🛠️ 개인화 가이드

### 1. profile.md 수정

`current/profile.md` 파일을 VS Code로 열어서 수정:

```markdown
# Profile Database

## Facts (변하지 않는 정보)

### 기본 정보
- **호칭**: 수강 (또는 대웅)
- **역할**: 기획/홍보 (또는 개발)
- **작업 환경**: Windows

### 기술 스택
- 수강: 기획, 마케팅, 리서치
- 대웅: 개발, 프론트엔드/백엔드

### 장기 비전
- 자신의 목표 기록
```

### 2. projects.md 수정

```markdown
# 현재 진행 중인 프로젝트

## 1️⃣ Prezento (수강 담당)
- 역할: 기획, 마케팅, 샘플 생성
- 현황: 개발 진행 중

## 2️⃣ 사주.io (대웅 담당)
- 역할: 개발
- 현황: 엔진 구현 필요
```

---

## 🎯 MindCollab 연동

### 노드 생성

```bash
# 새 Task 생성
mc add "Prezento 랜딩 페이지 개선" --type task --parent N8 --priority high --deadline 2026-01-20

# Feature 생성
mc add "사주.io 엔진 구현" --type feature --priority high
```

### 작업 플로우

```bash
# 1. 작업 시작
mc start N45
# → Git 브랜치 자동 생성

# 2. 작업 진행 (댓글로 체크포인트)
mc comment N45 "Step 1 완료" --author "JARVIS"

# 3. 작업 완료
mc done N45 --pr
# → PR 자동 생성
```

---

## 🧑‍🤝‍🧑 팀 협업 규칙

### 1. 노드 할당

- Tony님이 노드 생성 후 assignee 설정
- 또는 자신이 생성 후 Tony님께 공유

### 2. 댓글 대화

- **본인**: 작업 진행 상황, 질문, 블로커
- **JARVIS**: 브리핑, 체크포인트, 제안
- **Tony님**: 피드백, 우선순위 조정, 지시

### 3. 상태 업데이트

```bash
mc start N45    # backlog → in_progress
mc done N45     # in_progress → done
mc edit N45 --status blocked  # 블로커 발생 시
```

---

## ⚠️ 주의사항

### 1. 인코딩 문제 (Windows)

- ✅ **모든 파일은 UTF-8 인코딩**으로 저장됩니다
- ✅ Git이 자동으로 줄바꿈 변환 (Windows: CRLF ↔ Repo: LF)
- ❌ 메모장 대신 **VS Code 사용** 권장

### 2. TodoWrite는 영어로

```bash
❌ 잘못: "프레젠토 배포 확인"
✅ 올바름: "Check Prezento deployment"
```

### 3. --author 옵션 필수

```bash
# JARVIS가 작성하는 댓글은 반드시 --author "JARVIS" 추가
mc comment N45 "작업 완료" --author "JARVIS"
```

### 4. "와썹" = 브리핑 시작

- "와썹"은 인사가 아님
- 세션 시작 시 브리핑 트리거

---

## 📞 도움 받기

- **Tony님께 질문**: MindCollab 댓글로 @Tony 멘션
- **JARVIS에게 질문**: Claude Code에서 직접 대화
- **MindCollab 웹**: https://mindcollab-web-production.up.railway.app

---

## 🔄 업데이트

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

---

**이제 자신만의 JARVIS로 Tony님과 협업하세요! 🚀**
