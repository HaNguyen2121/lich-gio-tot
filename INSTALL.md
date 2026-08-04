# Hướng dẫn cài đặt (cho người mới)

App chỉ dùng **Python thư viện chuẩn** — **không cần cài thêm gói nào**.
Chạy được trên **macOS** và **Windows**.

---

## A. macOS

### 1. Chuẩn bị (một lần)

Mở **Terminal** (⌘+Space → gõ "Terminal") và kiểm tra:

```bash
python3 --version    # cần Python 3.x
git --version        # cần git
```

Nếu thiếu, cài Xcode Command Line Tools (có sẵn cả hai):

```bash
xcode-select --install
```

### 2. Tải mã nguồn

```bash
cd ~/Documents
git clone https://github.com/HaNguyen2121/lich-gio-tot.git
cd lich-gio-tot
```

### 3. Chạy thử

```bash
python3 -m giotot
```

Trình duyệt tự mở **http://127.0.0.1:5057**. Dừng bằng **Ctrl + C**.

> Đổi cổng nếu cần: `python3 -m giotot --port 8080`.
> (Tránh cổng **5000** vì macOS AirPlay chiếm → lỗi 403.)

### 4. (Khuyến nghị) Dịch vụ nền — luôn bật, không cần Terminal

```bash
bash deploy/install-service.sh
```

Xong! **Bookmark** http://127.0.0.1:5057. Gỡ: `bash deploy/uninstall-service.sh`.

---

## B. Windows

### 1. Chuẩn bị (một lần)

- **Python 3**: tải từ https://python.org → khi cài **nhớ tick "Add Python to PATH"**.
- **Git**: tải từ https://git-scm.com (hoặc tải mã nguồn dạng ZIP từ trang GitHub, giải nén).

Mở **PowerShell** (Start → gõ "PowerShell") và kiểm tra:

```powershell
python --version
git --version
```

### 2. Tải mã nguồn

```powershell
cd $HOME\Documents
git clone https://github.com/HaNguyen2121/lich-gio-tot.git
cd lich-gio-tot
```

### 3. Chạy thử

```powershell
python -m giotot
```

Trình duyệt tự mở **http://127.0.0.1:5057**. Dừng bằng **Ctrl + C**.

### 4. (Khuyến nghị) Dịch vụ nền — luôn bật, không cần cửa sổ nào

**Cách 1 — Script (tự động, tự bật lại nếu lỗi):**

```powershell
powershell -ExecutionPolicy Bypass -File deploy\install-service.ps1
```

Xong! **Bookmark** http://127.0.0.1:5057 (tự chạy khi đăng nhập).
Gỡ: `powershell -ExecutionPolicy Bypass -File deploy\uninstall-service.ps1`

**Cách 2 — Thủ công (không dùng script):** cho tự chạy khi đăng nhập bằng thư mục Startup.

1. Mở thư mục Startup: nhấn **Win + R**, gõ `shell:startup`, Enter.
2. Tạo file mới tên `giotot.vbs` trong thư mục đó, nội dung (sửa đường dẫn cho đúng
   nơi bạn đã clone):

   ```vbscript
   Set sh = CreateObject("WScript.Shell")
   sh.CurrentDirectory = "C:\Users\<TEN_BAN>\Documents\lich-gio-tot"
   sh.Run "pythonw -m giotot --no-open --port 5057", 0, False
   ```

3. Đăng xuất/đăng nhập lại (hoặc bấm đúp `giotot.vbs`) → server chạy ẩn.
   Gỡ: xoá file `giotot.vbs` khỏi thư mục Startup.

> `pythonw` chạy **không hiện cửa sổ**. Nếu báo không tìm thấy, dùng `python` thay cho
> `pythonw` (sẽ có một cửa sổ nhỏ chạy nền).

---

## Cập nhật lên bản mới

```bash
git pull
```

Rồi chạy lại script cài dịch vụ (nếu đang dùng dịch vụ nền) để nạp code mới —
macOS: `bash deploy/install-service.sh` · Windows: `...install-service.ps1`.

## Xử lý sự cố

| Vấn đề | Cách xử lý |
|---|---|
| `command not found` / `not recognized` | Chưa cài Python/Git hoặc chưa "Add to PATH" (Windows) |
| Mở trang báo **403** (macOS) | Cổng 5000 bị AirPlay chiếm — dùng 5057, hoặc `--port 8080` |
| Trang không mở được | Xem log: macOS `~/Library/Logs/giotot.log` · thử chạy tay `python -m giotot` để thấy lỗi |
| Muốn dừng hẳn dịch vụ | Chạy script `uninstall-service` tương ứng |

> Chi tiết tính năng và dòng lệnh: xem [README.md](README.md).
