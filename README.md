# Unmanned Manager

> *"At your service."*

Claude Code를 개인 비서 AI로 만들어주는 프로젝트 관리 시스템입니다.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Claude](https://img.shields.io/badge/Powered%20by-Claude_Code-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Python](https://img.shields.io/badge/Python-3.9+-yellow)

---

## 버전 정보

| 버전 | 날짜 | 변경사항 |
|------|------|----------|
| **v1.0.0** | 2024-11-30 | 첫 공개 릴리즈 |

### v1.0.0 주요 기능

- **자동화 Hooks**
  - `SessionStart`: 세션 시작 시 Git 프로젝트 자동 스캔, 상태 로드
  - `UserPromptSubmit`: 의사결정 시 유사 케이스 자동 검색 (Memento)
  - `PostToolUse`: 도구 실행 결과 자동 기록
  - `SessionEnd`: 케이스 자동 저장, 프로필 업데이트 리마인드

- **Memento 시스템**
  - 의사결정 케이스 저장 및 검색
  - 과거 경험 기반 일관된 판단 지원
  - `cases.md`에 자동 기록

- **Shadow Counselor**
  - 대화 패턴 관찰 및 적응
  - 사용자 상태에 맞는 응답 스타일 조절

- **Git 통합**
  - 프로젝트 폴더 자동 스캔
  - 비활성 프로젝트 알림
  - 변경사항 추적

---

## 이게 뭔가요?

**Unmanned Manager**는 Claude를 아이언맨의 자비스처럼 만들어줍니다:

- **프로젝트 추적** - Git 활동, 데드라인, 마일스톤 모니터링
- **일정 관리** - 할 일, 약속, 반복 일정
- **우선순위 정리** - 긴급도와 데드라인 기반으로 뭘 먼저 할지 추천
- **학습** - 대화하면서 당신의 스타일과 선호도를 파악
- **선제적 알림** - 데드라인, 방치된 프로젝트, 일정 충돌 미리 알려줌

---

## 빠른 시작

### 1. 저장소 클론

```bash
git clone https://github.com/unmanned-company/unmanned-manager.git
cd unmanned-manager
```

### 2. 초기 설정

```bash
chmod +x setup.sh
./setup.sh
```

setup.sh가 물어보는 것들:
- 이름
- 호칭 (sir, boss, 이름 등)
- 프로젝트 폴더 경로
- 언어 (한국어/영어/일본어)

### 3. Claude Code 실행

```bash
claude
```

### 4. 세션 시작

```
와썹
```

이렇게 치면 AI가 설정을 읽고, 프로젝트를 확인하고, 브리핑을 시작합니다.

---

## 어떻게 쓰면 되나요?

### 매일 아침 - 브리핑 받기

```
> 와썹

좋은 아침입니다. 오늘은 2024년 12월 2일 월요일입니다.

🚨 긴급 알림:
- Project X 데드라인 2일 남음
- Project Y 10일간 방치됨

📊 프로젝트 현황:
| 프로젝트 | 상태 | 긴급도 | 최근 활동 |
|---------|------|--------|----------|
| X       | 테스트 | HIGH  | 1일 전   |
| Y       | 중단  | MID   | 10일 전  |

📌 오늘의 우선순위:
1. Project X 테스트 마무리
2. Project Y 블로커 확인
```

### 자주 쓰는 명령어

| 명령어 | 하는 일 |
|--------|---------|
| `와썹` | 세션 시작, 전체 브리핑 |
| `브리핑해줘` | 빠른 현황 파악 |
| `오늘 뭐 해야 돼?` | 오늘 할 일 우선순위 |
| `[프로젝트] 어떻게 되고 있어?` | 특정 프로젝트 상세 현황 |
| `[할일] 추가해줘` | 할 일 목록에 추가 |
| `[아이디어] 기록해둬` | inbox에 빠르게 저장 |
| `우선순위 다시 정해줘` | 우선순위 재계산 |

### 일주일에 한 번 - 정리하기

1. `current/projects.md` 업데이트 - 진행 상황 반영
2. `current/inbox.md` 비우기 - 아이디어들 정리
3. `current/weekly-log.md` 간단히 기록

---

## 파일 구조 이해하기

```
unmanned-manager/
│
├── 🤖 AI 설정 파일
│   ├── CLAUDE.md      ← Claude가 읽는 세션 규칙
│   ├── GUIDE.md       ← 자비스 프로토콜 전체 정의
│   └── config.yaml    ← 당신의 개인 설정
│
├── 📁 .claude/        ← 자동화 시스템 (수정 불필요)
│   ├── settings.json  ← Hooks, 권한 설정
│   └── hooks/         ← 자동화 스크립트들
│       ├── manager/   ← 세션 관리 hooks
│       └── memento/   ← 학습/케이스 hooks
│
└── 📁 current/        ← 여기가 당신의 데이터!
    ├── profile.md     ← AI가 당신에 대해 학습한 것
    ├── projects.md    ← 프로젝트 목록 (직접 관리)
    ├── todo.md        ← 할 일 목록 (직접 관리)
    ├── cases.md       ← 의사결정 케이스 (자동 기록)
    ├── weekly-log.md  ← 주간 기록
    ├── inbox.md       ← 아이디어 임시 저장소
    └── backlog.md     ← 나중에 할 것들
```

### 어떤 파일을 수정해야 하나요?

| 파일 | 수정 주체 | 설명 |
|------|----------|------|
| `config.yaml` | 당신 | 초기 설정 후 거의 안 건드림 |
| `projects.md` | 당신 | 프로젝트 추가/상태 업데이트 |
| `todo.md` | 당신 + AI | 할 일 관리 |
| `inbox.md` | 당신 | 아이디어 빠르게 던져놓기 |
| `profile.md` | AI | 자동으로 학습 내용 기록 |
| `cases.md` | AI | 의사결정 케이스 자동 기록 (Memento) |
| `weekly-log.md` | 당신 | 간단한 일일 기록 (선택) |

---

## 프로젝트 추가하는 법

`current/projects.md` 파일을 열고 아래 형식으로 추가:

```markdown
## 프로젝트 이름

| 항목 | 내용 |
|------|------|
| **위치** | `../project-folder/` |
| **상태** | 진행중 |
| **긴급도** | HIGH / MID / LOW |
| **목표** | 이 프로젝트로 뭘 하려는지 |
| **데드라인** | 2024-12-31 또는 없음 |

### 마일스톤
- [ ] 할 일 1
- [ ] 할 일 2
- [ ] 할 일 3

### 이슈/메모
- 참고할 내용들
```

---

## 설정 커스터마이징

`config.yaml`에서 조절 가능한 것들:

```yaml
# 기본 정보
user:
  name: "홍길동"           # 이름
  honorific: "님"          # 호칭 (sir, boss, 님, 이름 등)
  timezone: "Asia/Seoul"

# 프로젝트 모니터링
projects:
  git_scan_enabled: true   # Git 상태 자동 수집
  scan_paths:              # 스캔할 프로젝트 폴더들
    - "/Users/me/projects"
  inactive_alert_days: 7   # N일 이상 방치 시 알림

# 브리핑 설정
briefing:
  deadline_alert_days: 3   # 데드라인 N일 전부터 알림
  show_git_status: true    # Git 상태 표시

# Shadow Counselor (심리 관찰)
shadow_counselor:
  enabled: true            # 켜기/끄기
  record_observations: true

# 커뮤니케이션 스타일
communication:
  language: "ko"           # ko, en, ja
  style: "formal"          # formal, casual
  prefer_structured: true  # 표/리스트 선호
  concise: true            # 간결하게
```

---

## Shadow Counselor가 뭔가요?

AI가 당신의 대화 패턴을 조용히 관찰하고 적응하는 기능입니다:

- 피곤해 보이면 → 더 간결하게 답변
- 여유 있어 보이면 → 상세 옵션 제공
- 뭔가 고민 있어 보이면 → 작게 쪼개서 제안

**절대 상담사처럼 행동하지 않습니다.** "기분 어떠세요?" 같은 질문 안 합니다.
그냥 조용히 파악해서 행동으로 반영할 뿐입니다.

끄고 싶으면 `config.yaml`에서:
```yaml
shadow_counselor:
  enabled: false
```

---

## 팁

### 1. 파일 업데이트를 꾸준히

AI는 파일에 있는 정보만 알 수 있습니다. `projects.md`와 `todo.md`를 꾸준히 업데이트해주세요.

### 2. inbox를 적극 활용

생각나는 거 있으면 일단 inbox에 던져놓으세요:
```
"OOO 아이디어 기록해둬"
```

나중에 정리하면 됩니다.

### 3. weekly-log는 간단하게

매일 한 줄이라도 기록하면 나중에 큰 도움이 됩니다:
```
- 월: Project X 버그 수정
- 화: 미팅, Project Y 기획
```

### 4. 학습 효과

오래 쓸수록 AI가 당신의 패턴을 더 잘 이해합니다. `profile.md`에 학습 내용이 쌓입니다.

---

## 팀으로 사용하기

팀원 각자 자기 인스턴스를 가지면 됩니다:

```
팀원1/unmanned-manager/
팀원2/unmanned-manager/
팀원3/unmanned-manager/
```

각자 `config.yaml`만 수정하면 됩니다.

---

## 문제가 생기면?

1. **AI가 이상하게 행동해요**
   - `CLAUDE.md`와 `GUIDE.md`가 있는지 확인
   - 세션 새로 시작 (`와썹`)

2. **Git 스캔이 안 돼요**
   - `config.yaml`의 `scan_paths` 경로 확인
   - 해당 폴더가 git 저장소인지 확인

3. **브리핑이 이상해요**
   - `current/projects.md` 형식 확인
   - 날짜 형식이 맞는지 확인 (YYYY-MM-DD)

---

## 기여하기

이슈와 PR 환영합니다!

---

## 라이선스

MIT License - 마음대로 쓰세요.

---

## 만든 곳

[Unmanned Company](https://github.com/unmanned-company)

---

*"At your service."*
