"""Sinh HTML cho form nhập và trang kết quả (không dùng thư viện ngoài)."""

import calendar
import datetime
import html
import json

from .dichtuong import DICH_TUONG
from .normalize import chuan_hoa
from .parse import THU_VN

_CSS = """
:root { --top1:#c62828; --top2:#1565c0; }
* { box-sizing: border-box; }
body { font-family: -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
       margin: 0; background:#f4f6f8; color:#1a1a1a; }
.wrap { max-width: 860px; margin: 0 auto; padding: 24px 18px 60px; }
h1 { font-size: 22px; margin: 0 0 4px; }
.sub { color:#607d8b; font-size:13px; margin-bottom:20px; }
.card { background:#fff; border:1px solid #e0e4e8; border-radius:12px; padding:18px; }
form.row { display:flex; gap:10px; flex-wrap:wrap; align-items:flex-end; margin:0; }
label { display:block; font-size:12px; color:#546e7a; margin-bottom:6px; font-weight:600; }
input[type=text], input[type=month], input[type=date] {
       font-size:16px; padding:10px 12px; border:1px solid #cfd8dc;
       border-radius:8px; width:220px; background:#fff; color:#1a1a1a; }
.mode-tabs { display:flex; gap:6px; margin-bottom:16px; background:#eceff1;
       padding:4px; border-radius:10px; width:fit-content; }
.mode-tab { background:transparent; color:#546e7a; padding:7px 18px; border-radius:7px;
       font-size:14px; }
.mode-tab.active { background:#fff; color:#13a923; box-shadow:0 1px 3px rgba(0,0,0,.12); }
.hidden { display:none !important; }
.divider { border:0; border-top:1px solid #eceff1; margin:16px 0; }
.tay { font-size:12px; color:#90a4ae; }
button { font-size:15px; font-weight:600; padding:10px 18px; border:0; border-radius:8px;
       background:#13a923; color:#fff; cursor:pointer; }
button.secondary { background:#455a64; }
.icon-btn { width:40px; height:40px; padding:0; border-radius:8px; background:#455a64;
       color:#fff; display:inline-flex; align-items:center; justify-content:center;
       cursor:pointer; }
.icon-btn:hover { background:#37474f; }
.icon-btn svg { width:20px; height:20px; }
.hint { font-size:12px; color:#78909c; margin-top:10px; }
.legend { display:flex; gap:14px; flex-wrap:wrap; margin:18px 0; font-size:13px; }
.badge { display:inline-block; padding:2px 9px; border-radius:20px; color:#fff;
       font-size:12px; font-weight:700; }
.badge.top1 { background:var(--top1); }
.badge.top2 { background:var(--top2); }
.day { background:#fff; border:1px solid #e0e4e8; border-radius:12px;
       margin:14px 0; overflow:hidden; }
.day > .head { background:#e8f5e9; padding:11px 16px; font-weight:700; font-size:15px;
       border-bottom:1px solid #d7e6d9; }
.day > .head .lunar { color:#607d8b; font-weight:500; font-size:13px; }
.gio { padding:9px 16px; border-bottom:1px solid #f0f2f4; display:flex;
       gap:12px; align-items:baseline; }
.gio:last-child { border-bottom:0; }
.gio .time { font-weight:700; min-width:78px; }
.gio.top1 .time { color:var(--top1); }
.gio.top2 .time { color:var(--top2); }
.gio .que { flex:1; font-size:15px; }
.gio .luc { color:#78909c; font-size:13px; }
.gio .tag { font-size:11px; color:#90a4ae; }
/* Giờ có lục thú Huyền Vũ: bôi đen (nền tối) để dễ nhận biết */
.gio.hv { background:#263238; }
.gio.hv .que { color:#eceff1; }
.gio.hv .luc { color:#ffab91; }
.gio.hv .tag { color:#b0bec5; }
.gio.hv.top1 .time { color:#ff8a80; }
.gio.hv.top2 .time { color:#82b1ff; }
.empty { background:#fff; border:1px dashed #cfd8dc; border-radius:12px;
       padding:26px; text-align:center; color:#78909c; }
.note { font-size:12px; color:#90a4ae; margin-top:18px; line-height:1.6; }
.toolbar { display:flex; gap:10px; margin:6px 0 4px; align-items:center; }
a.back { color:#455a64; text-decoration:none; font-size:14px; align-self:center; }
a.btn-sm { text-decoration:none; font-size:13px; font-weight:600; color:#fff;
       background:#455a64; padding:8px 12px; border-radius:8px; }
a.btn-sm:hover { background:#37474f; }
/* Banner "giờ tốt sắp tới" */
.banner { background:#13a923; color:#fff; border-radius:10px; padding:11px 16px;
       margin:14px 0 4px; font-size:15px; }
.banner .lbl { font-weight:700; background:rgba(255,255,255,.22);
       padding:2px 9px; border-radius:20px; margin-right:8px; }
.banner-muted { background:#eceff1; color:#607d8b; font-size:14px; }
/* Bộ lọc */
.filters { display:flex; gap:18px; margin:10px 0 2px; font-size:14px; color:#455a64; }
.filters label { font-weight:500; cursor:pointer; }
.filters input { vertical-align:middle; margin-right:5px; }
/* Ngày hôm nay + giờ sắp tới */
.day.today { border-color:#13a923; box-shadow:0 0 0 2px rgba(19,169,35,.18); }
.day.today > .head { background:#d7f2da; }
.today-tag { background:#13a923; color:#fff; font-size:10px; font-weight:700;
       padding:2px 7px; border-radius:20px; margin-left:6px; vertical-align:middle; }
.gio.next { box-shadow:inset 3px 0 0 #13a923; }
.gio.next.hv { box-shadow:inset 3px 0 0 #7CFC98; }
/* Tooltip dịch tượng (rê chuột vào tên quẻ) */
.qn { border-bottom:1px dotted currentColor; cursor:help; }
#tip { position:fixed; z-index:9999; max-width:340px; background:#263238; color:#eceff1;
       padding:11px 13px; border-radius:9px; font-size:13px; line-height:1.55;
       box-shadow:0 8px 28px rgba(0,0,0,.32); display:none; pointer-events:none; }
#tip .tip-ten { font-weight:700; color:#ffd54f; margin-bottom:5px; }
#tip .tip-ct { font-style:italic; color:#b0bec5; margin-bottom:5px; }

@media print {
  body { background:#fff; }
  .no-print { display:none !important; }
  .wrap { max-width:none; padding:0; }
  .day { break-inside: avoid; border-color:#ccc; }
  .day > .head { background:#eee !important; }
  /* Bản in dài hạn: bỏ mọi dấu hiệu "hôm nay" / "giờ sắp tới" để tránh nhầm về sau */
  .day.today { border-color:#ccc !important; box-shadow:none !important; }
  .day.today > .head { background:#eee !important; }
  .gio.next { box-shadow:none !important; }
  .badge, .gio.top1 .time, .gio.top2 .time, .gio.hv, .swatch,
  .banner, .day.today > .head, .today-tag {
       -webkit-print-color-adjust:exact; print-color-adjust:exact; }
}
.swatch { display:inline-block; width:26px; height:14px; border-radius:4px;
       background:#263238; vertical-align:middle; }
.chips { display:flex; gap:8px; flex-wrap:wrap; margin-bottom:16px; }
.chip { text-decoration:none; font-size:13px; font-weight:600; color:#13a923;
       border:1px solid #b7e0bd; background:#f1faf2; padding:7px 14px; border-radius:20px; }
.chip:hover { background:#13a923; color:#fff; border-color:#13a923; }
"""


