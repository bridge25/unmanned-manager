#!/usr/bin/env python3
"""
JARVIS Orchestrator IPC Handler
===============================
Claude Code 측에서 Orchestrator의 태스크를 수신하고 결과를 반환

Hook 타입: UserPromptSubmit
역할:
1. .jarvis/tasks/ 에서 새 태스크 감지
2. 태스크가 있으면 context에 주입
3. (Result Writer에서) 실행 결과를 .jarvis/results/에 저장

작성일: 2025-12-16
"""
import json
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Any, Union, Dict
from dataclasses import dataclass, field

# =============================================================================
# IPC 데이터 구조 (jarvis/orchestrator/ipc.py와 동일)
# =============================================================================

@dataclass
class TaskMessage:
    """태스크 메시지 (PM → Agent)"""
    task_id: str
    instruction: str
    project: str
    timeout: int = 300
    priority: str = "normal"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> str:
        return json.dumps(
            {
                "task_id": self.task_id,
                "instruction": self.instruction,
                "project": self.project,
                "timeout": self.timeout,
                "priority": self.priority,
                "created_at": self.created_at,
                "metadata": self.metadata,
            },
            ensure_ascii=False,
            indent=2,
        )

    @classmethod
    def from_json(cls, data: Union[str, dict]) -> "TaskMessage":
        if isinstance(data, str):
            data = json.loads(data)
        return cls(
            task_id=data["task_id"],
            instruction=data["instruction"],
            project=data["project"],
            timeout=data.get("timeout", 300),
            priority=data.get("priority", "normal"),
            created_at=data.get("created_at", datetime.now().isoformat()),
            metadata=data.get("metadata", {}),
        )


@dataclass
class ResultMessage:
    """결과 메시지 (Agent → PM)"""
    task_id: str
    status: str  # "completed" | "failed" | "timeout" | "cancelled"
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    completed_at: str = field(default_factory=lambda: datetime.now().isoformat())
    duration_seconds: float = 0.0

    def to_json(self) -> str:
        return json.dumps(
            {
                "task_id": self.task_id,
                "status": self.status,
                "result": self.result,
                "error": self.error,
                "completed_at": self.completed_at,
                "duration_seconds": self.duration_seconds,
            },
            ensure_ascii=False,
            indent=2,
        )


# =============================================================================
# IPC Handler
# =============================================================================

class OrchestratorIPC:
    """Orchestrator IPC 핸들러"""

    def __init__(self, base_dir: str = ".jarvis"):
        # 프로젝트 루트 기준
        self.project_root = Path(os.environ.get("CLAUDE_PROJECT_DIR", "."))
        self.base_dir = self.project_root / base_dir
        self.tasks_dir = self.base_dir / "tasks"
        self.results_dir = self.base_dir / "results"
        self.state_file = self.base_dir / ".current_task.json"

    def ensure_dirs(self) -> None:
        """디렉토리 생성"""
        self.tasks_dir.mkdir(parents=True, exist_ok=True)
        self.results_dir.mkdir(parents=True, exist_ok=True)

    def poll_task(self) -> Optional[TaskMessage]:
        """새 태스크 확인 (가장 오래된 것 우선)"""
        if not self.tasks_dir.exists():
            return None

        task_files = sorted(self.tasks_dir.glob("task_*.json"))

        for task_file in task_files:
            try:
                data = task_file.read_text(encoding="utf-8")
                task = TaskMessage.from_json(data)
                return task
            except (json.JSONDecodeError, KeyError):
                continue

        return None

    def claim_task(self, task_id: str) -> bool:
        """태스크 수신 확인 (파일 삭제)"""
        task_file = self.tasks_dir / f"task_{task_id}.json"
        if task_file.exists():
            task_file.unlink()
            return True
        return False

    def save_current_task(self, task: TaskMessage) -> None:
        """현재 처리 중인 태스크 저장"""
        self.ensure_dirs()
        state = {
            "task_id": task.task_id,
            "instruction": task.instruction,
            "project": task.project,
            "started_at": datetime.now().isoformat(),
            "timeout": task.timeout,
            "metadata": task.metadata,
        }
        self.state_file.write_text(json.dumps(state, ensure_ascii=False, indent=2))

    def get_current_task(self) -> Optional[dict]:
        """현재 처리 중인 태스크 조회"""
        if not self.state_file.exists():
            return None
        try:
            return json.loads(self.state_file.read_text())
        except (json.JSONDecodeError, FileNotFoundError):
            return None

    def clear_current_task(self) -> None:
        """현재 태스크 완료 처리"""
        if self.state_file.exists():
            self.state_file.unlink()

    def publish_result(
        self,
        task_id: str,
        status: str,
        result: dict = None,
        error: str = None,
        duration_seconds: float = 0.0,
    ) -> Path:
        """결과 발행"""
        self.ensure_dirs()

        result_msg = ResultMessage(
            task_id=task_id,
            status=status,
            result=result,
            error=error,
            duration_seconds=duration_seconds,
        )

        result_file = self.results_dir / f"result_{task_id}.json"

        # Atomic write
        import tempfile
        fd, tmp_path = tempfile.mkstemp(dir=self.results_dir, suffix=".tmp")
        try:
            os.write(fd, result_msg.to_json().encode("utf-8"))
            os.close(fd)
            os.rename(tmp_path, result_file)
        except Exception:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            raise

        return result_file


# =============================================================================
# Context Formatter
# =============================================================================

def format_task_context(task: TaskMessage) -> str:
    """태스크를 Claude context로 포맷"""
    lines = [
        "[JARVIS Orchestrator Task]",
        "",
        f"🎯 **Task ID**: {task.task_id}",
        f"📁 **Project**: {task.project}",
        f"⏱️ **Timeout**: {task.timeout}초",
        f"🔴 **Priority**: {task.priority}",
        "",
        "📋 **Instruction**:",
        f"```",
        task.instruction,
        f"```",
        "",
        "⚠️ 이 태스크는 JARVIS Orchestrator에서 자동 할당되었습니다.",
        "완료 후 `/jarvis:complete` 또는 실패 시 `/jarvis:fail` 명령을 사용하세요.",
    ]

    if task.metadata:
        lines.append("")
        lines.append("📎 **Metadata**:")
        for key, value in task.metadata.items():
            lines.append(f"  - {key}: {value}")

    return "\n".join(lines)


# =============================================================================
# Hook Main
# =============================================================================

def main():
    """UserPromptSubmit Hook - 새 태스크 감지 및 context 주입"""

    ipc = OrchestratorIPC()

    # 1. 현재 처리 중인 태스크가 있는지 확인
    current_task = ipc.get_current_task()
    if current_task:
        # 이미 처리 중인 태스크가 있으면 리마인더만
        print(f"[JARVIS] 진행 중인 태스크: {current_task['task_id']}")
        sys.exit(0)

    # 2. 새 태스크 확인
    task = ipc.poll_task()

    if not task:
        # 새 태스크 없음
        sys.exit(0)

    # 3. 태스크 수신 및 상태 저장
    ipc.claim_task(task.task_id)
    ipc.save_current_task(task)

    # 4. Context 출력 (Claude에게 주입)
    context = format_task_context(task)
    print(context)

    sys.exit(0)


if __name__ == "__main__":
    main()
