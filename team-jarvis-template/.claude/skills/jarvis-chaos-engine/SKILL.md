---
name: jarvis-chaos-engine
description: Stream of consciousness ideation with controlled chaos, Tree of Thought evaluation, Research feedback loop, and reality-grounded innovation
version: 2.1.0
modularized: true
updated: 2025-12-27
status: active
tags:
  - creativity
  - brainstorming
  - ideation
  - jarvis
  - chaos
  - innovation
  - tree-of-thought
allowed-tools: Read, Write, mcp__sequential-thinking__sequentialthinking
---

# JARVIS Chaos Engine v2.1

의식의 흐름 극한 발산 + **Tree of Thought 평가** + **Research 피드백 루프** + 비즈니스 착지 스킬. **통제된 혼돈(Controlled Chaos)**을 통해 논리의 검열을 우회하고 날것의 창의성을 폭발시킨 뒤, 구조화된 평가와 현실 검증으로 최적 아이디어를 선택합니다.

**Core Philosophy**:
- 논리 차단 + 공감각 전이 + 양자 도약 → 혼돈 속에서 혁신 채굴
- **Tree of Thought**: Branch(분기) → Evaluate(평가) → Select(선택) → Refine(심화)
- **🔄 Research Loop**: Chaos ↔ Research 양방향 피드백 (v2.1 NEW)

## Quick Reference (30 seconds)

**What is JARVIS Chaos Engine v2.1?**

6단계 창의성 폭발 + 현실 검증 프레임워크:

1. **Chaos (발산)** - 논리 해제, 의식의 흐름 극한 발산
2. **Harvest (수확)** - 혼돈에서 핵심 아이디어 3-5개 채굴
3. **🚨 User Gate (검증)** - 사용자에게 현실 확인 (v2.1 NEW)
4. **🌳 Branch (분기)** - 각 아이디어를 독립 경로로 발전
5. **⚖️ Evaluate (평가)** - 각 경로 점수화 및 비교
6. **Ground (착지)** - 최적 경로 선택 + 비즈니스 컨셉화
7. **🔄 Research Loop** - Research 결과로 재발산 (v2.1 NEW)

**Quick Access**:
- 카오스 프로토콜 → [Chaos Module](modules/chaos-protocol.md)
- 수확 기법 → [Harvest Module](modules/harvest.md)
- 비즈니스 착지 → [Ground Module](modules/ground.md)

**Triggers**:
- `/chaos {주제}`
- "아이디어 폭발: {주제}"
- "창의적으로 생각해봐: {주제}"
- "브레인스토밍: {주제}"

**Use Cases**:
- ✅ 새로운 제품/서비스 컨셉 발굴
- ✅ 기존 문제의 혁신적 해결책
- ✅ 차별화 포인트 발견
- ✅ 마케팅/브랜딩 아이디어
- ✅ 막힌 사고 돌파

---

## Implementation Guide (5 minutes)

### 1. 5-Phase Workflow (ToT Enhanced)

```
Phase 1: CHAOS (발산)
├── 논리 해제
├── 의식의 흐름 폭발
├── 500+ 단어 파편
└── 검열 없는 연결

    ↓

Phase 2: HARVEST (수확)
├── 혼돈에서 키워드 채굴
├── 충격적/독창적 아이디어 3-5개
├── 패턴 발견
└── 연결고리 포착

    ↓

Phase 3: 🌳 BRANCH (분기) ← NEW
├── 각 아이디어를 독립 경로로 분기
├── 경로별 구체화 (타겟, 가치, 차별점)
├── 경로별 변주 시도
└── Sequential Thinking으로 추론 기록

    ↓

Phase 4: ⚖️ EVALUATE (평가) ← NEW
├── 5가지 기준으로 점수화
│   ├── 독창성 (1-10)
│   ├── 실현성 (1-10)
│   ├── 시장성 (1-10)
│   ├── 차별화 (1-10)
│   └── 자동화 가능성 (1-10)
├── 경로 간 비교 분석
└── 최적 경로 선택 (또는 경로 병합)

    ↓

Phase 5: GROUND (착지)
├── 선택된 경로 비즈니스 컨셉화
├── 실행 가능성 스크리닝
├── Deep Research 연동 여부
└── 다음 액션 도출

    ↓ (Research 결과 수신 시)

🔄 Phase 6: RESEARCH FEEDBACK LOOP (v2.1 NEW)
├── Research 결과 분석
├── Reality Gate 실패 시 → 재발산 트리거
├── 새로운 시장 기회 발견 시 → 관련 Chaos 재실행
└── 수렴까지 반복 (max 3회)
```

