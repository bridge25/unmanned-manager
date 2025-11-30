#!/usr/bin/env python3
"""
RETRIEVE 단계: 사용자 입력과 유사한 과거 케이스 검색

트리거: UserPromptSubmit
역할: 의사결정 필요 시 유사 케이스 자동 검색 + 컨텍스트 주입
"""
import json
import os
import sys
from pathlib import Path

# lib 경로 추가
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from lib.case_bank import CaseBank

# 의사결정 관련 키워드
DECISION_KEYWORDS = [
    "우선순위", "먼저", "선택", "뭐 해", "어떻게", "결정",
    "vs", "아니면", "할까", "어느", "무엇을", "방향",
    "전략", "계획", "순서", "중요", "급한"
]


def extract_keywords(text: str) -> list[str]:
    """텍스트에서 검색용 키워드 추출"""
    keywords = []
    text_lower = text.lower()

    # 프로젝트명 추출
    project_names = ["japan", "해동", "dt-rag", "scraper", "premium", "트레이더", "saas"]
    for name in project_names:
        if name.lower() in text_lower:
            keywords.append(name)

    # 주제 키워드
    topic_keywords = ["수익", "긴급", "데드라인", "외주", "런칭", "전략", "우선순위", "먼저"]
    for kw in topic_keywords:
        if kw in text:
            keywords.append(kw)

    # 의사결정 관련 태그
    tag_keywords = ["긴급도", "수익판단", "리스크", "장기전략"]
    for kw in tag_keywords:
        if kw in text:
            keywords.append(kw)

    # 키워드 없으면 일반 단어라도 추가
    if not keywords:
        # 간단한 토큰화
        tokens = text.replace("?", " ").replace("!", " ").split()
        keywords = [t for t in tokens if len(t) > 1][:5]

    return keywords


def main():
    # stdin에서 Hook 입력 받기
    try:
        hook_input = json.load(sys.stdin)
    except Exception:
        # 입력 없으면 그냥 통과
        print(json.dumps({"continue": True}))
        sys.exit(0)

    user_prompt = hook_input.get("prompt", "")

    # 1. 의사결정 필요 여부 판단
    needs_decision = any(kw in user_prompt for kw in DECISION_KEYWORDS)

    if not needs_decision:
        # 의사결정 불필요 → 그냥 통과
        print(json.dumps({"continue": True}))
        sys.exit(0)

    # 2. Case Bank에서 유사 케이스 검색
    project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")).resolve()
    case_bank = CaseBank(project_dir)

    if not case_bank.exists():
        print(json.dumps({
            "continue": True,
            "context": "[Memento RETRIEVE] Case Bank 없음 - 새로운 의사결정"
        }))
        sys.exit(0)

    # 키워드 추출 및 검색
    keywords = extract_keywords(user_prompt)
    relevant_cases = case_bank.search_by_keywords(keywords, top_k=3)

    # 3. 컨텍스트에 추가
    if relevant_cases:
        context = case_bank.format_for_context(relevant_cases)
        output = {
            "continue": True,
            "context": f"""[Memento RETRIEVE - 유사 케이스 {len(relevant_cases)}개 발견]

{context}
위 케이스들을 참고하여 판단하세요."""
        }
    else:
        output = {
            "continue": True,
            "context": "[Memento RETRIEVE] 유사 케이스 없음 - 새로운 상황"
        }

    print(json.dumps(output, ensure_ascii=False))
    sys.exit(0)


if __name__ == "__main__":
    main()
