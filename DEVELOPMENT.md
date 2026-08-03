# Nhật ký phát triển — App Giờ tốt theo Dịch lý Việt Nam

Tài liệu ghi lại quá trình xây dựng app: bài toán, cách khảo sát nguồn dữ liệu,
các phát hiện cốt lõi, quyết định kiến trúc, và lịch sử tiến hoá tính năng.

---

## 1. Bài toán

Người dùng có sẵn **danh sách giờ tốt cố định** theo Dịch lý Việt Nam, phân theo 7 loại
ngày (Thiên, Trạch, Hỏa, Lôi, Phong, Thủy, Địa), mỗi loại gồm các **cặp quẻ** xếp
**Top 1 / Top 2**. Nguồn lịch quẻ theo giờ là trang `lich.vutrungu.com/xemthang`.

Yêu cầu: một app cho phép **chọn ngày/khoảng ngày** → ra danh sách ngày–giờ "động dụng",
phân biệt Top 1/Top 2 bằng màu, **loại trừ / đánh dấu** giờ có hào Huyền Vũ, và **xuất PDF**
để lưu lại.

---

## 2. Khảo sát nguồn dữ liệu (bước quyết định)

Trước khi viết code, khảo sát `lich.vutrungu.com` bằng trình duyệt + curl. Các phát hiện:

1. **Tham số URL đúng** để chọn tháng là `?yy=YYYY&mm=MM` — KHÔNG phải `thang/nam`
   (thử `thang/nam` thấy trang không đổi tháng nên suýt hiểu nhầm là không có API).
2. **Bảng quẻ `<table id="example">` được server render sẵn** trong HTML tĩnh
   (không phải JS dựng ở client). File `amlich-hnd-thang.js` trên site chỉ là thư viện
   âm lịch của Hồ Ngọc Đức, phần vòng lặp dựng bảng bị comment — tức bảng quẻ đến từ
   server. ⇒ Chỉ cần **fetch + parse HTML**, không cần chạy JavaScript.
3. **Phải gửi `User-Agent`** khi fetch, nếu không bị chặn **HTTP 403** (curl mặc định OK
   nhưng `urllib` thì bị chặn).
4. **Cấu trúc bảng**: mỗi `<tr>` dữ liệu = 1 ngày; 12 `<td>` = 12 khung giờ (Tý→Hợi);
   mỗi ô có 3 dòng ngăn bởi `<br>`: `QUẺ1 / QUẺ2 / Lục thú`. Xác nhận 1 tháng = 31×12 = 372 ô.

Kết luận: bám vào HTML server-render là con đường ổn định nhất (thay vì reverse-engineer
thuật toán sinh quẻ).

---

## 3. Phát hiện cốt lõi: loại ngày được "mã hoá" trong cặp quẻ

Vấn đề: site **không ghi loại ngày** (chỉ ghi Can-Chi, vd "Mậu Thân"). Vậy làm sao biết
áp danh sách con nào (Thiên/Trạch/...) cho mỗi ngày?

Phát hiện: **quẻ đầu của mọi giờ trong một ngày đều có chung quái thượng**. Ví dụ ngày
02/08/2026, quẻ đầu các giờ đều thuộc quái thượng Kiền (Lý, Đồng Nhân, Vô Vọng, Cấu, Tụng,
Độn, Bĩ, Thuần Kiền) ⇒ đó là **Ngày Thiên**.

Hệ quả quan trọng: **cặp quẻ có thứ tự** (`quẻ1 - quẻ2`) đã tự mã hoá loại ngày. Ví dụ
"Lý - Trung Phu" chỉ xuất hiện vào ngày Thiên, còn "Trung Phu - Lý" (đảo lại) thuộc ngày
Phong. ⇒ Chỉ cần **so khớp cặp quẻ có thứ tự** với danh sách tham chiếu là suy ra đúng
loại ngày + Top, **không cần tự tính loại ngày theo lý thuyết Dịch**.

**Kiểm chứng**: viết script kiểm bất biến "mọi giờ tốt trong cùng 1 ngày phải cùng 1 loại
ngày" trên **194 ngày (9 tháng)** → **0 vi phạm**. Thiết kế so khớp theo cặp là chính xác.

---

## 4. Quyết định kiến trúc

