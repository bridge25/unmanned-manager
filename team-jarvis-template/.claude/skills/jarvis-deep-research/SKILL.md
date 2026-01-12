---
name: jarvis-deep-research
description: Recursive exploration loop - 탐정의 추적처럼 발견을 따라가며 본질에 수렴하는 심층 리서치
version: 2.3.0
modularized: true
updated: 2025-12-31
status: active
tags:
  - research
  - analysis
  - jarvis
  - deep-dive
  - recursive
  - exploration
  - detective
  - hypothesis
  - verification
allowed-tools: WebSearch, WebFetch, Read, Grep, Glob, Task, mcp__sequential-thinking__sequentialthinking
---

# JARVIS Deep Research v2.1

**탐정의 추적, 과학자의 탐구** - 재귀적 탐구 루프 기반 심층 리서치.

고정된 Phase를 순차 실행하는 것이 아니라, **발견을 따라가며 궤도를 수정**하고, **연결을 만들어가며 본질에 수렴**합니다.

---

## v2.1 핵심 원칙: 동적 판단 + 완급 조절

```
┌─────────────────────────────────────────────────────────────┐
│  🚨 CRITICAL (절대 규칙) - 이건 무조건                       │
│  ⚠️ IMPORTANT - 웬만하면                                    │
│  💡 GUIDE - 권장 사항                                        │
└─────────────────────────────────────────────────────────────┘
```

### 🚨 CRITICAL: 절대 규칙 (이것만은 반드시)

```yaml
absolute_rules:
  1_no_confirmation_bias:
    rule: "지지 증거를 찾았으면 반드시 반박 증거도 찾아라"
    why: "확증 편향은 리서치의 적. 한쪽만 보면 틀린다"
    enforcement: "VERIFY 단계에서 반박 검색 없이 넘어가면 실패"

  2_no_premature_convergence:
    rule: "새로운 통찰이 계속 나오는데 수렴하지 마라"
    why: "숫자 채우기가 아닌 통찰 고갈이 수렴 기준"
    enforcement: "마지막 탐색에서 새 발견 있으면 더 파기"

  3_no_generic_conclusion:
    rule: "일반론으로 끝내지 마라. 사용자 맥락에 연결하라"
    why: "누구에게나 해당되는 결론은 무가치"
    enforcement: "결론에 사용자 이름/상황 없으면 미완성"

  # 🚨 v2.3.0 신규: 경쟁사 검색 선행 필수
  4_competition_search_first:
    rule: "결론 내기 전에 반드시 경쟁사부터 검색하라"
    why: "'블루오션'이라고 단정하면 안 된다. 내가 모르는 것 ≠ 없는 것"
    enforcement: |
      - PROBE 단계에서 경쟁사 검색 최소 5회 필수
      - "경쟁사 없음" 결론 전 반박 검색 3회 필수
      - User Gate에서 "아세요?" 대신 경쟁사 리스트 먼저 제시
    anti_pattern: |
      ❌ "한국에 이런 서비스 없어요" (검색 안 하고 단정)
      ❌ User에게 "경쟁사 아세요?" → "모름" → "블루오션!"
      ❌ 글로벌만 검색하고 한국 시장 검색 생략
    correct_pattern: |
      ✅ 먼저 검색: "[아이디어] 경쟁사 한국", "[아이디어] 대안"
      ✅ 한국 대기업 체크: "[아이디어] 네이버/카카오/토스"
      ✅ 글로벌 서비스 한국 진출 체크: "[글로벌 서비스] 한국어"
      ✅ 검색 결과 기반으로 경쟁사 리스트 제시 후 User 확인
```

### ⚠️ IMPORTANT: 중요 가이드라인

```yaml
important_guidelines:
  - "1차 소스를 우선 탐색하라 (블로그 요약 < 창업자 직접 글)"
  - "발견을 가설로 전환하고 검증하라"
  - "막다른 길은 과감히 버려라"
```

### 💡 GUIDE: 권장 사항

```yaml
recommendations:
  - "복잡한 판단에는 Sequential Thinking 활용"
  - "발견들 사이 연결 맵 시각화"
  - "버린 경로도 기록 (나중에 참고)"
```

---

## Core Philosophy

```
리서치는 정보 수집이 아니다.
리서치는 추론과 탐구가 동반되는 궤도 수정의 연속이다.

탐정이 단서를 따라가듯,
과학자가 가설을 검증하며 수정하듯,
발견이 다음 질문을 만들고, 그 질문이 더 깊은 발견으로 이어진다.

깊이는 검색량에서 오지 않는다.
깊이는 연결성에서 온다.
```

**Anti-Patterns (하지 말 것)**:
- ❌ 질문 10개 미리 쪼개놓고 병렬 수집
- ❌ 고정 역할 에이전트에 억지로 할당
- ❌ 정보량으로 승부
- ❌ 수집 후 합치기

**Core Patterns (해야 할 것)**:
- ✅ 탐색하면서 질문 생성
- ✅ 발견에 따라 방향 수정
- ✅ 연결성으로 승부
- ✅ 본질에 수렴할 때까지 반복

