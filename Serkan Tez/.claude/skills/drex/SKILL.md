---
name: drex
description: Nace.ai Drex API ile metin sınıflandırma ve karar verme. Bir müşteri mesajının acil olup olmadığını ve hangi ekibe (payments/support/engineering) gitmesi gerektiğini bulmak, birkaç seçenek arasından en iyi kombinasyonu seçmek ya da Drex'e yeni evet/hayır (noul), seçim (choice) veya ölçek (score) soruları sormak için kullan. Use for Nace, Drex, nace-sdk, classify message, urgency, routing, decide between options.
---

# Drex (Nace.ai)

Drex bir metni (`state`) alır ve hakkındaki sorulara olasılık olarak cevap verir.
Bu skill iki hazır script ve yeni Drex kodu yazmak için kısa bir rehber içerir.
Kullanıcıyla Türkçe, sade ve adım adım konuş.

## Ön koşullar

- `nace-sdk` kütüphanesi kurulu olmalı: `py -m pip install --user nace-sdk==0.1.0`
  (Windows'ta `py`, diğer sistemlerde `python3` kullan.)
- API anahtarı `NACE_API_KEY` ortam değişkeninde olmalı. SDK onu kendisi okur.
- Anahtarı **asla** ekrana yazdırma, koda yazma, commit etme veya sohbete koyma.
  Varlığını kontrol etmek için sadece "var / yok" yazdır:
  `if ($env:NACE_API_KEY) {"var"} else {"yok"}` (PowerShell)

Hata alınırsa:
- `No module named 'nace_sdk'` → kütüphane kurulu değil.
- `No API key was provided` → anahtar tanımlı değil ya da terminal anahtar
  kaydedildikten sonra yeniden açılmamış.
- `API anahtarı geçersiz` / 401 → anahtar yanlış.

## Hazır script 1: mesaj_yonlendir.py

Bir müşteri mesajının acil olup olmadığını (noul) ve hangi ekibe gitmesi
gerektiğini (choice) söyler. Ekip seçiminin güveni %50'nin altındaysa
"bir insan baksın" uyarısı verir.

```
py .claude/skills/drex/mesaj_yonlendir.py "Ödemem geçmedi, acil!"
py .claude/skills/drex/mesaj_yonlendir.py          # örnek mesajlarla
```

Ayarlar dosyanın başında: `ACIL_ESIGI`, `GUVEN_ESIGI` ve `SORULAR` içindeki ekipler.
Ekip açıklamalarını İngilizce + Türkçe yazmak Türkçe mesajlarda isabeti artırır.

## Hazır script 2: karar_ver.py

Seçenekleri bir JSON dosyasından okur, bütün kombinasyonları çıkarır ve
Drex'e en iyisini sorar. Örnek dosya: `secenekler.json`
(`amac`, `oncelik`, `kac_tane_secilecek`, `secenekler`).

```
py .claude/skills/drex/karar_ver.py .claude/skills/drex/secenekler.json
```

Kullanıcının kendi seçenekleri için yeni bir JSON dosyası oluştur ve yolunu ver.
`oncelik` alanı sonucu en çok etkileyen alandır. Güven düşükse kullanıcıya
neyin daha önemli olduğunu sor ve `oncelik`'e yaz.
Drex'in cevabı bir öneridir; sonucu kendi değerlendirmenle birlikte sun.

## Yeni Drex kodu yazmak için rehber

Tek endpoint: `POST https://console.nace.ai/v1/systemone` (Bearer anahtar).
Model: `drex-v2.0`. Bir istekte bir `state` ve en fazla 512 soru olur;
soruları tek istekte toplamak daha ucuzdur.

```python
from nace_sdk import Choice, NaceClient, Noul, Score

with NaceClient(model="drex-v2.0") as client:
    sonuc = client.system_one(
        state="Kartımdan iki kez para çekildi, iade istiyorum.",
        questions={
            "iade_mi": Noul(instructions="Is the customer asking for a refund?"),
            "konu": Choice(
                instructions="What is this message about?",
                criteria={"billing": "Ödeme, fatura, iade", "technical": "Hata, çökme", "other": None},
            ),
            "sinir": Score(instructions="How upset is the customer?", criteria=["Sakin", "Biraz kızgın", "Çok kızgın"]),
        },
    )
print(sonuc.nouls["iade_mi"].noul)        # 0-1 arası "evet" olasılığı
print(sonuc.choices["konu"].choice)       # seçilen etiket (+ .probabilities, .confidence)
print(sonuc.scores["sinir"].score)        # ölçek üzerindeki beklenen konum (0..n-1)
```

Soru tipi seçimi:
- **noul**: evet/hayır. Cevap olasılıktır; eşiği (ör. 0.5) sen seçersin.
- **choice**: sırasız etiketlerden biri. `criteria` = {etiket: açıklama veya None}.
- **score**: sıralı ölçek. `criteria` = düşükten yükseğe etiket listesi.

İpuçları:
- `criteria` açıklamaları sonucu `instructions`'tan daha çok etkiler.
- Kullanıcıya olasılıkları yüzde olarak açıkla (0.7353 → %74).
- Hata sınıfları: `NaceAuthenticationError` (401), `NaceUnprocessableEntityError`
  (422, `error.issues`'a bak), `NaceRateLimitError` (429), `NaceAPIError`,
  `NaceAPIConnectionError`, `NaceError` (anahtar yok vb.).
- Ayrıntılı doküman: https://console.nace.ai/llms-full.txt (çok büyük; "Questions",
  "Reading answers", "Errors and retries" bölümlerine bak).