def _esc(s):
    return html.escape(str(s))


def page(title, body):
    return f"""<!doctype html>
<html lang="vi"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_esc(title)}</title>
<style>{_CSS}</style>
</head><body><div class="wrap">{body}</div></body></html>"""


def _quick_links(today):
    iso = lambda d: d.strftime("%Y-%m-%d")
    mon = today - datetime.timedelta(days=today.weekday())     # thứ 2 tuần này
    sun = mon + datetime.timedelta(days=6)
    first = today.replace(day=1)
    last = today.replace(day=calendar.monthrange(today.year, today.month)[1])
    presets = [
        ("Hôm nay", today, today),
        ("Tuần này", mon, sun),
        ("Tháng này", first, last),
        ("30 ngày tới", today, today + datetime.timedelta(days=29)),
    ]
    return "".join(
        f'<a class="chip" href="/ket-qua?tu={iso(a)}&den={iso(b)}">{lbl}</a>'
        for lbl, a, b in presets
    )


def render_index(error=None):
    err = f'<div class="hint" style="color:#c62828">{_esc(error)}</div>' if error else ""
    today = datetime.date.today()
    first = today.replace(day=1).strftime("%Y-%m-%d")
    last_day = calendar.monthrange(today.year, today.month)[1]
    last = today.replace(day=last_day).strftime("%Y-%m-%d")
    body = f"""
<h1>Giờ tốt theo Dịch lý Việt Nam</h1>
<div class="sub">Chọn khoảng ngày để xem các giờ có thể động dụng.</div>
<div class="card">
  <div class="chips">{_quick_links(today)}</div>
  <form class="row" action="/ket-qua" method="get">
    <div>
      <label>Từ ngày</label>
      <input type="date" name="tu" value="{first}">
    </div>
    <div>
      <label>Đến ngày</label>
      <input type="date" name="den" value="{last}">
    </div>
    <button type="submit">Xem</button>
  </form>
  <div class="hint" style="margin-top:12px">
    • Xem <b>1 ngày</b>: để <i>Từ ngày</i> = <i>Đến ngày</i>.<br>
    • Xem <b>cả tháng</b>: chọn từ ngày 1 đến ngày cuối tháng (đang điền sẵn).<br>
    • Hoặc chọn một khoảng bất kỳ (tối đa 1 năm).
  </div>
</div>
{err}
<div class="legend" style="margin-top:26px">
  <span><span class="badge top1">Top 1</span> ưu tiên cao</span>
  <span><span class="badge top2">Top 2</span> ưu tiên vừa</span>
  <span><span class="swatch"></span> hào Huyền Vũ · không nên động, hợp cúng kiếng</span>
</div>
"""
    return page("Giờ tốt Dịch lý", body)