---

## The Exploration Loop

```
┌─────────────────────────────────────────────────────────────────┐
│                    RECURSIVE EXPLORATION LOOP                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [질문]                                                         │
│     ↓                                                           │
│  ╔═════════════════════════════════════════════════════════╗   │
│  ║  PROBE (탐침)                                            ║   │
│  ║  "이 주제의 지형이 어떻게 생겼지?"                         ║   │
│  ╚═════════════════════════════════════════════════════════╝   │
│     ↓                                                           │
│  ╔═════════════════════════════════════════════════════════╗   │
│  ║  DISCOVER (발견)                                         ║   │
│  ║  "어? 이게 뭐지?" - 예상 못한 것 포착                     ║   │
│  ╚═════════════════════════════════════════════════════════╝   │
│     ↓                                                           │
│  ╔═════════════════════════════════════════════════════════╗   │
│  ║  DECIDE (결정)                                           ║   │
│  ║  ├─ DIVE: 이 방향으로 깊이 파기                          ║   │
│  ║  ├─ BRANCH: 잠시 분기 후 유망한 쪽 선택                  ║   │
│  ║  └─ PRUNE: 이 경로 버리기                                ║   │
│  ╚═════════════════════════════════════════════════════════╝   │
│     ↓                                                           │
│  ╔═════════════════════════════════════════════════════════╗   │
│  ║  CONNECT (연결)                                          ║   │
│  ║  "이 발견이 저 발견과 어떻게 이어지지?"                   ║   │
│  ╚═════════════════════════════════════════════════════════╝   │
│     ↓                                                           │
│  ╔═════════════════════════════════════════════════════════╗   │
│  ║  CONVERGE? (수렴 판단)                                   ║   │
│  ║  "본질에 도달했나?"                                       ║   │
│  ║     ├─ NO → PROBE로 (새 방향)                            ║   │
│  ║     └─ YES → SYNTHESIZE                                  ║   │
│  ╚═════════════════════════════════════════════════════════╝   │
│     ↓                                                           │
│  [본질에 도달한 결론]                                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## PROBE: 탐침

**목적**: 주제의 지형 파악. 아직 어디로 갈지 모른다.

```yaml
probe:
  mindset: "지도 없이 정글에 들어간 탐험가"

  actions:
    - 초기 검색 2~3회 (많이 하지 않음)
    - 키워드, 플레이어, 쟁점 빠르게 스캔
    - "이 주제에서 뭐가 중요한 거지?" 감 잡기

  # 🚨 v2.3.0 신규: 경쟁사 검색 필수 (CRITICAL)
  competition_search_mandatory:
    when: "아이디어/제품/서비스 리서치 시"
    minimum_queries: 5
    required_searches:
      - query: "[아이디어] 경쟁사 한국"
        purpose: "한국 로컬 경쟁자 확인"
      - query: "[아이디어] 서비스 앱 2024 2025"
        purpose: "최신 서비스 현황"
      - query: "[아이디어] 대안 alternative"
        purpose: "대체재 확인"
      - query: "[글로벌 서비스] 한국어 지원"
        purpose: "글로벌 서비스 한국 진출 여부"
      - query: "[아이디어] 네이버 카카오 토스"
        purpose: "한국 대기업 진출 여부"

    # 🚨 경쟁사 없다고 결론 내기 전 필수
    before_blue_ocean_claim:
      - "[아이디어] 이미 있는 서비스"
      - "[유사 서비스명] 한국"
      - "[아이디어] 실패 사례"

    enforcement: |
      ⚠️ 위 검색 없이 "블루오션" 또는 "경쟁사 없음" 판정 불가
      ⚠️ User에게 "경쟁사 아세요?" 전에 내가 먼저 검색
      ⚠️ 검색 결과 기반 경쟁사 리스트 제시 후 User 확인

  outputs:
    - 발견한 키워드들
    - 주요 플레이어/소스
    - "흥미로운 냄새"가 나는 방향들
    - 🚨 경쟁사 리스트 (v2.3.0 필수)

  duration: 짧게 (5분 이내)

  questions:
    - "이 주제의 핵심 축은 뭐지?"
    - "누가 이 분야의 권위자지?"
    - "어떤 논쟁/쟁점이 있지?"
    - "뭔가 이상한 게 보이나?"
    - 🚨 "이미 이거 하는 곳 있나?" (v2.3.0 필수)
```

**출력 형식**:

```markdown
## PROBE: 지형 파악

**검색**: [실행한 쿼리들]

**발견한 지형**:
- 핵심 축: [이 주제를 관통하는 것]
- 주요 플레이어: [누가 있나]
- 쟁점: [뭐가 논쟁인가]

🚨 **경쟁사 분석** (v2.3.0 필수):
| 경쟁사 | 국적 | 핵심 기능 | 가격 | 한국어 |
|--------|:----:|----------|------|:------:|
| [A] | | | | |
| [B] | | | | |
| [C] | | | | |

