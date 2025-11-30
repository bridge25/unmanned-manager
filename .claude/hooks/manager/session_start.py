#!/usr/bin/env python3
"""
Unmanned Manager - Session Start Hook
세션 시작 시 자동으로 상태를 로드하고 Git 프로젝트를 스캔합니다.
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

def get_project_root():
    """프로젝트 루트 디렉토리 찾기"""
    # CLAUDE_PROJECT_DIR 환경변수 우선
    if "CLAUDE_PROJECT_DIR" in os.environ:
        return Path(os.environ["CLAUDE_PROJECT_DIR"])

    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "CLAUDE.md").exists():
            return parent
    return Path.cwd()

def load_config(project_root: Path) -> dict:
    """config.yaml 로드"""
    config_path = project_root / "config.yaml"
    if not config_path.exists():
        return {}

    try:
        import yaml
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    except ImportError:
        # PyYAML 없으면 간단히 파싱
        return parse_yaml_simple(config_path)
    except Exception:
        return {}

def parse_yaml_simple(config_path: Path) -> dict:
    """간단한 YAML 파서 (PyYAML 없을 때)"""
    config = {
        "user": {"name": "User", "honorific": "sir"},
        "projects": {"git_scan_enabled": False, "scan_paths": [], "inactive_alert_days": 7},
        "briefing": {"deadline_alert_days": 3}
    }

    try:
        content = config_path.read_text(encoding='utf-8')
        lines = content.split('\n')

        current_section = None
        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue

            # 섹션 감지
            if not line.startswith(' ') and ':' in stripped:
                key = stripped.split(':')[0].strip()
                value = stripped.split(':', 1)[1].strip() if ':' in stripped else ''

                if not value:  # 섹션 시작
                    current_section = key
                elif current_section and current_section in config:
                    if isinstance(config[current_section], dict):
                        config[current_section][key] = parse_value(value)

            # 하위 항목
            elif line.startswith('  ') and current_section:
                if ':' in stripped:
                    key = stripped.split(':')[0].strip()
                    value = stripped.split(':', 1)[1].strip()
                    if current_section in config and isinstance(config[current_section], dict):
                        config[current_section][key] = parse_value(value)
                elif stripped.startswith('- '):
                    # 리스트 항목
                    if current_section == "projects" and "scan_paths" not in config["projects"]:
                        config["projects"]["scan_paths"] = []
                    if current_section == "projects":
                        path = stripped[2:].strip().strip('"').strip("'")
                        config["projects"]["scan_paths"].append(path)
    except Exception:
        pass

    return config

def parse_value(value: str):
    """값 파싱"""
    value = value.strip().strip('"').strip("'")
    if value.lower() == 'true':
        return True
    if value.lower() == 'false':
        return False
    try:
        return int(value)
    except ValueError:
        return value

def scan_git_projects(scan_paths: list, inactive_days: int = 7) -> list:
    """Git 프로젝트들 스캔"""
    results = []

    for scan_path in scan_paths:
        path = Path(scan_path).expanduser()
        if not path.exists():
            continue

        # 하위 디렉토리 중 git repo 찾기
        try:
            for item in path.iterdir():
                if item.is_dir() and (item / ".git").exists():
                    info = get_git_info(item, inactive_days)
                    if info:
                        results.append(info)
        except PermissionError:
            continue

    return results

def get_git_info(repo_path: Path, inactive_days: int) -> dict:
    """개별 Git 저장소 정보 수집"""
    try:
        # 현재 브랜치
        branch = subprocess.run(
            ["git", "-C", str(repo_path), "branch", "--show-current"],
            capture_output=True, text=True, timeout=5
        ).stdout.strip()

        # 최근 커밋 날짜
        last_commit = subprocess.run(
            ["git", "-C", str(repo_path), "log", "-1", "--format=%ci"],
            capture_output=True, text=True, timeout=5
        ).stdout.strip()

        # 변경된 파일 수
        status = subprocess.run(
            ["git", "-C", str(repo_path), "status", "--porcelain"],
            capture_output=True, text=True, timeout=5
        ).stdout
        changed_files = len([l for l in status.split('\n') if l.strip()])

        # 비활성 일수 계산
        days_inactive = 0
        if last_commit:
            try:
                commit_date_str = last_commit.split()[0]
                commit_date = datetime.strptime(commit_date_str, "%Y-%m-%d")
                days_inactive = (datetime.now() - commit_date).days
            except Exception:
                pass

        return {
            "name": repo_path.name,
            "path": str(repo_path),
            "branch": branch or "unknown",
            "last_commit": last_commit.split()[0] if last_commit else "unknown",
            "days_inactive": days_inactive,
            "changed_files": changed_files,
            "alert": days_inactive >= inactive_days
        }
    except Exception:
        return None

def load_current_state(project_root: Path) -> dict:
    """current/ 폴더에서 현재 상태 로드"""
    current_dir = project_root / "current"
    weekdays_ko = ["월", "화", "수", "목", "금", "토", "일"]
    weekdays_en = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    state = {
        "today": datetime.now().strftime("%Y-%m-%d"),
        "weekday_ko": weekdays_ko[datetime.now().weekday()],
        "weekday_en": weekdays_en[datetime.now().weekday()],
    }

    # projects.md에서 HIGH 긴급도 프로젝트 수 카운트
    projects_file = current_dir / "projects.md"
    if projects_file.exists():
        try:
            content = projects_file.read_text(encoding='utf-8')
            state["high_priority_count"] = content.upper().count("HIGH")
        except Exception:
            state["high_priority_count"] = 0

    # todo.md에서 미완료 태스크 수 카운트
    todo_file = current_dir / "todo.md"
    if todo_file.exists():
        try:
            content = todo_file.read_text(encoding='utf-8')
            state["pending_tasks"] = content.count("- [ ]")
        except Exception:
            state["pending_tasks"] = 0

    return state

def main():
    try:
        project_root = get_project_root()
        config = load_config(project_root)

        # Git 스캔 설정
        projects_config = config.get("projects", {})
        git_enabled = projects_config.get("git_scan_enabled", False)
        scan_paths = projects_config.get("scan_paths", [])
        inactive_days = projects_config.get("inactive_alert_days", 7)

        # 사용자 설정
        user_config = config.get("user", {})
        user_name = user_config.get("name", "User")
        honorific = user_config.get("honorific", "sir")

        # 현재 상태 로드
        state = load_current_state(project_root)

        # Git 프로젝트 스캔
        git_projects = []
        if git_enabled and scan_paths:
            git_projects = scan_git_projects(scan_paths, inactive_days)

        # 알림 생성
        alerts = []
        for proj in git_projects:
            if proj and proj.get("alert"):
                alerts.append(f"{proj['name']}: {proj['days_inactive']}일간 비활성")
            if proj and proj.get("changed_files", 0) > 0:
                alerts.append(f"{proj['name']}: {proj['changed_files']}개 파일 변경됨")

        # 상태 저장 (memento와 공유)
        state_file = project_root / ".claude" / "memento" / ".session_state.json"
        state_file.parent.mkdir(parents=True, exist_ok=True)

        session_state = {
            "session_start": datetime.now().isoformat(),
            "user_name": user_name,
            "honorific": honorific,
            "state": state,
            "git_projects": git_projects,
            "alerts": alerts
        }

        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(session_state, f, ensure_ascii=False, indent=2)

        # 결과 출력 (Claude에게 전달)
        print(f"startup hook success: Success")

        return 0

    except Exception as e:
        print(f"startup hook error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
