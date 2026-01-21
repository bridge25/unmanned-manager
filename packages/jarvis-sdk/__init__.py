"""
JARVIS SDK - IPC v2.0
=====================

Worker용 Python SDK로 MindCollab을 통한 이벤트 기반 IPC를 제공합니다.

Usage:
    from jarvis_sdk import JarvisTask

    with JarvisTask(
        task_id="my_task",
        node_id="N148",
        worker_id="haedong"
    ) as task:
        task.start("작업 시작")
        # ... 작업 수행 ...
        task.complete({"result": "success"}, summary="완료")

    # 예외 발생 시 자동으로 task.blocked() 호출
"""

from .task import JarvisTask
from .client import JarvisClient
from .config import JarvisConfig

__version__ = "1.0.0"
__all__ = ["JarvisTask", "JarvisClient", "JarvisConfig"]
