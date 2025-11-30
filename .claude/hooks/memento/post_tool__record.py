#!/usr/bin/env python3
"""
RECORD 단계: 도구 실행 결과 기록

트리거: PostToolUse
역할: 의사결정 관련 도구 실행 시 결과 임시 기록
"""
import json
import os
import sys
from pathlib import Path

# lib 경로 추가
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from lib.state import StateManager

# 기록할 도구들 (의사결정 관련)
TRACKED_TOOLS = ["Edit", "Write", "MultiEdit", "Bash"]


def main():
    # stdin에서 Hook 입력 받기
    try:
        hook_input = json.load(sys.stdin)
    except Exception:
        print(json.dumps({"continue": True}))
        sys.exit(0)

    tool_name = hook_input.get("tool_name", "")

    # 추적 대상 도구만 기록
    if tool_name not in TRACKED_TOOLS:
        print(json.dumps({"continue": True}))
        sys.exit(0)

    # 세션 상태에 기록
    project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")).resolve()
    state_manager = StateManager(project_dir)
    state = state_manager.load()

    if state:
        # 결과 요약 (너무 길면 자름)
        result = hook_input.get("result", "")
        result_summary = result[:200] if isinstance(result, str) else str(result)[:200]

        state_manager.add_tool_execution(state, tool_name, result_summary)

    print(json.dumps({"continue": True}))
    sys.exit(0)


if __name__ == "__main__":
    main()
