#!/usr/bin/env bash
# Gỡ dịch vụ nền (macOS). Sau khi gỡ vẫn có thể chạy thủ công: python3 -m giotot
set -euo pipefail

PLIST="$HOME/Library/LaunchAgents/com.giotot.app.plist"
launchctl unload "$PLIST" 2>/dev/null || true
rm -f "$PLIST"
# tắt tiến trình còn sót (nếu có)
lsof -ti tcp:5057 2>/dev/null | xargs kill 2>/dev/null || true

echo "✅ Đã gỡ dịch vụ nền. Chạy thủ công khi cần: python3 -m giotot"
