from __future__ import annotations

from presentation_ai.web import _analyze_uploaded_csv, _parse_multipart_csv, _render_page


VALID_CSV = (
    "product,price,quality,customer_satisfaction,sales\n"
    "A,100,9,8,1000\n"
    "B,200,6,6,600\n"
)


def test_analyze_uploaded_csv_returns_ranked_result() -> None:
    result = _analyze_uploaded_csv(VALID_CSV.encode("utf-8"))
    assert result.ranked_products[0]["product"] == "A"


def test_parse_multipart_csv_extracts_uploaded_file() -> None:
    boundary = "----WebKitFormBoundaryXYZ"
    body = (
        f"--{boundary}\r\n"
        "Content-Disposition: form-data; name=\"csv_file\"; filename=\"products.csv\"\r\n"
        "Content-Type: text/csv\r\n\r\n"
        f"{VALID_CSV}"
        f"\r\n--{boundary}--\r\n"
    ).encode("utf-8")

    extracted = _parse_multipart_csv(f"multipart/form-data; boundary={boundary}", body)
    assert b"product,price" in extracted


def test_render_page_includes_ranking_table() -> None:
    result = _analyze_uploaded_csv(VALID_CSV.encode("utf-8"))
    page = _render_page(result=result)
    assert "Sıralama" in page
    assert "<table" in page