**경쟁 강도**: [레드오션 / 경쟁 있음 / 틈새 있음 / 블루오션]
**블루오션 판정 근거**: [검색 쿼리 + 결과 요약] (블루오션일 경우만)

**냄새나는 방향들**:
1. [방향 A] - 왜 흥미로운가
2. [방향 B] - 왜 흥미로운가
3. [방향 C] - 왜 흥미로운가

**다음**: [어느 방향부터 파볼까?]
```

---

## DISCOVER: 발견

**목적**: "어? 이게 뭐지?" 순간 포착.

```yaml
discover:
  mindset: "탐정이 단서를 발견하는 순간"

  what_to_look_for:
    - 예상과 다른 것
    - 모순되는 정보
    - 빈틈/갭
    - 연결점
    - "왜?"라는 질문이 떠오르는 것

  discovery_types:
    - type: "contradiction"
      desc: "A라고 했는데 B도 있네?"
      action: "왜 모순이지? → 파고들기"

    - type: "gap"
      desc: "이건 아무도 얘기 안 하네?"
      action: "왜 비어있지? → 기회 or 이유가 있나"

    - type: "connection"
      desc: "이게 저거랑 연결되네?"
      action: "어떻게 연결되지? → 인과관계 추적"

    - type: "anomaly"
      desc: "이건 좀 이상한데?"
      action: "왜 이상하지? → 깊이 파기"

    - type: "pattern"
      desc: "이 패턴이 반복되네?"
      action: "왜 반복되지? → 본질 추적"
```

**출력 형식**:

```markdown
## DISCOVER: 발견

**발견 유형**: [contradiction / gap / connection / anomaly / pattern]

**발견 내용**:
"[구체적으로 뭘 발견했는지]"

**왜 중요한가**:
[이 발견이 왜 주목할 만한지]

**떠오른 질문**:
- [이 발견에서 파생된 질문 1]
- [이 발견에서 파생된 질문 2]

**다음**: [이 발견을 어떻게 추적할까?]
```

---

## DECIDE: 결정

**목적**: 발견을 바탕으로 다음 행동 결정.

```yaml
decide:
  mindset: "체스 플레이어가 다음 수를 고르는 순간"

  options:
    dive:
      when: "이 발견이 핵심 같다"
      action: "이 방향으로 집중 탐색"
      searches: "5~10회 깊이 파기"

    branch:
      when: "두 방향 다 유망해 보인다"
      action: "짧게 양쪽 탐색 → 유망한 쪽 선택"
      searches: "각 2~3회 후 판단"

    prune:
      when: "이 방향은 막다른 길 같다"
      action: "버리고 다른 방향으로"
      note: "버린 이유 기록 (나중에 참고)"

  decision_criteria:
    - "이게 원래 질문의 본질에 가까워지나?"
    - "이게 다른 발견들과 연결되나?"
    - "이게 실행 가능한 통찰로 이어질 가능성이 있나?"
    - "이미 알고 있는 것의 반복인가?"
```

**출력 형식**:

```markdown
## DECIDE: 결정

**선택**: [DIVE / BRANCH / PRUNE]

**이유**:
[왜 이 선택을 했는지]

**예상 경로**:
[이 선택이 어디로 이어질 것 같은지]

**버린 것** (있다면):
[다른 옵션을 버린 이유]
```

---

## CONNECT: 연결

**목적**: 발견들 사이의 관계 매핑.

```yaml
connect:
  mindset: "퍼즐 조각을 맞추는 사람"

  connection_types:
    - type: "causal"
      pattern: "A 때문에 B가 일어난다"

    - type: "correlation"
      pattern: "A가 있으면 B도 있다"

    - type: "tension"
      pattern: "A와 B가 충돌한다"

    - type: "hierarchy"
      pattern: "A가 B의 상위 개념이다"

    - type: "sequence"
      pattern: "A 다음에 B가 온다"

  key_questions:
    - "이 발견이 저 발견을 설명하나?"
    - "이 둘이 같은 원인에서 나왔나?"
    - "이 둘이 충돌하면 뭐가 이기나?"
    - "이걸 합치면 새로운 통찰이 나오나?"
```

**출력 형식**:

```markdown
## CONNECT: 연결

**연결 맵**:

```
[발견 A] ──(causal)──→ [발견 B]
    │                      │
    └──(tension)──→ [발견 C]
                           │
                    (explains)
                           ↓
                     [발견 D]
```

**핵심 연결**:
1. [A→B]: [어떻게 연결되는지]
2. [A↔C]: [어떤 긴장이 있는지]

