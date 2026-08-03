"""Đổi ngày dương -> ngày âm lịch (thuật toán Âm lịch Việt Nam của Hồ Ngọc Đức).

Thuần thư viện chuẩn, tính trực tiếp bằng thiên văn nên không cần bảng tra.
Múi giờ Việt Nam = +7.
"""

import math

TZ_VN = 7

CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi",
       "Thân", "Dậu", "Tuất", "Hợi"]


def canchi_ngay(jd: int) -> str:
    """Can-Chi của ngày theo số Julian day."""
    return CAN[(jd + 9) % 10] + " " + CHI[(jd + 1) % 12]


def canchi_gio(jd: int, chi_index: int) -> str:
    """Can-Chi của giờ (chi_index 0=Tý .. 11=Hợi), theo quy tắc Ngũ thử độn."""
    can = CAN[((jd - 1) * 2 + chi_index) % 10]
    return can + " " + CHI[chi_index]


def jd_from_date(dd, mm, yy):
    a = (14 - mm) // 12
    y = yy + 4800 - a
    m = mm + 12 * a - 3
    jd = dd + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
    if jd < 2299161:
        jd = dd + (153 * m + 2) // 5 + 365 * y + y // 4 - 32083
    return jd


def _new_moon_day(k, tz):
    T = k / 1236.85
    T2 = T * T
    T3 = T2 * T
    dr = math.pi / 180
    Jd1 = 2415020.75933 + 29.53058868 * k + 0.0001178 * T2 - 0.000000155 * T3
    Jd1 += 0.00033 * math.sin((166.56 + 132.87 * T - 0.009173 * T2) * dr)
    M = 359.2242 + 29.10535608 * k - 0.0000333 * T2 - 0.00000347 * T3
    Mpr = 306.0253 + 385.81691806 * k + 0.0107306 * T2 + 0.00001236 * T3
    F = 21.2964 + 390.67050646 * k - 0.0016528 * T2 - 0.00000239 * T3
    C1 = (0.1734 - 0.000393 * T) * math.sin(M * dr) + 0.0021 * math.sin(2 * dr * M)
    C1 = C1 - 0.4068 * math.sin(Mpr * dr) + 0.0161 * math.sin(2 * dr * Mpr)
    C1 = C1 - 0.0004 * math.sin(3 * dr * Mpr)
    C1 = C1 + 0.0104 * math.sin(2 * dr * F) - 0.0051 * math.sin((M + Mpr) * dr)
    C1 = C1 - 0.0074 * math.sin((M - Mpr) * dr) + 0.0004 * math.sin((2 * F + M) * dr)
    C1 = C1 - 0.0004 * math.sin((2 * F - M) * dr) - 0.0006 * math.sin((2 * F + Mpr) * dr)
    C1 = C1 + 0.0010 * math.sin((2 * F - Mpr) * dr) + 0.0005 * math.sin((2 * Mpr + M) * dr)
    if T < -11:
        deltat = 0.001 + 0.000839 * T + 0.0002261 * T2 - 0.00000845 * T3 - 0.000000081 * T * T3
    else:
        deltat = -0.000278 + 0.000265 * T + 0.000262 * T2
    JdNew = Jd1 + C1 - deltat
    return int(JdNew + 0.5 + tz / 24)


def _sun_longitude(jdn, tz):
    T = (jdn - 2451545.5 - tz / 24) / 36525
    T2 = T * T
    dr = math.pi / 180
    M = 357.52910 + 35999.05030 * T - 0.0001559 * T2 - 0.00000048 * T * T2
    L0 = 280.46645 + 36000.76983 * T + 0.0003032 * T2
    DL = (1.914600 - 0.004817 * T - 0.000014 * T2) * math.sin(dr * M)
    DL = DL + (0.019993 - 0.000101 * T) * math.sin(dr * 2 * M) + 0.000290 * math.sin(dr * 3 * M)
    L = L0 + DL
    L = L * dr
    L = L - math.pi * 2 * int(L / (math.pi * 2))
    return int(L / math.pi * 6)


def _lunar_month_11(yy, tz):
    off = jd_from_date(31, 12, yy) - 2415021
    k = int(off / 29.530588853)
    nm = _new_moon_day(k, tz)
    if _sun_longitude(nm, tz) >= 9:
        nm = _new_moon_day(k - 1, tz)
    return nm


def _leap_month_offset(a11, tz):
    k = int((a11 - 2415021.076998695) / 29.530588853 + 0.5)
    i = 1
    arc = _sun_longitude(_new_moon_day(k + i, tz), tz)
    while True:
        last = arc
        i += 1
        arc = _sun_longitude(_new_moon_day(k + i, tz), tz)
        if not (arc != last and i < 14):
            break
    return i - 1


def solar_to_lunar(dd, mm, yy, tz=TZ_VN):
    """Trả về (lunar_day, lunar_month, lunar_year, is_leap)."""
    day_number = jd_from_date(dd, mm, yy)
    k = int((day_number - 2415021.076998695) / 29.530588853)
    month_start = _new_moon_day(k + 1, tz)
    if month_start > day_number:
        month_start = _new_moon_day(k, tz)
    a11 = _lunar_month_11(yy, tz)
    b11 = a11
    if a11 >= month_start:
        lunar_year = yy
        a11 = _lunar_month_11(yy - 1, tz)
    else:
        lunar_year = yy + 1
        b11 = _lunar_month_11(yy + 1, tz)
    lunar_day = day_number - month_start + 1
    diff = (month_start - a11) // 29
    lunar_leap = 0
    lunar_month = diff + 11
    if b11 - a11 > 365:
        leap_off = _leap_month_offset(a11, tz)
        if diff >= leap_off:
            lunar_month = diff + 10
            if diff == leap_off:
                lunar_leap = 1
    if lunar_month > 12:
        lunar_month -= 12
    if lunar_month >= 11 and diff < 4:
        lunar_year -= 1
    return (lunar_day, lunar_month, lunar_year, lunar_leap)
