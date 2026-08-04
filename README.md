# Giờ tốt theo Dịch lý Việt Nam

Web app chạy local: chọn **khoảng ngày** → danh sách các giờ có thể "động dụng",
phân biệt **Top 1 / Top 2** bằng màu. Có **In / Lưu PDF** và **xuất lịch .ics**.

Tính năng:
- Chọn khoảng ngày (1 ngày / cả tháng / khoảng bất kỳ), có nút nhanh *Hôm nay ·
  Tuần này · Tháng này · 30 ngày tới*.
- **Giờ tốt sắp tới** hiện ở đầu trang; ngày hôm nay được tô sáng.
- Hào **Huyền Vũ** vẫn hiển thị nhưng bôi đen (không nên động, hợp cúng kiếng).
- **Âm lịch** + **Can-Chi** ngày & giờ.
- **Rê chuột vào tên quẻ** để xem **dịch tượng + ý nghĩa** (học Dịch) — dữ liệu 64 quẻ
  nhúng sẵn trong `giotot/dichtuong.py`.
- Bộ lọc *Chỉ Top 1* / *Ẩn hào Huyền Vũ*.
- **Xuất .ics** để nạp vào Google Calendar / Lịch điện thoại (mỗi giờ tốt là 1 sự
  kiện có nhắc trước 10 phút).