| Quyết định | Lý do |
|---|---|
| **Web app chạy local** (thay vì trang tĩnh deploy) | Backend tự fetch vutrungu ⇒ né CORS; hợp với nhu cầu cá nhân |
| **Thuần thư viện chuẩn Python** (`http.server` + `urllib`), KHÔNG dùng Flask/requests | Máy chưa cài Flask; giữ "cài đặt bằng 0" — chạy `python3 -m giotot` là xong |
| **Parse bằng regex**, bỏ BeautifulSoup | Cấu trúc bảng đơn giản, ổn định; giảm phụ thuộc |
| **Cache HTML vĩnh viễn** vào `cache/YYYY-MM.html` | Dữ liệu Dịch cố định theo ngày; chạy được cả khi mất mạng/site sập |
| **Cổng mặc định 5057** | Trên macOS cổng 5000 bị **AirPlay Receiver** chiếm → trả HTTP 403 |
| **Xuất PDF bằng Print của trình duyệt** (không sinh PDF phía server) | Đơn giản, giữ nguyên màu, không cần thư viện in |

---

## 5. Cấu trúc module (`giotot/`)

| File | Vai trò |
|---|---|
| `__main__.py` | Điểm chạy `python -m giotot`: parse cờ, mở trình duyệt, khởi động server |
| `server.py` | HTTP server (`http.server`); route `/`, `/ket-qua`, `/lich.ics`, `/favicon.ico` |
| `fetch.py` | Tải HTML tháng từ vutrungu (kèm `User-Agent`), cache ra file |
| `parse.py` | Parse `#example` → cấu trúc ngày/giờ; tính âm lịch + can-chi; `hour_window()` (mốc giờ thực); `_FIX` sửa chính tả lục thú |
| `reference.py` | Bảng giờ tốt của người dùng (7 loại ngày, cặp quẻ Top 1/Top 2) → lookup phẳng |
| `normalize.py` | Chuẩn hoá tên quẻ để so khớp (NFC + upper, **không** bỏ dấu) |
| `matching.py` | Lọc giờ tốt: khớp cặp quẻ; gắn cờ `huyen_vu` |
| `amlich.py` | Đổi dương→âm lịch + Can-Chi (thuật toán Hồ Ngọc Đức, thuần thiên văn) |
| `service.py` | Ghép luồng: `tra_cuu_range()`, `next_good_hour()`, phân tích input, đặt tiêu đề |
| `ics.py` | Sinh file `.ics` (iCalendar) từ danh sách giờ tốt |
| `render.py` | Sinh toàn bộ HTML/CSS/JS (trang chủ + trang kết quả) |

Luồng xử lý một truy vấn:
`server` → `service.tra_cuu_range` → `fetch` → `parse` → `matching` → `render` → HTML.

---

## 6. Những xử lý dữ liệu đặc thù (và lý do)

- **Chuẩn hoá khớp tên quẻ = NFC + viết hoa, KHÔNG bỏ dấu thanh.** Vì trong 64 quẻ có
  những quẻ chỉ khác nhau ở dấu (ví dụ **BÍ** 賁 và **BĨ** 否) — bỏ dấu sẽ gây khớp nhầm.
  Danh sách tham chiếu được viết đúng chính tả theo site (vd dùng "Tụy" khớp "TỤY").
- **Sửa lỗi chính tả lục thú của nguồn** trong `parse._FIX`: site ghi "Chu Tuớc" và
  "Đăng xà" → hiển thị đúng thành **"Chu Tước"** và **"Đằng Xà"**.
- **Loại ngày dùng chính tả "Hỏa" / "Thủy"** (không phải "Hoả"/"Thuỷ").
- **Âm lịch tính offline** bằng thuật toán Hồ Ngọc Đức (không phụ thuộc internet). Kiểm
  khớp với site: 02/08→20/6, 13/08→1/7, mùng 1 Tết 17/02/2026→1/1.
- **Can-Chi giờ theo Ngũ thử độn**: can giờ Tý = `(jd-1)*2 % 10`, giờ thứ h cộng thêm h.
  Kiểm: ngày Mậu Thân → giờ Tý = Nhâm Tý (đúng lệ "Mậu/Quý → giờ Tý Nhâm Tý").
- **Giờ Tý (23h-1h) bắt đầu từ 23h TỐI HÔM TRƯỚC** đến 1h sáng ngày đó (lệ ngày bắt đầu
  từ giờ Tý). Gói trong `parse.hour_window()` dùng chung cho banner "sắp tới" và file `.ics`,
  tránh nhầm 23h là của ngày hiện tại.

---

## 7. Lịch sử tiến hoá tính năng

Xây theo lối lặp, mỗi vòng đáp một yêu cầu của người dùng:

1. **Lõi**: fetch + parse + so khớp danh sách → trang kết quả nhóm theo ngày, tô màu
   Top 1 (đỏ) / Top 2 (xanh), loại hào Huyền Vũ; nút In/PDF.
2. **Sửa cổng 5000→5057** (macOS AirPlay chiếm 5000 gây 403).
3. **Bỏ chữ "Top 1/Top 2"** ở tag phải, chỉ giữ phân biệt bằng màu.
4. **Nút In đổi thành icon** máy in gọn.
5. **Thêm ngày âm lịch** ở header; **footer chỉ giữ nguồn**; **chỉ còn bộ chọn lịch**
   (bỏ ô gõ tay).
