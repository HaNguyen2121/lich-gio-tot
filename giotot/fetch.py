"""Tải HTML lịch quẻ theo tháng từ lich.vutrungu.com, có cache vĩnh viễn.

Dữ liệu Dịch cố định theo ngày (không đổi) nên cache mãi mãi ra file. Nhờ cache
app vẫn chạy được cả khi vutrungu tạm sập, và không tải lại tháng đã xem.
"""

import os
import tempfile
import time
import urllib.request

BASE_URL = "https://lich.vutrungu.com/xemthang"
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)

CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cache")


def _cache_path(yy: int, mm: int) -> str:
    return os.path.join(CACHE_DIR, f"{yy:04d}-{mm:02d}.html")


def _read_cache(path: str) -> str:
    """Đọc cache, thử lại vài lần nếu gặp lỗi tạm (vd nhiều tiến trình đọc/ghi
    cùng lúc -> OSError 'Resource deadlock avoided')."""
    last = None
    for attempt in range(5):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except OSError as e:
            last = e
            time.sleep(0.1 * (attempt + 1))
    raise last


def _write_cache(path: str, html: str) -> None:
    """Ghi cache kiểu atomic (ghi file tạm rồi đổi tên) để reader không bao giờ
    thấy file ghi dở, và tránh 2 tiến trình ghi đè lẫn nhau."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=CACHE_DIR, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(html)
        os.replace(tmp, path)
    except OSError:
        try:
            os.remove(tmp)
        except OSError:
            pass


def get_month_html(yy: int, mm: int, force: bool = False) -> str:
    """Trả về HTML tháng mm/yy. Ưu tiên cache; nếu chưa có thì tải và lưu."""
    path = _cache_path(yy, mm)
    if not force and os.path.exists(path):
        try:
            return _read_cache(path)
        except OSError:
            pass  # cache lỗi -> tải lại

    url = f"{BASE_URL}?yy={yy}&mm={mm}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        html = resp.read().decode("utf-8", "replace")

    _write_cache(path, html)
    return html
