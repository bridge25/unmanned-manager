# v1.5.0 - Team JARVIS Template + Comment-based Project Tracking

> 🎉 **Major Release**: 팀원들이 각자의 JARVIS를 만들 수 있는 템플릿 + 댓글 기반 협업 트래킹!

---

## 🧑‍🤝‍🧑 Team JARVIS Template

**팀원들이 자신만의 JARVIS를 만들 수 있는 완전한 템플릿 제공!**

이제 수강, 대웅을 포함한 모든 팀원이 각자의 Windows 환경에서 자비스 시스템을 사용할 수 있습니다.

### 📁 위치

[`team-jarvis-template/`](./team-jarvis-template/)

### 📚 문서

- **메인 가이드**: [`team-jarvis-template/README.md`](./team-jarvis-template/README.md) - Windows 우선 설명, 3분 빠른 시작
- **릴리즈 노트**: [`team-jarvis-template/RELEASE-NOTES.md`](./team-jarvis-template/RELEASE-NOTES.md) - 상세 사용법, 팀 협업 규칙

### 🎯 대상 사용자

- **수강** (기획, 홍보, 리서치 담당 - Windows)
- **대웅** (개발 담당 - Windows)
- **Tony님의 팀에 합류하는 새 멤버**

### 🆕 새로운 파일

| 파일 | 설명 |
|------|------|
| `team-jarvis-template/` | 즉시 사용 가능한 완전한 템플릿 |
| `init-jarvis.ps1` | Windows PowerShell 초기화 스크립트 |
| `init-jarvis.sh` | macOS/Linux 초기화 스크립트 |
| `.gitattributes` | 줄바꿈 자동 변환 (CRLF/LF) |
| `README.md` | Windows 우선 가이드 (완전 재작성) |
| `RELEASE-NOTES.md` | v1.0.0 상세 릴리즈 노트 |

### 🪟 Windows 호환성 (CRITICAL)

- ✅ **UTF-8 인코딩 자동 처리** - 한글 깨짐 방지
- ✅ **PowerShell 스크립트** - 원클릭 초기화
- ✅ **Git 줄바꿈 자동 변환** - Mac-Windows 충돌 방지
- ✅ **VS Code 권장 설정** - 메모장 사용 금지

### ⚡ 빠른 시작 (Windows)

```powershell
# 1. 템플릿 다운로드
cd $HOME\Desktop
git clone https://github.com/bridge25/unmanned-manager.git
cd unmanned-manager\team-jarvis-template

# 2. 자신의 폴더로 복사
Copy-Item -Path . -Destination "$HOME\Desktop\sookang-jarvis" -Recurse
cd $HOME\Desktop\sookang-jarvis

# 3. 초기화 실행
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\init-jarvis.ps1

# 프롬프트에서 이름 입력 (예: sookang)

# 4. MindCollab CLI 설치 & 로그인
npm install -g @mindcollab/cli
mc auth login --code SOOKANG-MC-2026

# 5. 프로젝트 선택
mc init
# 참여 중인 프로젝트 선택 (Prezento, 사주.io 등)

# 6. Claude Code로 시작
code .
# Claude Code에서 "와썹" 입력
```

### 🍎 빠른 시작 (macOS)

```bash
# 1-2. 템플릿 복사
cp -r unmanned-manager/team-jarvis-template ~/Desktop/tony-jarvis
cd ~/Desktop/tony-jarvis

# 3. 초기화
chmod +x init-jarvis.sh
./init-jarvis.sh

# 4-5. MindCollab 설정
mc auth login --code TONY-MC-2026
mc init

# 6. 시작
claude
# "와썹" 입력
```

### 🔑 팀원 인증 코드

| 사용자 | 코드 | 역할 |
|--------|------|------|
| Tony | `TONY-MC-2026` | admin |
| Sookang | `SOOKANG-MC-2026` | member |
| Daewoong | `DAEWOONG-MC-2026` | member |

### ✅ 필수 파일 수정

템플릿 초기화 후 **반드시 수정해야 할 파일**:

| 파일 | 설명 |
|------|------|
| `current/profile.md` | ✅ **수정 필수** - 개인 정보, 기술 스택, 목표 |
| `current/projects.md` | ✅ **수정 필수** - 담당 프로젝트 목록 |
| `current/todo.md` | ✅ **수정 필수** - 개인 할 일 목록 |

### ❌ 그대로 사용하는 파일

| 파일 | 설명 |
|------|------|
| `CLAUDE.md` | 세션 규칙 (와썹 브리핑 등) |
| `GUIDE.md` | 자비스 프로토콜 |
| `PM-GUIDE.md` | PM 오케스트레이션 |
| `current/pm-context.md` | PM 관리 컨텍스트 |

### ⚠️ 주의사항

#### 1. 인코딩 문제 (Windows)

- ✅ 모든 파일은 **UTF-8 인코딩**으로 저장
- ✅ Git이 자동으로 줄바꿈 변환 (Windows: CRLF ↔ Repo: LF)
- ❌ **메모장 사용 금지** → **VS Code 사용 필수**

#### 2. TodoWrite는 영어로

```bash
❌ 잘못: "프레젠토 배포 확인"
✅ 올바름: "Check Prezento deployment"
```

Claude Code의 TodoWrite 기능은 한글 사용 시 크래시 발생!

#### 3. --author 옵션 필수

JARVIS가 작성하는 댓글은 반드시 `--author "JARVIS"` 추가:

```bash
mc comment N45 "작업 완료" --author "JARVIS"
```

---

## 💬 댓글 기반 프로젝트 트래킹 (Comment-based Project Tracking)

**MindCollab CLI에 `--author` 옵션 추가!**

이제 JARVIS가 작성하는 댓글과 Tony가 작성하는 댓글을 구분할 수 있습니다.

