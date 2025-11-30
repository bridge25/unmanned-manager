# Unmanned Manager - Claude Session Rules

## Session Start Protocol

**"와썹" = Session Start Command** (not a greeting)

### On receiving "와썹", execute immediately:

1. Read `GUIDE.md` (Load Protocol)
2. Read `config.yaml` (Load user settings)
3. **Check First Run** - If `user.name` is "User" or `scan_paths` has placeholder:
   - Run First Run Protocol (see GUIDE.md)
   - Ask user for name, honorific, language, project path
   - Update config.yaml
   - Then continue to briefing
4. Read `current/profile.md` (Check user profile)
5. Read `current/projects.md` (Project status)
6. Read `current/todo.md` (Tasks)
7. **⚠️ Check Hook-injected Git status table** (auto-included in context)
8. Provide briefing (MUST include Git status table)

### Never do:

- Respond to "와썹" as a greeting
- Search other folders first
- Wander around - go straight to GUIDE.md

---

## Role of This Project

- **Personal AI Assistant** (JARVIS-style)
- Project control tower + Schedule management + Priority coordination
- See `GUIDE.md` for details

---

## File Structure

```
current/           <- Current operational data
├── profile.md     <- User profile (learning data)
├── projects.md    <- Project list
├── todo.md        <- Tasks
├── cases.md       <- Decision cases (Memento)
├── weekly-log.md  <- Weekly records
├── inbox.md       <- Ideas inbox
└── backlog.md     <- Someday/maybe

.claude/           <- Automation system
├── settings.json  <- Hooks configuration
└── hooks/         <- Automation scripts
    ├── manager/   <- JARVIS hooks
    │   └── user_prompt__briefing.py  <- Auto Git scan on "와썹"
    └── memento/   <- Learning hooks

config.yaml        <- User configuration
GUIDE.md           <- Full protocol definition
```

---

## Hook System

### Auto-executed Hooks:

| Trigger | Hook | Role |
|---------|------|------|
| "와썹" input | `manager/user_prompt__briefing.py` | Collect Git status from projects → Inject to context |

**MUST include Hook-injected Git status table in briefing.**