Nguồn quẻ theo giờ: [lich.vutrungu.com](https://lich.vutrungu.com/xemthang) (tự tải & cache).

## Chạy

Không cần cài gì thêm (chỉ dùng Python thư viện chuẩn):

```bash
cd Gio-tot-Dich-ly
python3 -m giotot
```

Trình duyệt tự mở `http://127.0.0.1:5057`. Chọn **khoảng ngày** bằng lịch
(*Từ ngày* → *Đến ngày*):

- Xem **1 ngày**: để *Từ ngày* = *Đến ngày*
- Xem **cả tháng**: chọn từ ngày 1 đến ngày cuối tháng (điền sẵn khi mở app)
- Xem **khoảng bất kỳ**: kể cả vắt qua nhiều tháng, tối đa 1 năm

> **Lưu ý cổng:** mặc định dùng **5057**. Tránh cổng **5000** vì trên macOS bị
> AirPlay Receiver chiếm và trả về lỗi **HTTP 403**. (Nếu vẫn muốn dùng 5000: tắt
> *System Settings → General → AirDrop & Handoff → AirPlay Receiver*.)

## Dòng lệnh (command line)

```bash
python3 -m giotot [--port PORT] [--host HOST] [--no-open]
```

| Tuỳ chọn | Mặc định | Ý nghĩa |
|---|---|---|
| `--port PORT` | `5057` | Cổng chạy server |
| `--host HOST` | `127.0.0.1` | Địa chỉ lắng nghe |
| `--no-open` | (tắt) | Không tự mở trình duyệt khi khởi động |

Ví dụ:

```bash
# Chạy bình thường (tự mở trình duyệt ở http://127.0.0.1:5057)
python3 -m giotot

# Đổi cổng
python3 -m giotot --port 8080

# Không tự mở trình duyệt (vd chạy nền)
python3 -m giotot --no-open

# Mở cho điện thoại/máy khác cùng wifi truy cập:
# lắng nghe mọi địa chỉ, rồi trên điện thoại vào http://<IP-máy-Mac>:5057
python3 -m giotot --host 0.0.0.0
```

> Xem IP LAN của máy Mac: `ipconfig getifaddr en0` (wifi) — ví dụ `192.168.1.5`
> → trên điện thoại mở `http://192.168.1.5:5057`.

Dừng server: nhấn **Ctrl + C** trong cửa sổ terminal đang chạy.

## Chạy nền — luôn bật (macOS, không cần terminal)

Đã cài sẵn một **dịch vụ nền (LaunchAgent)** để server **tự chạy khi đăng nhập** và
**luôn sẵn sàng** — chỉ cần **bookmark** `http://127.0.0.1:5057` rồi mở bất cứ lúc nào,
không cần mở terminal, không mất khi refresh. Nếu server bị tắt/treo, launchd tự bật lại
(KeepAlive).

- File cấu hình: `~/Library/LaunchAgents/com.giotot.app.plist`
  (bản mẫu trong repo: [`deploy/com.giotot.app.plist`](deploy/com.giotot.app.plist))
- Log: `~/Library/Logs/giotot.log`

Quản lý dịch vụ:

```bash
# Xem trạng thái
launchctl list | grep giotot

# Tắt tạm (dừng dịch vụ)
launchctl unload ~/Library/LaunchAgents/com.giotot.app.plist

# Bật lại
launchctl load ~/Library/LaunchAgents/com.giotot.app.plist

# Khởi động lại (sau khi cập nhật code)
launchctl unload ~/Library/LaunchAgents/com.giotot.app.plist && \
launchctl load ~/Library/LaunchAgents/com.giotot.app.plist

# Gỡ hẳn dịch vụ (không chạy nền nữa)
launchctl unload ~/Library/LaunchAgents/com.giotot.app.plist && \
rm ~/Library/LaunchAgents/com.giotot.app.plist
```

> Nếu **di chuyển thư mục project** hoặc **đổi Python** (vd cài lại miniconda), phải sửa
> lại đường dẫn trong file plist (`ProgramArguments` và `WorkingDirectory`) rồi nạp lại.

## Xuất PDF

Ở trang kết quả bấm **🖨 In / Lưu PDF** → trong hộp thoại in chọn "Save as PDF".
Trang in đã ẩn nút/điều khiển và giữ nguyên màu Top 1 / Top 2 (nhớ bật
"Background graphics" nếu trình duyệt tắt).

## Cách hoạt động

1. `fetch.py` — tải HTML tháng từ vutrungu, cache vĩnh viễn vào `cache/YYYY-MM.html`
   (dữ liệu Dịch cố định theo ngày; cache giúp chạy cả khi mất mạng/site sập).
2. `parse.py` — tách bảng thành từng ngày × 12 khung giờ (quẻ1, quẻ2, lục thú).
   Ngày dương + thứ trong tuần tính bằng `datetime`.
3. `reference.py` — bảng giờ tốt của bạn: 7 loại ngày (Thiên, Trạch, Hỏa, Lôi, Phong,
   Thủy, Địa), mỗi loại có các **cặp quẻ có thứ tự** xếp Top 1 / Top 2.
4. `matching.py` — khớp cặp `(quẻ1, quẻ2)` với bảng tham chiếu; hào Huyền Vũ vẫn giữ
   nhưng gắn cờ để bôi đen. Vì cặp có thứ tự nên tự suy ra đúng loại ngày (đã kiểm 194
   ngày: mọi giờ tốt trong cùng một ngày đều cùng một loại ngày).

## Sửa / mở rộng danh sách giờ tốt

Chỉ cần sửa `giotot/reference.py`. Ví dụ bổ sung **Ngày Sơn/Núi** (hiện chưa có):

```python
"Sơn": {
    "top1": [("Quẻ A", "Quẻ B"), ...],
    "top2": [...],
},
```

Tên quẻ viết đúng chính tả theo nguồn site (ví dụ `Tụy`, `Đại Tráng`, `Thuần Kiền`).
So khớp không phân biệt hoa/thường nhưng **có phân biệt dấu** (vì `BÍ` và `BĨ` là hai
quẻ khác nhau).

## Giới hạn

- Danh sách chỉ có 7/8 loại ngày (thiếu Ngày Sơn). Ngày thuộc loại chưa có dữ liệu sẽ
  không hiện giờ tốt.
- Phụ thuộc nguồn vutrungu.com cho lần tải đầu mỗi tháng (sau đó dùng cache).