def _que_span(ten):
    """Tên quẻ có gạch chân chấm; rê chuột hiện dịch tượng (nếu có dữ liệu)."""
    key = chuan_hoa(ten)
    tip = ' class="qn"' if key in DICH_TUONG else ""
    return f'<span data-que="{_esc(key)}"{tip}>{_esc(ten)}</span>'


def _render_gio(g, next_key=None, day_key=None):
    cls = g["tier"] + (" hv" if g.get("huyen_vu") else "")
    if next_key and day_key and f"{day_key}|{g['chi']}" == next_key:
        cls += " next"
    que = f'{_que_span(g["que1"])} – {_que_span(g["que2"])}'
    return f"""<div class="gio {cls}">
  <span class="time">{_esc(g['khung_gio'])}</span>
  <span class="que">{que}
       <span class="luc">· {_esc(g['luc_thu'])}</span></span>
  <span class="tag">{_esc(g['canchi'])} · Ngày {_esc(g['loai_ngay'])}</span>
</div>"""


def _render_day(ngay, today=None, next_key=None):
    d = ngay["date"]
    day_key = d.isoformat()
    cls = "day" + (" today" if today and d == today else "")
    hom_nay = ' <span class="today-tag no-print">HÔM NAY</span>' if today and d == today else ""
    head = (f'{_esc(ngay["thu"])}, {d.day:02d}/{d.month:02d}/{d.year}'
            f' <span class="lunar">· ÂL {_esc(ngay["am"])} · {_esc(ngay["canchi"])}</span>'
            f'{hom_nay}')
    gios = "".join(_render_gio(g, next_key, day_key) for g in ngay["gio_tot"])
    return f'<div class="{cls}"><div class="head">{head}</div>{gios}</div>'


def _banner(nxt):
    if not nxt:
        return ('<div class="banner banner-muted no-print">'
                'Trong khoảng đã chọn không còn giờ tốt nào sắp tới.</div>')
    _key, start, g, dang = nxt
    tier = "Top 1" if g["tier"] == "top1" else "Top 2"
    que = f'{_esc(g["que1"])} – {_esc(g["que2"])}'
    khi = "Đang trong giờ tốt" if dang else "Giờ tốt sắp tới"
    # Dùng ngày thực của giờ (giờ Tý rơi vào tối hôm trước) để tránh nhầm.
    when = (f'{_esc(THU_VN[start.weekday()])} {start.day:02d}/{start.month:02d}'
            f' · {_esc(g["khung_gio"])}')
    hv = ' <b>· hào Huyền Vũ (không nên động, hợp cúng kiếng)</b>' if g.get("huyen_vu") else ""
    return (f'<div class="banner no-print"><span class="lbl">{khi}</span> '
            f'{when} · {que} · {tier}{hv}</div>')


