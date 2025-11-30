#!/usr/bin/env python3
"""
JARVIS Study Mode Hook: Force research mode on "공부하고 있어"

Trigger: UserPromptSubmit
Role: Detect study keywords → Parse research_queue.md → Force research execution
"""
import json
import os
import re
import sys
from pathlib import Path


# Study mode trigger keywords
STUDY_KEYWORDS = [
    "공부하고 있어",
    "공부하고있어",
    "공부해",
    "리서치 해둬",
    "리서치해둬",
    "알아봐둬",
    "알아봐 둬",
    "study mode",
    "research mode",
]


def is_study_request(prompt: str) -> bool:
    """Check if this is a study mode request"""
    prompt_lower = prompt.lower().strip()
    return any(kw in prompt_lower for kw in STUDY_KEYWORDS)


def parse_research_queue(project_dir: Path) -> list[dict]:
    """Parse pending topics from research_queue.md"""
    queue_path = project_dir / "current" / "research_queue.md"

    if not queue_path.exists():
        return []

    try:
        content = queue_path.read_text(encoding="utf-8")
    except Exception:
        return []

    # Parse pending topics: - [ ] [topic] | 관련: [project] | ...
    pending_pattern = r"- \[ \] (.+?) \| 관련: (.+?) \|"
    matches = re.findall(pending_pattern, content)

    topics = []
    for topic, project in matches:
        topics.append({
            "topic": topic.strip(),
            "project": project.strip()
        })

    return topics


def main():
    # Read Hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except Exception:
        print(json.dumps({"continue": True}))
        sys.exit(0)

    user_prompt = hook_input.get("prompt", "")

    # 1. Check if study mode request
    if not is_study_request(user_prompt):
        print(json.dumps({"continue": True}))
        sys.exit(0)

    # 2. Parse research queue
    project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")).resolve()
    queue = parse_research_queue(project_dir)

    if not queue:
        context = """[JARVIS Study Mode - Research Queue Empty]

⚠️ No research topics in queue.

📋 Actions to take:
1. Propose research topics to user → Add to research_queue.md when approved
2. Self-research current project trends

❌ "No topics available" is not an excuse
✅ If no topics, discover them yourself"""
    else:
        # Start with first topic
        first_topic = queue[0]

        topic_list = "\n".join([
            f"   {i+1}. {t['topic']} ({t['project']})"
            for i, t in enumerate(queue[:5])  # Max 5 displayed
        ])

        context = f"""[JARVIS Study Mode - Starting Research]

🎯 Research Queue: {len(queue)} topics pending

{topic_list}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ Execute NOW:

1. Start background research with Task(subagent):
   - Topic: "{first_topic['topic']}"
   - Related Project: {first_topic['project']}

2. Task prompt example:
   ```
   Task(subagent_type="general-purpose", prompt='''
   Research the following topic in depth and summarize findings:

   Topic: {first_topic['topic']}

   Research Requirements:
   1. Use WebSearch for latest information (2024-2025)
   2. Focus on practical, immediately applicable insights
   3. Include specific advice relevant to user's situation
   4. Cite reliable sources

   Output Format:
   - 3-5 key insights
   - Specific action items
   - Whether additional research is needed
   ''')
   ```

3. After research completion:
   - Record results in current/insights.md
   - Check off topic in research_queue.md ([ ] → [x])
   - Record follow-up questions in research_questions.md if any

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ Forbidden:
- "Will do later" responses
- Responding without research
- Shallow searches

✅ Required:
- Use Task(subagent) for background execution
- User can work on other things
- Report in next briefing when complete"""

    output = {
        "continue": True,
        "context": context
    }

    print(json.dumps(output, ensure_ascii=False))
    sys.exit(0)


if __name__ == "__main__":
    main()
