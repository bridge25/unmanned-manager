#!/usr/bin/env python3
"""
JARVIS PM Executor - /pm 슬래시 커맨드 실행기
=============================================
프로젝트별 작업을 최적의 LLM으로 위임

작성일: 2025-12-18
업데이트: 2025-12-25 (tmux 오케스트레이션 통합)
방식: tmux 세션 직접 주입 + LLM 라우팅
"""
import json
import subprocess
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

# tmux 오케스트레이터 임포트
try:
    from .tmux_orchestrator import TmuxOrchestrator, CommandResult
    TMUX_AVAILABLE = True
except ImportError:
    try:
        from tmux_orchestrator import TmuxOrchestrator, CommandResult
        TMUX_AVAILABLE = True
    except ImportError:
        TMUX_AVAILABLE = False
        TmuxOrchestrator = None
        CommandResult = None

# PM Cycle Recorder 임포트 (유사 케이스 제안용)
PM_CYCLE_RECORDER_AVAILABLE = False
try:
    import sys
    _pm_pipelines_path = Path(__file__).parent.parent.parent.parent / "jarvis" / "pipelines"
    if _pm_pipelines_path.exists() and str(_pm_pipelines_path) not in sys.path:
        sys.path.insert(0, str(_pm_pipelines_path))
    from pm_cycle_recorder import get_recorder, PMResolution
    PM_CYCLE_RECORDER_AVAILABLE = True
except ImportError:
    get_recorder = None
    PMResolution = None

# 프로젝트 베이스 경로
PROJECTS_BASE = Path("/Volumes/d/users/tony/Desktop/projects")

# 프로젝트 매핑 (별칭 → 실제 폴더명)
PROJECT_MAPPING = {
    # 해동기획
    "해동검도": "order-automation-saas",
    "해동기획": "order-automation-saas",
    "해동": "order-automation-saas",
    "haedong": "order-automation-saas",

    # Japan Sale
    "japan": "japan",
    "일본": "japan",
    "japansale": "japan",

    # FlyMoney
    "flymoney": "flymoney",
    "fly": "flymoney",
    "항공": "flymoney",

    # DT-RAG
    "dt-rag": "dt-rag",
    "rag": "dt-rag",
    "dtrag": "dt-rag",

    # 크립토멘토
    "크립토멘토": "premium-contents-scrraper",
    "멘토": "premium-contents-scrraper",
    "크립토": "premium-contents-scrraper",
    "crypto": "premium-contents-scrraper",

    # 사주
    "사주": "saju",
    "saju": "saju",

    # QR 주차
    "qr주차": "qr-parking-demo",
    "주차": "qr-parking-demo",
    "qrparking": "qr-parking-demo",
    "parking": "qr-parking-demo",

    # 프레젠토
    "프레젠토": "daddy's-ppt",
    "prezento": "daddy's-ppt",
}

# LLM 선택 키워드
LLM_KEYWORDS = {
    "codex": {
        "keywords": [
            "디버깅", "debug", "테스트", "test", "lint", "빌드", "build",
            "점검", "리뷰", "review", "cicd", "ci/cd", "배포", "deploy",
            "버그", "bug", "에러", "error", "fix", "수정", "체크", "check",
            "커버리지", "coverage", "타입", "type", "보안", "security"
        ],
        "confidence_boost": 0.2,
    },
    "gemini": {
        "keywords": [
            "리서치", "research", "문서", "조사", "검색", "탐색",
            "긴문서", "대용량", "분석레포트"
        ],
        "confidence_boost": 0.25,
    },
    "glm": {
        "keywords": [
            "벌크", "bulk", "대량", "변환", "transform", "추출", "extract",
            "간단", "simple", "빠르게", "quick", "요약", "summary",
            "번역", "translate", "포맷", "format"
        ],
        "confidence_boost": 0.2,
    },
    "glm-v": {
        "keywords": [
            "이미지", "image", "스크린샷", "screenshot", "ui", "디자인",
            "design", "시각", "visual", "영상", "video", "멀티모달",
            "화면", "캡처", "사진", "그림"
        ],
        "confidence_boost": 0.25,
    },
}

# 확신도 임계값 (이 이상이면 자동 선택, 미만이면 사용자 확인)
CONFIDENCE_THRESHOLD = 0.75