**통합 인사이트**:
[연결들을 합쳤을 때 떠오르는 통찰]
```

---

## HYPOTHESIS: 가설 수립 (v2.1 신규)

**목적**: 발견을 가설로 전환. 검증 가능한 형태로.

```yaml
hypothesis:
  mindset: "과학자가 실험을 설계하는 순간"

  when: "DISCOVER에서 흥미로운 발견 후"

  format:
    pattern: "만약 [X]라면, [Y]일 것이다"
    example: "만약 'AI Comment Generator가 빠른 현금화'라면, Zyki 외에 다른 성공 사례가 있을 것이다"

  types:
    - type: "causal_hypothesis"
      pattern: "A가 B를 유발한다"
      verification: "A 없이 B가 발생하는 사례 찾기"

    - type: "correlation_hypothesis"
      pattern: "A가 있으면 B도 있다"
      verification: "A 있는데 B 없는 사례 찾기"

    - type: "negation_hypothesis"
      pattern: "X는 사실이 아니다"
      verification: "X를 뒷받침하는 증거 찾기"

  quality_check:
    - "검증 가능한가? (Yes/No로 판단 가능)"
    - "반증 가능한가? (틀렸음을 증명할 수 있나)"
    - "구체적인가? (모호하지 않은가)"

  output_format: |
    ## HYPOTHESIS: 가설 수립

    **가설**: [구체적 가설]

    **검증 방법**:
    - [이걸 찾으면 가설 지지]
    - [이걸 찾으면 가설 반박]

    **예상 결과**: [가설이 맞다면 예상되는 것]
```

---

## VERIFY/REFUTE: 검증/반박 (v2.1 신규)

**목적**: 가설을 데이터로 검증하거나 반박.

```yaml
verify_refute:
  mindset: "검사가 증거를 검토하는 순간"

  process:
    1_search_for_support:
      action: "가설을 지지하는 증거 적극 검색"
      searches: 2-3회

    2_search_for_refutation:
      action: "가설을 반박하는 증거 적극 검색"
      searches: 2-3회
      note: "⚠️ 이 단계를 건너뛰지 말 것 - 확증 편향 방지"

    3_weigh_evidence:
      action: "양쪽 증거 무게 비교"
      criteria:
        - 소스 신뢰도
        - 데이터 구체성
        - 시간적 최신성
        - 반복 확인 여부

  outcomes:
    verified:
      condition: "지지 증거 > 반박 증거 (명확한 차이)"
      action: "가설 채택 → CONNECT으로"
      note: "완전 확신이 아닌 '현재까지 지지됨'"

    refuted:
      condition: "반박 증거 > 지지 증거"
      action: "가설 폐기 → 새 HYPOTHESIS 또는 PRUNE"
      note: "⚠️ 반박도 중요한 발견. 기록 필수"

    inconclusive:
      condition: "증거 불충분"
      action: "더 깊은 검색 또는 가설 수정"

  # ⚠️ 필수 규칙
  anti_confirmation_bias:
    - "지지 증거만 찾지 말 것"
    - "반박 검색을 생략하지 말 것"
    - "원하는 결론에 맞추지 말 것"

  output_format: |
    ## VERIFY/REFUTE: 검증 결과

    **가설**: [테스트한 가설]

    **지지 증거**:
    1. [소스 + 내용]
    2. [소스 + 내용]

    **반박 증거**:
    1. [소스 + 내용]
    2. [소스 + 내용]

    **판정**: [VERIFIED / REFUTED / INCONCLUSIVE]

    **근거**: [왜 이 판정인지]
```

---

## Source Hierarchy (v2.1 신규)

**목적**: 1차 소스 우선. 요약/블로그 의존 방지.

```yaml
source_hierarchy:
  # 우선순위 높은 순
  tier_1_primary:
    sources:
      - 창업자 직접 작성 글 (Medium, 개인 블로그)
      - 공식 발표/보도자료
      - 인터뷰 원문
      - 실제 데이터/통계 (Stripe Atlas, YC 등)
      - 학술 논문/연구 보고서
    weight: 1.0
    action: "적극 탐색, 인용 시 명시"

  tier_2_analysis:
    sources:
      - 전문 미디어 분석 (TechCrunch, The Information)
      - 업계 리포트 (Gartner, CB Insights)
      - 전문가 해석
    weight: 0.7
    action: "참고하되 1차 소스로 검증"

  tier_3_aggregation:
    sources:
      - 블로그 요약글
      - 리스티클 (10 best X, Top 50 Y)
      - 뉴스레터 큐레이션
    weight: 0.3
    action: "단서로만 사용, 직접 인용 금지"

  tier_4_avoid:
    sources:
      - AI 생성 콘텐츠 (출처 불명)
      - SEO 스팸 글
      - 익명 포럼 댓글 (검증 없이)
    weight: 0.0
    action: "사용 금지"

  enforcement:
    - "VERIFY 단계에서 tier_1 최소 2개 필수"
    - "tier_3만으로 가설 검증 금지"
    - "인용 시 tier 명시"

  output_format: |
    **출처 분석**:
    - Tier 1 (1차): [사용한 1차 소스들]
    - Tier 2 (분석): [사용한 분석 소스들]
    - Tier 3 (집계): [참고만 한 소스들]
    - 검증 충족: [Y/N - Tier 1 최소 2개?]
