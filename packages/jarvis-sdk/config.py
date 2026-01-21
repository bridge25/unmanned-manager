"""
JARVIS SDK Configuration
"""

import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class JarvisConfig:
    """JARVIS SDK 설정"""

    # API 설정
    api_base_url: str = field(
        default_factory=lambda: os.environ.get(
            "JARVIS_API_URL",
            "https://mindcollab-web-production.up.railway.app/api"
        )
    )
    api_key: Optional[str] = field(
        default_factory=lambda: os.environ.get("JARVIS_API_KEY")
    )

    # 타임아웃
    timeout_seconds: int = 30

    # 재시도 설정
    max_retries: int = 3
    retry_backoff_base: float = 1.0  # 1초, 2초, 4초

    # Outbox 설정
    outbox_path: Path = field(
        default_factory=lambda: Path(
            os.environ.get("JARVIS_OUTBOX_PATH", ".jarvis/outbox")
        )
    )

    # 로그 설정
    log_path: Path = field(
        default_factory=lambda: Path(
            os.environ.get("JARVIS_LOG_PATH", ".jarvis/logs")
        )
    )

    # Payload 제한
    payload_max_size_kb: int = 10

    # 스키마 버전
    schema_version: str = "1.0"

    def __post_init__(self):
        """설정 후처리"""
        # 경로를 Path 객체로 변환
        if isinstance(self.outbox_path, str):
            self.outbox_path = Path(self.outbox_path)
        if isinstance(self.log_path, str):
            self.log_path = Path(self.log_path)

    def validate(self) -> bool:
        """설정 유효성 검사"""
        if not self.api_key:
            raise ValueError("JARVIS_API_KEY environment variable is required")
        return True


# 전역 기본 설정
_default_config: Optional[JarvisConfig] = None


def get_config() -> JarvisConfig:
    """전역 설정 가져오기"""
    global _default_config
    if _default_config is None:
        _default_config = JarvisConfig()
    return _default_config


def set_config(config: JarvisConfig) -> None:
    """전역 설정 변경"""
    global _default_config
    _default_config = config
