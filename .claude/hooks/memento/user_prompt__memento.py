#!/usr/bin/env python3
"""
Memento v2 - DETECT 단계: 사용자 입력에서 6가지 유형 감지

트리거: UserPromptSubmit
역할:
1. 6가지 유형 다층 감지 (Fact, Preference, Pattern, History, Context, State)
2. 감지 결과 세션 상태에 저장
3. AI에게 힌트 컨텍스트 주입
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# lib 경로 추가
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

try:
    from lib.detection import detect_all, format_detection_hint, get_detection_summary
    from lib.state import StateManager
    from lib.case_bank import CaseBank
except ImportError as e:
    detect_all = None
    format_detection_hint = None
    get_detection_summary = None
    StateManager = None
    CaseBank = None


# 의사결정 관련 키워드 (기존 retrieve 기능 유지)
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

    return keywords


def save_detections_to_session(project_dir: Path, detections_summary: dict):
    """감지 결과를 세션 상태에 저장"""
    if not StateManager:
        return

    try:
        state_manager = StateManager(project_dir)
        state = state_manager.load()
        if state:
            # detections 필드가 없으면 생성
            if not hasattr(state, 'detections'):
                state.detections = []

            # 타임스탬프와 함께 추가
            detections_summary['timestamp'] = datetime.now().isoformat()
            state.detections.append(detections_summary)
            state_manager.save(state)
    except Exception:
        pass


def main():
    try:
        # stdin에서 Hook 입력 받기
        try:
            hook_input = json.load(sys.stdin)
        except Exception:
            print(json.dumps({"continue": True}))
            sys.exit(0)

        user_prompt = hook_input.get("prompt", "")

        if not user_prompt.strip():
            print(json.dumps({"continue": True}))
            sys.exit(0)

        project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")).resolve()
        context_parts = []

        # 1. 6가지 유형 감지
        if detect_all and format_detection_hint:
            detections = detect_all(user_prompt)

            if detections:
                # 힌트 생성
                hint = format_detection_hint(detections)
                context_parts.append(hint)

                # 세션 상태에 저장
                if get_detection_summary:
                    summary = get_detection_summary(detections)
                    save_detections_to_session(project_dir, summary)

        # 2. 의사결정 키워드 감지 (기존 retrieve 기능)
        needs_decision = any(kw in user_prompt for kw in DECISION_KEYWORDS)

        if needs_decision and CaseBank:
            case_bank = CaseBank(project_dir)

            if case_bank.exists():
                keywords = extract_keywords(user_prompt)
                relevant_cases = case_bank.search_by_keywords(keywords, top_k=3)

                if relevant_cases:
                    context = case_bank.format_for_context(relevant_cases)
                    context_parts.append(f"""[Memento - 유사 케이스 {len(relevant_cases)}개]

{context}

위 케이스를 참고하여 판단하세요.""")

        # 최종 출력
        if context_parts:
            output = {
                "continue": True,
                "context": "\n\n---\n\n".join(context_parts)
            }
        else:
            output = {"continue": True}

        print(json.dumps(output, ensure_ascii=False))
        sys.exit(0)

    except Exception as e:
        # 에러 발생해도 대화는 계속
        print(json.dumps({"continue": True}))
        sys.exit(0)


if __name__ == "__main__":
    main()
