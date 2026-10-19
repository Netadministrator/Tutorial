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
- **Ekipler:** `SORULAR` içindeki `criteria` sözlüğüne yeni ekip ekleyebilir veya açıklamaları değiştirebilirsin. Açıklamalar, Drex'in doğru ekibi seçmesine yardım eder. Açıklamaları hem İngilizce hem Türkçe yazmak Türkçe mesajlarda isabeti belirgin şekilde artırdı.
- **İnsan kontrolü:** Drex ekip seçiminden emin değilse (güven `GUVEN_ESIGI = 0.5` altında) program `⚠️ ... bir insan baksın` uyarısı verir. Daha fazla mesajın kontrol edilmesini istersen bu değeri yükselt.

---

# Karar verici (`karar_ver.py`)

Birkaç seçenek arasından en iyi kombinasyonu Drex'e sordurur. Seçenekleri koda değil, `secenekler.json` dosyasına yazarsın.

## Seçenekleri yaz

`secenekler.json` dosyasını aç ve doldur:

```json
{
  "amac": "Bir işletme veya çiftlik kurmak",
  "oncelik": "Maliyet, kullanım, kurulum ve verimliliği birlikte dengele.",
  "kac_tane_secilecek": 2,
  "secenekler": {
    "X": "kurulum kolay, kullanım kolay, verimlilik az, maliyet yüksek",
    "Y": "maliyet çok düşük, kullanım zor, kurulum orta, verimlilik yüksek"
  }
}
```

- **amac:** Ne için karar veriyorsun?
- **oncelik:** Senin için en önemli olan ne? Bu alan sonucu en çok değiştiren yerdir.
- **kac_tane_secilecek:** Kaç seçenek birlikte kullanılacak? Program bütün kombinasyonları kendisi çıkarır (4 seçenekten 2'li → 6 kombinasyon).
- **secenekler:** İstediğin kadar seçenek ekleyebilirsin.

## Çalıştır

```bash
python karar_ver.py                  # secenekler.json'u kullanır
python karar_ver.py baska_dosya.json # başka bir dosyayı kullanır
```

Örnek çıktı (sayılar her çağrıda biraz değişebilir):

```
Drex'in önerisi: Z+T (güven %32)

Tüm kombinasyonlar:
  Z+T          %43.6
  Y+Z          %21.7
  ...
```

İlk iki kombinasyon birbirine çok yakın çıkarsa program seni uyarır. O zaman `oncelik` alanına neyin daha önemli olduğunu açıkça yaz ve tekrar çalıştır.

**Unutma:** Drex bir öneri verir, son karar senindir. Güven puanı düşükse sonuca temkinli bak.
