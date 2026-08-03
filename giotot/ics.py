"""Xuất file lịch .ics (iCalendar) từ danh sách ngày giờ tốt.

Mỗi giờ tốt thành một sự kiện (VEVENT) giờ địa phương, kèm nhắc trước 10 phút.
Giờ Tý (23h-1h) kéo sang 1h sáng hôm sau.
"""

import datetime

from .parse import hour_window

TIER_LABEL = {"top1": "Top 1", "top2": "Top 2"}


def _esc(s: str) -> str:
    return (s.replace("\\", "\\\\").replace(";", "\\;")
             .replace(",", "\\,").replace("\n", "\\n"))


def _fold(line: str) -> str:
    """Gấp dòng theo chuẩn iCalendar (75 octet); tính theo byte UTF-8."""
    out = []
    raw = line.encode("utf-8")
    while len(raw) > 73:
        cut = 73
        while (raw[cut] & 0xC0) == 0x80:  # không cắt giữa ký tự UTF-8
            cut -= 1
        out.append(raw[:cut].decode("utf-8"))
        raw = b" " + raw[cut:]
    out.append(raw.decode("utf-8"))
    return "\r\n".join(out)


def _dt(t: datetime.datetime) -> str:
    return t.strftime("%Y%m%dT%H%M%S")


def _event(day, g, stamp):
    d = day["date"]
    start_dt, end_dt = hour_window(d, g)      # giờ Tý bắt đầu từ tối hôm trước
    start = _dt(start_dt)
    end = _dt(end_dt)
    uid = f"{d.isoformat()}-{g['chi']}-{g['start_hour']}@giotot"
    que = f"{g['que1']} - {g['que2']}"
    tier = TIER_LABEL.get(g["tier"], "")
    if g.get("huyen_vu"):
        summary = f"● {que} · hào Huyền Vũ ({tier})"
    else:
        summary = f"{que} ({tier})"
    desc_parts = [
        f"Ngày {day['canchi']} · giờ {g['canchi']}",
        f"Lục thú: {g['luc_thu']}",
        f"Loại ngày: {g['loai_ngay']} · {tier}",
    ]
    if g.get("huyen_vu"):
        desc_parts.append("Hào Huyền Vũ: không nên động, hợp cúng kiếng.")
    desc = "\n".join(desc_parts)
    return "\r\n".join(_fold(x) for x in [
        "BEGIN:VEVENT",
        f"UID:{uid}",
        f"DTSTAMP:{stamp}",
        f"DTSTART:{start}",
        f"DTEND:{end}",
        f"SUMMARY:{_esc(summary)}",
        f"DESCRIPTION:{_esc(desc)}",
        "BEGIN:VALARM",
        "TRIGGER:-PT10M",
        "ACTION:DISPLAY",
        f"DESCRIPTION:{_esc(summary)}",
        "END:VALARM",
        "END:VEVENT",
    ])


def build_ics(tieu_de: str, days) -> str:
    stamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Gio tot Dich ly//VI//",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        _fold("X-WR-CALNAME:" + _esc(tieu_de)),
    ]
    for day in days:
        for g in day["gio_tot"]:
            lines.append(_event(day, g, stamp))
    lines.append("END:VCALENDAR")
    return "\r\n".join(lines) + "\r\n"
