"""
JARVIS Task - Context Manager for IPC Events
"""

import os
import traceback
from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass

try:
    from .client import JarvisClient, JarvisEvent
    from .config import JarvisConfig, get_config
except ImportError:
    from client import JarvisClient, JarvisEvent
    from config import JarvisConfig, get_config


@dataclass
class TaskResult:
    """태스크 결과"""
    status: str  # 'success', 'partial', 'failed'
    summary: str
    data: Optional[Dict[str, Any]] = None
    artifacts: Optional[list] = None


class JarvisTask:
    """
    JARVIS 태스크 - Context Manager 지원

    Usage:
        # 방법 1: Context Manager (권장)
        with JarvisTask("my_task", node_id="N148", worker_id="haedong") as task:
            task.start("작업 시작")
            task.log("진행 중...", level="info")
            task.complete({"result": "ok"}, summary="완료")

        # 방법 2: 직접 호출
        task = JarvisTask("my_task", node_id="N148", worker_id="haedong")
        task.start("작업 시작")
        task.complete({"result": "ok"})
    """

    def __init__(
        self,
        task_id: str,
        node_id: Optional[str] = None,
        worker_id: Optional[str] = None,
        project_id: Optional[str] = None,
        session_id: Optional[str] = None,
        config: Optional[JarvisConfig] = None,
        strict: bool = False
    ):
        """
        Args:
            task_id: 작업 ID
            node_id: MindCollab 노드 ID (선택)
            worker_id: Worker 식별자 (기본: 환경변수 또는 'unknown')
            project_id: 프로젝트 ID (선택)
            session_id: tmux 세션 ID (기본: TMUX_PANE 환경변수)
            config: JarvisConfig (선택)
            strict: True면 API 오류 시 예외, False(기본)면 fail-open
        """
        self.task_id = task_id
        self.node_id = node_id
        self.worker_id = worker_id or os.environ.get("JARVIS_WORKER_ID", "unknown")
        self.project_id = project_id
        self.session_id = session_id or os.environ.get("TMUX_PANE", None)
        self.strict = strict

        self.config = config or get_config()
        self.client = JarvisClient(self.config, strict=strict)

        self._started = False
        self._completed = False
        self._log_sequence = 0
        self._start_time: Optional[datetime] = None

    def __enter__(self) -> "JarvisTask":
        """Context manager 진입"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """
        Context manager 종료
        - 예외 발생 시: blocked() 자동 호출 (실패해도 원래 예외 전파)
        - 정상 종료 + complete 미호출 시: 경고 로그
        """
        if exc_type is not None:
            # 예외 발생 → blocked (fail-safe: blocked() 실패해도 원래 예외 전파)
            try:
                error_details = "".join(traceback.format_exception(exc_type, exc_val, exc_tb))
                self.blocked(
                    reason=str(exc_val),
                    blocker_type="error",
                    error_details=error_details
                )
            except Exception:
                # blocked() 실패해도 무시하고 원래 예외 전파
                pass
            return False  # 예외 전파

        if self._started and not self._completed:
            # 시작했지만 완료 안함 → 경고 (실패해도 무시)
            try:
                self.log(
                    "Task exited without calling complete() or blocked()",
                    level="warning"
                )
            except Exception:
                pass

        return False

    def start(self, description: str) -> Dict[str, Any]:
        """
        태스크 시작 이벤트 전송

        Args:
            description: 작업 설명
        """
        if self._started:
            self.log("start() called multiple times", level="warning")
            return {"status": "skipped", "reason": "already_started"}

        self._started = True
        self._start_time = datetime.now()

        event = JarvisEvent(
            event_type="task_started",
            task_id=self.task_id,
            idempotency_key=self.client.generate_idempotency_key(
                self.worker_id, self.task_id, "task_started"
            ),
            worker_id=self.worker_id,
            node_id=self.node_id,
            project_id=self.project_id,
            session_id=self.session_id,
            payload={
                "description": description,
                "started_at": self._start_time.isoformat()
            },
            summary=f"시작: {description}"
        )

        return self.client.send_event(event)

    def complete(
        self,
        result: Dict[str, Any],
        summary: Optional[str] = None,
        status: str = "success"
    ) -> Dict[str, Any]:
        """
        태스크 완료 이벤트 전송

        Args:
            result: 결과 데이터
            summary: 알림용 요약 (선택)
            status: 'success', 'partial', 'failed'
        """
        if self._completed:
            self.log("complete() called multiple times", level="warning")
            return {"status": "skipped", "reason": "already_completed"}

        self._completed = True
        completed_at = datetime.now()

        duration_seconds = None
        if self._start_time:
            duration_seconds = (completed_at - self._start_time).total_seconds()

        event = JarvisEvent(
            event_type="task_completed",
            task_id=self.task_id,
            idempotency_key=self.client.generate_idempotency_key(
                self.worker_id, self.task_id, "task_completed"
            ),
            worker_id=self.worker_id,
            node_id=self.node_id,
            project_id=self.project_id,
            session_id=self.session_id,
            payload={
                "result": {
                    "status": status,
                    "data": result
                },
                "duration_seconds": duration_seconds,
                "completed_at": completed_at.isoformat()
            },
            summary=summary or f"완료 ({status})"
        )

        return self.client.send_event(event)

    def blocked(
        self,
        reason: str,
        blocker_type: str = "error",
        error_details: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        태스크 블로커 이벤트 전송

        Args:
            reason: 블로커 사유
            blocker_type: 'error', 'dependency', 'input_needed', 'external'
            error_details: 상세 에러 정보
        """
        if self._completed:
            self.log("blocked() called after complete()", level="warning")
            return {"status": "skipped", "reason": "already_completed"}

        self._completed = True  # blocked도 종료 상태
        blocked_at = datetime.now()

        event = JarvisEvent(
            event_type="task_blocked",
            task_id=self.task_id,
            idempotency_key=self.client.generate_idempotency_key(
                self.worker_id, self.task_id, "task_blocked"
            ),
            worker_id=self.worker_id,
            node_id=self.node_id,
            project_id=self.project_id,
            session_id=self.session_id,
            payload={
                "reason": reason,
                "blocker_type": blocker_type,
                "error_details": error_details,
                "blocked_at": blocked_at.isoformat()
            },
            summary=f"블로커: {reason}"
        )

        return self.client.send_event(event)

    def log(
        self,
        message: str,
        level: str = "info",
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        로그 이벤트 전송

        Args:
            message: 로그 메시지
            level: 'info', 'warning', 'error', 'debug'
            context: 추가 컨텍스트
        """
        self._log_sequence += 1

        event = JarvisEvent(
            event_type="task_log",
            task_id=self.task_id,
            idempotency_key=self.client.generate_idempotency_key(
                self.worker_id, self.task_id, "task_log", self._log_sequence
            ),
            worker_id=self.worker_id,
            node_id=self.node_id,
            project_id=self.project_id,
            session_id=self.session_id,
            payload={
                "level": level,
                "message": message,
                "context": context or {}
            },
            summary=None  # 로그는 알림 안함
        )

        return self.client.send_event(event)
