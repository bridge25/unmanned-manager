#!/usr/bin/env python3
"""
Memento v2 - OBSERVE 단계: 세션 시작 시 상태 로드

트리거: SessionStart
역할:
1. Profile 요약 로드 → 컨텍스트 주입
2. 이전 세션 누락 기록 확인 → 리마인드
3. Case Bank 상태 확인
4. 세션 상태 초기화
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
    from lib.profile import parse_profile, format_profile_context
    from lib.state import StateManager
    from lib.case_bank import CaseBank
except ImportError:
    # Import 실패해도 계속 진행
    parse_profile = None
    format_profile_context = None
    StateManager = None
    CaseBank = None


def count_projects(project_dir: Path) -> int:
    """활성 프로젝트 수 카운트"""
    projects_file = project_dir / "current" / "projects.md"
    if not projects_file.exists():
        return 0

    try:
        content = projects_file.read_text(encoding="utf-8")
        import re
        return len(re.findall(r"^## \d+\.", content, re.MULTILINE))
    except Exception:
        return 0


def count_todos(project_dir: Path) -> int:
    """대기 중인 할일 수 카운트"""
    todo_file = project_dir / "current" / "todo.md"
    if not todo_file.exists():
        return 0

    try:
        content = todo_file.read_text(encoding="utf-8")
        import re
        return len(re.findall(r"^- \[ \]", content, re.MULTILINE))
    except Exception:
        return 0


def load_missed_detections(project_dir: Path) -> list[dict]:
    """이전 세션에서 누락된 감지 항목 로드"""
    missed_file = project_dir / ".claude" / "memento" / ".missed_detections.json"
    if not missed_file.exists():
        return []

    try:
        with open(missed_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("missed", [])
    except Exception:
        return []


def clear_missed_detections(project_dir: Path):
    """누락 감지 파일 초기화"""
    missed_file = project_dir / ".claude" / "memento" / ".missed_detections.json"
    try:
        if missed_file.exists():
            missed_file.unlink()
    except Exception:
        pass


def main():
    try:
        project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")).resolve()

        context_parts = []

        # 1. Profile 요약 로드
        if parse_profile and format_profile_context:
            profile_path = project_dir / "current" / "profile.md"
            profile_summary = parse_profile(profile_path)
            if profile_summary:
                context_parts.append(format_profile_context(profile_summary))

        # 2. 이전 세션 누락 기록 확인
        missed = load_missed_detections(project_dir)
        if missed:
            missed_text = "\n".join([f"  - {m.get('type', '?')}: \"{m.get('matched', '?')}\"" for m in missed[:5]])
            context_parts.append(f"""[Memento - 이전 세션 누락 기록 ⚠️]

지난 세션에서 감지됐으나 기록되지 않은 항목:
{missed_text}

지금 기록하거나, 불필요하면 무시해도 됩니다.""")
            # 확인했으니 클리어
            clear_missed_detections(project_dir)

        # 3. Case Bank 확인
        if CaseBank:
            case_bank = CaseBank(project_dir)
            cases_exist = case_bank.exists()
            case_count = len(case_bank.load_cases()) if cases_exist else 0
        else:
            cases_exist = False
            case_count = 0

        # 4. 프로젝트/할일 현황
        project_count = count_projects(project_dir)
        todo_count = count_todos(project_dir)

        # 5. 세션 상태 초기화
        if StateManager:
            state_manager = StateManager(project_dir)
            state = state_manager.init()
            state.cases_loaded = cases_exist
            state.active_projects = project_count
            state.pending_todos = todo_count
            state_manager.save(state)
            session_id = state.session_id
        else:
            session_id = "unknown"

        # 6. 기본 상태 정보 추가
        context_parts.append(f"""[Memento v2 - 세션 시작]
- Case Bank: {'✅ ' + str(case_count) + '개 케이스' if cases_exist else '❌ 없음'}
- 활성 프로젝트: {project_count}개
- 대기 할일: {todo_count}개
- 세션 ID: {session_id}""")

        # 최종 출력
        output = {
            "continue": True,
            "context": "\n\n---\n\n".join(context_parts)
        }

        print(json.dumps(output, ensure_ascii=False))
        sys.exit(0)

    except Exception as e:
        # 에러 발생해도 대화는 계속
        print(json.dumps({
            "continue": True,
            "context": f"[Memento] 세션 초기화 중 오류: {str(e)[:50]}"
        }))
        sys.exit(0)


if __name__ == "__main__":
    main()
