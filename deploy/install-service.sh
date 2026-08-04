#!/usr/bin/env bash
# Cài dịch vụ nền (macOS LaunchAgent): app tự chạy khi đăng nhập, luôn sẵn ở
# http://127.0.0.1:<port>. Tự dò đường dẫn Python và thư mục project của máy này.
#
#   bash deploy/install-service.sh [port]   (mặc định 5057)

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="$(command -v python3 || true)"
PORT="${1:-5057}"

if [ -z "$PYTHON" ]; then
  echo "Không tìm thấy python3. Hãy cài Python 3 trước:" >&2
  echo "  xcode-select --install   (kèm Python)   hoặc   brew install python" >&2
  exit 1
fi

PLIST="$HOME/Library/LaunchAgents/com.giotot.app.plist"
mkdir -p "$HOME/Library/LaunchAgents" "$HOME/Library/Logs"

cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key><string>com.giotot.app</string>
    <key>ProgramArguments</key>
    <array>
        <string>$PYTHON</string>
        <string>-m</string><string>giotot</string>
        <string>--no-open</string>
        <string>--port</string><string>$PORT</string>
    </array>
    <key>WorkingDirectory</key><string>$PROJECT_DIR</string>
    <key>RunAtLoad</key><true/>
    <key>KeepAlive</key><true/>
    <key>StandardOutPath</key><string>$HOME/Library/Logs/giotot.log</string>
    <key>StandardErrorPath</key><string>$HOME/Library/Logs/giotot.log</string>
</dict>
</plist>
EOF

launchctl unload "$PLIST" 2>/dev/null || true
launchctl load "$PLIST"
sleep 2

echo "✅ Đã cài dịch vụ nền."
echo "   Mở app:  http://127.0.0.1:$PORT   (nên bookmark lại)"
echo "   Python:  $PYTHON"
echo "   Project: $PROJECT_DIR"
echo "   Log:     ~/Library/Logs/giotot.log"
echo "   Gỡ:      bash deploy/uninstall-service.sh"
