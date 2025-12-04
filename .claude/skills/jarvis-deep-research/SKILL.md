---
name: jarvis-deep-research
description: Agentic deep research with dynamic planning, self-reflection loops, and query refinement for actionable insights
version: 1.3.0
modularized: true
updated: 2025-12-04
status: active
tags:
  - research
  - analysis
  - jarvis
  - deep-dive
  - agentic
allowed-tools: WebSearch, WebFetch, Read, Grep, Glob, Task
---

# JARVIS Deep Research v1.3

**Agentic 방식의 재귀적(Recursive) 워크플로우** 기반 심층 리서치 스킬.
단순 정보 나열이 아닌, **스스로 질문을 생성하고 평가하는** 자율적 루프로 사용자 맥락에 맞는 실행 가능한 인사이트를 도출합니다.

**Core Philosophy**:
- Gemini Deep Research 아키텍처 참조
- Planning → Execution → Reflection → Iteration 루프
- Chain of Thought + ReAct(Reasoning + Acting) 결합

---

## Quick Reference (30 seconds)

**What is JARVIS Deep Research v1.3?**

5단계 Agentic 프로토콜 기반 심층 리서치 프레임워크:

```
Phase 0: PLANNING (동적 계획 수립) ← NEW
    ↓
Phase A: EXPLORE (Haiku 병렬 탐색)
    ↓
SELF-REFLECTION (매 검색 후 평가) ← NEW
    ↓
Phase B: SYNTHESIZE (Opus 종합 + 루프 트리거)
    ↓
Phase C: VERDICT (실행 판정)
```

**핵심 개선 (v1.2 → v1.3)**:
- ✅ Phase 0: 동적 하위 질문 생성
- ✅ Self-Reflection: 매 검색 후 자동 평가
- ✅ 쿼리 정제: 부족 시 동적 수정
- ✅ 정보 충분성: 자동 체크리스트

**Quick Access**:
- 리서치 프로토콜 → [Protocol Module](modules/protocol.md)
- 분석 렌즈 → [Lenses Module](modules/lenses.md)
- 실행 가능성 필터 → [Feasibility Module](modules/feasibility.md)

**Triggers**:
- `/research {주제}`
- `/research {주제} --deep` (강제 루프 활성화)
- `/research {주제} --parallel` (병렬 탐색)

---

## The Agentic Workflow

### 전체 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│  PHASE 0: PLANNING (동적 계획 수립)                          │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 1. 핵심 의도(Intent) + 암묵적 요구사항 파악             │  │
│  │ 2. 하위 질문(Sub-questions) 3-5개 자동 생성            │  │
│  │ 3. 각 질문별 검색 키워드 계획                          │  │
│  │ 4. 정보 의존성 순서 결정                               │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────┬───────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  PHASE A: EXPLORE (Haiku 병렬 탐색)                          │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐            │
│  │ Q1 탐색 │ │ Q2 탐색 │ │ Q3 탐색 │ │ Q4 탐색 │            │
│  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘            │
│       └───────────┴───────────┴───────────┘                 │
└─────────────────────────────┬───────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  SELF-REFLECTION (매 검색 후 자동 평가)                      │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ □ 충분한가? → 부족 시 쿼리 정제 후 재탐색              │  │
│  │ □ 모순되는가? → 팩트체크 검색 트리거                   │  │
│  │ □ 최신인가? → '2024', 'latest' 키워드 추가            │  │
│  │ □ 새 개념 발견? → 하위 질문 추가 (Branch)             │  │
│  └───────────────────────────────────────────────────────┘  │
│                              ↓                              │
│            ┌─────────────────┴─────────────────┐            │
│            ↓                                   ↓            │
│      [정보 부족]                          [충분함]          │
│            ↓                                   ↓            │
│      쿼리 정제 후                         Phase B로         │
│      Phase A 재실행                                         │
└─────────────────────────────┬───────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  PHASE B: SYNTHESIZE (Opus 종합 + 연쇄 검증 루프)            │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 중요 정보 "A+B=C" 발견 시:                             │  │
│  │ ┌─────────────────────────────────────────────────┐   │  │
│  │ │ 🔍 검증형: 정말 A+B=C 맞아?                      │   │  │
│  │ │ 🔄 반전형: A-B는 어떻게 돼?                      │   │  │
│  │ │ 📊 확장형: C 외에 D, E도 있어?                   │   │  │
│  │ └─────────────────────────────────────────────────┘   │  │
│  │                                                       │  │
│  │ Loop < 3 → 자동 Phase A' 트리거                       │  │
│  │ Loop ≥ 3 → "계속할까요?" 확인                         │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────┬───────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  PHASE C: VERDICT (사용자 맥락 기반 실행 판정)               │
│  Go / No-Go / Conditional + 다음 액션                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 0: PLANNING (동적 계획 수립)

