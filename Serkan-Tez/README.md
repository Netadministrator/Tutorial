# Serkan-Tez

Bu klasör Serkan Tez projesinin dosyaları içindir. Çalışmalarını buraya koy.

Drex (Nace.ai) bu depoda hazır:

- Drex skill'i: `.claude/skills/drex/` (deponun kökünde). Bu depoda açılan her
  Claude oturumu onu otomatik tanır. Claude'a "Drex ile şu mesaja bak: ..." demen yeterli.
- `nace-sdk` kütüphanesi her bulut oturumu başında otomatik kurulur
  (`.claude/hooks/session-start.sh`).
- API anahtarı bulut ortam ayarlarındaki `NACE_API_KEY` değişkeninden okunur.

Elle çalıştırmak için (deponun kökünden):

```bash
python3 .claude/skills/drex/mesaj_yonlendir.py "Ödemem geçmedi, acil!"
python3 .claude/skills/drex/karar_ver.py .claude/skills/drex/secenekler.json
```
