"""Chuẩn hoá tên quẻ / lục thú để so khớp.

Chỉ dùng NFC + viết hoa + gộp khoảng trắng. KHÔNG bỏ dấu thanh, vì trong
Kinh Dịch có những quẻ chỉ khác nhau ở dấu (ví dụ BÍ 賁 và BĨ 否) — bỏ dấu
sẽ gây nhầm. Danh sách tham chiếu đã được viết đúng chính tả theo nguồn site
nên chỉ cần chuẩn hoá hoa/thường là khớp.
"""

import unicodedata


def chuan_hoa(ten: str) -> str:
    ten = unicodedata.normalize("NFC", ten or "")
    ten = " ".join(ten.split())  # gộp mọi khoảng trắng thừa
    return ten.upper()