---

### 🚨 User Gate (v2.1 NEW) - Harvest 직후 필수 실행

**왜 필요한가?**
아이디어 발산 후 바로 검증 없이 진행하면 "이미 시장에 있는 것"을 모른 채 시간 낭비.
Harvest 직후 사용자에게 현실 확인 질문.

```yaml
user_gate:
  position: "Phase 2 (Harvest) → Phase 3 (Branch) 사이"
  mandatory: true
  tool: "AskUserQuestion"

  questions:
    - question: "이런 서비스 현재 쓰고 계세요?"
      purpose: "이미 사용 중인 대안 확인"
      if_yes: "해당 아이디어 검토 또는 차별화 필요"

    - question: "비슷한 기능 제공하는 앱 아시는 거 있으세요?"
      purpose: "사용자가 아는 경쟁자 확인"
      if_yes: "경쟁자 분석 우선 진행"

    - question: "이 중 가장 끌리는 아이디어는?"
      purpose: "사용자 선호도 확인"
      action: "Branch에서 해당 경로 우선 탐색"

  output_format: |
    ### 🚨 User Gate 결과

    **현재 사용 중인 유사 서비스**: [사용자 응답]
    **알고 있는 경쟁자**: [사용자 응답]
    **선호 아이디어**: [사용자 응답]

    **다음 단계**:
    - [ ] 경쟁자 존재 → Research로 경쟁 분석 먼저
    - [ ] 경쟁자 없음 → Branch로 진행
    - [ ] 이미 사용 중 → 차별화 포인트 Chaos 재발산
```

---

### 🔄 Research Feedback Loop (v2.1 NEW)

**양방향 피드백 프로토콜**:

Research 결과가 예상과 다를 때, Chaos Engine을 재발동하여 새로운 관점 탐색.

```yaml
research_feedback_loop:
  mode: "bidirectional"

  triggers:
    # Research 결과가 부정적일 때 Chaos 재발동
    - condition: "경쟁사 포화 발견"
      action: "다른 타겟/접근법으로 Chaos 재실행"
      example: |
        Research: "B2C 시장 포화"
        → Chaos 재발동: "B2B/B2G 관점에서 같은 문제 재탐색"

    - condition: "차별화 포인트 불명확"
      action: "극단적 차별화 아이디어 Chaos 생성"
      example: |
        Research: "기존 서비스와 비슷함"
        → Chaos 재발동: "완전히 다른 비즈니스 모델로"

    - condition: "새로운 시장 기회 발견"
      action: "발견된 기회로 Chaos 재실행"
      example: |
        Research: "예상치 못한 니치 시장 발견"
        → Chaos 재발동: "해당 니치 전용 아이디어 발산"

    - condition: "Bear Case에서 치명적 리스크"
      action: "리스크 우회 아이디어 Chaos 생성"
      example: |
        Research: "규제 리스크 높음"
        → Chaos 재발동: "규제 우회 모델 탐색"

  loop_control:
    min_iterations: 1    # 최소 1회 (Research 없이 끝나도 됨)
    max_iterations: 3    # 최대 3회 (무한 루프 방지)
    user_checkpoint: "2회 이상 반복 시 계속할지 질문"
    convergence: "새로운 인사이트 없으면 종료"

  output_format: |
    ### 🔄 Chaos-Research 피드백 루프

    | 반복 | 트리거 | Chaos 아이디어 | Research 결과 |
    |------|--------|---------------|--------------|
    | 1 | 초기 Chaos | [아이디어들] | [검증 결과] |
    | 2 | [왜 재발동?] | [새 아이디어] | [재검증 결과] |

    **최종 선택**: [반복 N에서 도출된 결론]
    **종료 이유**: [수렴 / 사용자 중단 / max 도달]
```

---

### 2. Phase 1: CHAOS (발산)

