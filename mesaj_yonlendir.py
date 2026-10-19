"""Bir müşteri mesajını Nace.ai Drex'e sorar:
1. Mesaj acil mi?           (noul: 0 ile 1 arası "evet" olasılığı)
2. Hangi ekibe gitmeli?     (choice: payments / support / engineering)

Kullanım:
    python mesaj_yonlendir.py "Ödemelerim 3 gündür başarısız oluyor!"
    python mesaj_yonlendir.py            # mesaj vermezsen örnek mesajlar denenir

API anahtarı NACE_API_KEY ortam değişkeninden okunur.
"""

import sys

from nace_sdk import Choice, NaceAPIConnectionError, NaceAPIError, NaceAuthenticationError, NaceClient, NaceError, Noul

# "noul" bu değerin üstündeyse mesajı acil sayarız. İhtiyacına göre değiştirebilirsin.
ACIL_ESIGI = 0.5

ORNEK_MESAJLAR = [
    "Help! My payouts have been failing for 3 days.",
    "How do I change the email address on my account?",
    "Your dashboard shows a 500 error every time I open the reports page.",
]

SORULAR = {
    "is_urgent": Noul(instructions="Does this convey urgency?"),
    "team": Choice(
        instructions="Which team should handle this?",
        criteria={
            "payments": "Payouts, charges, or refunds",
            "support": "General questions and how-to",
            "engineering": "Bugs and outages",
        },
    ),
}


def mesaji_incele(client, mesaj):
    sonuc = client.system_one(state=mesaj, questions=SORULAR)
    acil_olasiligi = sonuc.nouls["is_urgent"].noul
    ekip = sonuc.choices["team"]

    print(f"Mesaj : {mesaj}")
    durum = "ACİL" if acil_olasiligi > ACIL_ESIGI else "acil değil"
    print(f"Acil mi? {durum} (olasılık %{acil_olasiligi * 100:.0f})")
    print(f"Ekip  : {ekip.choice} (güven %{ekip.confidence * 100:.0f})")
    print()


def main():
    mesajlar = sys.argv[1:] or ORNEK_MESAJLAR
    try:
        with NaceClient(model="drex-v2.0") as client:
            for mesaj in mesajlar:
                mesaji_incele(client, mesaj)
    except NaceAuthenticationError:
        sys.exit("Hata: API anahtarı geçersiz. NACE_API_KEY değerini kontrol et.")
    except NaceAPIError as hata:
        sys.exit(f"Hata: Drex {hata.status} döndürdü: {hata.message} (request_id: {hata.request_id})")
    except NaceAPIConnectionError:
        sys.exit("Hata: Nace.ai'ye bağlanılamadı. İnternet bağlantını kontrol et.")
    except NaceError as hata:
        # Örneğin NACE_API_KEY hiç tanımlı değilse buraya düşer.
        sys.exit(f"Hata: {hata}")


if __name__ == "__main__":
    main()
