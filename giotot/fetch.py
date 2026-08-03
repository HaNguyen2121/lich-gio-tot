"""Tải HTML lịch quẻ theo tháng từ lich.vutrungu.com, có cache vĩnh viễn.

Dữ liệu Dịch cố định theo ngày (không đổi) nên cache mãi mãi ra file. Nhờ cache
app vẫn chạy được cả khi vutrungu tạm sập, và không tải lại tháng đã xem.
"""

import os
import urllib.request

BASE_URL = "https://lich.vutrungu.com/xemthang"
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)

CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cache")


def _cache_path(yy: int, mm: int) -> str:
    return os.path.join(CACHE_DIR, f"{yy:04d}-{mm:02d}.html")


def get_month_html(yy: int, mm: int, force: bool = False) -> str:
    """Trả về HTML tháng mm/yy. Ưu tiên cache; nếu chưa có thì tải và lưu."""
    path = _cache_path(yy, mm)
    if not force and os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    url = f"{BASE_URL}?yy={yy}&mm={mm}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        html = resp.read().decode("utf-8", "replace")

    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return html
