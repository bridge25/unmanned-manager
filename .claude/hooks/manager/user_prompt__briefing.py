#!/usr/bin/env python3
"""
JARVIS Briefing Hook: Auto Git Status Collection on "와썹"

Trigger: UserPromptSubmit
Role: Detect "와썹" keyword → Collect Git status from configured projects → Inject to context
"""
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

import yaml


# Briefing trigger keywords
BRIEFING_KEYWORDS = ["와썹", "wassup", "whatsup", "브리핑", "briefing"]


def load_config(project_dir: Path) -> dict:
    """Load config.yaml"""
    config_file = project_dir / "config.yaml"
    if not config_file.exists():
        return {}
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return {}


def get_projects_from_config(config: dict, project_dir: Path) -> list[dict]:
    """Extract project paths from config.yaml and projects.md"""
    projects = []

    # 1. From config.yaml scan_paths
    scan_paths = config.get("projects", {}).get("scan_paths", [])
    for path in scan_paths:
        if path and path != "/path/to/your/projects":
            p = Path(path)
            if p.exists():
                projects.append({
                    "name": p.name,
                    "path": str(p),
                    "urgency": "MID",
                    "absolute": True
                })

    # 2. From projects.md (parse locations)
    projects_md = project_dir / "current" / "projects.md"
    if projects_md.exists():
        try:
            content = projects_md.read_text(encoding="utf-8")

            # Parse project blocks
            # Pattern: ## N. ProjectName ... | **Location** | `path` | ... | **Urgency** | LEVEL |
            project_blocks = re.split(r'\n## \d+\.', content)[1:]  # Skip header

            for block in project_blocks:
                lines = block.strip().split('\n')
                if not lines:
                    continue

                name = lines[0].strip().split('(')[0].strip()
                location = None
                urgency = "MID"

                for line in lines:
                    # Extract location
                    loc_match = re.search(r'\*\*Location\*\*[^\|]*\|\s*`([^`]+)`', line, re.IGNORECASE)
                    if not loc_match:
                        loc_match = re.search(r'\*\*위치\*\*[^\|]*\|\s*`([^`]+)`', line)
                    if loc_match:
                        location = loc_match.group(1).strip()

                    # Extract urgency
                    urg_match = re.search(r'\*\*Urgency\*\*[^\|]*\|\s*(\w+)', line, re.IGNORECASE)
                    if not urg_match:
                        urg_match = re.search(r'\*\*긴급도\*\*[^\|]*\|\s*(\w+)', line)
                    if urg_match:
                        urgency = urg_match.group(1).upper()
                        if urgency not in ["HIGH", "MID", "LOW"]:
                            urgency = "MID"

                if location and name != "Project Template" and "Example" not in name:
                    projects.append({
                        "name": name,
                        "path": location,
                        "urgency": urgency,
                        "absolute": False
                    })
        except Exception:
            pass

    return projects


def is_briefing_request(prompt: str) -> bool:
    """Check if this is a briefing request"""
    prompt_lower = prompt.lower().strip()
    return any(kw in prompt_lower for kw in BRIEFING_KEYWORDS)


def run_git_command(project_path: Path, cmd: list[str]) -> str:
    """Execute Git command"""
    try:
        result = subprocess.run(
            cmd,
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=3
        )
        return result.stdout.strip() if result.returncode == 0 else ""
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError, OSError):
        return ""