```

---

## Depth Self-Assessment (v2.1)

**목적**: 수렴 전 깊이 자체 점검. **숫자가 아닌 질적 판단.**

```yaml
depth_assessment:
  # ❌ "5회마다" 같은 하드코딩 없음
  when: "수렴을 고려할 때마다 실행"

  # 🚨 CRITICAL 체크 (이건 반드시)
  critical_checks:
    - check: "반박 증거를 찾으려 시도했는가?"
      if_no: "🚨 수렴 불가 - 반박 검색 먼저"

    - check: "결론이 사용자 특화인가? (일반론 아닌가?)"
      if_no: "🚨 수렴 불가 - 맥락 연결 먼저"

    - check: "새 탐색에서 새 통찰이 고갈되었는가?"
      if_no: "🚨 수렴 불가 - 아직 캘 게 있음"

  # ⚠️ IMPORTANT 체크 (웬만하면)
  important_checks:
    - check: "가설을 세우고 검증했는가?"
    - check: "1차 소스를 봤는가? (블로그 요약만 아닌가?)"
    - check: "'왜냐하면...'으로 답할 수 있는가?"

  # 💡 GUIDE 체크 (권장)
  guide_checks:
    - check: "발견들 사이 연결을 만들었는가?"
    - check: "막다른 길을 버렸는가?"

  judgment:
    can_converge: "🚨 CRITICAL 모두 Yes + ⚠️ IMPORTANT 대부분 Yes"
    cannot_converge: "🚨 CRITICAL 하나라도 No"
    action_on_fail: "No인 항목을 Yes로 만드는 탐색 진행"

  output_format: |
    ## 🔍 Depth Check

    **🚨 CRITICAL**:
    - [ ] 반박 시도 완료
    - [ ] 맞춤 결론 (일반론 X)
    - [ ] 새 통찰 고갈

    **⚠️ IMPORTANT**:
    - [ ] 가설 검증
    - [ ] 1차 소스 활용
    - [ ] 근거 충분

    **판단**: [수렴 가능 / 더 파야 함]
    **부족한 것**: [구체적으로]
    **다음 액션**: [뭘 해야 하는지]
```

---

## Context Integration (v2.1 신규)

**목적**: 사용자 맥락과 연결 강제. 일반론 방지.

```yaml
context_integration:
  when: "CONNECT 단계에서 필수 실행"

  process:
    1_load_context:
      action: "사용자 프로필/상황 확인"
      sources:
        - current/profile.md
        - current/projects.md
        - current/survival-mission.md (있다면)
        - 대화에서 파악한 상황

    2_map_discoveries:
      action: "발견 ↔ 사용자 자산 매핑"
      questions:
        - "이 발견이 사용자의 기존 자산과 어떻게 연결되나?"
        - "사용자의 제약조건(시간/돈/기술)을 고려했나?"
        - "사용자의 목표에 직접 연결되나?"

    3_personalize:
      action: "일반 결론 → 맞춤 결론 전환"
      example:
        generic: "AI Comment Generator가 유망하다"
        personalized: "Tony님의 AI 경험 + 빌드인퍼블릭 역량으로 2주 내 MVP 가능"

  # ⚠️ 필수 체크
  validation:
    - "결론이 사용자 이름을 포함하는가?"
    - "사용자의 구체적 자산/제약이 언급되는가?"
    - "다른 사람에게도 해당되는 일반론이 아닌가?"

  output_format: |
    ## Context Integration: 맥락 연결

    **사용자 상황**:
    - 목표: [사용자의 핵심 목표]
    - 자산: [보유 기술/프로젝트/경험]
    - 제약: [시간/자금/리소스 한계]

    **발견 ↔ 맥락 매핑**:
    | 발견 | 사용자 연결점 | 적용 가능성 |
    |------|---------------|-------------|
    | [발견1] | [어떻게 연결?] | [높음/중간/낮음] |
    | [발견2] | [어떻게 연결?] | [높음/중간/낮음] |

    **맞춤 결론**:
    [일반론이 아닌 사용자 특화 결론]
