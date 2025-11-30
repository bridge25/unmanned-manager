#!/usr/bin/env python3
"""
UPDATE 단계: 세션 종료 시 Case Bank 업데이트

트리거: SessionEnd
역할: 세션 중 기록된 의사결정들을 Case Bank에 영구 저장
"""
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# lib 경로 추가
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from lib.case_bank import CaseBank
from lib.state import StateManager


def append_case_to_file(cases_file: Path, case_id: str, decision: dict):
    """케이스를 파일에 추가"""
    new_case = f"""
---

## {case_id}: {decision.get('title', '의사결정')}

| 항목 | 내용 |
|------|------|
| **날짜** | {datetime.now().strftime('%Y-%m-%d')} |
| **상황** | {decision.get('situation', '')} |
| **선택지** | {decision.get('options', '')} |
| **판단** | {decision.get('decision', '')} |
| **근거** | {decision.get('rationale', '')} |
| **결과** | {decision.get('result', '⏳ 대기')} |
| **학습** | {decision.get('learning', '')} |
| **태그** | {decision.get('tags', '')} |
"""

    # 기존 내용 읽기
    content = cases_file.read_text(encoding="utf-8")

    # Template 섹션 전에 추가
    if "## Template" in content:
        content = content.replace("## Template", new_case + "\n## Template")
    else:
        content += new_case

    cases_file.write_text(content, encoding="utf-8")

    # Index도 업데이트
    update_index(cases_file, case_id, decision)


def update_index(cases_file: Path, case_id: str, decision: dict):
    """Index 테이블 업데이트"""
    content = cases_file.read_text(encoding="utf-8")

    # Index 테이블 찾기
    index_line = f"| {case_id} | {datetime.now().strftime('%Y-%m-%d')} | {decision.get('title', '')[:20]} | ⏳ | {decision.get('tags', '')} |"

    # "---" 구분선 전에 추가
    lines = content.split("\n")
    new_lines = []
    index_section = False

    for line in lines:
        if "## Index" in line:
            index_section = True
        if index_section and line.startswith("---"):
            new_lines.append(index_line)
            index_section = False
        new_lines.append(line)

    cases_file.write_text("\n".join(new_lines), encoding="utf-8")


def main():
    project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")).resolve()

    # 세션 상태 로드
    state_manager = StateManager(project_dir)
    state = state_manager.load()

    if not state:
        print(json.dumps({"message": "세션 상태 없음"}))
        sys.exit(0)

    # 이번 세션에서 기록된 의사결정들
    decisions = state.decisions_made

    if not decisions:
        # 의사결정 없으면 세션 요약만
        output = {
            "message": f"세션 {state.session_id} 종료",
            "tool_executions": len(state.tool_executions),
            "decisions_made": 0
        }
        print(json.dumps(output, ensure_ascii=False))
        state_manager.cleanup()
        sys.exit(0)

    # Case Bank에 추가
    case_bank = CaseBank(project_dir)
    cases_file = case_bank.cases_file

    if cases_file.exists():
        for decision in decisions:
            case_id = case_bank.get_next_id()
            append_case_to_file(cases_file, case_id, decision)

    # 세션 상태 정리
    state_manager.cleanup()

    output = {
        "message": f"✅ {len(decisions)}개 케이스 저장됨",
        "session_id": state.session_id,
        "total_tool_executions": len(state.tool_executions)
    }

    print(json.dumps(output, ensure_ascii=False))
    sys.exit(0)


if __name__ == "__main__":
    main()
