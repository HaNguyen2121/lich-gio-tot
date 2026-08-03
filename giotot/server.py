"""HTTP server thuần thư viện chuẩn cho app Giờ tốt Dịch lý."""

import urllib.error
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import datetime

from . import render
from .ics import build_ics
from .service import InputError, next_good_hour, tra_cuu, tra_cuu_range


class Handler(BaseHTTPRequestHandler):
    def _send(self, body_html, status=200):
        data = body_html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _send_ics(self, text):
        data = text.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/calendar; charset=utf-8")
        self.send_header("Content-Disposition",
                         'attachment; filename="gio-tot.ics"')
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return

        if path == "/":
            self._send(render.render_index())
            return

        if path == "/ket-qua":
            params = urllib.parse.parse_qs(parsed.query)
            tu = (params.get("tu", [""])[0]).strip()
            den = (params.get("den", [""])[0]).strip()
            q = (params.get("q", [""])[0]).strip()
            try:
                if tu or den:                  # từ 2 ô chọn ngày (khoảng)
                    tieu_de, filtered = tra_cuu_range(tu, den)
                else:                          # gõ tay (tương thích cũ)
                    tieu_de, filtered = tra_cuu(q)
            except InputError as e:
                self._send(render.render_index(error=str(e)))
                return
            except (urllib.error.URLError, urllib.error.HTTPError):
                self._send(render.render_index(
                    error="Không tải được dữ liệu từ lich.vutrungu.com. "
                          "Kiểm tra kết nối mạng rồi thử lại."))
                return
            try:
                nxt = next_good_hour(datetime.datetime.now())
            except (urllib.error.URLError, urllib.error.HTTPError):
                nxt = None
            self._send(render.render_results(tieu_de, filtered,
                                             ics_query=parsed.query, nxt=nxt))
            return

        if path == "/lich.ics":
            params = urllib.parse.parse_qs(parsed.query)
            tu = (params.get("tu", [""])[0]).strip()
            den = (params.get("den", [""])[0]).strip()
            try:
                tieu_de, filtered = tra_cuu_range(tu, den)
            except InputError as e:
                self._send(render.render_index(error=str(e)))
                return
            except (urllib.error.URLError, urllib.error.HTTPError):
                self._send(render.render_index(
                    error="Không tải được dữ liệu từ lich.vutrungu.com."))
                return
            self._send_ics(build_ics(tieu_de, filtered))
            return

        self._send(render.render_index(error="Trang không tồn tại."), status=404)

    def log_message(self, *args):
        pass  # tắt log ồn ào ra terminal


def run(host="127.0.0.1", port=5057):
    server = ThreadingHTTPServer((host, port), Handler)
    url = f"http://{host}:{port}"
    print(f"  Giờ tốt Dịch lý đang chạy tại:  {url}")
    print("  Nhấn Ctrl+C để dừng.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Đã dừng.")
    finally:
        server.server_close()