```

---

## CONVERGE: 수렴 판단

**목적**: 본질에 도달했는지 판단.

```yaml
converge:
  mindset: "탐정이 '범인을 알았다'고 확신하는 순간"

  # ❌ 하드코딩 숫자 없음 - 질문 기반 판단
  # ✅ 아래 질문들로 수렴 여부 결정

  # ─────────────────────────────────────────────────────
  # 🚨 CRITICAL: 이 세 가지는 반드시 Yes여야 수렴 가능
  # ─────────────────────────────────────────────────────
  critical_gates:
    1_exhaustion:
      question: "마지막 탐색들에서 새로운 통찰이 나왔는가?"
      yes_means: "아직 캘 게 있다 → 더 파기"
      no_means: "고갈됨 → 수렴 가능 ✓"

    2_refutation:
      question: "반박 증거를 찾으려 시도했는가?"
      yes_means: "확증 편향 체크 완료 ✓"
      no_means: "🚨 절대 수렴 불가 - 반박 검색 먼저"

    3_personalization:
      question: "결론이 이 사용자만을 위한 것인가?"
      yes_means: "맞춤 완료 ✓"
      no_means: "🚨 절대 수렴 불가 - 일반론임"

  # ─────────────────────────────────────────────────────
  # ⚠️ IMPORTANT: 대부분 Yes면 좋음
  # ─────────────────────────────────────────────────────
  important_signals:
    - "'왜냐하면...'으로 답할 수 있다"
    - "가설을 세우고 검증했다"
    - "1차 소스(창업자 글, 실제 데이터)를 봤다"
    - "발견들이 하나의 그림으로 수렴한다"

  # ─────────────────────────────────────────────────────
  # 판단 흐름
  # ─────────────────────────────────────────────────────
  judgment_flow: |
    1. 🚨 CRITICAL 세 가지 체크
       └─ 하나라도 통과 못함 → 수렴 불가. 해당 항목 해결.

    2. ⚠️ IMPORTANT 시그널 체크
       └─ 대부분 No → 더 파기 권장
       └─ 대부분 Yes → 수렴 가능

    3. 최종 질문: "다른 사람에게 설명하면 납득시킬 수 있는가?"
       └─ Yes → SYNTHESIZE로
       └─ No → 뭐가 부족한지 파악 → 더 파기

  actions:
    converged:
      - CRITICAL 모두 통과 확인
      - SYNTHESIZE로 이동
      - 최종 정리

    not_converged:
      - 통과 못한 항목 식별
      - 해당 항목 해결 방향으로 탐색
      - 루프 계속
```

**출력 형식**:

```markdown
## CONVERGE: 수렴 판단

**상태**: [수렴 / 미수렴]

**근거**:
- [수렴/미수렴 시그널 체크]

**만약 미수렴**:
- 가장 큰 빈틈: [뭐가 부족한지]
- 다음 PROBE 방향: [어디를 더 파야 하는지]

**만약 수렴**:
- 도달한 본질: [한 문장으로]
- SYNTHESIZE로 이동
```

---

## Loop Execution Protocol

```yaml
loop_protocol:
  # ❌ 하드코딩 숫자 없음 - 동적 판단
  max_iterations: 20  # 안전장치 (무한 루프 방지용)

  per_iteration:
    - probe_or_dive
    - discover
    - hypothesis
    - verify_or_refute
    - decide
    - connect (발견 3개 이상 쌓이면)
    - converge_check (동적 기준으로)

  iteration_log:
    format: |
      ### Iteration {n}

      **PROBE/DIVE**: [뭘 탐색했나]
      **DISCOVER**: [뭘 발견했나] (새 발견 여부: Y/N)
      **HYPOTHESIS**: [가설 수립]
      **VERIFY/REFUTE**: [검증 결과]
      **DECIDE**: [뭘 선택했나]
      **CONNECT**: [뭘 연결했나]
      **수렴 판단**: [아래 질문들 체크]
```

### 🚨 동적 수렴 판단 (숫자가 아닌 질문으로)

```yaml
convergence_questions:
  # 모든 질문에 "Yes"면 수렴 가능
  # 하나라도 "No"면 해당 방향 더 파기

  🚨_critical_questions:  # 이건 반드시 Yes여야 함
    - question: "마지막 2번 탐색에서 새로운 통찰이 나왔는가?"
      if_yes: "아직 캘 게 있다 → 더 파기"
      if_no: "고갈됨 → 수렴 가능"

    - question: "반박 증거를 찾으려 시도했는가?"
      if_yes: "확증 편향 체크 완료"
      if_no: "🚨 반드시 반박 검색 먼저"

    - question: "결론이 이 사용자만을 위한 맞춤인가?"
      if_yes: "개인화 완료"
      if_no: "🚨 일반론 → 맥락 연결 먼저"

  ⚠️_important_questions:  # 웬만하면 Yes
    - question: "핵심 질문에 '왜냐하면...'으로 답할 수 있는가?"
      if_no: "근거 부족 → 더 파기"

    - question: "가설을 세우고 검증했는가?"
      if_no: "발견 나열만 함 → 가설화 필요"

    - question: "1차 소스(창업자 글, 실제 데이터)를 충분히 봤는가?"
      if_no: "블로그 요약 의존 → 1차 소스 탐색"

  💡_guide_questions:  # 권장
    - question: "막다른 길을 버렸는가?"
    - question: "발견들 사이 연결을 만들었는가?"
```

### 수렴 판단 흐름

```
매 Iteration 끝에:

1. 🚨 CRITICAL 질문 체크
   └─ 하나라도 No → 해당 항목 해결 먼저

2. ⚠️ IMPORTANT 질문 체크
   └─ 대부분 No → 더 파기
   └─ 대부분 Yes → 수렴 고려

3. 최종 판단
   └─ "새 통찰 고갈" + "반박 시도 완료" + "맞춤 결론"
   └─ 세 개 다 Yes면 → CONVERGE
