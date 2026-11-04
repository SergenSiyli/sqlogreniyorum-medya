# Yayın kuyruğu

Gönderiler buradaki `AAAA-AA-GG.json` dosyalarından, resmi Instagram API ile **tam hedef saatinde** yayınlanır
(`.github/workflows/instagram-yayin.yml`, `araclar/ig_yayin.py`). Ofset gerekmez: konteyner önceden hazırlanır, yayın hedef saniyede yapılır.

Öğe: `{"id": "AAAA-AA-GG_SSDD_tur_konu", "hedef": "AAAA-AA-GGTSS:DD", "tur": "STORY|REEL|TRIAL_REEL|CAROUSEL", "medya": url | [url,...], "kapak": url (REEL), "aciklama": "..." (REEL/CAROUSEL)}`

Medya adresleri: `https://cdn.jsdelivr.net/gh/SergenSiyli/sqlogreniyorum-medya@<TAM_SHA>/gun/.../dosya`
(raw.githubusercontent.com mp4'ü application/octet-stream sunduğu için KULLANMA.)

Yayınlanan/hatalı/kaçırılan her öğe `durum/<id>.json` dosyasına yazılır. `kontrol.json` son bağlantı testidir.

**Videolar (4 Kasım):** Kuyruktaki mp4 adresi kendi depomuzu gösteriyorsa (jsDelivr URL'si), `ig_yayin.py` videoyu Actions'taki çalışma kopyasından doğrudan Instagram'a yükler (resumable upload); jsDelivr yalnızca yedektir. Bu yüzden yayınlanmamış videoları depodan SİLME. Görseller (PNG) hâlâ jsDelivr URL'siyle verilir.
**Depo boyutu:** Her ayın 1'inde `gh api repos/SergenSiyli/sqlogreniyorum-medya --jq .size` (KB) kontrol et; 700 MB'ı geçerse hesap sahibine yeni depoya geçiş öner (geçmişi silmek onaysız yapılmaz).
