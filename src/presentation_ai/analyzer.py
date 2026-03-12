from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class AnalysisResult:
    summary: Dict[str, float]
    ranked_products: List[Dict[str, float | str]]


def _normalize(values: List[float]) -> List[float]:
    min_value = min(values)
    max_value = max(values)
    if min_value == max_value:
        return [1.0] * len(values)
    return [(value - min_value) / (max_value - min_value) for value in values]


def analyze_products(data: List[Dict[str, float | str]]) -> AnalysisResult:
    required_columns = {"product", "price", "quality", "customer_satisfaction", "sales"}
    if not data:
        raise ValueError("Veri boş olamaz")

    missing = required_columns - set(data[0].keys())
    if missing:
        raise ValueError(f"Eksik sütun(lar): {', '.join(sorted(missing))}")

    prices = [float(row["price"]) for row in data]
    qualities = [float(row["quality"]) for row in data]
    satisfactions = [float(row["customer_satisfaction"]) for row in data]
    sales = [float(row["sales"]) for row in data]

    price_scores = [1 - n for n in _normalize(prices)]
    quality_scores = _normalize(qualities)
    satisfaction_scores = _normalize(satisfactions)
    sales_scores = _normalize(sales)

    ranked_products: List[Dict[str, float | str]] = []
    for i, row in enumerate(data):
        overall_score = (
            0.25 * price_scores[i]
            + 0.30 * quality_scores[i]
            + 0.25 * satisfaction_scores[i]
            + 0.20 * sales_scores[i]
        )
        ranked_products.append(
            {
                "product": str(row["product"]),
                "overall_score": round(overall_score, 3),
                "price": float(row["price"]),
                "quality": float(row["quality"]),
                "customer_satisfaction": float(row["customer_satisfaction"]),
                "sales": float(row["sales"]),
            }
        )

    ranked_products.sort(key=lambda item: float(item["overall_score"]), reverse=True)

    summary = {
        "average_price": sum(prices) / len(prices),
        "average_quality": sum(qualities) / len(qualities),
        "average_customer_satisfaction": sum(satisfactions) / len(satisfactions),
        "average_sales": sum(sales) / len(sales),
    }

    return AnalysisResult(summary=summary, ranked_products=ranked_products)
