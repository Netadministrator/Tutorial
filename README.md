# Müşteri mesajı yönlendirici (Nace.ai Drex örneği)

Bu küçük Python programı bir müşteri mesajını [Nace.ai Drex](https://console.nace.ai) API'sine gönderir ve iki soru sorar:

1. **Mesaj acil mi?** Cevap 0 ile 1 arasında bir olasılıktır (`noul`). Örneğin `0.73`, "%73 ihtimalle acil" demektir.
2. **Hangi ekibe gitmeli?** `payments` (ödemeler), `support` (destek) veya `engineering` (mühendislik).

## Kurulum

1. Python 3.9 veya üstünün kurulu olduğundan emin ol.
2. Sanal ortam oluştur ve kütüphaneyi yükle:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. API anahtarını ortam değişkeni olarak tanımla. Anahtarı [console.nace.ai](https://console.nace.ai) → **API Keys** sayfasından alırsın:

   ```bash
   export NACE_API_KEY="nace_sk_..."
   ```

   İstersen `.env.example` dosyasını `.env` adıyla kopyalayıp anahtarı oraya yazabilirsin. `.env` dosyası git'e eklenmez. **Anahtarını asla koda yazma ve commit etme.**

## Çalıştırma

Örnek mesajlarla denemek için:

```bash
python mesaj_yonlendir.py
```

Kendi mesajınla denemek için:

```bash
python mesaj_yonlendir.py "Kartımdan iki kez para çekildi, acilen iade istiyorum!"
```

Örnek çıktı (sayılar her çağrıda biraz değişebilir):

```
Mesaj : Kartımdan iki kez para çekildi, acilen iade istiyorum!
Acil mi? ACİL (olasılık %85)
Ekip  : payments (güven %74)
```

## Nasıl değiştiririm?

- **Acil eşiği:** `mesaj_yonlendir.py` içindeki `ACIL_ESIGI = 0.5` satırını değiştir. Daha yüksek bir değer yazarsan daha az mesaj acil sayılır.
- **Ekipler:** `SORULAR` içindeki `criteria` sözlüğüne yeni ekip ekleyebilir veya açıklamaları değiştirebilirsin. Açıklamalar, Drex'in doğru ekibi seçmesine yardım eder.
