from presentation_ai.analyzer import analyze_products


def test_analyze_products_orders_by_score_desc() -> None:
    rows = [
        {"product": "A", "price": 100, "quality": 9, "customer_satisfaction": 8, "sales": 1000},
        {"product": "B", "price": 200, "quality": 6, "customer_satisfaction": 6, "sales": 600},
    ]

    result = analyze_products(rows)

    assert result.ranked_products[0]["product"] == "A"
    assert result.ranked_products[0]["overall_score"] > result.ranked_products[1]["overall_score"]


def test_analyze_products_requires_columns() -> None:
    rows = [{"product": "A", "price": 100}]

    try:
        analyze_products(rows)
        assert False, "ValueError bekleniyordu"
    except ValueError as exc:
        assert "Eksik sütun" in str(exc)
