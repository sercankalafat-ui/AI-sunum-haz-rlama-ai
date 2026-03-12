from __future__ import annotations

import csv
import html
import io
import tempfile
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Dict, List, Tuple

from .analyzer import AnalysisResult, analyze_products
from .ppt_generator import create_presentation


def _parse_multipart_csv(content_type: str, body: bytes) -> bytes:
    marker = "boundary="
    if marker not in content_type:
        raise ValueError("Geçersiz form verisi.")
    boundary = content_type.split(marker, 1)[1].strip().encode("utf-8")
    parts = body.split(b"--" + boundary)
    for part in parts:
        if b'name="csv_file"' in part:
            _, _, payload = part.partition(b"\r\n\r\n")
            payload = payload.rsplit(b"\r\n", 1)[0]
            return payload
    raise ValueError("Lütfen bir CSV dosyası seçin.")


def _analyze_uploaded_csv(raw_data: bytes) -> AnalysisResult:
    if not raw_data:
        raise ValueError("CSV dosyası boş olamaz.")

    try:
        decoded = raw_data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError("CSV dosyası UTF-8 formatında olmalıdır.") from exc

    reader = csv.DictReader(io.StringIO(decoded))
    rows = list(reader)
    if not rows:
        raise ValueError("CSV içinde satır bulunamadı.")

    return analyze_products(rows)


def _render_page(result: AnalysisResult | None = None, error: str | None = None) -> str:
    body = """
    <h1>Ürün Analizi + Otomatik PowerPoint</h1>
    <p>CSV dosyanızı yükleyin, tarayıcıdan analiz edin ve sunumu indirin.</p>
    <form action="/analyze" method="post" enctype="multipart/form-data">
      <input type="file" name="csv_file" accept=".csv" required />
      <button type="submit">Analiz Et</button>
    </form>
    <form action="/download-ppt" method="post" enctype="multipart/form-data" style="margin-top: 8px;">
      <input type="file" name="csv_file" accept=".csv" required />
      <button type="submit">PowerPoint İndir</button>
    </form>
    """

    if error:
        body += f'<p style="color:#b91c1c;">{html.escape(error)}</p>'

    if result:
        body += "<h2>Özet</h2><ul>"
        body += f"<li>Ortalama fiyat: {result.summary['average_price']:.2f}</li>"
        body += f"<li>Ortalama kalite: {result.summary['average_quality']:.2f}</li>"
        body += f"<li>Ortalama müşteri memnuniyeti: {result.summary['average_customer_satisfaction']:.2f}</li>"
        body += f"<li>Ortalama satış: {result.summary['average_sales']:.2f}</li>"
        body += "</ul><h2>Sıralama</h2><table border='1' cellpadding='6' cellspacing='0'><tr><th>Ürün</th><th>Skor</th><th>Fiyat</th><th>Kalite</th><th>Memnuniyet</th><th>Satış</th></tr>"
        for item in result.ranked_products:
            body += (
                f"<tr><td>{html.escape(str(item['product']))}</td>"
                f"<td>{float(item['overall_score']):.3f}</td>"
                f"<td>{float(item['price'])}</td><td>{float(item['quality'])}</td>"
                f"<td>{float(item['customer_satisfaction'])}</td><td>{float(item['sales'])}</td></tr>"
            )
        body += "</table>"

    return f"""<!doctype html><html lang='tr'><head><meta charset='utf-8'><title>Ürün Analizi</title></head>
    <body style='font-family:Arial; margin:2rem; background:#f7f8fb'>{body}</body></html>"""


class PresentationHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        if self.path != "/":
            self.send_error(HTTPStatus.NOT_FOUND, "Sayfa bulunamadı")
            return
        self._send_html(_render_page())

    def do_POST(self) -> None:  # noqa: N802
        if self.path not in {"/analyze", "/download-ppt"}:
            self.send_error(HTTPStatus.NOT_FOUND, "Sayfa bulunamadı")
            return

        length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(length)
        content_type = self.headers.get("Content-Type", "")

        try:
            csv_bytes = _parse_multipart_csv(content_type, raw_body)
            result = _analyze_uploaded_csv(csv_bytes)
        except ValueError as exc:
            self._send_html(_render_page(error=str(exc)), status=HTTPStatus.BAD_REQUEST)
            return

        if self.path == "/analyze":
            self._send_html(_render_page(result=result))
            return

        try:
            output_path = Path(tempfile.gettempdir()) / "urun-analizi-sunumu.pptx"
            created = create_presentation(result, str(output_path))
        except RuntimeError as exc:
            self._send_html(_render_page(error=str(exc)), status=HTTPStatus.INTERNAL_SERVER_ERROR)
            return

        data = created.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/vnd.openxmlformats-officedocument.presentationml.presentation")
        self.send_header("Content-Disposition", f"attachment; filename={created.name}")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _send_html(self, payload: str, status: HTTPStatus = HTTPStatus.OK) -> None:
        encoded = payload.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


def create_app(host: str = "0.0.0.0", port: int = 8000) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), PresentationHandler)


def main() -> None:
    server = create_app()
    print("Web uygulaması hazır: http://localhost:8000")
    server.serve_forever()


if __name__ == "__main__":
    main()