### 🆕 새로운 CLI 기능

```bash
# JARVIS가 작성
mc comment N45 "작업 시작합니다" --author "JARVIS"

# Tony가 작성 (기본값, --author 생략)
mc comment N45 "이 부분 수정해줘"

# 댓글 조회
mc comments N45

# 노드 상세 정보 (댓글 포함)
mc show N45
```

### ✨ 효과

- ✅ **Tony ↔ JARVIS 대화 구분** - 누가 작성했는지 명확히 표시
- ✅ **입체적 현황 파악** - 브리핑 시 노드 댓글 확인
- ✅ **리얼타임 트래킹** - 작업 진행 상황 실시간 기록

### 🤖 자비스 자동화 규칙

자비스는 다음 시점에 자동으로 댓글을 작성합니다:

| 시점 | 댓글 예시 |
|------|----------|
| 작업 시작 | "N45 작업 시작합니다. 예상 소요: 2-3시간" |
| 체크포인트 | "Step 1 완료. Step 2 진행 중" |
| 블로커 발견 | "⚠️ 블로커: API 크레딧 부족. Tony님 확인 필요" |
| 작업 완료 | "완료. 결과물: 테스트 5개 통과, 배포 완료" |

### 📊 브리핑 통합

이제 **"와썹"** 브리핑 시 주요 노드의 댓글을 자동으로 확인하여:

- Tony님의 최근 피드백
- 블로커 발견 사항
- 완료된 체크포인트
- 다음 액션 아이템

을 포함한 **입체적 프로젝트 현황**을 제공합니다.

### 💼 팀 협업 워크플로우

#### 1. Tony님이 노드 생성 & 할당

```bash
mc add "Prezento 랜딩 개선" --type task --assignee sookang --priority high
# → N78 생성됨
```

#### 2. 팀원이 작업 시작

```bash
mc start N78
# → Git 브랜치 자동 생성
# → 상태: backlog → in_progress

mc comment N78 "작업 시작합니다" --author "JARVIS"
```

#### 3. 진행 중 댓글로 소통

```bash
# JARVIS가 체크포인트 기록
mc comment N78 "Step 1 완료. Step 2 진행 중" --author "JARVIS"

# Tony님이 MindCollab 웹에서 확인 후 피드백
mc comment N78 "이 부분은 디자인 수정 필요해"

# JARVIS가 응답
mc comment N78 "알겠습니다. 디자인 수정했습니다" --author "JARVIS"
```

#### 4. 작업 완료 & PR 생성

```bash
mc done N78 --pr
# → PR 자동 생성
# → 상태: in_progress → done
```

### 📝 사용 예시 (전체 흐름)

```bash
# 1. 작업 시작
mc start N45
mc comment N45 "Prezento 에디터 개선 작업 시작합니다" --author "JARVIS"

# 2. 진행 중 체크포인트
mc comment N45 "Step 1 (텍스트 입력) 완료. Step 2 (이미지 업로드) 진행 중" --author "JARVIS"

# 3. 블로커 발견
mc comment N45 "⚠️ 블로커: GLM API 크레딧 부족. Tony님 확인 필요" --author "JARVIS"

# 4. Tony님 응답 (MindCollab 웹 or CLI)
mc comment N45 "크레딧 충전했어. 계속 진행해줘"

# 5. 작업 재개
mc comment N45 "크레딧 확인했습니다. 작업 재개합니다" --author "JARVIS"

# 6. 작업 완료
mc comment N45 "완료했습니다. 결과물: 에디터 기능 3개 구현, 테스트 통과" --author "JARVIS"
mc done N45 --pr
```

### 📚 문서 업데이트

| 파일 | 업데이트 내용 |
|------|--------------|
| `CLAUDE.md` | 브리핑 시 댓글 확인 규칙 추가 |
| `current/pm-context.md` | 댓글 트래킹 가이드 추가 |
| `team-jarvis-template/` | 댓글 사용법 포함 |

---

## 🎯 왜 이 릴리즈가 중요한가?

### 1. 팀 확장 가능

이제 Tony 혼자가 아닌 **팀 전체가 자비스 시스템을 사용**할 수 있습니다.

각 팀원이 자신만의 자비스를 가지고:
- 개인 프로젝트 관리
- Tony와 댓글로 실시간 소통
- MindCollab으로 팀 작업 트래킹

### 2. 입체적 프로젝트 관리

기존: 노드 상태만 확인 (TODO → IN_PROGRESS → DONE)
**새로운**: 노드 상태 + 댓글 대화로 **"왜 이 상태인지"** 파악

### 3. Windows 환경 완벽 지원

한글 인코딩, 줄바꿈 변환 등 Mac-Windows 간 모든 문제를 해결했습니다.

---

## 🔄 업그레이드 방법

### 기존 사용자

```bash
cd unmanned-manager
git pull origin main

# 새로운 기능 활용
mc comment N45 "테스트" --author "JARVIS"
```

### 신규 팀원

```powershell
# Windows
cd $HOME\Desktop
git clone https://github.com/bridge25/unmanned-manager.git
cd unmanned-manager\team-jarvis-template

# README.md 참고하여 설정
```

---

## 📞 도움 받기

- **Tony님께 질문**: MindCollab 댓글로 `@Tony` 멘션
- **JARVIS에게 질문**: Claude Code에서 직접 대화
- **MindCollab 웹**: https://mindcollab-web-production.up.railway.app

---

## 🐛 알려진 이슈

없음 (현재까지 보고된 이슈 없음)

---

## 🙏 감사의 말

팀원들(수강, 대웅)의 피드백을 통해 Windows 호환성을 완벽하게 만들 수 있었습니다.

---

**이제 자신만의 JARVIS로 Tony님과 협업하세요! 🚀**
