# 🪟 Windows Setup Guide for Team JARVIS

> WSL2를 사용하여 Windows에서 JARVIS 전체 기능 사용하기

---

## 📋 필요한 것

- Windows 10 (버전 2004 이상) 또는 Windows 11
- 관리자 권한
- 인터넷 연결

---

## 🚀 Step 1: WSL2 설치 (10분)

### 1.1 PowerShell 관리자 모드로 실행

```powershell
# Windows 키 → "PowerShell" 검색 → 우클릭 → "관리자 권한으로 실행"
```

### 1.2 WSL 설치

```powershell
wsl --install
```

이 명령어가:
- WSL2 활성화
- Ubuntu 기본 설치
- 필요한 기능 모두 설정

### 1.3 재부팅

```powershell
# 설치 완료 메시지 후 재부팅 필요
shutdown /r /t 0
```

### 1.4 Ubuntu 초기 설정

재부팅 후 자동으로 Ubuntu 창이 열립니다:

```bash
# 사용자 이름 입력 (예: daewoong)
Enter new UNIX username: daewoong

# 비밀번호 설정
New password: ********
Retype password: ********
```

---

## 🛠️ Step 2: 개발 환경 설정 (5분)

Ubuntu 터미널에서 실행:

### 2.1 패키지 업데이트

```bash
sudo apt update && sudo apt upgrade -y
```

### 2.2 필수 도구 설치

```bash
# tmux (오케스트레이션용)
sudo apt install -y tmux

# Node.js (Claude Code용)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Python (스크립트용)
sudo apt install -y python3 python3-pip
```

### 2.3 Claude Code 설치

```bash
npm install -g @anthropic-ai/claude-code
```

---

## 📁 Step 3: 프로젝트 설정 (5분)

### 3.1 Windows 폴더 접근

WSL에서 Windows 드라이브는 `/mnt/` 아래에 있습니다:

```bash
# C: 드라이브 접근
cd /mnt/c/Users/YourName/projects

# D: 드라이브 접근 (있다면)
cd /mnt/d/projects
```

### 3.2 작업 폴더 생성

```bash
# 예: C:\Users\대웅\projects\my-workspace
mkdir -p /mnt/c/Users/대웅/projects/my-workspace
cd /mnt/c/Users/대웅/projects/my-workspace
```

### 3.3 JARVIS 설치

```bash
# init-jarvis.sh 실행 (경로는 실제 위치로 수정)
bash /path/to/team-jarvis-template/init-jarvis.sh
```

---

## 🔧 Step 4: /pm 오케스트레이션 설정 (선택)

### 4.1 tmux 기본 사용법

```bash
# 새 세션 시작
tmux new -s myproject

# 세션 분리 (백그라운드로)
# Ctrl+B 누른 후 D

# 세션 목록 보기
tmux ls

# 세션 재접속
tmux attach -t myproject
```

### 4.2 멀티 프로젝트 세션 설정

```bash
# 예: 3개 프로젝트 세션 생성
tmux new -s project1 -d
tmux new -s project2 -d
tmux new -s project3 -d

# 각 세션에서 Claude Code 시작
tmux send-keys -t project1 "cd /mnt/c/projects/project1 && claude" Enter
tmux send-keys -t project2 "cd /mnt/c/projects/project2 && claude" Enter
tmux send-keys -t project3 "cd /mnt/c/projects/project3 && claude" Enter
```

### 4.3 오케스트레이션 스크립트 복사

```bash
# PM 기능 사용 시 hooks 복사
mkdir -p .claude/hooks/jarvis
cp /path/to/template/.claude/hooks/jarvis/*.py .claude/hooks/jarvis/
```

---

## 💡 Step 5: 일상 사용법

### 5.1 WSL 시작

```powershell
# PowerShell 또는 Windows Terminal에서
wsl
```

또는 시작 메뉴에서 "Ubuntu" 검색하여 실행

### 5.2 Claude Code 실행

```bash
# 프로젝트 폴더로 이동
cd /mnt/c/Users/대웅/projects/my-project

# Claude Code 시작
claude
```

### 5.3 세션 시작

```
와썹
```

---

## 🎯 Quick Reference

| 작업 | 명령어 |
|------|--------|
| WSL 시작 | `wsl` (PowerShell에서) |
| 프로젝트 이동 | `cd /mnt/c/Users/이름/projects/폴더` |
| Claude 시작 | `claude` |
| tmux 세션 생성 | `tmux new -s 이름` |
| tmux 세션 분리 | `Ctrl+B` → `D` |
| tmux 목록 | `tmux ls` |
| tmux 재접속 | `tmux attach -t 이름` |

---

## ⚠️ 주의사항

### 파일 경로

```bash
# Windows 경로 → WSL 경로 변환
C:\Users\대웅\projects  →  /mnt/c/Users/대웅/projects
D:\work                  →  /mnt/d/work
```

### 줄바꿈 문제

Windows에서 만든 파일은 줄바꿈이 다를 수 있음:

```bash
# 필요시 변환
sudo apt install dos2unix
dos2unix filename.sh
```

### VS Code 연동 (선택)

```bash
# WSL에서 VS Code 열기
code .
```

---

## 🆘 문제 해결

### WSL이 설치 안 될 때

```powershell
# Windows 기능 수동 활성화
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# 재부팅 후 다시 시도
wsl --install
```

### Claude Code 설치 오류

```bash
# npm 캐시 정리 후 재시도
npm cache clean --force
npm install -g @anthropic-ai/claude-code
```

### tmux 세션이 안 보일 때

```bash
# 모든 세션 강제 종료 후 재시작
tmux kill-server
tmux new -s myproject
```

---

## 📚 추가 자료

- [WSL 공식 문서](https://docs.microsoft.com/ko-kr/windows/wsl/)
- [tmux 치트시트](https://tmuxcheatsheet.com/)
- [Windows Terminal 설정](https://docs.microsoft.com/ko-kr/windows/terminal/)

---

*Team JARVIS Windows Setup Guide v1.0*
