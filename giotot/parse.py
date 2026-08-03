"""Parse HTML tháng -> cấu trúc ngày/giờ.

Bảng <table id="example"> gồm 1 hàng header + các hàng ngày (theo thứ tự ngày
1, 2, 3, ...). Mỗi hàng ngày có 12 ô = 12 khung giờ (Tý -> Hợi). Mỗi ô có 3 dòng
ngăn bởi <br>: quẻ1, quẻ2, lục thú.

Số ngày dương + thứ trong tuần được tính bằng datetime (không phụ thuộc site).
"""

import datetime
import html as _html
import re

from .amlich import canchi_gio, canchi_ngay, jd_from_date, solar_to_lunar

# 12 chi theo thứ tự cột, kèm khung giờ hiển thị và giờ bắt đầu (Tý = 23h).
GIO_COLS = [
    ("Tý", "23h-1h", 23),
    ("Sửu", "1h-3h", 1),
    ("Dần", "3h-5h", 3),
    ("Mão", "5h-7h", 5),
    ("Thìn", "7h-9h", 7),
    ("Tỵ", "9h-11h", 9),
    ("Ngọ", "11h-13h", 11),
    ("Mùi", "13h-15h", 13),
    ("Thân", "15h-17h", 15),
    ("Dậu", "17h-19h", 17),
    ("Tuất", "19h-21h", 19),
    ("Hợi", "21h-23h", 21),
]

THU_VN = [
    "Thứ hai", "Thứ ba", "Thứ tư", "Thứ năm",
    "Thứ sáu", "Thứ bảy", "Chủ nhật",
]  # datetime.weekday(): Mon=0 .. Sun=6

_TABLE_RE = re.compile(r'id="example".*?</table>', re.S)
_ROW_RE = re.compile(r"<tr>(.*?)</tr>", re.S)
_TD_RE = re.compile(r"<td[^>]*>(.*?)</td>", re.S)
_TAG_RE = re.compile(r"<[^>]+>")


def hour_window(day_date, g):
    """(start, end) thực tế của một giờ.

    Giờ Tý (23h-1h) của một ngày bắt đầu từ 23h TỐI HÔM TRƯỚC đến 1h sáng ngày đó
    (theo lệ ngày bắt đầu từ giờ Tý). Các giờ còn lại nằm trong chính ngày đó.
    """
    if g["start_hour"] == 23:
        start = datetime.datetime.combine(
            day_date - datetime.timedelta(days=1), datetime.time(23))
    else:
        start = datetime.datetime.combine(day_date, datetime.time(g["start_hour"]))
    return start, start + datetime.timedelta(hours=2)

# Sửa lỗi chính tả từ nguồn site (ví dụ site ghi "Chu Tuớc" thay vì "Chu Tước").
_FIX = {
    "Chu Tuớc": "Chu Tước",
    "Đăng xà": "Đằng Xà",
}


def _parse_cell(td_html: str):
    """Tách 1 ô -> (que1, que2, luc_thu) hoặc None nếu không phải ô dữ liệu."""
    parts = re.split(r"<br\s*/?>", td_html, flags=re.I)
    vals = []
    for p in parts:
        text = _html.unescape(_TAG_RE.sub("", p)).strip()
        text = " ".join(text.split())
        text = _FIX.get(text, text)
        if text:
            vals.append(text)
    if len(vals) >= 3:
        return vals[0], vals[1], vals[2]
    return None


def parse_month(html_text: str, yy: int, mm: int):
    """Trả về list các ngày: mỗi ngày là dict {date, day, thu, gio: [...]}."""
    m = _TABLE_RE.search(html_text)
    segment = m.group(0) if m else html_text

    data_rows = []
    for row_html in _ROW_RE.findall(segment):
        cells = _TD_RE.findall(row_html)
        parsed = [_parse_cell(c) for c in cells]
        parsed = [p for p in parsed if p]
        if len(parsed) == 12:  # hàng ngày hợp lệ
            data_rows.append(parsed)

    days = []
    for i, cells in enumerate(data_rows):
        day_num = i + 1
        try:
            d = datetime.date(yy, mm, day_num)
        except ValueError:
            break  # vượt quá số ngày của tháng
        jd = jd_from_date(day_num, mm, yy)
        gio_list = []
        for col, (chi, khung, start_h) in enumerate(GIO_COLS):
            que1, que2, luc_thu = cells[col]
            gio_list.append({
                "chi": chi,
                "khung_gio": khung,
                "start_hour": start_h,
                "canchi": canchi_gio(jd, col),
                "que1": que1,
                "que2": que2,
                "luc_thu": luc_thu,
            })
        ld, lm, _ly, leap = solar_to_lunar(day_num, mm, yy)
        am = f"{ld}/{lm}" + (" nhuận" if leap else "")
        days.append({
            "date": d,
            "day": day_num,
            "thu": THU_VN[d.weekday()],
            "am": am,
            "canchi": canchi_ngay(jd),
            "gio": gio_list,
        })
    return days
