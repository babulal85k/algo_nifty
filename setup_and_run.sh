#!/bin/bash

echo "======================================"
echo "🚀 NIFTY OPTIONS PAPER TRADING SETUP"
echo "======================================"

# -------- BASIC CHECKS --------
if [ "$EUID" -eq 0 ]; then
  echo "❌ Please do NOT run as root"
  exit 1
fi

# -------- UPDATE SYSTEM --------
echo "🔄 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# -------- INSTALL SYSTEM DEPENDENCIES --------
echo "📦 Installing system dependencies..."
sudo apt install -y \
  python3 \
  python3-venv \
  python3-pip \
  git \
  tmux \
  unzip

# -------- PROJECT DIRECTORY --------
PROJECT_DIR="$HOME/nifty_options_paper_trading"

if [ ! -d "$PROJECT_DIR" ]; then
  echo "📁 Creating project directory: $PROJECT_DIR"
  mkdir -p "$PROJECT_DIR"
fi

cd "$PROJECT_DIR" || exit 1

# -------- VIRTUAL ENV --------
if [ ! -d "venv" ]; then
  echo "🐍 Creating Python virtual environment..."
  python3 -m venv venv
fi

echo "✅ Activating virtual environment..."
source venv/bin/activate

# -------- PIP UPDATE --------
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# -------- INSTALL PYTHON PACKAGES --------
if [ -f "requirements.txt" ]; then
  echo "📦 Installing Python requirements..."
  pip install -r requirements.txt
else
  echo "❌ requirements.txt not found!"
  exit 1
fi

# -------- SAFETY FILES --------
if [ ! -f ".env" ]; then
  echo "🔐 Creating .env file (ADD YOUR KEYS!)"
  cat <<EOF > .env
UPSTOX_API_KEY=
UPSTOX_ACCESS_TOKEN=

TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
EOF
  echo "⚠️ Please edit .env before running the algo"
fi

# -------- STOP FILE --------
if [ ! -f "STOP" ]; then
  touch STOP
fi

# -------- PERMISSIONS --------
chmod +x *.py
chmod +x *.sh

# -------- FINAL MESSAGE --------
echo ""
echo "======================================"
echo "✅ SETUP COMPLETE"
echo "======================================"
echo ""
echo "📌 NEXT STEPS:"
echo "1️⃣ Edit .env and add API keys"
echo "2️⃣ Remove STOP file:  rm STOP"
echo "3️⃣ Run algo:"
echo ""
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""
echo "🛑 Emergency stop anytime:"
echo "   touch STOP"
echo ""
echo "💡 TIP: Use tmux for background run"
echo ""
echo "======================================"