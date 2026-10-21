"""Seçenekleri bir JSON dosyasından okur ve Drex'e sorar:
1. Hangi kombinasyon en iyisi?   (choice: tüm olası kombinasyonlar)
2. Her seçenek tek başına iyi mi? (noul: 0 ile 1 arası "evet" olasılığı)

Kullanım:
    python karar_ver.py                    # secenekler.json dosyasını kullanır
    python karar_ver.py baska_dosya.json

Dosyada şunlar olur (örnek için secenekler.json'a bak):
    amac                : Ne için karar veriyoruz?
    oncelik             : Senin için en önemli olan ne? (isteğe bağlı)
    kac_tane_secilecek  : Kaç seçenek birlikte kullanılacak? (1, 2, 3...)
    secenekler          : Seçenek adı -> özellikleri

API anahtarı NACE_API_KEY ortam değişkeninden okunur.
"""

import json
import sys
from itertools import combinations

from nace_sdk import Choice, NaceAPIConnectionError, NaceAPIError, NaceAuthenticationError, NaceClient, NaceError, Noul


def dosyayi_oku(yol):
    try:
        with open(yol, encoding="utf-8") as f:
            veri = json.load(f)
    except FileNotFoundError:
        sys.exit(f"Hata: '{yol}' dosyası bulunamadı.")
    except json.JSONDecodeError as hata:
        sys.exit(f"Hata: '{yol}' geçerli bir JSON değil (satır {hata.lineno}, sütun {hata.colno}).")
    for alan in ("amac", "secenekler"):
        if alan not in veri:
            sys.exit(f"Hata: '{yol}' dosyasında '{alan}' alanı eksik.")
    secenekler = veri["secenekler"]
    kac_tane = veri.get("kac_tane_secilecek", 1)
    if not 1 <= kac_tane <= len(secenekler):
        sys.exit(f"Hata: kac_tane_secilecek 1 ile {len(secenekler)} arasında olmalı.")
    return veri["amac"], veri.get("oncelik", ""), kac_tane, secenekler


def sorulari_hazirla(amac, oncelik, kac_tane, secenekler):
    # Her kombinasyon bir etiket olur, örneğin "Y+Z". Açıklamasında üyelerin özellikleri yazar.
    kombinasyonlar = {
        "+".join(grup): "; ".join(f"{ad}: {secenekler[ad]}" for ad in grup)
        for grup in combinations(secenekler, kac_tane)
    }
    talimat = f"Amaç: {amac}. Bu amaç için {kac_tane} seçeneğin en iyi kombinasyonu hangisidir? {oncelik}"
    sorular = {"en_iyi": Choice(instructions=talimat.strip(), criteria=kombinasyonlar)}
    for ad in secenekler:
        sorular[f"iyi_mi_{ad}"] = Noul(instructions=f"Amaç: {amac}. {ad} seçeneği tek başına iyi bir seçim midir?")
    return sorular


def sonucu_yazdir(sonuc, secenekler):
    en_iyi = sonuc.choices["en_iyi"]
    print(f"Drex'in önerisi: {en_iyi.choice} (güven %{en_iyi.confidence * 100:.0f})")
    print()
    print("Tüm kombinasyonlar:")
    for etiket, olasilik in sorted(en_iyi.probabilities.items(), key=lambda kv: -kv[1]):
        print(f"  {etiket:<12} %{olasilik * 100:.1f}")
    print()
    print("Seçenekler tek başına iyi mi?")
    for ad in secenekler:
        print(f"  {ad:<12} %{sonuc.nouls[f'iyi_mi_{ad}'].noul * 100:.0f}")

    # İlk iki kombinasyon birbirine çok yakınsa kullanıcıyı uyar.
    ilk_iki = sorted(en_iyi.probabilities.values(), reverse=True)[:2]
    if len(ilk_iki) == 2 and ilk_iki[0] - ilk_iki[1] < 0.10:
        print()
        print("Not: İlk iki kombinasyon birbirine çok yakın. Drex kararsız;")
        print("     'oncelik' alanına neyin daha önemli olduğunu yazarak tekrar dene.")


def main():
    yol = sys.argv[1] if len(sys.argv) > 1 else "secenekler.json"
    amac, oncelik, kac_tane, secenekler = dosyayi_oku(yol)
    sorular = sorulari_hazirla(amac, oncelik, kac_tane, secenekler)
    durum = "Seçenekler:\n" + "\n".join(f"{ad}: {ozellik}" for ad, ozellik in secenekler.items())
    try:
        with NaceClient(model="drex-v2.0") as client:
            sonuc = client.system_one(state=durum, questions=sorular)
    except NaceAuthenticationError:
        sys.exit("Hata: API anahtarı geçersiz. NACE_API_KEY değerini kontrol et.")
    except NaceAPIError as hata:
        sys.exit(f"Hata: Drex {hata.status} döndürdü: {hata.message} (request_id: {hata.request_id})")
    except NaceAPIConnectionError:
        sys.exit("Hata: Nace.ai'ye bağlanılamadı. İnternet bağlantını kontrol et.")
    except NaceError as hata:
        # Örneğin NACE_API_KEY hiç tanımlı değilse buraya düşer.
        sys.exit(f"Hata: {hata}")
    sonucu_yazdir(sonuc, secenekler)


if __name__ == "__main__":
    main()
