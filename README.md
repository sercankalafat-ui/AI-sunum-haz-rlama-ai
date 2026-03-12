# AI Sunum Hazırlama + Ürün Analizi

Bu proje, ürün verilerini kullanarak:

1. Ürünler arasında metrik bazlı analiz yapar,
2. Genel skora göre sıralama çıkarır,
3. Sonuçları otomatik bir PowerPoint sunumuna dönüştürür,
4. Tüm süreci tarayıcıdan yönetmenizi sağlar.

## Özellikler

- CSV'den ürün verisi okuma
- Fiyat, kalite, müşteri memnuniyeti ve satışa göre puanlama
- Tarayıcıda özet ve ürün sıralama tablosu
- Otomatik grafik üretimi
- PPTX sunum çıktısı indirme

## Kurulum

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Web uygulamasını çalıştırma

```bash
presentation-ai-web
```

Uygulama varsayılan olarak `http://localhost:8000` adresinde açılır.

## CLI ile kullanım (opsiyonel)

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
