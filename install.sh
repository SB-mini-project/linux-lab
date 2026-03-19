#!/bin/bash
# LINUX LAB - SANGAM BEAVERS
# 설치 스크립트

echo "========================================"
echo "  LINUX LAB - Installation"
echo "  Sangam Beavers"
echo "========================================"

PYTHON=$(which python3 2>/dev/null)
if [ -z "$PYTHON" ]; then
    echo "❌ Python3 가 설치되어 있지 않습니다."
    exit 1
fi

PY_MINOR=$($PYTHON -c 'import sys; print(sys.version_info.minor)')
PY_MAJOR=$($PYTHON -c 'import sys; print(sys.version_info.major)')

if [ "$PY_MAJOR" -lt 3 ] || [ "$PY_MINOR" -lt 7 ]; then
    echo "❌ Python 3.7 이상 필요. (현재: $($PYTHON --version))"
    exit 1
fi
echo "✓ Python 버전: $($PYTHON --version)"

INSTALL_DIR="/opt/linux-lab"
echo "✓ 설치 경로: $INSTALL_DIR"

sudo mkdir -p "$INSTALL_DIR"
sudo cp -r . "$INSTALL_DIR/"
sudo chmod +x "$INSTALL_DIR/quiz.py"
sudo ln -sf "$INSTALL_DIR/quiz.py" /usr/local/bin/linux-lab

echo ""
echo "========================================"
echo "  ✅ 설치 완료!"
echo ""
echo "  실행:  linux-lab"
echo "  또는:  python3 quiz.py"
echo "========================================"