@dataclass
class SimilarSuggestion:
    """유사 해결 사례 제안"""
    score: float  # 0.0 ~ 1.0
    project: str
    issue_title: str
    resolution_summary: str
    commit_hash: Optional[str] = None


@dataclass
class LLMSelection:
    """LLM 선택 결과"""
    llm: str
    confidence: float
    reason: str
    matched_keywords: list[str]


@dataclass
class PMResult:
    """PM 실행 결과"""
    success: bool
    llm_used: str
    output: str
    duration: float
    project_path: str
    error: Optional[str] = None


def get_project_path(project_name: str) -> Optional[Path]:
    """프로젝트명으로 실제 경로 찾기"""
    # 정확한 매핑 먼저
    normalized = project_name.lower().strip()

    if normalized in PROJECT_MAPPING:
        path = PROJECTS_BASE / PROJECT_MAPPING[normalized]
        if path.exists():
            return path

    # 부분 매칭
    for alias, folder in PROJECT_MAPPING.items():
        if alias in normalized or normalized in alias:
            path = PROJECTS_BASE / folder
            if path.exists():
                return path

    # 직접 폴더명으로 시도
    direct_path = PROJECTS_BASE / project_name
    if direct_path.exists():
        return direct_path

    return None


def select_llm(instruction: str) -> LLMSelection:
    """지시 내용 분석하여 최적 LLM 선택"""
    instruction_lower = instruction.lower()

    scores = {"codex": 0.0, "gemini": 0.0, "glm": -100.0, "glm-v": -100.0, "claude": 0.3}  # claude 기본값, glm/glm-v 라우팅 제외
    matched = {"codex": [], "gemini": [], "glm": [], "glm-v": [], "claude": []}

    # 키워드 매칭
    for llm, config in LLM_KEYWORDS.items():
        for keyword in config["keywords"]:
            if keyword.lower() in instruction_lower:
                scores[llm] += config["confidence_boost"]
                matched[llm].append(keyword)

    # 최고 점수 LLM 선택
    best_llm = max(scores, key=scores.get)
    best_score = scores[best_llm]

    # 이유 생성
    if matched[best_llm]:
        reason = f"키워드 매칭: {', '.join(matched[best_llm][:3])}"
    else:
        reason = "기본 선택 (복잡한 판단 필요)"

    return LLMSelection(
        llm=best_llm,
        confidence=min(best_score + 0.3, 1.0),  # 기본 0.3 + 키워드 점수
        reason=reason,
        matched_keywords=matched[best_llm]
    )


def needs_confirmation(selection: LLMSelection) -> bool:
    """사용자 확인이 필요한지 판단"""
    return selection.confidence < CONFIDENCE_THRESHOLD


def get_similar_suggestions(
    instruction: str,
    project: Optional[str] = None,
    limit: int = 3
) -> list[SimilarSuggestion]:
    """
    지시 내용과 유사한 해결 사례 검색

    Args:
        instruction: PM 지시 내용
        project: 프로젝트명 (선택, 있으면 해당 프로젝트 우선)
        limit: 반환할 최대 건수

    Returns:
        SimilarSuggestion 리스트 (유사도 높은 순)
    """
    if not PM_CYCLE_RECORDER_AVAILABLE or get_recorder is None:
        return []

    try:
        recorder = get_recorder()
        results = recorder.search_similar(instruction, limit=limit + 2)

        suggestions = []
        for score, resolution in results:
            # 유사도 50% 이상만
            if score >= 0.5:
                # 같은 프로젝트면 점수 부스트
                adjusted_score = score
                if project and resolution.project.lower() == project.lower():
                    adjusted_score = min(score + 0.1, 1.0)

                suggestions.append(SimilarSuggestion(
                    score=adjusted_score,
                    project=resolution.project,
                    issue_title=resolution.issue_title,
                    resolution_summary=resolution.resolution_summary,
                    commit_hash=resolution.commit_hash
                ))

        # 점수순 재정렬
        suggestions.sort(key=lambda x: x.score, reverse=True)
        return suggestions[:limit]

    except Exception:
        return []


def format_suggestions_context(suggestions: list[SimilarSuggestion]) -> str:
    """유사 케이스 제안을 컨텍스트 문자열로 포맷"""
    if not suggestions:
        return ""

    lines = ["💡 **유사 해결 사례 발견**"]

    for i, s in enumerate(suggestions, 1):
        score_pct = int(s.score * 100)
        lines.append(f"   {i}. [{score_pct}%] {s.project}: {s.issue_title}")
        lines.append(f"      → {s.resolution_summary[:60]}...")
        if s.commit_hash:
            lines.append(f"      🔗 `{s.commit_hash}`")

    lines.append("")
    lines.append("   참고: `/pm:similar <키워드>` 로 더 검색 가능")

    return "\n".join(lines)


