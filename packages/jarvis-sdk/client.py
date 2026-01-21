"""
JARVIS API Client
"""

import json
import time
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
import urllib.request
import urllib.error

try:
    from .config import JarvisConfig, get_config
except ImportError:
    from config import JarvisConfig, get_config


@dataclass
class JarvisEvent:
    """JARVIS 이벤트 데이터"""
    event_type: str
    task_id: str
    idempotency_key: str
    worker_id: str
    payload: Dict[str, Any]
    node_id: Optional[str] = None
    project_id: Optional[str] = None
    session_id: Optional[str] = None
    summary: Optional[str] = None
    sdk_version: str = "1.0.0"
    trace_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리 변환 (None 값 제외)"""
        data = asdict(self)
        return {k: v for k, v in data.items() if v is not None}


class JarvisClient:
    """MindCollab API 클라이언트"""

    def __init__(self, config: Optional[JarvisConfig] = None, strict: bool = False):
        """
        Args:
            config: JarvisConfig 인스턴스
            strict: True면 4xx 에러에서 예외 발생, False(기본)면 outbox 저장 후 계속
        """
        self.config = config or get_config()
        self.strict = strict
        self._ensure_directories()

    def _ensure_directories(self):
        """필요한 디렉토리 생성"""
        self.config.outbox_path.mkdir(parents=True, exist_ok=True)
        (self.config.outbox_path / "pending").mkdir(exist_ok=True)
        (self.config.outbox_path / "failed").mkdir(exist_ok=True)
        self.config.log_path.mkdir(parents=True, exist_ok=True)

    def generate_idempotency_key(
        self,
        worker_id: str,
        task_id: str,
        event_type: str,
        sequence: Optional[int] = None
    ) -> str:
        """Idempotency Key 생성"""
        timestamp = int(time.time())
        if sequence is not None:
            return f"{worker_id}:{task_id}:{event_type}:{timestamp}:{sequence}"
        return f"{worker_id}:{task_id}:{event_type}:{timestamp}"

    def send_event(self, event: JarvisEvent) -> Dict[str, Any]:
        """
        이벤트 전송 (재시도 + Outbox fallback)

        Returns:
            {"status": "created", "event_id": "..."} 또는
            {"status": "duplicate", "event_id": "..."} 또는
            {"status": "outboxed", "path": "..."} (실패 시)
        """
        last_error = None

        # 재시도 루프
        for attempt in range(self.config.max_retries):
            try:
                result = self._send_request(event)
                self._log_event(event, "sent", result)
                return result

            except urllib.error.HTTPError as e:
                if e.code < 500:
                    # 4xx 에러는 재시도 안함
                    error_body = e.read().decode('utf-8', errors='replace')
                    self._log_event(event, "client_error", {"code": e.code, "body": error_body})
                    if self.strict:
                        # strict 모드: 예외 발생
                        raise JarvisAPIError(f"API error {e.code}: {error_body}")
                    else:
                        # fail-open 모드 (기본): outbox 저장 후 계속
                        outbox_path = self._save_to_outbox(event, f"HTTP {e.code}: {error_body}")
                        self._log_event(event, "outboxed_4xx", {"code": e.code, "path": str(outbox_path)})
                        return {"status": "outboxed", "path": str(outbox_path), "error_code": e.code}
                last_error = e

            except Exception as e:
                last_error = e

            # 백오프
            if attempt < self.config.max_retries - 1:
                backoff = self.config.retry_backoff_base * (2 ** attempt)
                time.sleep(backoff)

        # 모든 재시도 실패 → Outbox 저장
        outbox_path = self._save_to_outbox(event, str(last_error))
        self._log_event(event, "outboxed", {"error": str(last_error), "path": str(outbox_path)})

        return {"status": "outboxed", "path": str(outbox_path)}

    def _send_request(self, event: JarvisEvent) -> Dict[str, Any]:
        """HTTP 요청 전송"""
        url = f"{self.config.api_base_url}/jarvis/events"
        data = json.dumps(event.to_dict()).encode('utf-8')

        headers = {
            "Content-Type": "application/json",
            "X-Jarvis-API-Key": self.config.api_key or "",
        }

        request = urllib.request.Request(url, data=data, headers=headers, method="POST")

        with urllib.request.urlopen(request, timeout=self.config.timeout_seconds) as response:
            return json.loads(response.read().decode('utf-8'))

    def _save_to_outbox(self, event: JarvisEvent, error: str) -> Path:
        """Outbox에 이벤트 저장"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"{timestamp}_{event.idempotency_key.replace(':', '_')}.json"
        filepath = self.config.outbox_path / "pending" / filename

        outbox_data = {
            "event": event.to_dict(),
            "error": error,
            "created_at": datetime.now().isoformat(),
            "_retry_count": 0
        }

        filepath.write_text(json.dumps(outbox_data, ensure_ascii=False, indent=2))
        return filepath

    def _log_event(self, event: JarvisEvent, action: str, details: Dict[str, Any]):
        """이벤트 로깅"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "event_type": event.event_type,
            "task_id": event.task_id,
            "idempotency_key": event.idempotency_key,
            "details": details
        }

        log_file = self.config.log_path / f"jarvis_sdk_{datetime.now().strftime('%Y%m%d')}.jsonl"
        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    def retry_outbox(self) -> Dict[str, int]:
        """Outbox에 있는 이벤트 재전송"""
        pending_dir = self.config.outbox_path / "pending"
        failed_dir = self.config.outbox_path / "failed"

        stats = {"success": 0, "failed": 0, "skipped": 0}

        for filepath in pending_dir.glob("*.json"):
            try:
                data = json.loads(filepath.read_text())
                retry_count = data.get("_retry_count", 0)

                if retry_count >= self.config.max_retries:
                    # 최대 재시도 초과 → failed로 이동
                    failed_path = failed_dir / filepath.name
                    filepath.rename(failed_path)
                    stats["skipped"] += 1
                    continue

                event = JarvisEvent(**data["event"])
                result = self._send_request(event)

                if result.get("status") in ("created", "duplicate"):
                    filepath.unlink()  # 성공 시 삭제
                    stats["success"] += 1
                else:
                    raise Exception(f"Unexpected response: {result}")

            except Exception as e:
                # 재시도 카운트 증가
                data["_retry_count"] = data.get("_retry_count", 0) + 1
                data["last_error"] = str(e)
                data["last_retry"] = datetime.now().isoformat()
                filepath.write_text(json.dumps(data, ensure_ascii=False, indent=2))
                stats["failed"] += 1

        return stats


class JarvisAPIError(Exception):
    """JARVIS API 오류"""
    pass
