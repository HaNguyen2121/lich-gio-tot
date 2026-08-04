# Hướng dẫn cài đặt (cho người mới)

App chạy trên **macOS**, chỉ dùng **Python thư viện chuẩn** — **không cần cài thêm gói nào**.

## 1. Chuẩn bị (một lần)

Mở **Terminal** (Spotlight ⌘+Space, gõ "Terminal"), rồi kiểm tra:

```bash
python3 --version    # cần Python 3.x
git --version        # cần git
```

Nếu thiếu, cài Xcode Command Line Tools (có sẵn cả hai):

```bash
xcode-select --install
```

## 2. Tải mã nguồn

```bash
cd ~/Documents
git clone https://github.com/HaNguyen2121/lich-gio-tot.git
cd lich-gio-tot
```

## 3. Chạy thử

```bash
python3 -m giotot
```

Trình duyệt tự mở **http://127.0.0.1:5057**. Dừng bằng **Ctrl + C**.

> Nếu cổng bận, đổi cổng: `python3 -m giotot --port 8080`.
> (Tránh cổng **5000** vì trên macOS bị AirPlay Receiver chiếm → lỗi 403.)

## 4. (Khuyến nghị) Cài dịch vụ nền — luôn bật, không cần Terminal

Để server **tự chạy khi đăng nhập** và luôn sẵn sàng (không mất khi đóng Terminal / refresh):

```bash
bash deploy/install-service.sh
```

Xong! **Bookmark** http://127.0.0.1:5057 và mở bất cứ lúc nào.
Script tự dò đường dẫn Python và thư mục project — không cần sửa tay.

Gỡ dịch vụ nền:

```bash
bash deploy/uninstall-service.sh
```

## Cập nhật lên bản mới

```bash
cd ~/Documents/lich-gio-tot
git pull
bash deploy/install-service.sh   # nạp lại code mới (nếu đang dùng dịch vụ nền)
```

## Xử lý sự cố

| Vấn đề | Cách xử lý |
|---|---|
| `python3: command not found` | Chạy `xcode-select --install` |
| Mở trang báo **403** | Cổng 5000 bị AirPlay chiếm — dùng cổng mặc định 5057, hoặc `--port 8080` |
| Trang không mở được | Kiểm tra dịch vụ: `launchctl list \| grep giotot`; xem log `~/Library/Logs/giotot.log` |
| Muốn dừng hẳn | `bash deploy/uninstall-service.sh` |

> Chi tiết thêm về tính năng và dòng lệnh: xem [README.md](README.md).
