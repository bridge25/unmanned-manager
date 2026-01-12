#!/usr/bin/env python3
"""
JARVIS tmux Orchestrator - 멀티 프로젝트 터미널 오케스트레이션
================================================================
tmux 세션을 통해 여러 프로젝트 터미널에 명령을 주입하고 결과를 수집
파일 IPC를 통해 구조화된 결과 수신

작성일: 2025-12-25
업데이트: 2025-12-25 (파일 IPC 통합)
방식: tmux send-keys + JSON 파일 IPC
"""
import json
import subprocess
import time
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
from datetime import datetime

# 파일 IPC 임포트
try:
    from .task_ipc import TaskDispatcher, Task, TaskResult
    IPC_AVAILABLE = True
except ImportError:
    try:
        from task_ipc import TaskDispatcher, Task, TaskResult
        IPC_AVAILABLE = True
    except ImportError:
        IPC_AVAILABLE = False
        TaskDispatcher = None

# PM Cycle Recorder 임포트
try:
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "jarvis" / "pipelines"))
    from pm_cycle_recorder import get_recorder, ExecutionStatus
    CYCLE_RECORDER_AVAILABLE = True
except ImportError:
    CYCLE_RECORDER_AVAILABLE = False
    get_recorder = None
    ExecutionStatus = None

# 프로젝트 베이스 경로
PROJECTS_BASE = Path("/Volumes/d/users/tony/Desktop/projects")

# 프로젝트 매핑 (별칭 → 실제 폴더명, tmux 세션명)
PROJECT_CONFIG = {
    # 해동기획
    "해동검도": {"folder": "order-automation-saas", "session": "haedong"},
    "해동기획": {"folder": "order-automation-saas", "session": "haedong"},
    "해동": {"folder": "order-automation-saas", "session": "haedong"},
    "haedong": {"folder": "order-automation-saas", "session": "haedong"},

    # Japan Sale
    "japan": {"folder": "japan", "session": "japan"},
    "일본": {"folder": "japan", "session": "japan"},
    "japansale": {"folder": "japan", "session": "japan"},

    # FlyMoney
    "flymoney": {"folder": "flymoney", "session": "flymoney"},
    "fly": {"folder": "flymoney", "session": "flymoney"},

    # DT-RAG
    "dt-rag": {"folder": "dt-rag", "session": "dtrag"},
    "rag": {"folder": "dt-rag", "session": "dtrag"},
    "dtrag": {"folder": "dt-rag", "session": "dtrag"},

    # 크립토멘토
    "크립토멘토": {"folder": "premium-contents-scrraper", "session": "crypto"},
    "멘토": {"folder": "premium-contents-scrraper", "session": "crypto"},
    "크립토": {"folder": "premium-contents-scrraper", "session": "crypto"},
    "crypto": {"folder": "premium-contents-scrraper", "session": "crypto"},

    # 프레젠토
    "프레젠토": {"folder": "daddy's-ppt", "session": "prezento"},
    "prezento": {"folder": "daddy's-ppt", "session": "prezento"},

    # 사주
    "사주": {"folder": "saju", "session": "saju"},
    "saju": {"folder": "saju", "session": "saju"},

    # QR 주차
    "qr주차": {"folder": "qr-parking-demo", "session": "qrparking"},
    "주차": {"folder": "qr-parking-demo", "session": "qrparking"},
    "qrparking": {"folder": "qr-parking-demo", "session": "qrparking"},
    "parking": {"folder": "qr-parking-demo", "session": "qrparking"},

    # Japan Auto (이미지 검색 자동화)
    "japan-auto": {"folder": "japan-auto", "session": "japanauto"},
    "japanauto": {"folder": "japan-auto", "session": "japanauto"},
    "자동화": {"folder": "japan-auto", "session": "japanauto"},

    # MindCollab (마인드맵 협업 도구)
    "mindcollab": {"folder": "mindcollab", "session": "mindcollab"},
    "mind": {"folder": "mindcollab", "session": "mindcollab"},
    "콜라보": {"folder": "mindcollab", "session": "mindcollab"},

    # Weekly Planner (PM)
    "weekly": {"folder": "weekly planner", "session": "jarvis-pm"},
    "planner": {"folder": "weekly planner", "session": "jarvis-pm"},
    "jarvis": {"folder": "weekly planner", "session": "jarvis-pm"},
}

# ANSI 이스케이프 코드 제거 패턴
ANSI_ESCAPE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')


@dataclass
class TmuxSession:
    """tmux 세션 정보"""
    name: str
    project_path: Path
    exists: bool = False
    has_claude: bool = False