def render_results(tieu_de, filtered_days, ics_query="", nxt=None):
    today = datetime.date.today()
    next_key = nxt[0] if nxt else None

    ics_href = "/lich.ics?" + ics_query if ics_query else "/lich.ics"
    toolbar = f"""
<div class="toolbar no-print">
  <a class="back" href="/">← Tra cứu khác</a>
  <a class="btn-sm" href="{_esc(ics_href)}">📅 Xuất lịch .ics</a>
  <button class="icon-btn" onclick="window.print()" title="In / Lưu PDF"
          aria-label="In / Lưu PDF">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round">
      <polyline points="6 9 6 2 18 2 18 9"></polyline>
      <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
      <rect x="6" y="14" width="12" height="8"></rect>
    </svg>
  </button>
</div>"""
    filters = """
<div class="filters no-print">
  <label><input type="checkbox" id="f-hidehv"> Ẩn hào Huyền Vũ</label>
</div>"""
    legend = """
<div class="legend">
  <span><span class="badge top1">Top 1</span> ưu tiên cao</span>
  <span><span class="badge top2">Top 2</span> ưu tiên vừa</span>
  <span><span class="swatch"></span> hào Huyền Vũ · không nên động, hợp cúng kiếng</span>
</div>"""
    if filtered_days:
        days_html = "".join(_render_day(n, today, next_key) for n in filtered_days)
    else:
        days_html = ('<div class="empty">Không có giờ tốt nào phù hợp danh sách '
                     'trong khoảng đã chọn.</div>')
    note = """
<div class="note">Nguồn quẻ theo giờ: lich.vutrungu.com.</div>"""
    script = """
<script>
  function applyFilters() {
    var hidehv = document.getElementById('f-hidehv').checked;
    document.querySelectorAll('.day').forEach(function(day) {
      var visible = 0;
      day.querySelectorAll('.gio').forEach(function(g) {
        var hide = hidehv && g.classList.contains('hv');
        g.style.display = hide ? 'none' : '';
        if (!hide) visible++;
      });
      day.style.display = visible ? '' : 'none';
    });
  }
  document.getElementById('f-hidehv').addEventListener('change', applyFilters);

  // Tooltip dịch tượng
  var DICHTUONG = __TIPDATA__;
  var tip = document.getElementById('tip');
  function moveTip(x, y) {
    var w = tip.offsetWidth, h = tip.offsetHeight;
    var nx = x + 14, ny = y + 16;
    if (nx + w > window.innerWidth - 8) nx = x - w - 14;
    if (ny + h > window.innerHeight - 8) ny = y - h - 16;
    tip.style.left = Math.max(8, nx) + 'px';
    tip.style.top = Math.max(8, ny) + 'px';
  }
  document.addEventListener('mouseover', function(e) {
    var el = e.target.closest ? e.target.closest('.qn') : null;
    if (!el) return;
    var d = DICHTUONG[el.getAttribute('data-que')];
    if (!d) return;
    tip.innerHTML = '<div class="tip-ten"></div><div class="tip-ct"></div><div class="tip-yn"></div>';
    tip.querySelector('.tip-ten').textContent = d.ten;
    tip.querySelector('.tip-ct').textContent = d.chi_tuong;
    tip.querySelector('.tip-yn').textContent = d.y_nghia;
    tip.style.display = 'block';
    moveTip(e.clientX, e.clientY);
  });
  document.addEventListener('mousemove', function(e) {
    if (tip.style.display !== 'block') return;
    var el = e.target.closest ? e.target.closest('.qn') : null;
    if (el) moveTip(e.clientX, e.clientY); else tip.style.display = 'none';
  });
  document.addEventListener('mouseout', function(e) {
    if (e.target.closest && e.target.closest('.qn')) tip.style.display = 'none';
  });
</script>""".replace("__TIPDATA__", json.dumps(DICH_TUONG, ensure_ascii=False))
    body = f"""
<h1>{_esc(tieu_de)}</h1>
{toolbar}
{_banner(nxt)}
{filters}
{legend}
{days_html}
{note}
<div id="tip" class="no-print"></div>
{script}
"""
    return page(tieu_de, body)
