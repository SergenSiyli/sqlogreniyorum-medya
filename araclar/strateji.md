# Strateji (Büyüme Stratejisti)

## ⚡ HIZLANDIRMA v3 (8 Kasım 17:45, Sergen'in isteği) — EN ÜST KURAL
Bu bölüm tetik talimatındaki "Haftada 2-3 TRIAL_REEL" kuralının YERİNE geçer.
- HER GÜN 2 Reels: 12:30 normal REEL (takipçiler) + 20:30 TRIAL_REEL (takip etmeyenler, yeni takipçi kanalı). Haftada 7 deneme.
- Deneme Reels'te öncelik SQL TEST (SQL Reels erişimi AI haberinin ~4 katı). Haber denemesi en fazla haftada 2.
- Tüm Reels ve story'ler renkli şablonla: `python3 araclar/anne_canli.py <json> gun/<tarih> --sadece-reels` / `--story`, tema sql/tekno/ai/kariyer/gunes/koyu, "hesap":"sqlogreniyorum". Eski PIL şablonları (uret_*.py story_card vb.) KULLANILMAZ.
- Kapak = kanca + test sorusu (secenekler A/B/C), ilk saniyede yazı tam görünür. Akış: kapak(test) → tablo/kod → adim "Cevap" → doğrusu → son.
- Story düzeni: 09:00 günaydın (gunes) · 10:00 SQL TEST story ("Cevap 12:30 Reels'te") · 14:00 kariyer · 15:00/17:00 haber kartı · 19:30 30 saniyelik test · 22:00 özet (testin cevabı) · 23:00 iyi geceler (koyu, kullanilan_bilgiler.txt'ye ekle).
- Seri sayacı: #1 COUNT/NULL (10 Kasım 12:30), #2 CASE WHEN (9 Kasım 12:30), #3 HAVING (10 Kasım 20:30 deneme), #4 ikinci en yüksek maaş/OFFSET (11 Kasım 20:30 deneme, HAZIR), #5 LEFT JOIN+WHERE (12 Kasım 20:30 deneme, HAZIR). #6 BETWEEN tarih tuzağı (11 Kasım 12:30, HAZIR). Sıradaki: #7 NULL = NULL, #8 AVG ve NULL, #9 GROUP BY + HAVING COUNT, #10 IN/EXISTS. (DISTINCT vs GROUP BY "X mi Y mi" kancası düşük performanslı; atlandı.)
- 11 ve 12 Kasım kuyruk dosyalarında 20:30 deneme Reels zaten var: dosyayı EZME, diğer öğeleri EKLE. 13 Kasım'dan itibaren her gün 20:30 denemeyi sen üret.
- Konu kuralı (9 Kasım, Sergen onayıyla her gün deneme): aynı gün 12:30 Reels ile 20:30 deneme aynı konu OLAMAZ.
- 22 Kasım'da: deneme Reels 3 sn izlenme ve takipçi kazanımı karşılaştır, günlük denemeyi sürdür/ayarla.

## Durum (30 Ekim 2026 gece turu)
- Takipçi: 1.490 (Metricool, 28 Ekim). Son 7 gün: +1 kazanılan, -6 kaybedilen → net -5. Hedef hızın gerisinde (14 günde +40-70).
- Sıradaki ara hedef: 2.000.
- En iyi Reels: SQL çalışma sırası (29 Ekim): erişim 334, 3 sn %32,5, ort. 8,2 sn, 12 kaydetme. En kötü: Genie 4 haber: erişim 171, 3 sn %15,4, ort. 3,3 sn. Fark: kanca (SQL'de somut hata/soru, haberde şirket adı + animasyonlu giriş).

## Bu turun tek önceliği
Kanca: her Reels ilk karede tam görünen soru/hata/etki cümlesiyle açılıyor. Paylaşım çağrısı son sahnede ve açıklamada.

## Seriler
- "SQL Mülakat Sorusu #N": 1 Kasım LIKE ile #1 başladı. Her pazar ve en az haftada 2 kez devam. Sıradaki: #2 İkinci en yüksek maaş.
- "SQL Tuzağı": NULL (31 Ekim) ilk örnek. 7-10 gün sonra çalışma sırası açısı yeni örnekle tekrar (hedef 6-8 Kasım).

## Takvim notları
- 6 Kasım akşamı: SQL vs haber Reels verisi + "SQL ağırlığını artıralım mı" önerisi.
- 7-13 Kasım: saat A/B testi. 12 Kasım akşamı: hikâye verisi önerisi.

## Durum (31 Ekim 2026 gece turu)
- Takipçi: 1.490 (29 Ekim). Son 7 gün: +8 / -8 → net 0. Hedef hızın (14 günde +40-70) gerisinde.
- Son 7 gün Reels (3 sn izlenme): Apple Numbers haber %35,4 (en iyi; kanca somut fayda), SQL çalışma sırası %33,8, Genie 4 %18,6, DISTINCT/GROUP BY %8,9 (en kötü; kanca "aynı şey mi?" soyut, yanlış sonuç gösterilmiyordu).
- Ortalama 3 sn %24,2 (hedef ≥%35). (Paylaşım+kaydetme)/erişim: 37/1.060 = %3,5 (hedef ≥%5).
- Karar: SQL Reels kancası artık ilk karede YANLIŞ SONUCU da gösteriyor ("Sonuç: 90000. Yanlış!"). Soyut "fark ne?" kancası kullanılmayacak.
- Haber seçimi: Türkiye'de herkesin kullandığı uygulamalara (WhatsApp, Instagram, Gemini/ChatGPT) dokunan haberler öncelikli.
- 2 Kasım: SQL Mülakat Sorusu #2 (ikinci en yüksek maaş). Sıradaki #3: LEFT JOIN + WHERE tuzağı.

## Durum (1 Kasım 2026 gece turu)
- Takipçi: 1.497 (Metricool, 30 Ekim; sonrası henüz gelmedi). 25-30 Ekim: +9 / -8 → net +1. Hedef hızın (14 günde +40-70) çok gerisinde.
- Son 7 gün Reels 3 sn izlenme: NULL tuzağı %41,2 (en iyi; erişim 959, 1.244 izlenme, "HİÇ satır" kancası + ilk karede yanlış sonuç), SQL çalışma sırası %35,1, Apple Numbers %34,0, Gemini 4 Carbon %31,9, Genie 4 %18,9, DISTINCT/GROUP BY %12,3 (en kötü). Ort. %28,9 (hedef ≥%35). (Kaydetme+paylaşım)/erişim: 59/2.197 = %2,7 (hedef ≥%5).
- Karar: "kaybolan/yanlış satır" kancası (NULL'un kazanan açısı) SQL Mülakat Sorusu #3'te kullanıldı (LEFT JOIN + WHERE, 3 Kasım 18:00). Kural: SQL kancası = somut bir veri kaybı/yanlış sonuç + sayı ("4 müşteri vardı, 2 satır geldi").
- Haber: 31 Ekim-1 Kasım'da yaygın uygulamalara dokunan iki kaynaklı haber çıkmadı; 3 Kasım'da DeepSeek Super-Agent (kod ajanı) işlendi. Kitle verisi (kaydetme) teknik haberlerde düşükse 4 Kasım'dan itibaren haber seçiminde "kullanıcı uygulaması" önceliği sürer.
- Sıradaki seri: #4 CTE ya da tekrar eden kayıtları temizleme (ROW_NUMBER) — Trend Avcısı önerisi pencere fonksiyonları.

## Haftalık plan (2 Kasım 2026 Pazartesi turu)
- Takipçi: 1.507 (Metricool, 31 Ekim; 1-2 Kasım verisi henüz yok). 26-31 Ekim: +17 / -6 → net +11. Hedef (14 günde +40-70) gerisinde.
- Bu hafta hedefi: 1.540 (net +30/hafta). Sıradaki ara hedef: 2.000.
- Son 7 gün Reels 3 sn izlenme: LIKE #1 %39,7 (erişim 1.228, 17 kaydetme; en iyi), NULL %35,3 (1.328), çalışma sırası %34,8, Apple Numbers %34,0, Gemini 4 Carbon %29,1, Genie 4 %18,7, Gemini dosya düzenleme %19,2 (erişim 146; en kötü). SQL Reels erişimi haberin 3-8 katı.
- Hipotez (bu hafta test): "Mülakat Sorusu #N + ilk karede yanlış sonuç" kancası SQL'de %38+ 3 sn verir; haberde en yaygın uygulama (ChatGPT/WhatsApp) + "artık/yakında sen X" kancası %30 altına düşmez. Ölçüm 6 Kasım akşamı.
- Devam: SQL Mülakat serisi (#3 3 Kasım, #4 4 Kasım tekrar eden kayıtlar/ROW_NUMBER). Sıradaki #5: CTE ya da IN/EXISTS.
- Durdur: Teknik/kurumsal haber (model puanları, kurumsal araçlar). Haber yalnızca kitlenin kullandığı uygulamadan.
- 6 Kasım akşamı: veri iki hafta üst üste SQL lehine çıkarsa öneri günde 2 SQL'e yakın (haber 1/2 güne).

## Durum (3 Kasım 2026 gece turu)
- Takipçi: 1.516 (Metricool, 1 Kasım; 2-3 Kasım verisi henüz yok). 27 Ekim-1 Kasım: +29 / -6 → net +23. Haftalık hedef 1.540 yolunda; ara hedef 2.000.
- Son 7 gün Reels 3 sn: LIKE #1 %40,2 (en iyi, erişim 1.294), İkinci en yüksek maaş #2 %37,5, NULL %35,7; Gemini dosya %21,2 (en kötü, erişim 194), WhatsApp kapak %27,0. Ort. ~%30 (hedef ≥%35). (Kaydetme+paylaşım)/erişim ≈ %1,8 (hedef ≥%5) — asıl darboğaz.
- Karar: haber Reels'inde video içi paylaşım çağrısı hedef kişiye özel ("Ne izleyeceğini seçemeyen birine gönder"); bilgi kartı story'sinde "ekran görüntüsünü al" kaydetme çağrısı. 6 Kasım akşamı ölçülecek.
- 5 Kasım: 11:00 SQL (WHERE/HAVING, eski kalıp, kuyrukta), 18:00 haber (Netflix AI Discover). Sıradaki SQL Mülakat #5: LAG/LEAD (Trend Avcısı önerisi) ya da CTE.

## Durum (4 Kasım 2026 gece turu)
- Takipçi: 1.522 (Metricool, 2 Kasım; 3-4 Kasım verisi henüz yok). 28 Ekim-2 Kasım: 1.490 → 1.522, net +32 (~6/gün). Bu hızla 50.000'e ~7.500 gün: hedefin çok gerisinde.
- Son 7 gün Reels 3 sn: SQL ort. ~%35 (LEFT JOIN #3 %41,9; LIKE #1 %40,0; #2 %37,5), haber ort. ~%25 (Apple Numbers %33,8 en iyi; Genie 4 %19,3). Erişimin ~%75'i SQL Reels'ten. (Kaydetme+paylaşım)/erişim: 132/6.572 = %2,0 (hedef ≥%5).
- Bu tur değiştirdiğimiz: (1) İlk DENEME Reels'i 6 Kasım 18:00 (SQL Mülakat #5, LAG; takip etmeyenlere gider → yeni takipçi kanalı). Hafta için 1 deneme daha (7-8 Kasım, SQL tuzağı). (2) Günde 8 story: 13:30 kariyer/ilham + 16:00 hap haber eklendi; "Teknik Mülakat Taktiği #1" serisi başladı. (3) Haber seçimi öğrenci gündemine yöneldi (Google okul hesapları).
- Sıradaki SQL: CTE (#6), IN/EXISTS, SUM() OVER. 6 Kasım akşamı sütun oranı önerisi: veri SQL lehine, +1 SQL önerilecek.

## Durum (5 Kasım 2026 gece turu)
- Takipçi: 1.538 (Metricool, 3 Kasım; 4-5 Kasım verisi henüz yok). 29 Ekim-3 Kasım: 1.490 → 1.538, net +48 (~9,6/gün; önceki ölçümde ~6/gün). Bu hızla 50.000'e ~5.000 gün.
- Son 7 gün (14 Reels) 3 sn ort. %30,4; (kaydetme+paylaşım)/erişim 150/8.663 = %1,7. 18:00 SQL Reels: %35,8-40,1, erişim 1.116-1.480. 11:00 haber Reels: %22,7-29,0, erişim 153-372 (SQL'in ~1/5'i).
- Uyarı: içerik ve saat tamamen iç içe (haber hep 11:00, SQL hep 18:00) → A/B testi saat etkisini ölçemez. Karar: 8 Kasım'dan itibaren A/B günlerinde içerik slotu dönüşümlü (bir gün SQL öğlen, bir gün akşam). 8 Kasım Pazar: SQL 13:00, haber 21:00 (haber ≤72 sa kuralına dikkat).
- 7 Kasım: 13:00 haber (ChatGPT Images 2.6 GIF), 21:00 DENEME Reels SQL Mülakat #6 (NOT IN + NULL → 0 satır; "HİÇ satır" kazanan kancası). Haftanın 2. denemesi. Teknik Mülakat Taktiği #2 (NULL'ı sor) 14:00.
- Sıradaki SQL: CTE (#7), SUM() OVER, CASE WHEN, UNION/UNION ALL.
- 6 Kasım akşam önerisi (veri): SQL 6→7, haber 5→4.

## Durum (6 Kasım 2026 akşam turu) — sütun oranı kararı
- Takipçi: 1.547 (Metricool, 4 Kasım; 5-6 Kasım verisi henüz yok). 28 Ekim-4 Kasım: 1.490 → 1.547, net +57 (~8,1/gün). Bu hızla 50.000'e ~6.000 gün.
- Son 7 gün (31 Ekim-5 Kasım, 12 Reels) sütunlara göre: SQL 6 Reels, erişim 6.968 (ort. 1.161), 3 sn ort. %34,4, (kaydetme+paylaşım)/erişim %1,3. AI+teknoloji haberi 6 Reels, erişim 1.412 (ort. 235), 3 sn ort. %26,0, oran %2,2. Kariyer/ilham Reels: henüz yok. Deneme Reels: ilki 6 Kasım (veri yok).
- En iyi: NULL tuzağı (erişim 1.480, %35,8) ve LIKE #1 (1.331, %40,2, 25 kaydetme+paylaşım). En kötü: Netflix AI Discover (132, %22,7) ve eski kalıp WHERE/HAVING (649, %18,8; kancada yanlış sonuç yoktu).
- KARAR (9 Kasım haftasından): SQL 6→7, haber 5→4, kariyer 2, ilham 1. SQL'in erişimi haberin ~5 katı. Haber yüzde olarak daha çok kaydediliyor; o yüzden haber sıfırlanmıyor, yalnızca en güçlü 4 haber.
- Asıl darboğaz: (kaydetme+paylaşım)/erişim %1,5 (hedef ≥%5). Bu tur: 15:00 bilgi kartı "EKRAN GÖRÜNTÜSÜNÜ AL" kaydetme çağrısıyla. Ayrıca "Teknoloji Tarihinden #1" (Codd) ilham story serisi başladı.
- 8 Kasım: 13:00 SQL Mülakat #7 (UNION → ciro 750/1000, "kaybolan para" kancası), 21:00 haber (Siri AI Türkçe, iOS 27.3). Sıradaki SQL: CTE, SUM() OVER, CASE WHEN, IN/EXISTS. Haftanın 3. denemesi açılmadı (6 ve 7 Kasım deneme; 9-15 Kasım için 2-3 deneme planlanacak).

## Durum (7 Kasım 2026 gece turu)
- Takipçi: 1.549 (Metricool, 5 Kasım; 6-7 Kasım verisi gelmedi). 29 Ekim-5 Kasım net +59 (~8,4/gün). Bu hızla 50.000'e ~5.750 gün.
- 18 Reels (28 Ekim-6 Kasım): SQL 8 Reels ort. erişim 974, 3 sn %32,8; AI haber 8 Reels ort. erişim 241, %25,8. Deneme #5 LAG (6 Kasım): 3 sn %40,7 (dönemin en yükseği), erişim 528 (<24 sa), kaydetme oranı %0,6. "X mi Y mi" kancaları %19 civarı: kullanılmayacak. Story verisi Metricool'da yok.
- Karar: haber seçimi "Türkiye'deki kullanıcıya dokunan uygulama" (WhatsApp/Meta AI); ABD'ye özel haber yok (Google K-12 ve Netflix en kötü). 9 Kasım 20:30 SQL #8 CASE WHEN sırası DENEME Reels (haftanın 1. denemesi; 2. deneme 11-12 Kasım).
- Sıradaki SQL: CTE, SUM() OVER, IN/EXISTS, Index, PK/FK.

## Durum (8 Kasım 2026 gece turu)
- Takipçi: 1.551 (Metricool, 6 Kasım; 7-8 Kasım verisi gelmedi). 30 Ekim-6 Kasım net +54 (~7,7/gün). Bu hızla 50.000'e ~6.300 gün.
- 1-7 Kasım (14 Reels): SQL 7 Reels 3 sn ort. %34,2 (LIKE #1 %40,3 en iyi; WHERE/HAVING %19,5 en kötü), haber 7 Reels %25,7 (ChatGPT birleşme %28,5 en iyi; Netflix %23,0). (Kaydetme+paylaşım)/erişim 116/8.976 = %1,3. Deneme #6 NOT IN: %38,6, erişim 471. v2 stilin verisi henüz yok (ilk v2 içerikler 8 Kasım akşamı).
- Bu tur değiştirdiğimiz: deneme Reels'i olan akşamlarda duyuru story'si yerine "30 saniyelik test" (takipçi deneme Reels'i görmüyor); 9 Kasım 23:00 tekrar eden bilgi değiştirildi. "Teknoloji Tarihinden #2" (Hamilton) 10 Kasım 14:00.

## Durum (9 Kasım 2026 gece turu)
- Takipçi: 1.553 (Metricool, 7 Kasım; 8-9 Kasım verisi gelmedi). 31 Ekim-7 Kasım net +46 (~6,6/gün). Bu hızla 50.000'e ~7.370 gün. Hedefin çok gerisinde.
- 2-8 Kasım 14 Reels: SQL 7 ort. izlenme 1.155, 3 sn %32,3, (kayd.+payl.)/erişim %1,07; haber 7 ort. izlenme 261, %24,3, %1,81. Denemeler LAG/NOT IN %29,5 (deneme dışı mülakat #2-#4 %37,1). Yorum: 14 Reels'te 0. v2 verisi tek gönderi (WhatsApp %17,1) — yorumlanamaz. Story verisi yok.
- Bu tur değiştirdiğimiz: (1) 11 Kasım 12:30 haber yerine SQL TEST #6 (BETWEEN; aday haberler ABD'ye özel Gemini Memory ve küçük iOS 27.2.1 güncellemesiydi) → haber hap story'ye (17:00). Bu hafta SQL +1, haber -1; 13-15 Kasım'da en az 2 haber Reels'i (biri deneme) yerine konmalı. (2) Yorum 0 → açıklamada "Sen A mı dedin, B mi, C mi? Harfini yorumlara yaz" (tek harf = düşük eşik). 12 Kasım'da yorum sayısı ölçülecek.

## Durum (10 Kasım 2026 gece turu)
- 12 Kasım dolduruldu: 12:30 AI haber Reels (Instagram yapay zekâ ile yaş tahmini, Meta 9 Kasım), 20:30 SQL TEST #5 LEFT JOIN+WHERE (deneme → normal Reels; haftanın deneme sayısı 3'te kaldı). Hikâyeler: RAMAC günaydın, Teknoloji Tarihinden #3 (Katherine Johnson), Apple Türkiye 7 merkez hap haber, bit/Tukey iyi geceler.
- 9-15 Kasım dengesi (12 Kasım sonu): SQL 6, AI/haber 2, kariyer 0, ilham 0. 13-15 Kasım'daki 6 Reels: en az 3 haber, 2 teknoloji kariyeri/mülakat, 1 ilham (Teknoloji Tarihinden). Deneme Reels bu hafta artık yok.
- Analist (Metricool, 10 Kasım gece): takipçi 1.554 (8 Kasım; 1-8 Kasım net +38, ~5,4/gün → 50 bine ~8.900 gün). 3-9 Kasım 14 Reels: 3 sn ort. %25,4, (kayd.+payl.)/erişim %1,2, yorum 0. UYARI: v2 Reels (8-9 Kasım, 4 adet) ort. erişim 150 / 3 sn %19,5; eski stil (10 adet) 670 / %27,8. v2 gönderiler ≤2,5 günlük, kesin değil; v2 içinde en iyisi UNION (%36,8). 10-11 Kasım SQL TEST verisi gelince (12 Kasım turu) karar: v2'de kanca karesine somut sonuç/sayı + ilk 1 sn çizim; düşüş sürerse hesap sahibine eski kanca stiline dönüş önerilecek.

## Durum (11 Kasım 2026 gece turu)
- 13 Kasım dolduruldu: 12:30 SQL Mülakat Sorusu #9 COUNT(DISTINCT) + NULL (SQL + teknik mülakat sütunu), 20:30 AI haber Reels (ChatGPT eski sesli modlar 11 Aralık'ta kalkıyor; ilk çıkış 11 Kasım 01:07 TSİ, yayında ~67 sa). Deneme yok (haftada 3 deneme doldu: 9-10-11 Kasım). Hikâyeler: Hollerith kartı günaydın, Teknoloji Tarihinden #4 (Ada Lovelace), Apple Support Community kapanıyor hap haber, Ctrl+Alt+Del iyi geceler.
- 9-15 Kasım dengesi (13 Kasım sonu): SQL 7 (1'i mülakat), haber 3, kariyer (mülakat) 1, ilham 0. 14-15 Kasım'daki 4 Reels: 2 haber, 1 teknoloji kariyeri, 1 ilham (Teknoloji Tarihinden Reels) — SQL bu hafta tavanı aştı.
- Analist (Metricool, 11 Kasım gece): takipçi 1.555 (9 Kasım; 3-9 Kasım 1.538→1.555, net +17, ~2,8/gün → 50 bine ~17.000 gün). v2 Reels (8-10 Kasım, 6 adet) ort. erişim 150, 3 sn %19,4; eski stil (4-7 Kasım, 8 adet) ort. erişim 663, %26,6. v2 SQL TEST'ler: COUNT %28,0 / HAVING %11,5 / CASE %15,8 (erişim 122-165) vs eski SQL mülakat #4-#6 %29-37 (erişim 1.172-1.254). Yorum hâlâ 0.
- KARAR/ÖNERİ: v2'nin düşüşü 3 gündür sürüyor (yeni gönderiler genç ama fark 4 kat). Hesap sahibine öneri: SQL Reels'te eski kanca stiline (koyu zemin, tek büyük soru, kod ilk saniyede) dönülmesi ya da 1 gün A/B (aynı gün 1 v2 + 1 eski stil SQL). Hesap sahibinin açık v2 talebi nedeniyle onaysız geri dönülmedi.

## Durum (12 Kasım 2026 gece turu)
- 14 Kasım (Cumartesi) dolduruldu: 13:00 TEKNOLOJİ HABERİ Reels (GTA VI çıkış günü YouTube'da 24 saat yayın; YouTube Blog 12 Kasım 18:00 TSİ, yayında ~43 sa), 18:00 TEKNİK MÜLAKAT TAKTİĞİ #5 Reels (LIMIT 1 eşitlikte 1 kişiyi kaybeder; "2 kişi vardı, sorgu 1'ini getirdi"). Hikâyeler: Oracle V2 günaydın, SQL test (cevap 18:00), Teknoloji Tarihinden #5 Grace Hopper, GTA saat kartı, Gemini CarPlay hap haber, 17:30 duyuru, 21:30 özet, robot kelimesi iyi geceler. Deneme yok (hafta 3 deneme doldu).
- 9-15 Kasım dengesi (14 Kasım sonu): SQL 7, haber 4, kariyer/mülakat 2, ilham 0 → 15 Kasım: 1 haber + 1 ilham (Teknoloji Tarihinden Reels); 15 Kasım 10:00 SQL test story'si zorunlu (iyi geceler "yarın SQL testi" diyor).
- A/B SONUCU (7-12 Kasım, Metricool): öğlen slotu (12:30/13:00) normal Reels ort. erişim 322, 3 sn %26,9; akşam 20:30/21:00 deneme dışı Reels (2 haber) ort. erişim 128, 3 sn %12,6 (akşam SQL'lerin hepsi deneme olduğu için karışık). A/B öncesi 18:00 SQL Reels erişimi 1.100-1.480 idi. KARAR (14 Kasım'dan): Reels 1 hafta içi 12:30 / hafta sonu 13:00; Reels 2 18:00 (20:30/21:00 bırakıldı). Akşam duyurusu 17:00 (hafta içi) / 17:30 (hafta sonu); 21:30 özet, 23:00 iyi geceler.
- v2 YORUMU DEĞİŞTİ: v2 BETWEEN (SQL TEST #6, "4 sipariş vardı, 3 satır geldi") erişim 858, 3 sn %30,6 — eski stil seviyesinde. Zayıf v2'lerin kancası soyuttu (HAVING "hangisiyle süzersin" %11,6; CASE %16,6). Sorun stil değil kanca tipi. Kural: SQL/mülakat Reels kancası her zaman "X vardı, Y geldi" somut kayıp + sayı; eski stile dönüş önerisi geri çekildi.
- Analist: takipçi 1.555 (10 Kasım; 3-10 Kasım 1.538→1.555, net +17, ~2,4/gün → 50 bine ~20.000 gün). Yorum hâlâ 0 (14 Reels).

## Durum (13 Kasım 2026 gece turu)
- 15 Kasım (Pazar) dolduruldu: 13:00 YAPAY ZEKÂ HABERİ Reels (Gemini 4 Hydrogen dağıtılıyor; Google blog 12 Kasım 21:00 TSİ, yayında ~64 sa), 18:00 TEKNOLOJİ TARİHİNDEN #6 Reels (NCSA Mosaic: lisans öğrencisi + programcı). Hikâyeler: SQLite günaydın, SQL test SUM() OVER (cevap 14:00 kartında, o gün SQL Reels'i yok), Teknik Mülakat Taktiği #6 (çıktıyı önce söyle), AMD SSD sürücü hap haber, 17:30 duyuru, 21:30 özet, PostgreSQL iyi geceler. Deneme yok (hafta 3 doldu).
- 9-15 Kasım nihai: SQL 7, haber 5, kariyer/mülakat 2, ilham 1 = 15 Reels (14 hedef; SQL +1, A/B dönemindeki eski kayma).
- Analist (Metricool, 13 Kasım): takipçi 1.554 (11 Kasım; 4→11 Kasım net +7, ~1/gün → 50 bine ~48.000 gün). 6-12 Kasım 14 Reels: 3 sn %22,2, (kayd.+payl.)/erişim %0,84, yorum 0. SQL deneme dışı ort. erişim 681 / %28,8; haber 151 / %17,7; deneme SQL TEST'ler 125 / %16,5 (deneme formatı bu hesapta çalışmıyor). En iyi BETWEEN 1.117/%31,4 ("X vardı Y geldi").
- KARAR (16 Kasım haftası için öneri, pazartesi turu uygular): (1) Deneme Reels haftada 3 → 1 (veri: denemeler normalin 1/5'i erişim, 0 kaydetme); (2) haber Reels'i 5 → 4, SQL 6 → 7, hepsi "X vardı, Y geldi" somut kanca; (3) SQL TEST kapağında "SQL TEST #N:" etiketi başlıkta değil yalnızca rozette.
