"""
Session State - 세션 상태 관리
"""
import json
import uuid
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class SessionState:
    """세션 상태"""
    session_id: str = ""
    started_at: str = ""
    cases_loaded: bool = False
    active_projects: int = 0
    pending_todos: int = 0
    decisions_made: list = field(default_factory=list)
    tool_executions: list = field(default_factory=list)

    def __post_init__(self):
        if not self.session_id:
            self.session_id = str(uuid.uuid4())[:8]
        if not self.started_at:
            self.started_at = datetime.now().isoformat()


class StateManager:
    """세션 상태 관리자"""

    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.state_dir = project_dir / ".claude" / "memento"
        self.state_file = self.state_dir / ".session_state.json"

    def init(self) -> SessionState:
        """새 세션 상태 초기화"""
        self.state_dir.mkdir(parents=True, exist_ok=True)

        state = SessionState()
        self.save(state)
        return state

    def load(self) -> Optional[SessionState]:
        """세션 상태 로드"""
        if not self.state_file.exists():
            return None

        try:
            data = json.loads(self.state_file.read_text(encoding="utf-8"))
            return SessionState(**data)
        except Exception:
            return None

    def save(self, state: SessionState):
        """세션 상태 저장"""
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(
            json.dumps(asdict(state), indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

    def add_decision(self, state: SessionState, decision: dict):
        """의사결정 추가"""
        decision["timestamp"] = datetime.now().isoformat()
        state.decisions_made.append(decision)
        self.save(state)

    def add_tool_execution(self, state: SessionState, tool_name: str, result_summary: str):
        """도구 실행 기록 추가"""
        state.tool_executions.append({
            "tool": tool_name,
            "timestamp": datetime.now().isoformat(),
            "result_summary": result_summary[:200]  # 요약만
        })
        self.save(state)

    def cleanup(self):
        """세션 상태 파일 정리"""
        if self.state_file.exists():
            self.state_file.unlink()
