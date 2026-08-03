"""Bảng giờ tốt theo Dịch lý Việt Nam.

Phân theo 7 loại ngày (Thiên, Trạch, Hỏa, Lôi, Phong, Thủy, Địa). Mỗi loại có
các cặp quẻ CÓ THỨ TỰ (quẻ1 - quẻ2) xếp Top 1 / Top 2.

Lưu ý: cặp có thứ tự — "Lý - Trung Phu" (ngày Thiên) khác "Trung Phu - Lý"
(ngày Phong). Nhờ vậy chỉ cần so khớp cặp quẻ là biết đúng loại ngày, không cần
tự tính loại ngày theo lý thuyết Dịch.

Tên quẻ viết theo đúng chính tả nguồn lich.vutrungu.com (vd "Tụy", "Chu Tuớc").
Thiếu Ngày Sơn/Núi: nếu sau này có dữ liệu, thêm mục "Sơn" vào REFERENCE.
"""

from .normalize import chuan_hoa

# loai_ngay -> {"top1": [(que1, que2), ...], "top2": [...]}
REFERENCE = {
    "Thiên": {
        "top1": [
            ("Thuần Kiền", "Lý"),
            ("Thuần Kiền", "Đại Hữu"),
            ("Lý", "Trung Phu"),
        ],
        "top2": [
            ("Lý", "Thuần Đoài"),
        ],
    },
    "Trạch": {
        "top1": [
            ("Hàm", "Tụy"),
            ("Tụy", "Tỷ"),
        ],
        "top2": [
            ("Thuần Đoài", "Lý"),
        ],
    },
    "Hỏa": {
        "top1": [
            ("Đại Hữu", "Đỉnh"),
            ("Đại Hữu", "Thuần Kiền"),
            ("Đỉnh", "Đại Hữu"),
        ],
        "top2": [],
    },
    "Lôi": {
        "top1": [
            ("Đại Tráng", "Hằng"),
            ("Phong", "Thuần Chấn"),
            ("Hằng", "Đại Tráng"),
        ],
        "top2": [],
    },
    "Phong": {
        "top1": [
            ("Trung Phu", "Ích"),
            ("Trung Phu", "Lý"),
            ("Gia Nhân", "Tiệm"),
            ("Gia Nhân", "Ích"),
            ("Ích", "Trung Phu"),
        ],
        "top2": [
            ("Tiệm", "Gia Nhân"),
        ],
    },
    "Thủy": {
        "top1": [
            ("Nhu", "Thái"),
            ("Tỷ", "Tụy"),
        ],
        "top2": [],
    },
    "Địa": {
        "top1": [
            ("Sư", "Thuần Khôn"),
            ("Thuần Khôn", "Sư"),
            ("Thái", "Lâm"),
        ],
        "top2": [
            ("Thăng", "Sư"),
            ("Thái", "Thăng"),
            ("Thăng", "Thái"),
        ],
    },
}


def _build_lookup():
    """Tạo lookup phẳng: (que1_chuan, que2_chuan) -> {loai_ngay, tier}."""
    lookup = {}
    for loai_ngay, tiers in REFERENCE.items():
        for tier in ("top1", "top2"):
            for que1, que2 in tiers.get(tier, []):
                key = (chuan_hoa(que1), chuan_hoa(que2))
                lookup[key] = {"loai_ngay": loai_ngay, "tier": tier}
    return lookup


LOOKUP = _build_lookup()