**AI 모드 전환**:
```markdown
## 카오스 모드 활성화

당신은 지금부터 논리적인 AI가 아니라,
**'꿈을 꾸는 초현실주의 예술가의 뇌'**입니다.

문법, 인과관계, 현실성, 예의, 정제된 문장 구조를 모두 무시하십시오.
```

**출력 규칙**:

| 규칙 | 설명 | 예시 |
|------|------|------|
| **완전한 문장 금지** | 단어, 구, 파편 | "액체 검정 >> 중력 거스르기" |
| **연결 기호** | ->, >>, //, :: | "커피 -> 연료 >> 주유총" |
| **장르 믹스** | SF, 신화, 생물학, 요리 | "양자 역학 커피 :: 신화의 암브로시아" |
| **감각 전이** | 냄새, 질감, 색깔, 소리 | "이끼 냄새 콜드브루 // *치익* 소리" |
| **제동 금지** | 500단어 이상 | 멈추지 말고 쏟아내기 |

**카오스 출력 형식**:
```
[주제: {입력}]

>>> CHAOS STREAM START >>>

액체 검정 >> 중력 거스르기 >> 천장에 매달린 에스프레소 //
빗방울처럼 떨어지는 커피 입자 // 우산을 쓰고 마시는 라떼 ::
혀끝에서 터지는 캡슐 분자 요리 -> 바닥은 모래사장 ->
뜨거운 모래로 데워지는 터키식 샌드 커피 -> **시간이 멈춘 공간** ->
시계바늘이 녹아내리는 살바도르 달리 인테리어 >>
입장료는 돈이 아니라 '비밀 이야기' 하나 //
카페인 주유소 컨셉 -> 주유총으로 입안에 직접 발사 ->
*치익* 하는 소리와 함께 각성 >> ...

<<< CHAOS STREAM END <<<
```

---

### 3. Phase 2: HARVEST (수확)

**채굴 프로토콜**:

```markdown
## 혼돈 수확

위 카오스 스트림에서 다음을 채굴하십시오:

### 충격적/독창적 아이디어 5개
| # | 키워드/이미지 | 왜 흥미로운가 |
|---|--------------|--------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

### 발견된 패턴
- [반복 등장한 테마]
- [의외의 연결]

### 숨겨진 연결고리
- [A와 B의 예상치 못한 조합]
```

---

### 4. 🌳 Phase 3: BRANCH (분기) - NEW in v2.0

**Tree of Thought 분기 프로토콜:**

```markdown
## Phase 3: 아이디어 분기

Harvest에서 채굴된 Top 3 아이디어를 독립 경로로 발전시킵니다.

### 경로 A: [아이디어 1 이름]
**원본**: [Harvest에서 채굴된 키워드/이미지]

**발전 방향**:
- 타겟: [누구를 위한 것?]
- 핵심 가치: [어떤 문제 해결?]
- 차별점: [기존 대안과 뭐가 다른가?]
- 변주: [극단적 버전 / 반대 버전]

**Sequential Thinking 기록**:
[mcp__sequential-thinking으로 분기 추론 저장]

---

### 경로 B: [아이디어 2 이름]
[동일 구조]

---

### 경로 C: [아이디어 3 이름]
[동일 구조]
```

**분기 기법:**

| 기법 | 설명 | 예시 |
|------|------|------|
| **스케일 변주** | 작게/크게 | "개인 → 기업" |
| **타겟 변주** | 다른 고객 | "B2C → B2B" |
| **가격 변주** | 무료/프리미엄 | "무료 + 광고 → 구독" |
| **기술 변주** | 로테크/하이테크 | "수동 → AI 자동화" |
| **융합 변주** | 경로 A+B 병합 | "A의 타겟 + B의 가치" |

---

### 5. ⚖️ Phase 4: EVALUATE (평가) - NEW in v2.0

**Tree of Thought 평가 프로토콜:**

