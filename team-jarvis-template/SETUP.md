# 🤖 Team JARVIS Setup Guide

> Your personal AI assistant for project management and deep research.

---

## Quick Start (2 minutes)

### Option 1: Automated Setup (Recommended)

```bash
# 1. Navigate to your project directory
cd /path/to/your/project

# 2. Run the setup script
/path/to/team-jarvis-template/init-jarvis.sh
```

The script will:
- Ask for your name and role
- Copy all necessary files
- Personalize your profile
- Set up skills (Deep Research, Chaos Engine)

### Option 2: Manual Setup

```bash
# 1. Copy template to your project
cp -r /path/to/team-jarvis-template/* /path/to/your/project/

# 2. Edit your profile
# Open current/profile.md and fill in your info
```

---

## After Installation

### 1. Start a Session

Open Claude Code in your project directory and type:

```
와썹
```

JARVIS will respond with a briefing based on your projects and tasks.

### 2. Update Your Profile

Edit `current/profile.md` to add:
- Your background
- Current focus areas
- Communication preferences

JARVIS will learn more about you over time through conversations.

### 3. Track Your Projects

Edit `current/projects.md` to add your active projects. JARVIS uses this for:
- Daily briefings
- Proactive reminders
- Progress tracking

---

## Available Skills

### 🔍 Deep Research

Use for thorough investigation of any topic.

```
/research AI trends in 2026
/research {topic} --deep      # Until convergence
/research {topic} --quick     # Quick 3-iteration scan
```

**What it does:**
- Recursive exploration loop
- Verifies against opposing evidence
- Connects discoveries to your context
- Produces actionable insights

### 💡 Chaos Engine

Use for creative ideation and brainstorming.

```
/chaos new product ideas
/chaos {topic} --wild    # Maximum creativity
```

**What it does:**
- Controlled chaos ideation
- Tree of Thought evaluation
- Reality grounding
- Practical recommendations

---

## MindCollab Integration

MindCollab enables team collaboration.

### Setup

1. Get your auth code from Tony:
   - Tony: `TONY-MC-2026`
   - Sookang: `SOOKANG-MC-2026`
   - Daewoong: `DAEWOONG-MC-2026`

2. Login:
```bash
mc auth login --code YOUR_CODE
```

3. Initialize in your project:
```bash
mc init
```

### Daily Usage

```bash
mc tasks                    # List your tasks
mc start TASK_ID            # Start a task (creates branch)
mc done TASK_ID --pr        # Complete task + create PR
mc status                   # Project overview
```

---

## File Structure

```
your-project/
├── CLAUDE.md              # Claude Code session rules
├── GUIDE.md               # JARVIS protocol
├── current/
│   ├── profile.md         # Your profile (JARVIS learns from this)
│   ├── projects.md        # Active projects
│   ├── todo.md            # Personal tasks
│   └── weekly-log.md      # Weekly records
└── .claude/
    └── skills/
        ├── jarvis-deep-research/   # Research skill
        └── jarvis-chaos-engine/    # Ideation skill
```

---

## Session Commands

| Command | Description |
|---------|-------------|
| `와썹` | Start session, get briefing |
| `/research {topic}` | Deep research |
| `/chaos {topic}` | Creative ideation |
| `mc tasks` | MindCollab tasks |

---

## Tips

### 1. Let JARVIS Learn About You

The more you interact, the better JARVIS understands you:
- Share your preferences
- Explain your decisions
- Talk about your goals

JARVIS records important patterns to `current/profile.md`.

### 2. Keep Projects Updated

Update `current/projects.md` when:
- Starting a new project
- Completing a milestone
- Changing priorities

### 3. Use Parallel Execution

JARVIS designs parallel work tracks, not sequential steps:

```
❌ Bad: Task 1 → Task 2 → Task 3

✅ Good:
[Track A] Research (background)
[Track B] Development (main focus)
[Track C] Admin tasks (when available)
```

### 4. English Todo Items

Use English for todo items to avoid encoding issues:

```
❌ "프로젝트 완료" (may crash)
✅ "Complete project" (safe)
```

---

## Troubleshooting

### JARVIS doesn't respond to "와썹"

Make sure:
1. `CLAUDE.md` exists in project root
2. `GUIDE.md` exists in project root
3. You're using Claude Code (not regular Claude)

### Skills not working

Check that `.claude/skills/` directory exists with:
- `jarvis-deep-research/SKILL.md`
- `jarvis-chaos-engine/SKILL.md`

### MindCollab errors

1. Check login: `mc status`
2. Re-login if needed: `mc auth login --code YOUR_CODE`

---

## Need Help?

- Ask Tony in team chat
- Check MindCollab for team updates
- File issues in the team repo

---

---

## 🪟 Windows Users

Windows를 사용하시나요? **[WINDOWS-SETUP.md](./WINDOWS-SETUP.md)** 를 참조하세요.

WSL2 + tmux 환경에서 macOS와 동일하게 모든 기능을 사용할 수 있습니다.

---

*Team JARVIS Template v1.0*
*Built for Unmanned Company*
