from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List

from .analyzer import analyze_products
from .ppt_generator import create_presentation


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Ürün verisinden analiz ve otomatik PowerPoint sunumu üretir."
    )
    parser.add_argument("input_file", type=Path, help="CSV dosyası yolu")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("urun-analizi-sunumu.pptx"),
        help="Oluşturulacak PPTX dosya yolu",
    )
    return parser


def _load_csv(path: Path) -> List[Dict[str, float | str]]:
    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


def main() -> None:
    args = build_parser().parse_args()
    rows = _load_csv(args.input_file)
    result = analyze_products(rows)
    output = create_presentation(result, str(args.output))
    print(f"Sunum oluşturuldu: {output}")


if __name__ == "__main__":
    main()
