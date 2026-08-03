"""Ghép các bước: nhận chuỗi người dùng nhập -> danh sách ngày giờ tốt."""

import calendar
import datetime
import re

from .fetch import get_month_html
from .matching import loc_thang
from .parse import hour_window, parse_month


def next_good_hour(now, max_months=4):
    """Tìm giờ tốt kế tiếp thật sự tính từ `now`, độc lập với khoảng đang xem.

    Trả về (key, start_dt, gio, dang_dien) hoặc None. Dò tối đa `max_months` tháng
    tới để không lặp vô hạn.
    """
    yy, mm = now.year, now.month
    for _ in range(max_months):
        try:
            days = loc_thang(parse_month(get_month_html(yy, mm), yy, mm))
        except Exception:
            return None
        cands = []
        for day in days:
            for g in day["gio_tot"]:
                start, end = hour_window(day["date"], g)
                if end > now:
                    cands.append((start, end, day, g))
        if cands:
            start, end, day, g = min(cands, key=lambda x: x[0])
            key = f'{day["date"].isoformat()}|{g["chi"]}'
            return (key, start, g, start <= now < end)
        mm, yy = (1, yy + 1) if mm == 12 else (mm + 1, yy)
    return None


class InputError(ValueError):
    pass


def _parse_iso_date(s: str) -> datetime.date:
    """'YYYY-MM-DD' -> date, có kiểm tra hợp lệ."""
    m = re.fullmatch(r"\s*(\d{4})-(\d{1,2})-(\d{1,2})\s*", s or "")
    if not m:
        raise InputError("Chưa chọn ngày hợp lệ.")
    yy, mm, dd = int(m.group(1)), int(m.group(2)), int(m.group(3))
    if not (1900 <= yy <= 2199):
        raise InputError("Năm phải trong khoảng 1900–2199.")
    try:
        return datetime.date(yy, mm, dd)
    except ValueError:
        raise InputError("Ngày không hợp lệ.")


def _iter_months(d1: datetime.date, d2: datetime.date):
    """Sinh (yy, mm) cho từng tháng từ tháng của d1 đến tháng của d2."""
    y, m = d1.year, d1.month
    while (y, m) <= (d2.year, d2.month):
        yield y, m
        m, y = (1, y + 1) if m == 12 else (m + 1, y)


def _range_title(tu: datetime.date, den: datetime.date) -> str:
    if tu == den:
        return f"Giờ tốt ngày {tu.day:02d}/{tu.month:02d}/{tu.year}"
    last = calendar.monthrange(tu.year, tu.month)[1]
    if (tu.day == 1 and den.day == last
            and (tu.year, tu.month) == (den.year, den.month)):
        return f"Giờ tốt tháng {tu.month}/{tu.year}"
    return (f"Giờ tốt {tu.day:02d}/{tu.month:02d}/{tu.year} – "
            f"{den.day:02d}/{den.month:02d}/{den.year}")


def tra_cuu_range(tu_iso: str, den_iso: str):
    """Nhận 2 ngày (từ / đến) dạng ISO -> giờ tốt của mọi ngày trong khoảng."""
    tu = _parse_iso_date(tu_iso)
    den = _parse_iso_date(den_iso)
    if tu > den:              # nhập ngược thì tự đảo
        tu, den = den, tu
    if (den - tu).days > 366:
        raise InputError("Khoảng thời gian tối đa 1 năm.")
    ket_qua = []
    for yy, mm in _iter_months(tu, den):
        days = loc_thang(parse_month(get_month_html(yy, mm), yy, mm))
        ket_qua.extend(d for d in days if tu <= d["date"] <= den)
    ket_qua.sort(key=lambda d: d["date"])
    return (_range_title(tu, den), ket_qua)


def parse_query(q: str):
    """Phân tích chuỗi nhập -> ('thang', yy, mm) hoặc ('ngay', yy, mm, dd)."""
    nums = [int(x) for x in re.findall(r"\d+", q or "")]
    if len(nums) == 2:
        mm, yy = nums
        _validate(yy, mm)
        return ("thang", yy, mm, None)
    if len(nums) == 3:
        dd, mm, yy = nums
        _validate(yy, mm, dd)
        return ("ngay", yy, mm, dd)
    raise InputError(
        "Định dạng chưa đúng. Nhập tháng 'MM/YYYY' (vd 8/2026) "
        "hoặc ngày 'DD/MM/YYYY' (vd 02/08/2026)."
    )


def _validate(yy, mm, dd=None):
    if not (1900 <= yy <= 2199):
        raise InputError("Năm phải trong khoảng 1900–2199.")
    if not (1 <= mm <= 12):
        raise InputError("Tháng phải từ 1 đến 12.")
    if dd is not None and not (1 <= dd <= 31):
        raise InputError("Ngày phải từ 1 đến 31.")


def tra_cuu_thang_iso(s: str):
    """Nhận giá trị từ <input type=month> ('YYYY-MM')."""
    m = re.fullmatch(r"\s*(\d{4})-(\d{1,2})\s*", s or "")
    if not m:
        raise InputError("Chưa chọn tháng hợp lệ.")
    return tra_cuu(f"{int(m.group(2))}/{int(m.group(1))}")


def tra_cuu_ngay_iso(s: str):
    """Nhận giá trị từ <input type=date> ('YYYY-MM-DD')."""
    m = re.fullmatch(r"\s*(\d{4})-(\d{1,2})-(\d{1,2})\s*", s or "")
    if not m:
        raise InputError("Chưa chọn ngày hợp lệ.")
    return tra_cuu(f"{int(m.group(3))}/{int(m.group(2))}/{int(m.group(1))}")


def tra_cuu(q: str):
    """Trả về (tieu_de, filtered_days). Ném InputError nếu chuỗi nhập sai."""
    kind, yy, mm, dd = parse_query(q)
    html_text = get_month_html(yy, mm)
    days = parse_month(html_text, yy, mm)
    filtered = loc_thang(days)

    if kind == "thang":
        return (f"Giờ tốt tháng {mm}/{yy}", filtered)

    # kind == "ngay": lọc riêng ngày được chọn
    filtered = [n for n in filtered if n["day"] == dd]
    return (f"Giờ tốt ngày {dd:02d}/{mm:02d}/{yy}", filtered)
