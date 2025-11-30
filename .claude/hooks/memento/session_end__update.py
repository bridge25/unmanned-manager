#!/usr/bin/env python3
"""
Memento v2 - UPDATE 단계: 세션 종료 시 검증 및 저장

트리거: SessionEnd
역할:
1. 세션 중 감지 vs 기록 비교 → 누락 목록 생성
2. 누락 있으면 다음 세션용 리마인드 저장
3. 의사결정 케이스 저장
4. 세션 요약 생성
"""
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# lib 경로 추가
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

try:
    from lib.case_bank import CaseBank
    from lib.state import StateManager
    from lib.profile import get_profile_hash
except ImportError:
    CaseBank = None
    StateManager = None
    get_profile_hash = None


def get_file_changes(project_dir: Path) -> dict:
    """Git으로 세션 중 변경된 파일 확인"""
    changes = {
        "profile_changed": False,
        "cases_changed": False,
        "projects_changed": False,
    }

    try:
        result = subprocess.run(
            ["git", "diff", "--name-only"],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=3
        )
        if result.returncode == 0:
            changed_files = result.stdout.strip().split('\n')
            for f in changed_files:
                if 'profile.md' in f:
                    changes["profile_changed"] = True
                if 'cases.md' in f:
                    changes["cases_changed"] = True
                if 'projects.md' in f:
                    changes["projects_changed"] = True
    except Exception:
        pass

    return changes


def find_missed_detections(project_dir: Path) -> list[dict]:
    """
    감지됐으나 기록되지 않은 항목 찾기
    - 강한 신호 중 profile.md/cases.md에 반영 안 된 것
    """
    if not StateManager:
        return []

    try:
        state_manager = StateManager(project_dir)
        state = state_manager.load()

        if not state or not hasattr(state, 'detections'):
            return []

        # 파일 변경 확인
        changes = get_file_changes(project_dir)

        missed = []
        for detection_batch in state.detections:
            for detail in detection_batch.get('details', []):
                # 강한 신호만 체크
                if detail.get('strength') != 'strong':
                    continue

                det_type = detail.get('type', '')

                # 타입별 파일 변경 확인
                should_record = False
                if det_type in ['fact', 'preference', 'pattern']:
                    should_record = not changes["profile_changed"]
                elif det_type == 'history':
                    should_record = not changes["cases_changed"]
                elif det_type in ['context', 'state']:
                    should_record = not changes["projects_changed"]

                if should_record:
                    missed.append(detail)

        return missed

    except Exception:
        return []


def save_missed_for_next_session(project_dir: Path, missed: list[dict]):
    """누락 감지 항목을 다음 세션용으로 저장"""
    if not missed:
        return

    missed_file = project_dir / ".claude" / "memento" / ".missed_detections.json"

    try:
        missed_file.parent.mkdir(parents=True, exist_ok=True)
        with open(missed_file, "w", encoding="utf-8") as f:
            json.dump({
                "missed": missed,
                "saved_at": datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


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

    try:
        content = cases_file.read_text(encoding="utf-8")

        # Template 섹션 전에 추가
        if "## Template" in content:
            content = content.replace("## Template", new_case + "\n## Template")
        else:
            content += new_case

        cases_file.write_text(content, encoding="utf-8")
    except Exception:
        pass


def main():
    try:
        project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")).resolve()

        output_parts = []

        # 세션 상태 로드
        state = None
        if StateManager:
            state_manager = StateManager(project_dir)
            state = state_manager.load()

        # 1. 감지 vs 기록 비교
        missed = find_missed_detections(project_dir)

        if missed:
            # 다음 세션용으로 저장
            save_missed_for_next_session(project_dir, missed)
            output_parts.append(f"⚠️ 감지됐으나 미기록: {len(missed)}건 (다음 세션에서 리마인드)")

        # 2. 의사결정 케이스 저장 (기존 기능 유지)
        if state and hasattr(state, 'decisions_made') and state.decisions_made:
            decisions = state.decisions_made

            if CaseBank:
                case_bank = CaseBank(project_dir)
                cases_file = case_bank.cases_file

                if cases_file.exists():
                    for decision in decisions:
                        case_id = case_bank.get_next_id()
                        append_case_to_file(cases_file, case_id, decision)

                    output_parts.append(f"✅ {len(decisions)}개 케이스 저장됨")

        # 3. 세션 요약
        if state:
            tool_count = len(state.tool_executions) if hasattr(state, 'tool_executions') else 0
            detection_count = len(state.detections) if hasattr(state, 'detections') else 0

            output_parts.append(f"""[Memento v2 - 세션 종료]
- 세션 ID: {state.session_id}
- 도구 실행: {tool_count}회
- 감지 이벤트: {detection_count}회
- 미기록 항목: {len(missed)}건""")

        # 4. 세션 상태 정리
        if StateManager and state:
            state_manager.cleanup()

        # 최종 출력
        if output_parts:
            output = {
                "message": "\n".join(output_parts)
            }
        else:
            output = {"message": "세션 종료"}

        print(json.dumps(output, ensure_ascii=False))
        sys.exit(0)

    except Exception as e:
        # 에러 발생해도 조용히 종료
        print(json.dumps({"message": f"세션 종료 (오류: {str(e)[:30]})"}))
        sys.exit(0)


if __name__ == "__main__":
    main()
