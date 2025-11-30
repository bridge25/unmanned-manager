#!/usr/bin/env python3
"""
OBSERVE 단계: 세션 시작 시 Memento 상태 로드

트리거: SessionStart
역할: Case Bank 존재 확인 + 세션 상태 초기화 + 컨텍스트 주입
"""
import json
import os
import sys
from pathlib import Path

# lib 경로 추가
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from lib.case_bank import CaseBank
from lib.state import StateManager


def count_projects(project_dir: Path) -> int:
    """활성 프로젝트 수 카운트"""
    projects_file = project_dir / "current" / "projects.md"
    if not projects_file.exists():
        return 0

    content = projects_file.read_text(encoding="utf-8")
    # ## 숫자. 로 시작하는 프로젝트 헤더 카운트
    import re
    return len(re.findall(r"^## \d+\.", content, re.MULTILINE))


def count_todos(project_dir: Path) -> int:
    """대기 중인 할일 수 카운트"""
    todo_file = project_dir / "current" / "todo.md"
    if not todo_file.exists():
        return 0

    content = todo_file.read_text(encoding="utf-8")
    # - [ ] 로 시작하는 미완료 항목 카운트
    import re
    return len(re.findall(r"^- \[ \]", content, re.MULTILINE))


def main():
    project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")).resolve()

    # 1. Case Bank 확인
    case_bank = CaseBank(project_dir)
    cases_exist = case_bank.exists()
    case_count = len(case_bank.load_cases()) if cases_exist else 0

    # 2. 프로젝트/할일 현황
    project_count = count_projects(project_dir)
    todo_count = count_todos(project_dir)

    # 3. 세션 상태 초기화
    state_manager = StateManager(project_dir)
    state = state_manager.init()
    state.cases_loaded = cases_exist
    state.active_projects = project_count
    state.pending_todos = todo_count
    state_manager.save(state)

    # 4. 컨텍스트 출력
    output = {
        "context": f"""[Memento OBSERVE]
- Case Bank: {'✅ ' + str(case_count) + '개 케이스' if cases_exist else '❌ 없음'}
- 활성 프로젝트: {project_count}개
- 대기 할일: {todo_count}개
- 세션 ID: {state.session_id}

의사결정 시 유사 케이스를 참조하세요."""
    }

    print(json.dumps(output, ensure_ascii=False))
    sys.exit(0)


if __name__ == "__main__":
    main()
