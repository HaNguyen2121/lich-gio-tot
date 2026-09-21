# Báo cáo hoàn thành — App Giờ tốt theo Dịch lý Việt Nam

_Cập nhật: 21/09/2026 · Repo: https://github.com/HaNguyen2121/lich-gio-tot_

Tài liệu ghi nhận toàn bộ **lỗi đã xử lý** (nguyên nhân + cách khắc phục) và **các
thay đổi/tính năng** của app từ lúc khởi tạo đến nay.

---

## 1. Tóm tắt

App web chạy **local** trên máy, giúp tra cứu **giờ tốt để động dụng** theo Dịch lý
Việt Nam. Người dùng chọn một khoảng ngày → xem danh sách ngày/giờ tốt (phân Top 1 / Top 2
bằng màu), kèm âm lịch, Can-Chi, và tooltip học Dịch (vạch hào, dịch tượng, lục thú).
Có thể **In/Lưu PDF** và **xuất lịch .ics**.

- Ngôn ngữ: **Python thuần thư viện chuẩn** (không cần cài gói ngoài).
- Nguồn dữ liệu quẻ theo giờ: `lich.vutrungu.com` (tự tải + cache vĩnh viễn).
- Chạy nền tự động: **launchd** (macOS) / **Task Scheduler** (Windows).
- Quy mô: ~1.700 dòng, 12 module trong `giotot/`.

---

## 2. Các lỗi đã xử lý

| # | Lỗi / hiện tượng | Nguyên nhân | Cách khắc phục |
|---|---|---|---|
| 1 | **HTTP 403** khi mở `127.0.0.1:5000` | Trên macOS cổng 5000 bị **AirPlay Receiver** chiếm | Đổi cổng mặc định sang **5057**; thêm cờ `--port` |
| 2 | `urllib` bị **chặn 403** khi tải vutrungu | Thiếu header User-Agent | Gửi `User-Agent` trong `fetch.py` |
| 3 | Sai tham số tháng (đổi `thang/nam` không có tác dụng) | URL thật dùng `yy`/`mm` | Dùng đúng `?yy=YYYY&mm=MM` |
| 4 | Sai chính tả lục thú: **"Chu Tuớc"**, **"Đăng xà"** | Lỗi từ chính nguồn site | Bảng sửa `parse._FIX` → "Chu Tước", "Đằng Xà" |
| 5 | Sai chính tả loại ngày: **"Hoả"/"Thuỷ"** | Đặt dấu kiểu cũ | Sửa thành **"Hỏa"/"Thủy"** trong `reference.py` |
| 6 | Bộ chọn tab hiện **cả 2 form** cùng lúc | CSS `form.row` đè `.hidden` (đặc thù cao hơn) | Thêm `.hidden { display:none !important }` |
| 7 | Định dạng ngày **lẫn `/` và `.`** | Header ngày dùng dấu `.` | Thống nhất **DD/MM/YYYY** toàn app |
| 8 | Giờ Tý (23h-1h) bị tính **nhầm sang ngày hiện tại** | 23h thực ra là **tối hôm trước** | `parse.hour_window()`: giờ Tý = 23h(hôm trước)→1h; dùng chung cho banner "sắp tới" & .ics |
| 9 | Bản in PDF hiện dấu hiệu "thời điểm" gây rối | Banner/HÔM NAY/highlight/gạch chân in ra | `@media print`: ẩn banner, nhãn HÔM NAY, highlight ngày & giờ sắp tới, bỏ gạch chân |
| 10 | Banner "sắp tới" **biến mất** khi xem ngày/tuần | Chỉ dò trong khoảng đang xem (đã qua) | `service.next_good_hour()` — luôn dò giờ kế tiếp thật sự từ hiện tại, độc lập khoảng xem |
| 11 | **ERR_EMPTY_RESPONSE** khi xem khoảng nhiều tháng | **Nhiều tiến trình server trùng** đọc/ghi cùng file cache + tranh ghi `.pyc` lúc khởi động → `OSError: Resource deadlock avoided` làm handler chết giữa chừng | (a) `fetch.py` ghi cache **atomic** (temp + `os.replace`) + **retry** khi đọc; (b) `server.py` **bọc handler bắt mọi lỗi** → luôn trả trang, không bao giờ rỗng; (c) **chặn tạo listener thứ 2** trên cùng cổng; (d) **precompile bytecode** trong script cài |

---

## 3. Các thay đổi / tính năng (theo commit)