### 목적
사용자 질문을 분석하여 **하위 질문(Sub-questions)**을 자동 생성하고 탐색 전략을 수립합니다.

### 프로토콜

```markdown
## Phase 0: 동적 계획 수립

### 핵심 의도 분석
- **Primary Intent**: [사용자가 명시적으로 원하는 것]
- **Secondary Intent**: [암묵적으로 필요한 것]
- **Implicit Needs**: [사용자 맥락에서 추론되는 것]

### 하위 질문 자동 생성

| # | 하위 질문 | 검색 키워드 | 우선순위 | 의존성 |
|---|----------|-----------|---------|--------|
| 1 | [질문1] | [키워드1, 키워드2] | 필수 | 없음 |
| 2 | [질문2] | [키워드1] | 필수 | Q1 후 |
| 3 | [질문3] | [키워드1] | 선택 | 없음 |
| 4 | [질문4] | [키워드1] | 필수 | Q2 후 |
| 5 | [질문5] | [키워드1] | 선택 | Q3 후 |

### 정보 의존성 그래프
[질문 간 의존 관계 시각화]
```

### 하위 질문 생성 규칙

```yaml
sub_question_rules:
  count: 3-5개

  categories:
    - type: "시장/규모"
      keywords: ["market size", "growth rate", "TAM"]
    - type: "경쟁사"
      keywords: ["competitors", "alternatives", "market share"]
    - type: "타겟 고객"
      keywords: ["pain points", "needs", "willingness to pay"]
    - type: "기술/구현"
      keywords: ["how to", "implementation", "technology"]
    - type: "리스크"
      keywords: ["risk", "legal", "challenges"]

  priority:
    필수: "의사결정에 필수적인 정보"
    선택: "있으면 좋은 추가 정보"
```

---

## Self-Reflection (매 검색 후 평가)

### 목적
매 검색 결과를 자동 평가하여 **충분성/모순/최신성**을 판단하고 필요시 쿼리를 정제합니다.

### 평가 체크리스트

```yaml
self_reflection:
  questions:
    - id: sufficiency
      question: "이 정보가 질문에 대한 답이 되는가?"
      if_no: "구체적 데이터를 위해 'statistics', 'data', 'report' 추가"

    - id: contradiction
      question: "정보가 서로 모순되는가?"
      if_yes: "팩트체크 검색 트리거 (다른 소스 교차 검증)"

    - id: recency
      question: "정보가 최신인가? (2024년 이후?)"
      if_no: "'2024', 'latest', 'recent' 키워드 추가 후 재검색"

    - id: new_concept
      question: "새로운 중요 개념이 발견되었는가?"
      if_yes: "새 하위 질문으로 추가 (Branch)"

    - id: completeness
      question: "핵심 질문에 데이터 기반 답변이 가능한가?"
      if_no: "부족한 영역 식별 → 추가 검색"
```

### 쿼리 정제 규칙

```yaml
query_refinement:
  triggers:
    - condition: "결과가 너무 넓음"
      action: "니치 키워드 추가"
      example: '"LEGO tools" → "LEGO retirement prediction tools"'

    - condition: "결과가 오래됨"
      action: "연도 키워드 추가"
      example: '"market size" → "market size 2024"'

    - condition: "데이터 부족"
      action: "수치 키워드 추가"
      example: '"LEGO investment" → "LEGO investment returns statistics"'

    - condition: "가격 정보 필요"
      action: "가격 키워드 추가"
      example: '"BrickEconomy Premium" → "BrickEconomy Premium price $ monthly"'
```