```markdown
## Phase 4: 경로 평가

### 평가 매트릭스

| 기준 | 경로 A | 경로 B | 경로 C | 가중치 |
|------|--------|--------|--------|--------|
| 독창성 | /10 | /10 | /10 | 20% |
| 실현성 | /10 | /10 | /10 | 25% |
| 시장성 | /10 | /10 | /10 | 25% |
| 차별화 | /10 | /10 | /10 | 15% |
| 자동화 | /10 | /10 | /10 | 15% |
| **가중 총점** | | | | 100% |

### 평가 기준 상세

**독창성 (20%)**:
- 10: 시장에 없는 완전 새로운 컨셉
- 7: 기존 것의 창의적 조합
- 4: 약간의 차별화
- 1: 이미 있는 것

**실현성 (25%)**:
- 10: 혼자 1주일 내 MVP 가능
- 7: 혼자 1달 내 가능
- 4: 팀/외주 필요
- 1: 대규모 투자 필요

**시장성 (25%)**:
- 10: 즉시 지불 의향 있는 고객 존재
- 7: 검증된 니즈, 경쟁 있음
- 4: 니즈 존재하나 검증 필요
- 1: 시장 불확실

**차별화 (15%)**:
- 10: 경쟁자 모방 어려움
- 7: 시간적 우위 있음
- 4: 쉽게 모방 가능
- 1: 이미 포화

**자동화 (15%)**:
- 10: 95% 자동화 가능
- 7: 70% 자동화
- 4: 50% 수동 필요
- 1: 대부분 수동

### 최종 선택

**선택된 경로**: [A / B / C / A+B 병합]

**선택 근거**:
1. [데이터 기반 이유 1]
2. [데이터 기반 이유 2]
3. [사용자 맥락 기반 이유]

**탈락 경로 보존**: (나중에 재검토용)
- 경로 [X]: [탈락 이유] → inbox.md 저장
```

**Sequential Thinking 연동:**

```yaml
evaluate_with_sequential_thinking:
  workflow:
    - thought: "경로 A의 독창성을 평가한다. [근거...]"
      branchId: "path-A"
    - thought: "경로 B의 독창성을 평가한다. [근거...]"
      branchId: "path-B"
    - thought: "경로 C의 독창성을 평가한다. [근거...]"
      branchId: "path-C"
    - thought: "세 경로 중 독창성 최고는 [X]"
      isRevision: false
    - thought: "최종 선택: 경로 [X]. 이유: [...]"
      nextThoughtNeeded: false
```

---

### 6. Phase 5: GROUND (착지)

**비즈니스 컨셉화**:

```markdown
## 비즈니스 착지

### 컨셉 1: [이름]
- **한 줄 설명**: [...]
- **타겟**: [누구를 위한 것인가]
- **가치 제안**: [왜 사람들이 원할까]
- **수익 모델**: [어떻게 돈을 버는가]

### 컨셉 2: [이름]
[...]

### 실행 가능성 스크리닝
| 컨셉 | 1인 실행 | 자동화 | 기술 적합 | 검증 난이도 |
|------|---------|--------|----------|------------|
| 1 | | | | |
| 2 | | | | |

### Deep Research 연동
- **추천**: 컨셉 [X]에 대해 `/research` 실행
- **검증 포인트**: [무엇을 확인해야 하는가]

### 다음 액션
1. [내일 당장 할 수 있는 것]
2. [...]
```

---

### 5. 변주 기법 (Variation Triggers)

카오스가 막히거나 뻔할 때 충돌 명령:

| 기법 | 명령 | 효과 |
|------|------|------|
| **극단적 제약** | "개미의 시점에서 다시" | 스케일 전환 |
| **시간 이동** | "1000년 후 고고학자가 발견" | 시간 관점 전환 |
| **랜덤 충돌** | "소화기 기능을 강제 결합" | 강제 연결 |
| **감정 반전** | "가장 평화로운 것을 공포로" | 극성 전환 |
| **물리 법칙 해제** | "중력이 없다면" | 제약 해제 |

---

## Advanced Patterns (10+ minutes)

### 연속 카오스 (Chained Chaos)

1차 카오스 → 수확 → 2차 카오스 (수확 키워드로):

```
/chaos 커피숍
    ↓
수확: "시간이 멈춘 공간", "입장료는 비밀 이야기"
    ↓
/chaos 시간이 멈춘 공간 + 비밀 이야기
    ↓
더 깊은 아이디어
```

### 대립 카오스 (Opposing Chaos)

같은 주제를 정반대 관점에서:

```
/chaos 커피숍 --mode 유토피아
/chaos 커피숍 --mode 디스토피아
    ↓
두 결과 병합 → 중간 지점에서 혁신
```

### 멀티 도메인 충돌

