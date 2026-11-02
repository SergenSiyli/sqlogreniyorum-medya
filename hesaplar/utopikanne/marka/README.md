# Marka kiti
Kod: araclar/anne_story.py (şablonlar) + araclar/anne_gun.py (içerik JSON → PNG).
Palet: krem (250,243,235), şeftali (240,168,138), adaçayı (150,178,148), kahve (74,54,44); vurgu turuncu (232,132,72), yeşil (110,150,100); gece mor-lacivert (40,36,62)→(58,52,86), ay sarısı (250,232,196).
Yazı: Inter (Black başlık, SemiBold/Medium gövde). 1080x1920, güvenli alan y=250–1580 (assert), @utopikanne y=1640.
Şablonlar: gunaydin, tarif_karti, hamilelik_haftasi, efsane_gercek, kontrol_listesi (numarali=liste), dm_cagrisi, iyi_geceler.
Çizimler yalnızca kendi vektörlerimiz (güneş, kase-kaşık, havuç, balkabağı, takvim, tik, balon, kalp, hilal-yıldız). Hilal maske ile. Fotoğraf, logo, emoji yok.

## v2 Renkli kit (2 Kasım 2026)
Kod: araclar/anne_renkli.py (gündüz şablonları), iyi geceler anne_story.py'den aynen. Degrade zemin + yarı saydam organik blob'lar, beyaz yuvarlak kartlar, koyu mürdüm metin, koyu tonlu seri rozetleri (TARİF #N, HAFTA N, HAP BİLGİ #N...). Dekorlar yalnızca y<230 ve y>1690 bantlarında. Yerleşim ölçek 1.2→0.7 denenir, y≤1480'e sığmazsa AssertionError.
Şablonlar: gunaydin, tarif (cizim: havuc, balkabagi, brokoli, elma, armut, avokado, kabak, patates, muz), hamilelik, lohusa, emzirme, temizlik, haber, efsane, hap, kontrol, liste, dm, iyi_geceler.
Limitler: tarif ≤3 malzeme, ≤4 adım (≤45 kr); hap başlık ≤ ~12 kr; DM seçenek ≤12 kr (2x2); başlıklar ≤ ~40 kr.
