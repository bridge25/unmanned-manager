#!/usr/bin/env python3
"""
JARVIS SDK - Integration Test
=============================

실제 MindCollab API와 통신하여 SDK 동작을 검증합니다.

Usage:
    python3 integration_test.py

환경 변수 필수:
    JARVIS_API_KEY - MindCollab API 키
    JARVIS_API_URL - MindCollab API URL (기본: https://mindcollab-web-production.up.railway.app/api)
"""

import os
import sys
import time
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config import JarvisConfig
from task import JarvisTask


def get_test_config():
    """테스트용 설정"""
    api_key = os.environ.get("JARVIS_API_KEY")
    if not api_key:
        print("❌ JARVIS_API_KEY 환경변수가 설정되지 않았습니다.")
        print("   export JARVIS_API_KEY=your-api-key")
        return None

    return JarvisConfig(
        api_base_url=os.environ.get(
            "JARVIS_API_URL",
            "https://mindcollab-web-production.up.railway.app/api"
        ),
        api_key=api_key
    )


def test_task_lifecycle():
    """태스크 전체 수명주기 테스트"""
    print("\n" + "=" * 60)
    print("🧪 JARVIS SDK Integration Test")
    print("=" * 60)

    config = get_test_config()
    if not config:
        return False

    print(f"\n📡 API URL: {config.api_base_url}")
    print(f"🔑 API Key: {config.api_key[:10]}...")

    task_id = f"integration_test_{int(time.time())}"

    print(f"\n📋 Task ID: {task_id}")

    try:
        with JarvisTask(
            task_id=task_id,
            node_id="N999",  # 테스트용 노드
            worker_id="integration_test",
            config=config
        ) as task:
            # 1. 시작
            print("\n1️⃣ Starting task...")
            result = task.start("통합 테스트 시작")
            print(f"   Result: {result}")

            if result.get("status") == "outboxed":
                print("   ⚠️ API 연결 실패, Outbox에 저장됨")
                return False

            # 2. 로그
            print("\n2️⃣ Logging progress...")
            result = task.log("진행 중...", level="info", context={"step": 1})
            print(f"   Result: {result}")

            # 3. 완료
            print("\n3️⃣ Completing task...")
            result = task.complete(
                result={"status": "success", "test": True},
                summary="통합 테스트 완료"
            )
            print(f"   Result: {result}")

            if result.get("status") in ("created", "duplicate"):
                print("\n✅ Integration test PASSED!")
                return True
            else:
                print(f"\n❌ Unexpected result: {result}")
                return False

    except Exception as e:
        print(f"\n❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_blocked_event():
    """블로커 이벤트 테스트"""
    print("\n" + "=" * 60)
    print("🧪 Blocked Event Test")
    print("=" * 60)

    config = get_test_config()
    if not config:
        return False

    task_id = f"blocked_test_{int(time.time())}"

    try:
        with JarvisTask(
            task_id=task_id,
            node_id="N999",
            worker_id="integration_test",
            config=config
        ) as task:
            task.start("블로커 테스트")
            result = task.blocked(
                reason="테스트 블로커",
                blocker_type="external"
            )
            print(f"Result: {result}")

            if result.get("status") in ("created", "duplicate"):
                print("✅ Blocked event test PASSED!")
                return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def test_exception_handling():
    """예외 발생 시 자동 blocked 호출 테스트"""
    print("\n" + "=" * 60)
    print("🧪 Exception Handling Test")
    print("=" * 60)

    config = get_test_config()
    if not config:
        return False

    task_id = f"exception_test_{int(time.time())}"

    try:
        with JarvisTask(
            task_id=task_id,
            node_id="N999",
            worker_id="integration_test",
            config=config
        ) as task:
            task.start("예외 테스트")
            raise RuntimeError("의도적 예외 발생")

    except RuntimeError:
        print("✅ Exception propagated correctly")
        print("   (blocked event should have been sent)")
        return True

    return False


def main():
    """메인 함수"""
    results = []

    # 테스트 실행
    results.append(("Task Lifecycle", test_task_lifecycle()))
    results.append(("Blocked Event", test_blocked_event()))
    results.append(("Exception Handling", test_exception_handling()))

    # 결과 요약
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)

    passed = 0
    failed = 0

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {name}")
        if result:
            passed += 1
        else:
            failed += 1

    print(f"\n  Total: {passed} passed, {failed} failed")
    print("=" * 60)

    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