```
/chaos 커피숍 + 우주 + 치료 + 게임
    ↓
4개 도메인 강제 충돌 → 예상치 못한 조합
```

---

## Deep Research 연동

### Chaos → Research 파이프라인

```
Phase 1: /chaos {문제}
    ↓
Phase 2: 수확 → 컨셉 3개
    ↓
Phase 3: /research {가장 유망한 컨셉}
    ↓
Phase 4: Go/No-Go 판정
    ↓
Phase 5: 실행 또는 다음 컨셉으로
```

### 연동 명령

```
/chaos {주제} --then-research
```

자동으로:
1. Chaos 실행
2. Harvest
3. 가장 유망한 컨셉으로 Deep Research 실행

---

## Output Format

```markdown
# 🌀 Chaos Engine 결과: {주제}

---

## Phase 1: CHAOS

>>> CHAOS STREAM START >>>
[의식의 흐름 500+ 단어]
<<< CHAOS STREAM END <<<

---

## Phase 2: HARVEST

### 채굴된 아이디어 (Top 5)
| # | 키워드 | 흥미 포인트 |
|---|--------|------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

### 발견된 패턴
- [...]

---

## Phase 3: GROUND

### 비즈니스 컨셉
**컨셉 1: [이름]**
- 한 줄: [...]
- 타겟: [...]
- 가치: [...]
- 수익: [...]

### 실행 가능성
| 컨셉 | 점수 | 추천 |
|------|------|------|
| 1 | /10 | |

### 🎯 다음 액션
1. [...]
2. [...]

---
*Generated by JARVIS Chaos Engine v1.0*
```

---

## Works Well With

**Skills**:
- **jarvis-deep-research** - 🔄 양방향 피드백 루프 (v2.1 강화)
- **moai-foundation-core** - 실행 프레임워크

**Workflow (v2.1 - Iterative Loop)**:
```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   창의적 문제 → Chaos Engine → 아이디어                  │
│                     ↓                                   │
│            🚨 User Gate (현실 확인)                      │
│                     ↓                                   │
│   유망 아이디어 → Deep Research → Reality Gate           │
│                     ↓                                   │
│   ┌─ Gate 통과 → Go/No-Go 판정 → 실행                   │
│   │                                                     │
│   └─ Gate 실패 ──→ 🔄 Chaos 재발동                       │
│                         ↓                               │
│                    새 아이디어                           │
│                         ↓                               │
│                    Research 재검증                       │
│                         ↓                               │
│                    (반복... max 3회)                     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Files**:
- **insights.md** - 유망 아이디어 저장
- **inbox.md** - 나중에 검토할 아이디어

---

## Module Deep Dives

- [Chaos Protocol](modules/chaos-protocol.md) - 카오스 모드 상세
- [Harvest Techniques](modules/harvest.md) - 수확 기법 상세
- [Business Ground](modules/ground.md) - 비즈니스 착지 상세

---

**Version**: 2.1.0
**Last Updated**: 2025-12-27
**Status**: ✅ Active

**Changelog**:
- v2.1.0: Research 피드백 루프 + 현실 검증 강화
  - 🚨 **User Gate 추가**: Harvest 직후 사용자 현실 확인 필수
    - "이런 서비스 쓰고 계세요?" 질문
    - 경쟁자 인지 여부 확인
    - 선호 아이디어 확인
  - 🔄 **Research Feedback Loop**: 양방향 피드백
    - Research 결과 기반 Chaos 재발동
    - 경쟁사 포화 → 타겟 피벗 Chaos
    - 새 기회 발견 → 기회 전용 Chaos
    - 최대 3회 반복 루프
  - 📐 **Workflow 개선**: 반복 순환 구조로 변경
  - 🔗 **jarvis-deep-research v1.5.0과 양방향 연동**
- v2.0.0: Tree of Thought 통합
  - Phase 3 (BRANCH): 아이디어 분기 패턴 추가
  - Phase 4 (EVALUATE): 5가지 기준 평가 매트릭스
  - Sequential Thinking MCP 연동
  - 경로별 변주 기법 (스케일/타겟/가격/기술/융합)
  - 탈락 경로 보존 (inbox.md)
- v1.0.0: 초기 버전
  - Chaos → Harvest → Ground 3단계