### 정보 충분성 판단

```yaml
information_completeness:
  checklist:
    - "핵심 질문에 데이터 기반 답변 가능한가?"
    - "주요 주장에 출처가 있는가?"
    - "반대 의견/리스크가 포함됐는가?"
    - "실행 가능한 결론이 도출됐는가?"

  threshold:
    충분: 4/4 만족 → Phase B 진행
    부족: 3/4 이하 → 추가 검색 루프
```

---

## Phase A: EXPLORE (Haiku 병렬 탐색)

### 병렬 탐색 구조

```yaml
parallel_exploration:
  agents: 4개 (Haiku 모델)

  default_areas:
    - name: "시장/규모"
      focus: "시장 크기, 성장률, TAM"
    - name: "경쟁사"
      focus: "기존 플레이어, 기능, 가격"
    - name: "타겟 고객"
      focus: "페인포인트, 니즈, 지불 의향"
    - name: "리스크"
      focus: "법적/기술적/사업적 리스크"

  output_format:
    - 핵심 수치 테이블
    - 출처 명시
    - 신뢰도 (High/Medium/Low)
```

### 탐색 에이전트 프롬프트 템플릿

```markdown
**리서치 임무**: [하위 질문]

**검색 키워드**:
- "[키워드1]"
- "[키워드2]"
- "[키워드3]"

**수집할 정보**:
1. [구체적 데이터 포인트 1]
2. [구체적 데이터 포인트 2]
3. [구체적 데이터 포인트 3]

**출력 형식**:
- 핵심 수치 테이블
- 출처 명시
- 정보 신뢰도 (High/Medium/Low)
```

---

## Phase B: SYNTHESIZE (종합 + 연쇄 검증)

### 연쇄 검증 트리거

```yaml
loop_triggers:
  # 1️⃣ 검증형 (Verify)
  verify:
    condition: "의사결정에 영향 주는 핵심 정보 발견"
    question: "이 정보가 정말 맞는가?"
    action: "다른 소스에서 교차 검증"
    examples:
      - '"시장 규모 $705M" → 다른 소스 확인'
      - '"AI 예측 정확도 90%" → 커뮤니티 반응 확인'

  # 2️⃣ 반전형 (Invert)
  invert:
    condition: "A→B 관계 발견, 역방향 미탐색"
    question: "반대 경우는 어떻게 되는가?"
    action: "역방향/반대 케이스 탐색"
    examples:
      - '"예측 서비스 장점" → 예측 서비스 단점/실패 사례'
      - '"가격 하락 알림" → 가격 상승 알림 수요'

  # 3️⃣ 확장형 (Expand)
  expand:
    condition: "발견된 옵션 외 대안 가능성"
    question: "C 외에 D, E도 존재하는가?"
    action: "범위 확장 탐색"
    examples:
      - '"경쟁사 A, B" → 신생 스타트업은?'
      - '"레고 투자" → 포켓몬/TCG 투자 비교'

loop_control:
  auto_loop: 3        # 3회까지 자동 실행
  max_loop: 5         # 최대 5회 (안전장치)
  confirm_after: 3    # 3회 이후 사용자 확인
```

### 합성(Synthesis) 규칙

```yaml
synthesis_rules:
  - name: "인과관계 연결"
    description: "A문서의 원인 + B문서의 결과 연결"
    example: "시장 성장(A) → 경쟁 심화(B) → 차별화 필요(결론)"

  - name: "교차 검증"
    description: "서로 다른 소스에서 온 정보 비교"
    example: "BrickEconomy $705M vs WILCO $705M → High 신뢰도"

  - name: "패턴 발견"
    description: "여러 데이터에서 공통 패턴 추출"
    example: "페인포인트 3개 모두 '타이밍' 관련 → 핵심 니즈"
```

---

## Phase C: VERDICT (실행 판정)

### 사용자 맥락 필터