def get_project_git_status(project: dict, base_dir: Path) -> dict:
    """Collect Git status for a single project"""
    if project.get("absolute"):
        project_path = Path(project["path"])
    else:
        project_path = (base_dir / project["path"]).resolve()

    if not project_path.exists():
        return {
            "name": project["name"],
            "urgency": project["urgency"],
            "status": "❌ Not found",
            "branch": "-",
            "last_commit": "-",
            "commit_date": "-",
            "uncommitted": 0,
            "error": "path_not_found"
        }

    # Check if Git repository
    git_dir = project_path / ".git"
    if not git_dir.exists():
        return {
            "name": project["name"],
            "urgency": project["urgency"],
            "status": "⚠️ No Git",
            "branch": "-",
            "last_commit": "-",
            "commit_date": "-",
            "uncommitted": 0,
            "error": "not_git_repo"
        }

    # Collect Git info (parallel)
    git_commands = [
        (["git", "branch", "--show-current"], "branch"),
        (["git", "log", "--pretty=format:%h %s", "-1"], "last_commit"),
        (["git", "log", "--pretty=format:%ar", "-1"], "commit_date"),
        (["git", "status", "--porcelain"], "changes_raw"),
    ]

    results = {}
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(run_git_command, project_path, cmd): key
            for cmd, key in git_commands
        }
        for future in as_completed(futures):
            key = futures[future]
            try:
                results[key] = future.result()
            except Exception:
                results[key] = ""

    # Parse results
    branch = results.get("branch", "unknown") or "unknown"
    last_commit = results.get("last_commit", "unknown") or "unknown"
    commit_date = results.get("commit_date", "unknown") or "unknown"
    changes_raw = results.get("changes_raw", "")
    uncommitted = len(changes_raw.splitlines()) if changes_raw else 0

    # Determine status
    if uncommitted > 10:
        status = f"⚠️ {uncommitted} uncommitted"
    elif uncommitted > 0:
        status = f"📝 {uncommitted} uncommitted"
    else:
        status = "✅ Clean"

    return {
        "name": project["name"],
        "urgency": project["urgency"],
        "status": status,
        "branch": branch,
        "last_commit": last_commit[:50] if len(last_commit) > 50 else last_commit,
        "commit_date": commit_date,
        "uncommitted": uncommitted,
        "error": None
    }


def collect_all_git_status(projects: list[dict], base_dir: Path) -> list[dict]:
    """Collect Git status for all projects (parallel)"""
    if not projects:
        return []

    results = []

    with ThreadPoolExecutor(max_workers=min(len(projects), 8)) as executor:
        futures = {
            executor.submit(get_project_git_status, proj, base_dir): proj["name"]
            for proj in projects
        }
        for future in as_completed(futures):
            try:
                results.append(future.result())
            except Exception as e:
                results.append({
                    "name": futures[future],
                    "status": f"❌ Error: {str(e)[:30]}",
                    "error": str(e)
                })

    # Sort by urgency (HIGH > MID > LOW)
    urgency_order = {"HIGH": 0, "MID": 1, "LOW": 2, "TBD": 3}
    results.sort(key=lambda x: urgency_order.get(x.get("urgency", "TBD"), 99))

    return results


def format_git_status_table(statuses: list[dict]) -> str:
    """Format Git status as table"""
    if not statuses:
        return "No projects configured. Add projects to `current/projects.md` or configure `scan_paths` in `config.yaml`."

    lines = [
        "| Project | Urgency | Branch | Status | Last Commit |",
        "|---------|---------|--------|--------|-------------|"
    ]

    for s in statuses:
        urgency_icon = {"HIGH": "🔴", "MID": "🟡", "LOW": "🟢"}.get(s.get("urgency", ""), "⚪")
        lines.append(
            f"| {s['name']} | {urgency_icon} {s.get('urgency', '-')} | "
            f"`{s.get('branch', '-')}` | {s.get('status', '-')} | "
            f"{s.get('commit_date', '-')} |"
        )

    return "\n".join(lines)


def main():
    # Read Hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except Exception:
        print(json.dumps({"continue": True}))
        sys.exit(0)

    user_prompt = hook_input.get("prompt", "")

    # 1. Check if briefing request
    if not is_briefing_request(user_prompt):
        print(json.dumps({"continue": True}))
        sys.exit(0)

    # 2. Load config and get projects
    project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")).resolve()
    config = load_config(project_dir)
    projects = get_projects_from_config(config, project_dir)

    # 3. Collect Git status
    statuses = collect_all_git_status(projects, project_dir)

    # 4. Format as table
    table = format_git_status_table(statuses)
    today = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 5. Output context
    context = f"""[JARVIS Git Status - {today}]

{table}

⚠️ Include this Git status table in your briefing."""

    output = {
        "continue": True,
        "context": context
    }

    print(json.dumps(output, ensure_ascii=False))
    sys.exit(0)


if __name__ == "__main__":
    main()