```

### 사용자 체크포인트 (동적)

```yaml
user_checkpoints:
  # 숫자 기반이 아닌 상황 기반

  - when: "방향 전환(BRANCH) 2회 발생 시"
    ask: "여러 방향을 탐색 중입니다. [요약]. 집중할 방향 있으신가요?"

  - when: "같은 주제 3회 연속 탐색 시"
    ask: "이 방향 깊이 파고 있습니다. 계속할까요, 다른 방향 볼까요?"

  - when: "수렴 조건 충족 시"
    ask: "본질에 도달한 것 같습니다. 마무리할까요, 더 파볼까요?"
```

---

## Sequential Thinking Integration

매 단계에서 **추론 과정을 명시적으로 기록**:

```yaml
sequential_thinking:
  when: "DECIDE 또는 CONNECT에서 복잡한 판단 필요시"

  usage:
    - thought: "발견 A와 B가 모순된다. 왜일까?"
      thoughtNumber: 1
      totalThoughts: 4
      nextThoughtNeeded: true

    - thought: "가설: A는 2023년 데이터, B는 2025년 데이터. 시장이 변했나?"
      thoughtNumber: 2

    - thought: "검증: 2024년 데이터를 찾아보자"
      thoughtNumber: 3

    - thought: "결론: 시장이 2024년에 전환점을 맞았다. A→B 변화가 설명됨"
      thoughtNumber: 4
      nextThoughtNeeded: false

  benefits:
    - 추론 과정 투명화
    - 나중에 왜 이런 결론에 도달했는지 추적 가능
    - 분기(branch) 지원으로 대안 탐색
```

---

## Output Format

```markdown
# 🔍 Deep Research: {주제}

---

## 탐구 여정 (Exploration Journey)

### Iteration 1: 지형 파악
**PROBE**: [초기 탐색]
**DISCOVER**: [첫 발견]
**DECIDE**: [선택 - DIVE/BRANCH/PRUNE]

### Iteration 2: 깊이 파기
**DIVE**: [파고든 방향]
**DISCOVER**: [새 발견]
**CONNECT**: [연결]
**DECIDE**: [다음 선택]

### Iteration 3: ...

[반복...]

### Iteration N: 수렴
**CONVERGE**: 본질에 도달

---

## 발견 맵 (Discovery Map)

```
[핵심 발견 1] ──────→ [핵심 발견 2]
      │                    │
      └───→ [핵심 발견 3] ←─┘
                  │
                  ↓
            [본질/결론]
```

---

## 본질 (The Core)

**한 문장**: [이 리서치의 핵심 결론]

**도달 경로**: [어떻게 여기까지 왔는지 3줄 요약]

**핵심 근거**:
1. [데이터 기반 근거 1]
2. [데이터 기반 근거 2]
3. [데이터 기반 근거 3]

---

## 실행 판정

**Go / No-Go / Conditional**: [판정]

**이유**: [왜 이 판정인지]

**다음 액션**:
1. [내일 당장 할 수 있는 것]
2. [이번 주 할 것]
3. [더 알아봐야 할 것]

---

## 버린 경로들 (Pruned Paths)

| 경로 | 버린 이유 | 나중에 재검토? |
|------|----------|---------------|
| [A] | [이유] | Y/N |
| [B] | [이유] | Y/N |

---

*Generated by JARVIS Deep Research v2.0*
*Exploration Loop: {N} iterations*
*Total Discoveries: {M}*
```

---

## Triggers

```
/research {주제}
/research {주제} --deep        # 수렴까지 계속 (checkpoint 있음)
/research {주제} --quick       # 3 iteration 후 정리
```

---

## Reality Gates (from v1.5)

수렴 판단 전 필수 체크:

```yaml
reality_gates:
  - gate: "경쟁사 Gate"
    question: "이거 이미 시장에 있지 않나?"

  - gate: "사용자 Gate"
    question: "실제로 돈 내는 사람 있나?"

  - gate: "Why Not Gate"
    question: "이게 좋은 거면 왜 대기업이 안 했나?"
```

---

## 🐻 Bear Case Analysis (v2.2 통합)

**목적**: 최악의 시나리오 필수 분석. 낙관적 편향 방지.

```yaml
bear_case:
  position: "SYNTHESIZE 직전"
  mandatory: true
  minimum_scenarios: 3

  questions:
    - "이 결론이 틀릴 이유 3가지는?"
    - "경쟁자가 내일 똑같은 걸 하면?"
    - "6개월 후에도 이 가정이 유효할까?"
    - "이 방향을 선택했는데 실패하면 매몰 비용은?"
    - "다른 사람도 이 결론에 도달했다면 왜 실행 안 했을까?"

  severity_levels:
    CRITICAL: "결론 자체 무효 → 재탐색 필요"
    HIGH: "심각한 리스크 → 대응 전략 필수"
    MEDIUM: "주의 필요 → 모니터링"
    LOW: "관리 가능 → 일반 대응"

  # 🚨 CRITICAL: 수렴 전 반드시 실행
  enforcement:
    - "CRITICAL 시나리오 있으면 수렴 불가"
    - "최소 3개 시나리오 분석 필수"
    - "각 시나리오에 대응 전략 있어야 함"

  output_format: |
    ## 🐻 Bear Case 분석

    | 시나리오 | 확률 | 심각도 | 대응 전략 |
    |---------|------|--------|----------|
    | [시나리오 1] | H/M/L | [레벨] | [전략] |
    | [시나리오 2] | H/M/L | [레벨] | [전략] |
    | [시나리오 3] | H/M/L | [레벨] | [전략] |

    **CRITICAL 존재**: [Yes/No]
    **Bear Case 결론**: [수렴 가능 / 재탐색 / 보류]
