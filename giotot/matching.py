"""Lọc giờ tốt từ dữ liệu đã parse.

Quy tắc:
- Nếu cặp (quẻ1, quẻ2) khớp danh sách tham chiếu -> giờ tốt, kèm loại ngày + Top.
- Giờ có lục thú Huyền Vũ vẫn đưa vào nhưng gắn cờ 'huyen_vu' để bôi đen phân biệt.
"""

from .normalize import chuan_hoa
from .reference import LOOKUP

HUYEN_VU = chuan_hoa("Huyền Vũ")


def loc_gio_tot_ngay(ngay: dict):
    """Trả về list giờ tốt của 1 ngày (mỗi phần tử = 1 giờ kèm loai_ngay, tier)."""
    ket_qua = []
    for g in ngay["gio"]:
        key = (chuan_hoa(g["que1"]), chuan_hoa(g["que2"]))
        hit = LOOKUP.get(key)
        if hit:
            ket_qua.append({
                **g,
                "loai_ngay": hit["loai_ngay"],
                "tier": hit["tier"],
                "huyen_vu": chuan_hoa(g["luc_thu"]) == HUYEN_VU,
            })
    return ket_qua


def loc_thang(days):
    """Nhận list ngày (từ parse_month) -> list ngày kèm 'gio_tot' (chỉ ngày có ≥1 giờ)."""
    out = []
    for ngay in days:
        gio_tot = loc_gio_tot_ngay(ngay)
        if gio_tot:
            out.append({**ngay, "gio_tot": gio_tot})
    return out
