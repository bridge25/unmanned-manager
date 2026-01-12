#!/bin/bash

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║                     🤖 Team JARVIS Setup Script                            ║
# ║                                                                            ║
# ║  Interactive setup for your personal JARVIS AI assistant                   ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
echo -e "${CYAN}"
echo "╔═══════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                           ║"
echo "║       ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗                             ║"
echo "║       ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝                             ║"
echo "║       ██║███████║██████╔╝██║   ██║██║███████╗                             ║"
echo "║  ██   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║                             ║"
echo "║  ╚█████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║                             ║"
echo "║   ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝                             ║"
echo "║                                                                           ║"
echo "║              🤖 Your Personal AI Assistant Setup                          ║"
echo "║                                                                           ║"
echo "╚═══════════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo -e "${YELLOW}👋 Welcome to Team JARVIS Setup!${NC}"
echo ""
echo -e "This script will help you set up JARVIS in your project."
echo ""

# Step 1: Get user info
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${PURPLE}Step 1: Tell me about yourself${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

read -p "$(echo -e ${CYAN}Your name: ${NC})" USER_NAME
read -p "$(echo -e ${CYAN}Your role \(e.g., Developer, Designer\): ${NC})" USER_ROLE

echo ""
echo -e "${GREEN}✓ Got it! Hello, ${USER_NAME}!${NC}"
echo ""

# Step 2: Select target directory
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${PURPLE}Step 2: Where to install JARVIS?${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

echo "Choose installation location:"
echo ""
echo -e "  ${CYAN}1)${NC} Current directory ($(pwd))"
echo -e "  ${CYAN}2)${NC} Custom path"
echo ""

read -p "$(echo -e ${CYAN}Select \[1/2\]: ${NC})" INSTALL_CHOICE

if [ "$INSTALL_CHOICE" == "2" ]; then
    read -p "$(echo -e ${CYAN}Enter full path: ${NC})" TARGET_DIR
else
    TARGET_DIR="$(pwd)"
fi

# Validate directory
if [ ! -d "$TARGET_DIR" ]; then
    echo -e "${YELLOW}⚠️  Directory doesn't exist. Create it? [y/n]${NC}"
    read CREATE_DIR
    if [ "$CREATE_DIR" == "y" ]; then
        mkdir -p "$TARGET_DIR"
        echo -e "${GREEN}✓ Created directory${NC}"
    else
        echo -e "${RED}✗ Aborted. Please create the directory first.${NC}"
        exit 1
    fi
fi

echo ""
echo -e "${GREEN}✓ Installing to: ${TARGET_DIR}${NC}"
echo ""

# Step 3: MindCollab setup
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${PURPLE}Step 3: MindCollab Integration (Optional)${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

echo "MindCollab enables team collaboration and task tracking."
echo ""
read -p "$(echo -e ${CYAN}Do you have a MindCollab auth code? \[y/n\]: ${NC})" HAS_MC

if [ "$HAS_MC" == "y" ]; then
    read -p "$(echo -e ${CYAN}Enter your MindCollab code: ${NC})" MC_CODE
    echo -e "${GREEN}✓ MindCollab code saved${NC}"
else
    MC_CODE=""
    echo -e "${YELLOW}ℹ️  You can set up MindCollab later. Ask Tony for your auth code.${NC}"
fi

echo ""

# Step 4: Install files
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${PURPLE}Step 4: Installing JARVIS...${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Create directories
echo -e "  ${CYAN}→${NC} Creating directories..."
mkdir -p "$TARGET_DIR"/.claude/skills
mkdir -p "$TARGET_DIR"/.claude/hooks/jarvis
mkdir -p "$TARGET_DIR"/.claude/commands
mkdir -p "$TARGET_DIR"/current

# Copy files
echo -e "  ${CYAN}→${NC} Copying JARVIS core files..."
cp "$SCRIPT_DIR/CLAUDE.md" "$TARGET_DIR/"
cp "$SCRIPT_DIR/GUIDE.md" "$TARGET_DIR/"

echo -e "  ${CYAN}→${NC} Copying skills (Deep Research, Chaos Engine)..."
cp -r "$SCRIPT_DIR/.claude/skills/"* "$TARGET_DIR/.claude/skills/"

echo -e "  ${CYAN}→${NC} Copying template files..."
cp "$SCRIPT_DIR/current/"* "$TARGET_DIR/current/"

# Personalize profile
echo -e "  ${CYAN}→${NC} Personalizing your profile..."
sed -i '' "s/{{YOUR_NAME}}/${USER_NAME}/g" "$TARGET_DIR/current/profile.md"
sed -i '' "s/{{YOUR_ROLE}}/${USER_ROLE}/g" "$TARGET_DIR/current/profile.md"

echo ""
echo -e "${GREEN}✓ JARVIS installed successfully!${NC}"
echo ""

# Step 5: Summary
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${PURPLE}Installation Complete!${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

echo -e "${GREEN}📁 Installed files:${NC}"
echo ""
echo "  $TARGET_DIR/"
echo "  ├── CLAUDE.md            # Claude Code rules"
echo "  ├── GUIDE.md             # JARVIS protocol"
echo "  ├── current/"
echo "  │   ├── profile.md       # Your profile (JARVIS learns about you)"
echo "  │   ├── projects.md      # Project tracking"
echo "  │   ├── todo.md          # Task list"
echo "  │   └── weekly-log.md    # Weekly records"
echo "  └── .claude/"
echo "      └── skills/"
echo "          ├── jarvis-deep-research/  # Research skill"
echo "          └── jarvis-chaos-engine/   # Ideation skill"
echo ""

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}🚀 Getting Started:${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "  ${CYAN}1.${NC} Open Claude Code in: ${GREEN}$TARGET_DIR${NC}"
echo -e "  ${CYAN}2.${NC} Type: ${GREEN}와썹${NC}"
echo -e "  ${CYAN}3.${NC} JARVIS will greet you with a briefing!"
echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}📚 Available Commands:${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "  ${GREEN}/research {topic}${NC}  - Deep research on any topic"
echo -e "  ${GREEN}/chaos {topic}${NC}     - Creative ideation session"
echo ""

if [ -n "$MC_CODE" ]; then
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}🤝 MindCollab Setup:${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "  Run: ${GREEN}mc auth login --code ${MC_CODE}${NC}"
    echo ""
fi

echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🤖 JARVIS is ready to assist you, ${USER_NAME}!${NC}"
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