@dataclass
class CommandResult:
    """명령 실행 결과"""
    success: bool
    session: str
    command: str
    output: str
    duration: float
    error: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class TmuxOrchestrator:
    """tmux 기반 멀티 프로젝트 오케스트레이터"""

    # 대화형 프롬프트 패턴 (PM 자동 응답용)
    INTERACTIVE_PATTERNS = {
        # 권한 요청 (Yes 선택)
        "permission_yes": {
            "patterns": [
                r"Do you want to proceed\?",
                r"Permission rule .* requires confirmation",
                r"❯\s*1\.\s*Yes",
                r"1\.\s*Yes\s*\n\s*2\.",
            ],
            "response": "1",
            "description": "권한 승인 요청"
        },
        # 객관식 선택 (첫 번째 = 권장 옵션)
        "select_first": {
            "patterns": [
                r"❯\s*1\.\s*.+\(Recommended\)",
                r"❯\s*1\.\s*.+\(권장\)",
            ],
            "response": "1",
            "description": "권장 옵션 선택"
        },
        # .gitignore 추가 선택
        "gitignore_add": {
            "patterns": [
                r"1\.\s*\.gitignore에 추가",
                r"\.gitignore에 추가 \(권장\)",
            ],
            "response": "1",
            "description": ".gitignore 추가"
        },
        # 계속 진행
        "continue": {
            "patterns": [
                r"Enter to select",
                r"Press Enter to continue",
                r"계속하려면 Enter",
            ],
            "response": "",  # 빈 문자열 = Enter만
            "description": "계속 진행"
        },
    }

    # LLM 라우팅 키워드 → 강제 명령어
    LLM_ROUTING = {
        "codex": {
            "keywords": ["codex", "/codex", "코덱스"],
            "enforce_cmd": "codex --full-auto",
            "warning": "⚠️ 중요: 직접 분석하지 말고 반드시 `codex --full-auto` CLI를 실행해서 위임할 것. 네가 직접 하면 안 됨."
        },
        "gemini": {
            "keywords": ["gemini", "/gemini", "제미나이"],
            "enforce_cmd": "gemini",
            "warning": "⚠️ 중요: 직접 검색하지 말고 반드시 `gemini` CLI를 실행해서 위임할 것."
        }
    }

    def __init__(self):
        self.sessions: dict[str, TmuxSession] = {}
        self._refresh_sessions()

    def _run_tmux(self, args: list[str], timeout: int = 10) -> tuple[bool, str]:
        """tmux 명령 실행"""
        try:
            result = subprocess.run(
                ["tmux"] + args,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return result.returncode == 0, result.stdout.strip()
        except subprocess.TimeoutExpired:
            return False, "Timeout"
        except FileNotFoundError:
            return False, "tmux not installed"
        except Exception as e:
            return False, str(e)

    def _refresh_sessions(self):
        """현재 tmux 세션 목록 갱신"""
        success, output = self._run_tmux(["list-sessions", "-F", "#{session_name}"])

        if success and output:
            existing = set(output.split("\n"))
        else:
            existing = set()

        # 프로젝트별 세션 상태 확인
        seen_sessions = set()
        for alias, config in PROJECT_CONFIG.items():
            session_name = config["session"]
            if session_name in seen_sessions:
                continue
            seen_sessions.add(session_name)

            folder = config["folder"]
            project_path = PROJECTS_BASE / folder

            self.sessions[session_name] = TmuxSession(
                name=session_name,
                project_path=project_path,
                exists=session_name in existing
            )

    def list_sessions(self) -> dict[str, dict]:
        """현재 세션 상태 반환"""
        self._refresh_sessions()
        return {
            name: {
                "exists": s.exists,
                "project_path": str(s.project_path),
                "path_exists": s.project_path.exists()
            }
            for name, s in self.sessions.items()
        }

    def _detect_interactive_prompt(self, session_name: str) -> Optional[tuple[str, str, str]]:
        """
        세션에서 대화형 프롬프트 감지

        Returns:
            (pattern_name, response, description) or None
        """
        output = self.capture_output(session_name, lines=50)
        if not output:
            return None

        for pattern_name, config in self.INTERACTIVE_PATTERNS.items():
            for pattern in config["patterns"]:
                if re.search(pattern, output, re.MULTILINE | re.IGNORECASE):
                    return (
                        pattern_name,
                        config["response"],
                        config["description"]
                    )

        return None

    def _send_interactive_response(
        self,
        session_name: str,
        response: str,
        description: str
    ) -> bool:
        """
        대화형 프롬프트에 응답 전송

        Args:
            session_name: tmux 세션명
            response: 전송할 응답 (빈 문자열 = Enter만)
            description: 로깅용 설명

        Returns:
            성공 여부
        """
        print(f"[PM] Auto-respond: {description} → '{response or 'Enter'}'")

        if response:
            # 응답 텍스트 전송
            success, _ = self._run_tmux([
                "send-keys", "-t", session_name, response
            ])
            if not success:
                return False
            time.sleep(0.2)

        # Enter 전송 (Claude Code는 Enter 2번 필요 - 별도 호출)
        success, _ = self._run_tmux([
            "send-keys", "-t", session_name, "Enter"
        ])
        if success:
            time.sleep(0.1)
            self._run_tmux(["send-keys", "-t", session_name, "Enter"])

        return success

    def _check_and_respond_to_prompt(self, session_name: str) -> bool:
        """
        대화형 프롬프트 확인 및 자동 응답

        Returns:
            프롬프트가 있어서 응답했으면 True
        """
        detected = self._detect_interactive_prompt(session_name)
        if not detected:
            return False

        pattern_name, response, description = detected
        return self._send_interactive_response(session_name, response, description)

    def create_session(self, project: str) -> tuple[bool, str]:
        """프로젝트용 tmux 세션 생성"""
        config = self._get_project_config(project)
        if not config:
            return False, f"Unknown project: {project}"

        session_name = config["session"]
        project_path = PROJECTS_BASE / config["folder"]

        if not project_path.exists():
            return False, f"Project path not found: {project_path}"

        # 이미 존재하는지 확인
        self._refresh_sessions()
        if session_name in self.sessions and self.sessions[session_name].exists:
            return True, f"Session already exists: {session_name}"

        # 세션 생성
        success, msg = self._run_tmux([
            "new-session", "-d",
            "-s", session_name,
            "-c", str(project_path)
        ])

        if success:
            self._refresh_sessions()
            return True, f"Created session: {session_name}"
        else:
            return False, f"Failed to create session: {msg}"

    def create_all_sessions(self) -> dict[str, str]:
        """모든 프로젝트 세션 생성"""
        results = {}
        seen = set()

        for alias, config in PROJECT_CONFIG.items():
            session_name = config["session"]
            if session_name in seen:
                continue
            seen.add(session_name)

            success, msg = self.create_session(alias)
            results[session_name] = msg

        return results

    def kill_session(self, project: str) -> tuple[bool, str]:
        """세션 종료"""
        config = self._get_project_config(project)
        if not config:
            return False, f"Unknown project: {project}"

        session_name = config["session"]
        success, msg = self._run_tmux(["kill-session", "-t", session_name])

        if success:
            self._refresh_sessions()
            return True, f"Killed session: {session_name}"
        else:
            return False, f"Failed to kill session: {msg}"

    def send_command(
        self,
        project: str,
        command: str,
        wait_seconds: float = 2.0,
        capture_lines: int = 100
    ) -> CommandResult:
        """
        프로젝트 세션에 명령 전송 및 결과 캡처

        Args:
            project: 프로젝트명 또는 별칭
            command: 실행할 명령
            wait_seconds: 결과 대기 시간
            capture_lines: 캡처할 출력 줄 수
        """
        start_time = time.time()

        config = self._get_project_config(project)
        if not config:
            return CommandResult(
                success=False,
                session="",
                command=command,
                output="",
                duration=0,
                error=f"Unknown project: {project}"
            )

        session_name = config["session"]

        # 세션 존재 확인
        self._refresh_sessions()
        if session_name not in self.sessions or not self.sessions[session_name].exists:
            return CommandResult(
                success=False,
                session=session_name,
                command=command,
                output="",
                duration=0,
                error=f"Session not found: {session_name}. Run create_session first."
            )

        # 명령 전송 (Claude Code는 Enter 2번 필요 - 별도 호출)
        success, msg = self._run_tmux([
            "send-keys", "-t", session_name, command, "Enter"
        ])
        if success:
            time.sleep(0.1)
            self._run_tmux(["send-keys", "-t", session_name, "Enter"])

        if not success:
            return CommandResult(
                success=False,
                session=session_name,
                command=command,
                output="",
                duration=time.time() - start_time,
                error=f"Failed to send command: {msg}"
            )

        # 결과 대기
        time.sleep(wait_seconds)

        # 출력 캡처
        output = self.capture_output(session_name, capture_lines)

        return CommandResult(
            success=True,
            session=session_name,
            command=command,
            output=output,
            duration=time.time() - start_time
        )

    def capture_output(self, session: str, lines: int = 100) -> str:
        """세션 출력 캡처"""
        success, output = self._run_tmux([
            "capture-pane", "-t", session,
            "-p",  # stdout으로 출력
            "-S", f"-{lines}"  # 최근 N줄
        ])

        if success:
            # ANSI 코드 제거
            clean_output = ANSI_ESCAPE.sub('', output)
            return clean_output.strip()
        return ""

    def send_to_claude(
        self,
        project: str,
        instruction: str,
        wait_seconds: float = 30.0
    ) -> CommandResult:
        """
        프로젝트 세션의 Claude에게 지시 전송

        세션에서 Claude Code가 실행 중이어야 함
        """
        # Claude 프롬프트에 직접 입력
        return self.send_command(
            project=project,
            command=instruction,
            wait_seconds=wait_seconds,
            capture_lines=200
        )

    def _get_project_config(self, project: str) -> Optional[dict]:
        """프로젝트 설정 찾기"""
        normalized = project.lower().strip()
        return PROJECT_CONFIG.get(normalized)

    def get_session_name(self, project: str) -> Optional[str]:
        """프로젝트의 세션명 반환"""
        config = self._get_project_config(project)
        return config["session"] if config else None

    def _detect_llm_routing(self, instruction: str) -> Optional[dict]:
        """지시에서 LLM 라우팅 키워드 감지"""
        instruction_lower = instruction.lower()
        for llm_name, config in self.LLM_ROUTING.items():
            for keyword in config["keywords"]:
                if keyword in instruction_lower:
                    return config
        return None

    def _enforce_llm_routing(self, instruction: str) -> str:
        """LLM 라우팅 키워드 감지 시 강제 명령 추가"""
        routing = self._detect_llm_routing(instruction)
        if routing:
            return f"""{instruction}

{routing["warning"]}
실행할 명령: `{routing["enforce_cmd"]}`
절대 네가 직접 수행하지 말고 위 CLI를 호출해서 결과를 받아와."""
        return instruction

    def start_claude_in_session(
        self,
        project: str,
        skip_permissions: bool = True
    ) -> tuple[bool, str]:
        """
        세션에서 Claude 시작

        Args:
            project: 프로젝트명
            skip_permissions: True면 --dangerously-skip-permissions 플래그 사용

        Returns:
            (success, message)
        """
        config = self._get_project_config(project)
        if not config:
            return False, f"Unknown project: {project}"

        session_name = config["session"]

        # 세션 존재 확인
        self._refresh_sessions()
        if session_name not in self.sessions or not self.sessions[session_name].exists:
            return False, f"Session not found: {session_name}. Run create_session first."

        # Claude 실행 명령 구성
        if skip_permissions:
            claude_cmd = "claude --dangerously-skip-permissions"
        else:
            claude_cmd = "claude"

        # 명령 전송
        success, msg = self._run_tmux([
            "send-keys", "-t", session_name,
            claude_cmd, "Enter"
        ])

        if success:
            time.sleep(2)  # Claude 시작 대기
            return True, f"Started Claude in {session_name} (skip_permissions={skip_permissions})"
        else:
            return False, f"Failed to start Claude: {msg}"

    def start_all_claude_sessions(self, skip_permissions: bool = True) -> dict[str, str]:
        """모든 세션에서 Claude 시작"""
        results = {}
        seen = set()

        for alias, config in PROJECT_CONFIG.items():
            session_name = config["session"]
            if session_name in seen:
                continue
            seen.add(session_name)

            success, msg = self.start_claude_in_session(alias, skip_permissions)
            results[session_name] = msg

        return results

    def dispatch_task(
        self,
        project: str,
        instruction: str,
        timeout: int = 300,
        wait_for_result: bool = True
    ) -> tuple[Optional[str], Optional[str]]:
        """
        tmux로 지시 전송 + 파일 IPC로 결과 수신

        1. 지시에 결과 저장 요청 추가
        2. tmux send-keys로 전송
        3. .jarvis/results/ 폴더 폴링
        4. 결과 파일 읽어서 반환

        Args:
            project: 프로젝트명
            instruction: 지시 내용
            timeout: 타임아웃 (초)
            wait_for_result: True면 결과 대기 후 반환

        Returns:
            (task_id, result_text) 튜플
        """
        import uuid
        from datetime import datetime

        config = self._get_project_config(project)
        if not config:
            print(f"[E] Unknown project: {project}")
            return None, None

        session_name = config["session"]
        project_path = PROJECTS_BASE / config["folder"]
        results_dir = project_path / ".jarvis" / "results"
        results_dir.mkdir(parents=True, exist_ok=True)

        # 세션 존재 확인
        self._refresh_sessions()
        if session_name not in self.sessions or not self.sessions[session_name].exists:
            print(f"[E] Session not found: {session_name}")
            return None, None

        task_id = uuid.uuid4().hex[:8]
        result_file = results_dir / f"result_{task_id}.json"

        # LLM 라우팅 강제 (codex, gemini 등)
        instruction = self._enforce_llm_routing(instruction)

        # 결과 저장 요청을 지시에 추가
        full_instruction = f"""{instruction}

[작업 완료 후 결과를 아래 JSON 형식으로 저장해줘]
⚠️ 중요: result에는 "이번 요청"에 대한 직접적인 답변만 작성 (이전 작업/세션 컨텍스트 X)

파일: {result_file}
```json
{{"task_id": "{task_id}", "status": "completed", "result": "<이번 요청에 대한 직접 답변>", "completed_at": "{datetime.now().isoformat()}"}}
```
예시:
- "git status 확인" → result: "main 브랜치, 3 commits ahead, 2 modified files"
- "테스트 실행" → result: "pytest 완료: 15 passed, 2 failed"
- "빌드해줘" → result: "npm run build 성공, 0 errors\""""

        # 1. 지시 전송
        self._run_tmux([
            "send-keys", "-t", session_name,
            full_instruction
        ])
        time.sleep(0.3)

        # 2. Enter 2번 전송 (Claude Code는 Enter 2번 필요 - 별도 호출)
        self._run_tmux(["send-keys", "-t", session_name, "Enter"])
        time.sleep(0.1)
        self._run_tmux(["send-keys", "-t", session_name, "Enter"])

        print(f"[>] {session_name} (task:{task_id}): {instruction[:40]}...")

        if not wait_for_result:
            return task_id, None

        # 3. 결과 파일 폴링 (대화형 프롬프트 자동 응답 포함)
        start_time = time.time()
        result = self._wait_for_result_file(
            result_file,
            session_name=session_name,
            timeout=timeout
        )
        duration = time.time() - start_time

        # 4. PM Cycle에 실행 기록 (자동)
        self._record_execution_to_ontology(
            project=project,
            instruction=instruction,
            result=result,
            duration_seconds=duration,
            session_name=session_name,
        )

        return task_id, result

    def _record_execution_to_ontology(
        self,
        project: str,
        instruction: str,
        result: Optional[str],
        duration_seconds: float,
        session_name: str,
    ) -> None:
        """PM 실행 결과를 온톨로지에 기록"""
        if not CYCLE_RECORDER_AVAILABLE:
            return

        try:
            recorder = get_recorder()

            # 상태 결정
            if result:
                status = ExecutionStatus.SUCCESS
            else:
                status = ExecutionStatus.TIMEOUT

            # 기록
            recorder.record_execution(
                project=project,
                instruction=instruction,
                result=result or "(no result)",
                status=status,
                duration_seconds=duration_seconds,
                worker_session=session_name,
            )
        except Exception as e:
            # 기록 실패해도 메인 흐름에 영향 없음
            print(f"[PM] Ontology record failed: {e}")

    def _wait_for_result_file(
        self,
        result_file: Path,
        session_name: Optional[str] = None,
        timeout: int = 300,
        poll_interval: float = 3.0,
        prompt_check_interval: int = 15  # 프롬프트 확인 주기 (초)
    ) -> Optional[str]:
        """
        결과 파일 대기 + 대화형 프롬프트 자동 응답

        Args:
            result_file: 결과 파일 경로
            session_name: 대화형 프롬프트 확인용 세션명 (없으면 프롬프트 확인 안함)
            timeout: 전체 타임아웃 (초)
            poll_interval: 결과 파일 폴링 주기 (초)
            prompt_check_interval: 대화형 프롬프트 확인 주기 (초)
        """
        import json
        start_time = time.time()
        last_prompt_check = 0
        auto_respond_count = 0
        max_auto_responds = 5  # 무한 루프 방지

        print(f"[..] Waiting for result file...")

        while time.time() - start_time < timeout:
            # 1. 결과 파일 확인
            if result_file.exists():
                try:
                    data = json.loads(result_file.read_text())
                    print(f"[OK] Result received (status: {data.get('status', 'unknown')})")
                    return data.get("result", str(data))
                except json.JSONDecodeError:
                    # 파일이 아직 쓰는 중일 수 있음
                    time.sleep(1)
                    continue

            # 2. 대화형 프롬프트 확인 (주기적으로)
            elapsed = time.time() - start_time
            if (session_name and
                elapsed - last_prompt_check >= prompt_check_interval and
                auto_respond_count < max_auto_responds):

                last_prompt_check = elapsed

                if self._check_and_respond_to_prompt(session_name):
                    auto_respond_count += 1
                    print(f"[PM] Auto-responded ({auto_respond_count}/{max_auto_responds})")
                    # 응답 후 잠시 대기
                    time.sleep(2)
                    continue

            time.sleep(poll_interval)

        print(f"[!] Timeout after {timeout}s - no result file")
        return None

    def _wait_for_completion(
        self,
        session_name: str,
        timeout: int = 300,
        poll_interval: float = 2.0
    ) -> Optional[str]:
        """
        Claude 작업 완료 대기 및 결과 캡처

        완료 조건: 프롬프트("> ")가 표시되고 토큰 카운터가 안정화
        """
        start_time = time.time()
        last_tokens = 0
        stable_count = 0

        while time.time() - start_time < timeout:
            output = self.capture_output(session_name, lines=100)

            # 토큰 수 추출
            import re
            token_match = re.search(r'(\d+)\s*tokens', output)
            current_tokens = int(token_match.group(1)) if token_match else 0

            # 프롬프트 복귀 확인 ("> " 로 끝나는지)
            lines = output.strip().split('\n')
            last_line = lines[-1] if lines else ""
            has_prompt = "> " in last_line or last_line.strip().startswith(">")

            # 토큰이 증가하지 않고 프롬프트가 있으면 완료
            if has_prompt and current_tokens > 0:
                if current_tokens == last_tokens:
                    stable_count += 1
                    if stable_count >= 2:  # 2회 연속 안정 = 완료
                        print(f"[OK] Complete ({current_tokens} tokens)")
                        return self._extract_result(output)
                else:
                    stable_count = 0

            last_tokens = current_tokens
            time.sleep(poll_interval)

        print(f"[!] Timeout after {timeout}s")
        return self.capture_output(session_name, lines=100)

    def _extract_result(self, output: str) -> str:
        """
        Claude 출력에서 결과 부분 추출

        Claude 출력 마커(⏺, ∴, ✳ 등)와 상태바 사이의 내용 추출
        """
        lines = output.split('\n')
        result_lines = []
        in_result = False

        # Claude 출력 시작 마커들
        start_markers = ['⏺', '∴', '✳', '🤖', '💡', '📋', '✅', '❌']

        for line in lines:
            stripped = line.strip()

            # Claude 출력 시작 감지
            if not in_result:
                if any(stripped.startswith(m) for m in start_markers):
                    in_result = True
                    result_lines.append(line)
                    continue

            # 상태바 감지 (결과 끝) - 마지막 프롬프트 영역
            if in_result:
                # 빈 프롬프트 라인이나 상태바는 제외
                if stripped.startswith("> ") and len(stripped) < 10:
                    continue
                if "tokens" in line and ("Opus" in line or "Sonnet" in line or "Haiku" in line):
                    break
                if "───────" in line:  # 구분선
                    continue

                result_lines.append(line)

        result = '\n'.join(result_lines).strip()

        # 결과가 너무 짧으면 전체 출력 반환
        if len(result) < 50:
            return output

        return result

    def dispatch_task_async(
        self,
        project: str,
        instruction: str
    ) -> Optional[str]:
        """
        비동기 태스크 발송 (지시 직접 전송, 결과 대기 안 함)

        Returns:
            task_id (나중에 wait_task_result로 결과 확인)
        """
        task_id, _ = self.dispatch_task(project, instruction, wait_for_result=False)
        return task_id

    def wait_task_result(
        self,
        project: str,
        task_id: str,
        timeout: int = 300
    ) -> TaskResult:
        """비동기 태스크 결과 대기"""
        if not IPC_AVAILABLE:
            return TaskResult(task_id=task_id, status="failed", error="IPC not available")

        dispatcher = TaskDispatcher()
        return dispatcher.wait_result(project, task_id, timeout)

    # =========================================================================
    # TTY 기반 LLM 실행 (codex, gemini)
    # =========================================================================

    def run_codex(
        self,
        project: str,
        instruction: str,
        timeout: int = 120,
        full_auto: bool = True
    ) -> CommandResult:
        """
        Codex CLI 실행 (TTY 환경에서)

        Args:
            project: 프로젝트명
            instruction: 지시 내용
            timeout: 최대 대기 시간 (초)
            full_auto: --full-auto 플래그 사용 여부

        Returns:
            CommandResult (output에 codex 실행 결과)
        """
        return self._run_tty_tool(
            project=project,
            tool="codex",
            instruction=instruction,
            timeout=timeout,
            extra_args="--full-auto" if full_auto else ""
        )

    def run_gemini(
        self,
        project: str,
        instruction: str,
        timeout: int = 120,
        yolo: bool = True
    ) -> CommandResult:
        """
        Gemini CLI 실행 (TTY 환경에서)

        Args:
            project: 프로젝트명
            instruction: 지시 내용
            timeout: 최대 대기 시간 (초)
            yolo: --yolo 플래그 사용 여부 (자동 승인 모드)

        Returns:
            CommandResult (output에 gemini 실행 결과)
        """
        return self._run_tty_tool(
            project=project,
            tool="gemini",
            instruction=instruction,
            timeout=timeout,
            extra_args="--yolo" if yolo else ""
        )

    def _run_tty_tool(
        self,
        project: str,
        tool: str,
        instruction: str,
        timeout: int = 120,
        extra_args: str = ""
    ) -> CommandResult:
        """
        TTY가 필요한 도구를 tmux new-window + script로 실행

        Args:
            project: 프로젝트명
            tool: 실행할 도구 (codex, gemini 등)
            instruction: 지시 내용
            timeout: 최대 대기 시간
            extra_args: 추가 인자

        Returns:
            CommandResult
        """
        import uuid
        start_time = time.time()

        config = self._get_project_config(project)
        if not config:
            return CommandResult(
                success=False,
                session="",
                command=f"{tool} {instruction}",
                output="",
                duration=0,
                error=f"Unknown project: {project}"
            )

        session_name = config["session"]
        project_path = PROJECTS_BASE / config["folder"]

        # 세션 존재 확인
        self._refresh_sessions()
        if session_name not in self.sessions or not self.sessions[session_name].exists:
            return CommandResult(
                success=False,
                session=session_name,
                command=f"{tool} {instruction}",
                output="",
                duration=0,
                error=f"Session not found: {session_name}"
            )

        task_id = uuid.uuid4().hex[:8]
        result_file = Path(f"/tmp/{tool}_{task_id}.txt")
        done_marker = f"---{tool.upper()}-DONE-{task_id}---"

        # 명령 구성
        escaped_instruction = instruction.replace("'", "'\"'\"'")
        if extra_args:
            cmd = f"{tool} {extra_args} '{escaped_instruction}'"
        else:
            cmd = f"{tool} '{escaped_instruction}'"

        # tmux new-window + script로 TTY 환경에서 실행
        window_name = f"{tool}-{task_id}"
        tmux_cmd = [
            "tmux", "new-window",
            "-t", session_name,
            "-n", window_name,
            f"cd {project_path} && script -q {result_file} {cmd}; echo '{done_marker}' >> {result_file}"
        ]

        try:
            subprocess.run(tmux_cmd, capture_output=True, timeout=5)
        except Exception as e:
            return CommandResult(
                success=False,
                session=session_name,
                command=cmd,
                output="",
                duration=time.time() - start_time,
                error=f"Failed to start {tool}: {e}"
            )

        # 결과 대기
        poll_interval = 2.0
        while time.time() - start_time < timeout:
            if result_file.exists():
                content = result_file.read_text()
                if done_marker in content:
                    # ANSI 코드 제거
                    clean_output = ANSI_ESCAPE.sub('', content)
                    clean_output = clean_output.replace(done_marker, '').strip()

                    # 창 닫기
                    self._run_tmux(["kill-window", "-t", f"{session_name}:{window_name}"])

                    return CommandResult(
                        success=True,
                        session=session_name,
                        command=cmd,
                        output=clean_output,
                        duration=time.time() - start_time
                    )
            time.sleep(poll_interval)

        # 타임아웃
        self._run_tmux(["kill-window", "-t", f"{session_name}:{window_name}"])

        return CommandResult(
            success=False,
            session=session_name,
            command=cmd,
            output=result_file.read_text() if result_file.exists() else "",
            duration=timeout,
            error=f"Timeout after {timeout}s"
        )

    def dispatch_with_context(
        self,
        project: str,
        instruction: str,
        context: str,
        timeout: int = 300
    ) -> tuple[Optional[str], Optional[str]]:
        """
        이전 작업 맥락을 포함하여 Worker에게 지시 전송

        Args:
            project: 프로젝트명
            instruction: 주요 지시 내용
            context: 이전 작업 결과/맥락 (codex 결과 등)
            timeout: 타임아웃

        Returns:
            (task_id, result) 튜플

        Example:
            # Codex → Worker 순차 협업
            codex_result = orch.run_codex("japan", "린트 체크")
            task_id, result = orch.dispatch_with_context(
                project="japan",
                instruction="아래 린트 오류들을 수정해줘",
                context=f"[Codex 린트 결과]\n{codex_result.output}"
            )
        """
        full_instruction = f"""[이전 작업 맥락]
{context}

[요청 사항]
{instruction}"""

        return self.dispatch_task(
            project=project,
            instruction=full_instruction,
            timeout=timeout,
            wait_for_result=True
        )


# CLI 테스트
if __name__ == "__main__":
    import sys

    orch = TmuxOrchestrator()

    if len(sys.argv) < 2:
        print("Usage:")
        print("  list                         - List all sessions")
        print("  create <project>             - Create session")
        print("  create-all                   - Create all sessions")
        print("  send <project> <cmd>         - Send shell command")
        print("  capture <project>            - Capture output")
        print("  kill <project>               - Kill session")
        print("")
        print("  [Claude control]")
        print("  start-claude <project>       - Start Claude (--dangerously-skip-permissions)")
        print("  start-claude-all             - Start Claude in all sessions")
        print("  start-claude-safe <project>  - Start Claude (normal mode)")
        print("")
        print("  [Claude task]")
        print("  task <project> <instruction> - Send + wait for result")
        print("  task-nowait <project> <inst> - Send only (no wait)")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "list":
        sessions = orch.list_sessions()
        print(json.dumps(sessions, indent=2, ensure_ascii=False))

    elif cmd == "create" and len(sys.argv) >= 3:
        success, msg = orch.create_session(sys.argv[2])
        print(f"{'✅' if success else '❌'} {msg}")

    elif cmd == "create-all":
        results = orch.create_all_sessions()
        for session, msg in results.items():
            print(f"  {session}: {msg}")

    elif cmd == "send" and len(sys.argv) >= 4:
        project = sys.argv[2]
        command = " ".join(sys.argv[3:])
        result = orch.send_command(project, command)
        print(f"{'✅' if result.success else '❌'} {result.session}")
        print(f"Duration: {result.duration:.1f}s")
        if result.error:
            print(f"Error: {result.error}")
        if result.output:
            print("--- Output ---")
            print(result.output[:1000])

    elif cmd == "capture" and len(sys.argv) >= 3:
        session = orch.get_session_name(sys.argv[2])
        if session:
            output = orch.capture_output(session)
            print(output[:2000])
        else:
            print(f"Unknown project: {sys.argv[2]}")

    elif cmd == "kill" and len(sys.argv) >= 3:
        success, msg = orch.kill_session(sys.argv[2])
        print(f"{'✅' if success else '❌'} {msg}")

    elif cmd == "start-claude" and len(sys.argv) >= 3:
        # Claude 시작 (skip permissions)
        success, msg = orch.start_claude_in_session(sys.argv[2], skip_permissions=True)
        print(f"{'✅' if success else '❌'} {msg}")

    elif cmd == "start-claude-safe" and len(sys.argv) >= 3:
        # Claude 시작 (normal mode)
        success, msg = orch.start_claude_in_session(sys.argv[2], skip_permissions=False)
        print(f"{'✅' if success else '❌'} {msg}")

    elif cmd == "start-claude-all":
        # 모든 세션에서 Claude 시작
        results = orch.start_all_claude_sessions(skip_permissions=True)
        for session, msg in results.items():
            print(f"  {session}: {msg}")

    elif cmd == "task" and len(sys.argv) >= 4:
        # 지시 전송 + 결과 대기
        project = sys.argv[2]
        instruction = " ".join(sys.argv[3:])
        print(f"[PM] {project} <- {instruction[:50]}...")
        print(f"[..] Waiting for result...")
        task_id, result = orch.dispatch_task(project, instruction, wait_for_result=True)
        if task_id:
            print(f"\n[Result from {project}]")
            print("-" * 60)
            if result:
                print(result[:2000])
            else:
                print("(No result captured)")
            print("-" * 60)

    elif cmd == "task-nowait" and len(sys.argv) >= 4:
        # 지시 전송만 (결과 대기 안함)
        project = sys.argv[2]
        instruction = " ".join(sys.argv[3:])
        print(f"[PM] {project} <- {instruction[:50]}... (no wait)")
        task_id = orch.dispatch_task_async(project, instruction)
        if task_id:
            print(f"[OK] Dispatched (task_id: {task_id})")

    else:
        print("Invalid command or missing arguments")
