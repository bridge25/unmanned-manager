# Team JARVIS Initialization Script for Windows
# PowerShell 5.1+ required

param(
    [string]$ProjectName = ""
)

Write-Host "🤖 Team JARVIS Template Initialization" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check PowerShell version
if ($PSVersionTable.PSVersion.Major -lt 5) {
    Write-Host "❌ PowerShell 5.1 or higher is required" -ForegroundColor Red
    Write-Host "Current version: $($PSVersionTable.PSVersion)" -ForegroundColor Red
    exit 1
}

# Get project name
if (-not $ProjectName) {
    $ProjectName = Read-Host "Enter your name (e.g., sookang, daewoong)"
}

Write-Host ""
Write-Host "📋 Project Name: $ProjectName" -ForegroundColor Green
Write-Host ""

# Create directories
Write-Host "📁 Creating directories..." -ForegroundColor Yellow
$dirs = @(
    "current",
    ".claude/hooks/jarvis",
    ".claude/skills",
    ".moai/memory",
    ".moai/logs/sessions"
)

foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "   ✓ Created: $dir" -ForegroundColor Green
    }
}

# Initialize current files if they don't exist
Write-Host ""
Write-Host "📝 Initializing files..." -ForegroundColor Yellow

# profile.md
if (-not (Test-Path "current/profile.md")) {
    @"
# Profile Database

> ${ProjectName}의 개인 프로필

## Facts (변하지 않는 정보)

### 기본 정보
- **호칭**: ${ProjectName}
- **역할**: [기획/개발/디자인 등]
- **작업 환경**: Windows

### 기술 스택
- 자신의 기술 스택 기록

### 장기 비전
- 자신의 목표 기록
"@ | Out-File -FilePath "current/profile.md" -Encoding UTF8
    Write-Host "   ✓ Created: current/profile.md" -ForegroundColor Green
}

# projects.md
if (-not (Test-Path "current/projects.md")) {
    @"
# 현재 진행 중인 프로젝트

> ${ProjectName}이 담당하는 프로젝트들

## 진행 중

### 프로젝트 1
- 역할:
- 현황:
- 우선순위:

## 예정

### 프로젝트 2
- 역할:
- 일정:
"@ | Out-File -FilePath "current/projects.md" -Encoding UTF8
    Write-Host "   ✓ Created: current/projects.md" -ForegroundColor Green
}

# todo.md
if (-not (Test-Path "current/todo.md")) {
    @"
# Todo List

> ${ProjectName}의 할 일 목록

## 🔴 High Priority

- [ ] TODO 1

## 🟡 Medium Priority

- [ ] TODO 2

## 🟢 Low Priority

- [ ] TODO 3
"@ | Out-File -FilePath "current/todo.md" -Encoding UTF8
    Write-Host "   ✓ Created: current/todo.md" -ForegroundColor Green
}

# weekly-log.md
if (-not (Test-Path "current/weekly-log.md")) {
    $weekNumber = (Get-Date).ToString("yyyy-MM-dd")
    @"
# Weekly Log

> ${ProjectName}의 주간 기록

## Week of $weekNumber

### 완료한 일
-

### 배운 것
-

### 다음 주 계획
-
"@ | Out-File -FilePath "current/weekly-log.md" -Encoding UTF8
    Write-Host "   ✓ Created: current/weekly-log.md" -ForegroundColor Green
}

# Git initialization
Write-Host ""
Write-Host "🔧 Git setup..." -ForegroundColor Yellow

if (-not (Test-Path ".git")) {
    git init | Out-Null
    Write-Host "   ✓ Git initialized" -ForegroundColor Green
} else {
    Write-Host "   ✓ Git already initialized" -ForegroundColor Green
}

# .gitignore
if (-not (Test-Path ".gitignore")) {
    @"
# Python
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/
ENV/

# Node
node_modules/
.npm

# OS
.DS_Store
Thumbs.db
desktop.ini

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
*.log

# Local
.env
.env.local
*.local

# MoAI
.moai/memory/
.moai/logs/
.moai/cache/
"@ | Out-File -FilePath ".gitignore" -Encoding UTF8
    Write-Host "   ✓ Created: .gitignore" -ForegroundColor Green
}

Write-Host ""
Write-Host "✅ Initialization complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Cyan
Write-Host "   1. Install MindCollab CLI: npm install -g @mindcollab/cli" -ForegroundColor White
Write-Host "   2. Login to MindCollab: mc auth login --code YOUR-CODE" -ForegroundColor White
Write-Host "   3. Initialize project: mc init" -ForegroundColor White
Write-Host "   4. Open with VS Code: code ." -ForegroundColor White
Write-Host "   5. Start Claude: type '와썹' to start briefing" -ForegroundColor White
Write-Host ""
Write-Host "🎉 Happy coding with JARVIS!" -ForegroundColor Green
