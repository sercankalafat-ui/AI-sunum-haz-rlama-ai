# AI Sunum Hazırlama + Ürün Analizi

Bu proje, ürün verilerini kullanarak:

1. Ürünler arasında metrik bazlı analiz yapar,
2. Genel skora göre sıralama çıkarır,
3. Sonuçları otomatik bir PowerPoint sunumuna dönüştürür.

## Özellikler

- CSV'den ürün verisi okuma
- Fiyat, kalite, müşteri memnuniyeti ve satışa göre puanlama
- Ürün sıralama tablosu
- Otomatik grafik üretimi
- PPTX sunum çıktısı

## Kurulum

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Örnek kullanım

```bash
presentation-ai data/products_sample.csv --output cikti-sunum.pptx
```

## Beklenen CSV kolonları

- `product`
- `price`
- `quality`
- `customer_satisfaction`
- `sales`

## Üretilen sunum içeriği

- Kapak slaytı
- Genel özet slaytı
- Ürün sıralama tablosu
- Ürün skor grafiği
- Öneri slaytı