def format_confirmation_question(selection: LLMSelection, instruction: str) -> dict:
    """AskUserQuestion용 질문 포맷"""
    llm_descriptions = {
        "codex": "코드 점검/디버깅/보안",
        "gemini": "Gemini 3 Flash (2M 컨텍스트)",
        "glm": "GLM-4.7 텍스트 (벌크/요약/코딩)",
        "glm-v": "GLM-4.6V 비전 (이미지/UI 분석)",
        "claude": "복잡한 판단/개발"
    }

    options = []

    # 추천 LLM 먼저
    desc = llm_descriptions.get(selection.llm, selection.llm)
    options.append({
        "label": f"{selection.llm.upper()} (추천)",
        "description": f"{desc} - {selection.reason}"
    })

    # 나머지 LLM (중요도 순) - glm/glm-v 제외
    for llm in ["codex", "gemini", "claude"]:
        if llm != selection.llm and len(options) < 4:
            options.append({
                "label": llm.upper(),
                "description": llm_descriptions.get(llm, llm)
            })

    return {
        "question": f"'{instruction[:30]}...' 작업에 어떤 LLM을 사용할까요?",
        "header": "LLM 선택",
        "options": options[:4],  # 최대 4개
        "multiSelect": False
    }


def run_with_codex(project_path: Path, instruction: str, timeout: int = 300) -> PMResult:
    """Codex CLI로 실행"""
    start = time.time()
    session_id = f"jarvis-pm-{uuid.uuid4().hex[:8]}"

    try:
        # codex 명령어 구성
        cmd = [
            "codex", "exec",
            "--sandbox", "workspace-write",
            instruction
        ]

        result = subprocess.run(
            cmd,
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        duration = time.time() - start

        if result.returncode == 0:
            return PMResult(
                success=True,
                llm_used="codex",
                output=result.stdout,
                duration=duration,
                project_path=str(project_path)
            )
        else:
            return PMResult(
                success=False,
                llm_used="codex",
                output=result.stdout,
                duration=duration,
                project_path=str(project_path),
                error=result.stderr or f"Exit code: {result.returncode}"
            )

    except subprocess.TimeoutExpired:
        return PMResult(
            success=False,
            llm_used="codex",
            output="",
            duration=timeout,
            project_path=str(project_path),
            error=f"Timeout after {timeout}s"
        )
    except Exception as e:
        return PMResult(
            success=False,
            llm_used="codex",
            output="",
            duration=time.time() - start,
            project_path=str(project_path),
            error=str(e)
        )


def run_with_gemini(project_path: Path, instruction: str, timeout: int = 180) -> PMResult:
    """Gemini CLI로 실행"""
    start = time.time()

    try:
        cmd = ["gemini", "--yolo", instruction]

        result = subprocess.run(
            cmd,
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        duration = time.time() - start

        return PMResult(
            success=result.returncode == 0,
            llm_used="gemini",
            output=result.stdout,
            duration=duration,
            project_path=str(project_path),
            error=result.stderr if result.returncode != 0 else None
        )

    except subprocess.TimeoutExpired:
        return PMResult(
            success=False,
            llm_used="gemini",
            output="",
            duration=timeout,
            project_path=str(project_path),
            error=f"Timeout after {timeout}s"
        )
    except Exception as e:
        return PMResult(
            success=False,
            llm_used="gemini",
            output="",
            duration=time.time() - start,
            project_path=str(project_path),
            error=str(e)
        )


def run_with_glm(project_path: Path, instruction: str, timeout: int = 90) -> PMResult:
    """GLM-4.6 (텍스트) HTTP API로 실행"""
    start = time.time()

    try:
        # GLMExecutor 임포트 시도
        import sys
        jarvis_path = Path(__file__).parent.parent.parent.parent / "jarvis"
        if str(jarvis_path) not in sys.path:
            sys.path.insert(0, str(jarvis_path))

        from orchestrator.executors.glm_executor import GLMExecutor
        from orchestrator.executors.base import ExecutorContext

        executor = GLMExecutor(model="glm-4.7", timeout=timeout)
        context = ExecutorContext(
            task_id=f"pm-{uuid.uuid4().hex[:8]}",
            instruction=instruction,
            project=str(project_path.name),
            timeout=timeout,
            metadata={"project_path": str(project_path)}
        )

        result = executor.execute(context)
        duration = time.time() - start

        if result.success:
            output = result.output.get("agent_response", "") if isinstance(result.output, dict) else str(result.output)
            return PMResult(
                success=True,
                llm_used="glm-4.7",
                output=output,
                duration=duration,
                project_path=str(project_path)
            )
        else:
            return PMResult(
                success=False,
                llm_used="glm-4.7",
                output="",
                duration=duration,
                project_path=str(project_path),
                error=result.error
            )

    except ImportError as e:
        return PMResult(
            success=False,
            llm_used="glm-4.7",
            output="",
            duration=time.time() - start,
            project_path=str(project_path),
            error=f"GLMExecutor 임포트 실패: {e}"
        )
    except Exception as e:
        return PMResult(
            success=False,
            llm_used="glm-4.7",
            output="",
            duration=time.time() - start,
            project_path=str(project_path),
            error=str(e)
        )


def run_with_glm_vision(project_path: Path, instruction: str, image_path: str = None, timeout: int = 120) -> PMResult:
    """GLM-4.6V (비전) HTTP API로 실행"""
    start = time.time()

    try:
        import sys
        jarvis_path = Path(__file__).parent.parent.parent.parent / "jarvis"
        if str(jarvis_path) not in sys.path:
            sys.path.insert(0, str(jarvis_path))

        from orchestrator.executors.glm_executor import GLMExecutor
        from orchestrator.executors.base import ExecutorContext

        executor = GLMExecutor(vision_model="glm-4.6v", timeout=timeout)

        metadata = {"project_path": str(project_path)}
        if image_path:
            metadata["image_url"] = image_path

        context = ExecutorContext(
            task_id=f"pm-v-{uuid.uuid4().hex[:8]}",
            instruction=instruction,
            project=str(project_path.name),
            timeout=timeout,
            metadata=metadata
        )

        result = executor.execute(context)
        duration = time.time() - start

        if result.success:
            output = result.output.get("agent_response", "") if isinstance(result.output, dict) else str(result.output)
            return PMResult(
                success=True,
                llm_used="glm-4.6v",
                output=output,
                duration=duration,
                project_path=str(project_path)
            )
        else:
            return PMResult(
                success=False,
                llm_used="glm-4.6v",
                output="",
                duration=duration,
                project_path=str(project_path),
                error=result.error
            )

    except ImportError as e:
        return PMResult(
            success=False,
            llm_used="glm-4.6v",
            output="",
            duration=time.time() - start,
            project_path=str(project_path),
            error=f"GLMExecutor 임포트 실패: {e}"
        )
    except Exception as e:
        return PMResult(
            success=False,
            llm_used="glm-4.6v",
            output="",
            duration=time.time() - start,
            project_path=str(project_path),
            error=str(e)
        )


# =============================================================================
# tmux 기반 실행 함수들 (2025-12-25 추가)
# =============================================================================

def run_with_tmux(
    project: str,
    instruction: str,
    wait_seconds: float = 30.0,
    use_claude: bool = True
) -> PMResult:
    """
    tmux 세션에 명령/지시 전송

    Args:
        project: 프로젝트명
        instruction: 지시 내용
        wait_seconds: 결과 대기 시간
        use_claude: True면 Claude에게 지시, False면 쉘 명령

    Returns:
        PMResult
    """
    if not TMUX_AVAILABLE:
        return PMResult(
            success=False,
            llm_used="tmux",
            output="",
            duration=0,
            project_path="",
            error="tmux_orchestrator not available"
        )

    start = time.time()
    orch = TmuxOrchestrator()

    # 세션 존재 확인, 없으면 생성
    session_name = orch.get_session_name(project)
    if not session_name:
        return PMResult(
            success=False,
            llm_used="tmux",
            output="",
            duration=0,
            project_path="",
            error=f"Unknown project: {project}"
        )

    sessions = orch.list_sessions()
    if session_name not in sessions or not sessions[session_name]["exists"]:
        success, msg = orch.create_session(project)
        if not success:
            return PMResult(
                success=False,
                llm_used="tmux",
                output="",
                duration=time.time() - start,
                project_path="",
                error=f"Failed to create session: {msg}"
            )

    # 명령 전송
    if use_claude:
        result = orch.send_to_claude(project, instruction, wait_seconds)
    else:
        result = orch.send_command(project, instruction, wait_seconds)

    return PMResult(
        success=result.success,
        llm_used="tmux-claude" if use_claude else "tmux-shell",
        output=result.output,
        duration=result.duration,
        project_path=str(orch.sessions[session_name].project_path) if session_name in orch.sessions else "",
        error=result.error
    )


def run_with_tmux_dispatch(
    project: str,
    instruction: str,
    timeout: int = 300,
    wait_for_result: bool = True
) -> PMResult:
    """
    tmux 세션에 지시 전송 (dispatch_task 사용, 파일 IPC 결과 수신)

    Args:
        project: 프로젝트명
        instruction: 지시 내용
        timeout: 타임아웃 (초)
        wait_for_result: 결과 대기 여부

    이 함수는 tmux_orchestrator의 dispatch_task를 사용하여:
    1. 지시에 LLM 라우팅 강제 명령 자동 추가 (codex, gemini 등)
    2. 결과를 파일 IPC로 수신
    """
    if not TMUX_AVAILABLE:
        return PMResult(
            success=False,
            llm_used="tmux",
            output="",
            duration=0,
            project_path="",
            error="tmux_orchestrator not available"
        )

    start = time.time()
    orch = TmuxOrchestrator()

    # 세션 확인/생성
    session_name = orch.get_session_name(project)
    if not session_name:
        return PMResult(
            success=False,
            llm_used="tmux",
            output="",
            duration=0,
            project_path="",
            error=f"Unknown project: {project}"
        )

    sessions = orch.list_sessions()
    if session_name not in sessions or not sessions[session_name]["exists"]:
        success, msg = orch.create_session(project)
        if not success:
            return PMResult(
                success=False,
                llm_used="tmux",
                output="",
                duration=time.time() - start,
                project_path="",
                error=f"Failed to create session: {msg}"
            )

    # dispatch_task로 전송 (LLM 라우팅 강제 자동 적용됨)
    task_id, result_text = orch.dispatch_task(
        project=project,
        instruction=instruction,
        timeout=timeout,
        wait_for_result=wait_for_result
    )

    duration = time.time() - start
    project_path = str(orch.sessions[session_name].project_path) if session_name in orch.sessions else ""

    if task_id:
        return PMResult(
            success=result_text is not None,
            llm_used="tmux-claude",
            output=result_text or f"Task dispatched: {task_id} (async)",
            duration=duration,
            project_path=project_path,
            error=None if result_text else "No result received" if wait_for_result else None
        )
    else:
        return PMResult(
            success=False,
            llm_used="tmux-claude",
            output="",
            duration=duration,
            project_path=project_path,
            error="Failed to dispatch task"
        )


# =============================================================================
# 메인 실행 함수
# =============================================================================

def run_pm_task(
    project: str,
    instruction: str,
    llm_override: Optional[str] = None,
    use_tmux: bool = True  # 기본값: tmux 사용
) -> Tuple[PMResult, LLMSelection]:
    """
    PM 작업 실행 메인 함수

    Args:
        project: 프로젝트명 또는 별칭
        instruction: 지시 내용
        llm_override: 사용자가 직접 선택한 LLM (있으면 자동 선택 무시)
        use_tmux: True면 tmux 세션 사용, False면 subprocess 사용

    Returns:
        (PMResult, LLMSelection) 튜플
    """
    # 1. 프로젝트 경로 찾기
    project_path = get_project_path(project)
    if not project_path:
        return PMResult(
            success=False,
            llm_used="none",
            output="",
            duration=0,
            project_path="",
            error=f"프로젝트를 찾을 수 없습니다: {project}"
        ), LLMSelection("none", 0, "프로젝트 없음", [])

    # 2. LLM 선택
    selection = select_llm(instruction)

    # 사용자 지정이 있으면 오버라이드
    if llm_override:
        selection.llm = llm_override.lower()
        selection.confidence = 1.0
        selection.reason = "사용자 선택"

    # 3. 선택된 LLM으로 실행
    if use_tmux and TMUX_AVAILABLE:
        # tmux 모드: dispatch_task 사용 (LLM 라우팅 강제 자동 적용)
        # codex/gemini 키워드가 지시에 있으면 자동으로 CLI 호출 강제 명령 추가됨
        if selection.llm in ("codex", "gemini", "claude"):
            result = run_with_tmux_dispatch(project, instruction, timeout=300)
        else:
            # GLM은 tmux 미지원, subprocess 폴백
            if selection.llm == "glm":
                result = run_with_glm(project_path, instruction)
            elif selection.llm == "glm-v":
                result = run_with_glm_vision(project_path, instruction)
            else:
                result = run_with_tmux_dispatch(project, instruction, timeout=300)
    else:
        # subprocess 모드 (레거시)
        if selection.llm == "codex":
            result = run_with_codex(project_path, instruction)
        elif selection.llm == "gemini":
            result = run_with_gemini(project_path, instruction)
        elif selection.llm == "glm":
            result = run_with_glm(project_path, instruction)
        elif selection.llm == "glm-v":
            result = run_with_glm_vision(project_path, instruction)
        else:
            # Claude는 현재 세션에서 직접 처리하므로 여기서는 안내만
            result = PMResult(
                success=True,
                llm_used="claude",
                output="Claude는 현재 세션에서 직접 처리합니다.",
                duration=0,
                project_path=str(project_path)
            )

    return result, selection


def format_result_report(
    result: PMResult,
    selection: LLMSelection,
    suggestions: Optional[list[SimilarSuggestion]] = None
) -> str:
    """결과를 보고 형식으로 포맷

    Args:
        result: PM 실행 결과
        selection: LLM 선택 정보
        suggestions: 유사 케이스 제안 (선택)
    """
    lines = []

    # 헤더
    status = "✅ 성공" if result.success else "❌ 실패"
    lines.append(f"## PM 작업 결과: {status}")
    lines.append("")

    # 메타 정보
    lines.append(f"- **LLM**: {result.llm_used.upper()}")
    lines.append(f"- **선택 이유**: {selection.reason}")
    lines.append(f"- **확신도**: {selection.confidence:.0%}")
    lines.append(f"- **소요 시간**: {result.duration:.1f}초")
    lines.append(f"- **프로젝트**: `{result.project_path}`")
    lines.append("")

    # 유사 케이스 제안 (있으면)
    if suggestions:
        suggestion_text = format_suggestions_context(suggestions)
        if suggestion_text:
            lines.append(suggestion_text)
            lines.append("")

    # 출력
    if result.output:
        lines.append("### 실행 결과")
        lines.append("```")
        # 출력이 너무 길면 자르기
        output = result.output[:2000]
        if len(result.output) > 2000:
            output += "\n... (출력 생략)"
        lines.append(output)
        lines.append("```")

    # 에러
    if result.error:
        lines.append("")
        lines.append("### ⚠️ 에러")
        lines.append(f"```\n{result.error[:500]}\n```")

    return "\n".join(lines)


def run_pm_task_with_suggestions(
    project: str,
    instruction: str,
    llm_override: Optional[str] = None,
    use_tmux: bool = True
) -> Tuple[PMResult, LLMSelection, list[SimilarSuggestion]]:
    """
    PM 작업 실행 + 유사 케이스 제안 포함

    Args:
        project: 프로젝트명 또는 별칭
        instruction: 지시 내용
        llm_override: 사용자가 직접 선택한 LLM (있으면 자동 선택 무시)
        use_tmux: True면 tmux 세션 사용, False면 subprocess 사용

    Returns:
        (PMResult, LLMSelection, list[SimilarSuggestion]) 튜플
    """
    # 1. 유사 케이스 먼저 검색
    suggestions = get_similar_suggestions(instruction, project=project, limit=3)

    # 2. 작업 실행
    result, selection = run_pm_task(project, instruction, llm_override, use_tmux)

    return result, selection, suggestions


# CLI 테스트
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: pm_executor.py <project> <instruction>")
        print("Example: pm_executor.py 해동검도 '테스트 실행'")
        sys.exit(1)

    project = sys.argv[1]
    instruction = " ".join(sys.argv[2:])

    print(f"프로젝트: {project}")
    print(f"지시: {instruction}")
    print("-" * 40)

    # LLM 선택 미리보기
    selection = select_llm(instruction)
    print(f"추천 LLM: {selection.llm}")
    print(f"확신도: {selection.confidence:.0%}")
    print(f"이유: {selection.reason}")
    print(f"확인 필요: {needs_confirmation(selection)}")