```yaml
user_context_filter:
  auto_load:
    - profile.md → 역할, 목표, 기술 스택, 제약 조건
    - insights.md → 이미 검토한 아이템 (재추천 방지)

  evaluation_criteria:
    - 초기 비용: "$"
    - 1인 실행 가능: "Y/N"
    - 자동화 범위: "%"
    - 기술 스택 적합: "Y/N"
    - 첫 수익까지: "기간"
    - 예상 ROI: "배수"
    - 리스크 레벨: "H/M/L"
```

### Go/No-Go 판정

```markdown
### 최종 판정: [Go / No-Go / Conditional]

**판정 근거:**
1. [데이터 기반 근거 1]
2. [데이터 기반 근거 2]
3. [사용자 맥락 기반 근거]

### 다음 액션 (내일 당장 할 수 있는 것)
1. [구체적 액션 1] - [예상 시간]
2. [구체적 액션 2] - [예상 시간]
3. [구체적 액션 3] - [예상 시간]
```

---

## Output Format

```markdown
# 📊 Deep Research: {주제}

## Phase 0: 계획 수립
- 하위 질문 5개
- 검색 키워드 계획
- 의존성 그래프

## Phase A: 탐색 결과
### Q1: [하위 질문 1]
[결과 테이블 + 출처]

### Q2: [하위 질문 2]
[결과 테이블 + 출처]

...

## Self-Reflection 로그
| 질문 | 평가 | 액션 |
|------|------|------|
| Q1 충분성 | ✅/🟡/🔴 | [취한 액션] |
| Q2 모순 | ✅/🟡/🔴 | [취한 액션] |

## Phase B: 종합 분석
### 핵심 발견
1. [인사이트 1]
2. [인사이트 2]

### 루프 트리거 결과
- 검증형: [결과]
- 반전형: [결과]
- 확장형: [결과]

## Phase C: 실행 판정
### 사용자 맥락 필터
| 항목 | 평가 |
|------|------|
| 초기 비용 | $ |
| 1인 실행 | Y/N |
| ... | ... |

### 🎯 최종 판정: [Go / No-Go / Conditional]

**근거:**
1. ...
2. ...

### ⚡ 다음 액션
1. [액션] - [시간]
2. [액션] - [시간]

---
*Generated by JARVIS Deep Research v1.3*
*Auto-saved to: insights.md*
```

---

## Quality Constraints

| 제약 | 설명 |
|------|------|
| **No Fluff** | 뻔한 내용 과감히 생략, 밀도 높은 정보 |
| **Data-Backed** | 모든 주장에 데이터/출처 근거 |
| **Self-Critical** | 매 검색마다 자기 평가 |
| **User-Fit** | 사용자 상황 무시한 일반론 금지 |
| **Actionable** | 실행 불가능한 제안 금지 |
| **Transparent** | Self-Reflection 로그 공개 |

---

## Works Well With

**Agents**:
- **Explore (Haiku)** - 병렬 탐색
- **mcp-context7** - 최신 문서/API 참조
- **mcp-sequential-thinking** - 복잡한 추론

**Skills**:
- **jarvis-chaos-engine** - 창의적 발산 → 검증 루프
- **moai-foundation-core** - 기본 원칙

**Files**:
- **profile.md** - 사용자 맥락 로드
- **insights.md** - 리서치 결과 저장

---

## Module Deep Dives

- [Protocol Module](modules/protocol.md) - Phase별 상세 가이드
- [Lenses Module](modules/lenses.md) - 분석 렌즈 상세
- [Feasibility Module](modules/feasibility.md) - 실행 가능성 필터 상세

---

**Version**: 1.3.0
**Last Updated**: 2025-12-04
**Status**: ✅ Active

**Changelog**:
- v1.3.0: Agentic 워크플로우 도입
  - Phase 0 (동적 계획 수립) 추가
  - Self-Reflection (매 검색 후 평가) 추가
  - 쿼리 정제 규칙 추가
  - 정보 충분성 자동 체크리스트
  - Gemini Deep Research 아키텍처 참조
- v1.2.0: 연쇄 검증 루프 추가
- v1.1.0: 2-Phase 병렬 탐색 패턴 추가
- v1.0.0: 초기 버전
