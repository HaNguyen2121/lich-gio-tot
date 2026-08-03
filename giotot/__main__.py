"""Chạy: python -m giotot   (mặc định cổng 5000, tự mở trình duyệt)."""

import argparse
import threading
import webbrowser

from .server import run


def main():
    ap = argparse.ArgumentParser(description="Web app Giờ tốt Dịch lý Việt Nam")
    ap.add_argument("--port", type=int, default=5057,
                    help="Cổng (mặc định 5057; tránh 5000 vì macOS AirPlay chiếm)")
    ap.add_argument("--host", default="127.0.0.1", help="Host (mặc định 127.0.0.1)")
    ap.add_argument("--no-open", action="store_true", help="Không tự mở trình duyệt")
    args = ap.parse_args()

    if not args.no_open:
        url = f"http://{args.host}:{args.port}"
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()

    run(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