6. **Đưa hào Huyền Vũ trở lại** danh sách nhưng **bôi đen** (nền tối), ghi chú
   "không nên động, hợp cúng kiếng"; dùng đúng thuật ngữ **"hào"** Huyền Vũ.
7. **Chuẩn hoá thuật ngữ/chính tả**: "Thăng-Thái" (Địa/Top 2), "Chu Tước", "Đằng Xà",
   "Hỏa"/"Thủy".
8. **Gộp chọn ngày + chọn tháng thành một bộ chọn khoảng** (Từ ngày → Đến ngày), hỗ trợ
   1 ngày / cả tháng / khoảng bất kỳ vắt nhiều tháng (≤1 năm), tự đảo nếu nhập ngược.
9. **4 tính năng lớn** (theo đề xuất): (a) banner **giờ tốt sắp tới** + tô sáng hôm nay,
   (b) **nút chọn nhanh** (Hôm nay/Tuần/Tháng/30 ngày) + bộ lọc, (c) **xuất .ics** (mỗi
   giờ = 1 sự kiện, nhắc trước 10'), (d) **Can-Chi** ngày & giờ.
10. **Sửa mốc giờ Tý = tối hôm trước** (ảnh hưởng banner "sắp tới" và .ics).
11. **Tách rõ MÀN HÌNH vs BẢN IN**: bản in PDF (để lưu dài hạn) **ẩn** banner sắp tới,
    nhãn "HÔM NAY", highlight ngày hiện tại và highlight giờ sắp tới — tránh gây nhầm khi
    xem lại sau này. Bỏ luôn chữ "tối hôm trước" (chỉ giữ trong logic).
12. **Bỏ bộ lọc "Chỉ Top 1"**, chỉ giữ "Ẩn hào Huyền Vũ".
13. **Thống nhất format ngày** về `DD/MM/YYYY` (trước đó lẫn `/` và `.`).
14. **Banner "sắp tới" tính toàn cục**: luôn hiển thị giờ tốt kế tiếp thật sự từ thời điểm
    hiện tại, **độc lập với khoảng đang xem** (dò tối đa 4 tháng tới — `service.next_good_hour`).

---

## 8. Vài quyết định UX đáng chú ý

- **Màn hình ≠ bản in.** Màn hình phục vụ tra cứu hằng ngày (có banner, HÔM NAY, highlight);
  bản in PDF phục vụ lưu trữ dài hạn nên loại bỏ mọi thứ mang tính "thời điểm hiện tại".
- **Banner là "từ bây giờ", không phải "trong khoảng đang xem".** Người dùng muốn luôn biết
  giờ tốt gần nhất, nên banner có thể hiện một ngày không nằm trong danh sách bên dưới.
- **Không im lặng.** Khi không có kết quả (hoặc trước đây khi banner trống), luôn hiện thông
  báo rõ ràng thay vì để trống gây hiểu nhầm là lỗi.

---

## 9. Kiểm thử & xác minh

- **Đối chiếu ví dụ mẫu**: 02/08/2026 phải có "13h-15h Thuần Kiền – Đại Hữu (Thiên/Top 1)".
- **Bất biến loại ngày**: 194 ngày × không vi phạm.
- **Không lọt / đúng cờ Huyền Vũ**: đếm 62 hào Huyền Vũ toàn tháng nhưng chỉ 8 hào là giờ
  tốt trong danh sách → chỉ giữ đúng 8.
- **Âm lịch & Can-Chi**: đối chiếu nhiều mốc với site.
- **Khoảng ngày**: 1 ngày / cả tháng (tự nhận tiêu đề) / vắt tháng / nhập ngược / quá 1 năm.
- **.ics**: kiểm VEVENT, VALARM, gấp dòng, escape, giờ Tý kéo sang hôm sau.
- **Kiểm trực quan** bằng trình duyệt cho từng thay đổi giao diện.

---

## 10. Hạn chế & hướng mở rộng

- Danh sách hiện có **7/8 loại ngày** — thiếu **Ngày Sơn/Núi** (ngày loại này không hiện
  giờ tốt; bổ sung sau chỉ cần thêm vào `reference.py`).
- Phụ thuộc `vutrungu.com` cho lần tải đầu mỗi tháng (sau đó dùng cache).
- Chưa làm: **truy cập trên điện thoại** (đang chạy localhost trên máy Mac) và **diễn giải
  ý nghĩa từng cặp quẻ / nên động dụng việc gì** (cần nội dung Dịch lý).

---

*Chi tiết cách chạy & tính năng: xem [README.md](README.md).*