| Commit | Ngày | Nội dung chính |
|---|---|---|
| `0d9d8f4` | 03/08 | **Khởi tạo app**: fetch + parse + khớp danh sách giờ tốt; nhóm theo ngày; Top 1 (đỏ)/Top 2 (xanh); In/PDF |
| `73bff42` | 04/08 | **Dịch vụ nền luôn bật** (LaunchAgent) + hướng dẫn quản lý |
| `1520396` | 04/08 | **Tooltip dịch tượng 64 quẻ** (rê chuột tên quẻ) — `dichtuong.py` |
| `4aec3c4` | 04/08 | Tooltip thêm **vạch hào**; thêm **tooltip lục thú**; bỏ gạch chân khi in |
| `71ec4fd` | 04/08 | **Lục thú mô tả đầy đủ** + ngũ hành + màu sắc |
| `e250168` | 04/08 | **INSTALL.md** + script cài/gỡ dịch vụ (macOS) |
| `a6588b0` | 04/08 | Hướng dẫn + script cài đặt cho **Windows** (Task Scheduler) |
| `8ec42c2` | 12/08 | Bổ sung giờ tốt **Thái-Nhu** (Địa/Top1) và **Bí-Di** (Sơn/Top2 — thêm loại Ngày Sơn) |
| `4259c91` | 21/09 | **Sửa lỗi ERR_EMPTY_RESPONSE** (xem mục lỗi #11) |

### Ngoài ra (các tinh chỉnh trong quá trình làm, gộp vào các commit trên)

- **Giao diện kết quả**: nút In đổi thành **icon máy in**; bỏ chữ "Top 1/Top 2" ở tag phải (chỉ phân biệt bằng màu); footer rút gọn chỉ còn dòng nguồn.
- **Chọn thời gian**: gộp "chọn ngày" + "chọn tháng" thành **một bộ chọn khoảng** (Từ ngày → Đến ngày; hỗ trợ 1 ngày / cả tháng / khoảng bất kỳ vắt nhiều tháng ≤ 1 năm; tự đảo nếu nhập ngược). Bỏ ô gõ tay. Thêm **nút nhanh**: Hôm nay · Tuần này · Tháng này · 30 ngày tới.
- **Hào Huyền Vũ**: trước loại bỏ → sau **giữ lại nhưng bôi đen** (nền tối), ghi chú *"không nên động, hợp cúng kiếng"*; dùng đúng thuật ngữ "hào".
- **Âm lịch + Can-Chi**: `amlich.py` tính offline (thuật toán Hồ Ngọc Đức); Can-Chi ngày (vd Mậu Thân) & giờ (Ngũ thử độn).
- **Banner "Giờ tốt sắp tới"** + tô sáng ngày hôm nay; bộ lọc **Ẩn hào Huyền Vũ**.
- **Xuất .ics**: mỗi giờ tốt = 1 sự kiện lịch, **nhắc trước 10 phút**.
- **Danh sách giờ tốt** giờ đủ **cả 8 loại ngày** (Thiên, Trạch, Hỏa, Lôi, Phong, Thủy, Địa, Sơn).
- **Vị trí project**: chuyển sang `~/Documents/Personal/Applications/Gio-tot-Dich-ly` và đưa lên **GitHub**.

---

## 4. Cấu trúc hiện tại

```
Gio-tot-Dich-ly/
  giotot/
    __main__.py   # python -m giotot
    server.py     # HTTP server (route /, /ket-qua, /lich.ics) + chặn double-instance
    fetch.py      # tải vutrungu + cache atomic + retry
    parse.py      # parse bảng quẻ; âm lịch; Can-Chi; hour_window (giờ Tý)
    reference.py  # 8 loại ngày, cặp quẻ Top 1/Top 2
    normalize.py  # chuẩn hoá tên quẻ (NFC+upper, KHÔNG bỏ dấu: BÍ ≠ BĨ)
    matching.py   # lọc giờ tốt; cờ Huyền Vũ
    amlich.py     # dương→âm lịch + Can-Chi (offline)
    dichtuong.py  # dịch tượng 64 quẻ (+ hào) + 6 lục thú
    service.py    # tra_cuu_range, next_good_hour
    ics.py        # sinh file .ics
    render.py     # HTML/CSS/JS (trang chủ + kết quả + tooltip)
  deploy/         # script cài/gỡ dịch vụ (macOS .sh, Windows .ps1) + plist mẫu
  cache/          # HTML tháng đã tải (không đưa lên git)
  README.md · INSTALL.md · DEVELOPMENT.md · COMPLETION_REPORT.md
```

**Chạy:** `python3 -m giotot` (thủ công) hoặc dịch vụ nền → `http://127.0.0.1:5057`.

---

## 5. Nguyên tắc thiết kế then chốt (đã kiểm chứng)

- **Loại ngày mã hoá trong cặp quẻ**: quẻ đầu mỗi giờ trong 1 ngày có chung quái thượng
  → chỉ cần khớp **cặp quẻ có thứ tự** là suy ra đúng loại ngày. Đã kiểm 194 ngày:
  0 vi phạm "mỗi ngày một loại ngày".
- **So khớp không bỏ dấu thanh** (BÍ 賁 ≠ BĨ 否).
- **Màn hình ≠ bản in**: bản in loại bỏ mọi dấu hiệu "thời điểm hiện tại" để lưu dài hạn.
- **Bền bỉ**: cache atomic + retry + handler bắt-mọi-lỗi → không còn trắng trang.

---

## 6. Hạn chế & hướng mở rộng

- Chỉ có **dịch vụ nền tự động** trên macOS/Windows (Linux chạy thủ công được).
- Phụ thuộc `vutrungu.com` cho **lần tải đầu mỗi tháng** (sau đó dùng cache).
- Mô tả lục thú/dịch tượng lấy theo nguồn — có thể mở rộng chi tiết hơn khi cần.
- Ý tưởng tương lai: xem trên điện thoại tiện hơn (hiện dùng LAN), diễn giải "nên động
  dụng việc gì" cho từng cặp quẻ.

---

_Chi tiết quá trình phát triển: [DEVELOPMENT.md](DEVELOPMENT.md) · Cài đặt: [INSTALL.md](INSTALL.md) · Sử dụng: [README.md](README.md)._
