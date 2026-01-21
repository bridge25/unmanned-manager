"""
JARVIS SDK - Test Script
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# SDK 테스트 전 환경 설정
os.environ.setdefault("JARVIS_API_KEY", "test-key")
os.environ.setdefault("JARVIS_API_URL", "http://localhost:3000/api")

# Import without relative imports for standalone testing
from config import JarvisConfig, get_config  # noqa: E402
from client import JarvisClient, JarvisEvent  # noqa: E402
from task import JarvisTask  # noqa: E402


def test_config():
    """설정 테스트"""
    print("=" * 50)
    print("1. Config Test")
    print("=" * 50)

    config = get_config()
    print(f"  API URL: {config.api_base_url}")
    print(f"  Timeout: {config.timeout_seconds}s")
    print(f"  Max Retries: {config.max_retries}")
    print(f"  Outbox Path: {config.outbox_path}")
    print("  ✅ Config loaded successfully")
    return True


def test_event_creation():
    """이벤트 생성 테스트"""
    print("\n" + "=" * 50)
    print("2. Event Creation Test")
    print("=" * 50)

    event = JarvisEvent(
        event_type="task_completed",
        task_id="test_task_001",
        idempotency_key="test:test_task_001:completed:1234567890",
        worker_id="test_worker",
        payload={"result": {"status": "success", "data": "test"}},
        node_id="N999",
        summary="테스트 완료"
    )

    event_dict = event.to_dict()
    print(f"  Event Type: {event_dict['event_type']}")
    print(f"  Task ID: {event_dict['task_id']}")
    print(f"  Idempotency Key: {event_dict['idempotency_key']}")
    print(f"  Worker ID: {event_dict['worker_id']}")
    print(f"  Summary: {event_dict['summary']}")
    print("  ✅ Event created successfully")
    return True


def test_idempotency_key():
    """Idempotency Key 생성 테스트"""
    print("\n" + "=" * 50)
    print("3. Idempotency Key Test")
    print("=" * 50)

    config = JarvisConfig()
    client = JarvisClient(config)

    key1 = client.generate_idempotency_key("haedong", "task_001", "task_completed")
    key2 = client.generate_idempotency_key("haedong", "task_001", "task_log", 1)
    key3 = client.generate_idempotency_key("haedong", "task_001", "task_log", 2)

    print(f"  Key 1: {key1}")
    print(f"  Key 2: {key2}")
    print(f"  Key 3: {key3}")

    # 포맷 검증
    assert "haedong" in key1
    assert "task_001" in key1
    assert "task_completed" in key1

    print("  ✅ Idempotency keys generated correctly")
    return True


def test_task_context_manager():
    """Task Context Manager 테스트 (API 없이)"""
    print("\n" + "=" * 50)
    print("4. Task Context Manager Test (Dry Run)")
    print("=" * 50)

    # 실제 API 호출 없이 객체 생성만 테스트
    task = JarvisTask(
        task_id="test_task_002",
        node_id="N100",
        worker_id="test_worker"
    )

    print(f"  Task ID: {task.task_id}")
    print(f"  Node ID: {task.node_id}")
    print(f"  Worker ID: {task.worker_id}")
    print(f"  Started: {task._started}")
    print(f"  Completed: {task._completed}")

    print("  ✅ JarvisTask object created successfully")
    return True


def test_outbox_directory():
    """Outbox 디렉토리 생성 테스트"""
    print("\n" + "=" * 50)
    print("5. Outbox Directory Test")
    print("=" * 50)

    config = JarvisConfig()
    client = JarvisClient(config)

    assert config.outbox_path.exists(), "Outbox path should be created"
    assert (config.outbox_path / "pending").exists(), "Pending dir should exist"
    assert (config.outbox_path / "failed").exists(), "Failed dir should exist"
    assert config.log_path.exists(), "Log path should be created"

    print(f"  Outbox: {config.outbox_path}")
    print(f"  Pending: {config.outbox_path / 'pending'}")
    print(f"  Failed: {config.outbox_path / 'failed'}")
    print(f"  Logs: {config.log_path}")
    print("  ✅ All directories created successfully")
    return True


def run_all_tests():
    """모든 테스트 실행"""
    print("\n🚀 JARVIS SDK Test Suite")
    print("=" * 50)

    tests = [
        ("Config", test_config),
        ("Event Creation", test_event_creation),
        ("Idempotency Key", test_idempotency_key),
        ("Task Context Manager", test_task_context_manager),
        ("Outbox Directory", test_outbox_directory),
    ]

    passed = 0
    failed = 0

    for name, test_fn in tests:
        try:
            if test_fn():
                passed += 1
        except Exception as e:
            print(f"\n  ❌ {name} FAILED: {e}")
            failed += 1

    print("\n" + "=" * 50)
    print(f"📊 Results: {passed} passed, {failed} failed")
    print("=" * 50)

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