```

---

## Chaos Engine Integration

```yaml
chaos_integration:
  when: "CONVERGE에서 막다른 길 도달 시"

  trigger:
    - "모든 경로가 PRUNE됨"
    - "기존 발견으로는 본질에 못 감"

  action: "Chaos Engine 발동 → 새 관점 → 새 PROBE"
```

---

## Quality Constraints

| 제약 | 설명 |
|------|------|
| **No Premature Structure** | 처음부터 구조 짜지 말고 발견을 따라가기 |
| **Follow the Scent** | "냄새나는" 방향 추적 |
| **Kill Your Darlings** | 아까워도 막다른 길은 버리기 |
| **Connect, Don't Collect** | 수집이 아닌 연결 |
| **Converge to Essence** | 정보가 아닌 본질에 수렴 |

---

## Works Well With

**Skills**:
- **jarvis-chaos-engine** - 막다른 길에서 새 관점
- **moai-foundation-core** - 실행 프레임워크

**Tools**:
- **mcp__sequential-thinking** - 추론 과정 기록
- **WebSearch / WebFetch** - 탐색 도구

---

**Version**: 2.3.0
**Last Updated**: 2025-12-31
**Status**: ✅ Active

**Changelog**:
- v2.3.0: 경쟁사 검색 선행 필수 (2025-12-31)
  - 🚨 **4번째 CRITICAL 규칙 추가**: `4_competition_search_first`
  - 🔍 **PROBE 단계 강화**: 경쟁사 검색 최소 5회 필수
  - ❌ **"블루오션" 단정 금지**: 검색 없이 "경쟁사 없음" 결론 금지
  - 🏢 **한국 시장 검색 필수**: 글로벌만 보고 한국 시장 생략 방지
  - 📋 **User Gate 개선**: "아세요?" 대신 검색 결과 기반 경쟁사 리스트 제시
  - 📊 **경쟁사 분석 테이블 필수**: PROBE 출력에 경쟁사 매트릭스 추가
  - ⚠️ **교훈**: "강의안 생성기 블루오션 오판" 사례에서 학습
- v2.2.0: Bear Case 통합 (jarvis-iterative-research 폐기)
  - 🐻 **Bear Case Analysis**: 최악의 시나리오 필수 분석
  - 🚨 **CRITICAL 시나리오**: 수렴 전 반드시 체크
  - 📋 **severity_levels**: CRITICAL/HIGH/MEDIUM/LOW 분류
  - ⚠️ **jarvis-iterative-research v1.0.0 폐기** (이 스킬로 통합)
- v2.1.0: 동적 판단 + 완급 조절
  - 🚨 **하드코딩 제거**: 숫자 기반 → 질문 기반 판단
  - 🎚️ **완급 조절 체계**: 🚨CRITICAL / ⚠️IMPORTANT / 💡GUIDE 구분
  - 🔬 **HYPOTHESIS 단계**: 발견 → 검증 가능한 가설로 전환
  - ⚖️ **VERIFY/REFUTE 단계**: 🚨 반박 증거 검색 강제 (확증 편향 방지)
  - 📚 **Source Hierarchy**: 1차 소스 우선 (Tier 분류)
  - 👤 **Context Integration**: 🚨 일반론 금지, 사용자 맞춤 강제
  - 🔄 **동적 수렴 판단**: iteration 횟수가 아닌 "새 통찰 고갈 + 반박 시도 + 맞춤 결론"
  - 📊 **Depth Check**: 점수가 아닌 질적 체크리스트
- v2.0.0: 완전 재설계 - Recursive Exploration Loop
  - 🔄 **패러다임 전환**: 고정 Phase → 재귀적 탐구 루프
  - 🕵️ **탐정의 추적**: 발견을 따라가며 궤도 수정
  - 🔗 **연결 중심**: 정보량이 아닌 연결성으로 깊이
  - 🎯 **수렴 지향**: 본질에 도달할 때까지 반복
  - ✂️ **가지치기**: 막다른 길 과감히 버리기
  - 📍 **체크포인트**: 3/6회 반복 후 사용자 확인
- v1.5.0: Reality Gates + Critical Reflection
- v1.4.0: Chain of Thought 강화
- v1.3.0: Agentic 워크플로우 도입
