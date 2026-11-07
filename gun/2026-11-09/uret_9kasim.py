"""9 Kasım 2026 (Pazartesi, A/B: Reels 12:30 haber + 20:30 SQL DENEME) ve 8 Kasım 21:00 haber değişimi
(Siri Türkçe 72 saat kuralına göre bayat). Kullanım: python3 uret_9kasim.py news8 stories8 sql news stories"""
import sys
sys.path.insert(0, "/home/claude/sqlogreniyorum-medya/araclar")
import reels as R
from uretim import reel, story_poll, story_card, story_greeting
from brand import *
_src = open("/home/claude/sqlogreniyorum-medya/gun/2026-11-01/uret_31ekim_1kasim.py").read().split(
    "# ------------------------------------------------------------------ 31 Ekim haber")[0]
_ns = {}
exec(_src.replace("which = sys.argv[1:]", "which = []"), _ns)
hook_title, news_with_hook, sql_cta = _ns["hook_title"], _ns["news_with_hook"], _ns["sql_cta"]
D = "/home/claude/sqlogreniyorum-medya/gun/2026-11-09/"
D8 = "/home/claude/sqlogreniyorum-medya/gun/2026-11-08/"
which = sys.argv[1:]

# ------------------------------------------------------------ 8 Kasım 21:00 haber (Siri yerine)
if "news8" in which:
    sc = news_with_hook("TEKNOLOJİ", [("Numaranı", TEXT), ("kimin göreceğini", YELLOW), ("seçebileceksin.", TEXT)],
                        "WhatsApp yeni bir gizlilik ayarı geliştiriyor.", [
        "Numara gizliliği için yeni ayar geliştiriliyor.",
        "Herkes / Kişilerim / Kişilerim, şunlar hariç / Hiç\u00a0kimse.",
        "Kullanıcı adı olanlarda varsayılan: Hiç\u00a0kimse.",
        "Numaranı kayıtlı tutanlar görmeye devam eder.",
    ], "Özellik henüz beta testine açık değil ve WhatsApp resmî bir çıkış tarihi açıklamadı.",
        "Numaranı gizleyip kullanıcı adıyla yazışır mıydın?",
        "PhoneWorld, ETV Bharat (WABetaInfo'ya dayanarak, 7 Kasım 2026)")
    print(reel("reel_whatsapp_numara", sc, D8, seed=85))

if "stories8" in which:
    story_card(D8 + "story_2000_duyuru_v2.png", "21:00'DE", "Numaran [gizlenebilir]", [
        "WhatsApp yeni bir numara gizliliği ayarı geliştiriyor.",
        "Kimler görecek, ne zaman gelecek? 21:00 Reels'inde.",
    ], footer="Bunu bilmesi gereken birine gönder.", tag_col=PINK)
    story_card(D8 + "story_2200_ozet_v2.png", "GÜNÜN ÖZETİ", "Bugün ne [öğrendik]?", [
        "UNION tekrar eden satırları siler.",
        "Ciro ve toplamda UNION ALL kullan.",
        "WhatsApp numara gizliliği ayarı geliştiriyor.",
    ], footer="Yarın yeni Reels var.")
    print("stories8 ok")

# ------------------------------------------------------------ 9 Kasım 20:30 SQL (DENEME)
ROWS_Y = [(1, 300, "küçük"), (2, 1500, "orta"), (3, 5000, "orta")]
ROWS_D = [(1, 300, "küçük"), (2, 1500, "orta"), (3, 5000, "büyük")]
QY = ["SELECT id, tutar,", "  CASE WHEN tutar > 1000 THEN 'orta'", "       WHEN tutar > 4000 THEN 'büyük'",
      "       ELSE 'küçük' END AS segment", "FROM siparisler;"]
QD = ["SELECT id, tutar,", "  CASE WHEN tutar > 4000 THEN 'büyük'", "       WHEN tutar > 1000 THEN 'orta'",
      "       ELSE 'küçük' END AS segment", "FROM siparisler;"]
H = ["id", "tutar", "segment"]

if "sql" in which:
    def s_hook(d, t):
        pill(d, (70, 300), "SQL MÜLAKAT SORUSU #8", fill=YELLOW, size=40)
        y = hook_title(d, [("5000 TL", TEXT), ("'büyük' olmalıydı.", TEXT), ("SQL 'orta' dedi.", PINK)], 410, 118)
        table(d, (40, y + 40), H, ROWS_Y, [200, 330, 450], size=42, hl_rows=[2], hl_col=RED)
        R.caption(d, t, "Neden?", y + 420, start=1.0, size=60, col=RED, weight="Black")

    def s_code(d, t):
        pill(d, (70, 300), "SORGU", fill=TEAL, size=40)
        code_box(d, (40, 400), QY, size=34, w=1000, title="segment.sql")
        R.caption(d, t, "Koşullar [doğru] gibi duruyor.", 930, start=0.6, size=52, hl=YELLOW)
        R.caption(d, t, "5000, 4000'den büyük değil mi?", 1060, start=1.4, size=52, col=PINK, weight="Bold")

    def s_trap(d, t):
        pill(d, (70, 300), "NEDEN?", fill=RED, size=44)
        R.caption(d, t, "CASE ilk doğru koşulda [durur].", 420, size=56, hl=PINK, weight="Bold")
        R.caption(d, t, "5000 > 1000 → doğru.", 620, start=0.8, size=58, col=YELLOW, weight="Black")
        R.caption(d, t, "'orta' yazıldı, CASE bitti.", 770, start=1.5, size=54, weight="Bold")
        R.caption(d, t, "> 4000 koşulu hiç denenmedi.", 920, start=2.3, size=54, col=RED, weight="Bold")

    def s_fix(d, t):
        pill(d, (70, 300), "ÇÖZÜM: SIRAYI ÇEVİR", fill=GREEN, size=40)
        code_box(d, (40, 400), QD, size=34, w=1000, title="segment.sql")
        if R.visible(t, 1.0):
            table(d, (40, 900 + R.rise(t, 1.0)), H, ROWS_D, [200, 330, 450], size=42,
                  hl_rows=[2], hl_col=GREEN)
        R.caption(d, t, "5000 artık [büyük].", 1340, start=2.0, size=54, hl=GREEN)

    def s_rule(d, t):
        pill(d, (70, 330), "KURAL", fill=TEAL, size=44)
        y = 460
        for i, (a, b) in enumerate([("CASE ilk doğru koşulda", "DURUR"),
                                    ("En dar koşulu", "EN ÜSTE YAZ")]):
            st = 0.2 + i * 0.8
            if R.visible(t, st):
                yy = y + R.rise(t, st, 40)
                d.rounded_rectangle([50, yy, 1030, yy + 230], radius=26, fill=CARD, outline=LINE, width=2)
                d.text((90, yy + 40), a, font=font("Bold", 46), fill=TEXT)
                d.text((90, yy + 120), b, font=font("Black", 62), fill=YELLOW if i == 0 else TEAL)
            y += 270
        R.caption(d, t, "Büyükten küçüğe [sırala].", 1060, start=1.8, size=50, hl=GREEN)

    sc = [(2.9, s_hook), (3.8, s_code), (4.6, s_trap), (4.4, s_fix), (3.8, s_rule), (3.2, sql_cta)]
    print(reel("reel_case_when_sira", sc, D, seed=91))

# ------------------------------------------------------------ 9 Kasım 12:30 haber
if "news" in which:
    sc = news_with_hook("YAPAY ZEKÂ", [("WhatsApp'taki", TEXT), ("Meta AI", YELLOW), ("yenileniyor.", TEXT)],
                        "Yeni modeller dağıtılmaya başladı.", [
        "Meta, 6 Kasım'da yeni modelleri dağıtmaya başladı.",
        "Meta AI, WhatsApp ve Instagram'ın içinde.",
        "Meta'ya göre sorunları adımlara bölüyor.",
        "Meta'ya göre daha isabetli takip soruları soruyor.",
    ], "Meta, 6 Kasım'da dağıtıma başladığını söyledi; ülke listesi verilmedi. İddialar Meta'nın kendi testleri.",
        "Yapay zekânın seni hatırlaması: rahatlatıcı mı, ürkütücü mü?",
        "Meta AI Research, RuntimeWire, ShiftDelete (6-7\u00a0Kasım)")
    print(reel("reel_meta_ai_model", sc, D, seed=93))

if "stories" in which:
    story_greeting(D + "story_gunaydin.png", "gunaydin", "Wi-Fi kara delik avından doğdu",
                   "1970'lerde CSIRO astronomları patlayan kara deliklerin sinyallerini aradı. Kara delik "
                   "bulunamadı ama geliştirilen matematik kablosuz ağları hızlandırdı.",
                   "Bugün 12:30 ve 20:30'da yeni Reels var.")
    story_poll(D + "story_1000_soru.png", "GÜNÜN SORUSU", "CASE WHEN'de iki koşul da doğruysa hangisi çalışır?",
               ["İlk doğru olan", "Son doğru olan", "Hata verir"],
               note="Cevabını DM'den yaz. Cevap 20:30 Reels'inde.")
    story_card(D + "story_1400_kariyer.png", "TEKNİK MÜLAKAT TAKTİĞİ #3", "Önce [örnek] tablo kur", [
        "Soruyu kendi cümlelerinle tekrar et.",
        "3-4 satırlık küçük bir örnek tablo çiz.",
        "Beklenen sonucu önce elle yaz.",
        "Sorguyu yazınca örnekle kontrol et.",
    ], footer="Veri analisti mülakatına hazırlanan bir arkadaşına gönder.", tag_col=BLUE)
    story_card(D + "story_1500_meta_kart.png", "YAPAY ZEKÂ", "Meta AI: [kısaca]", [
        "Meta AI'a yeni modeller dağıtılıyor.",
        "Ülke listesi verilmedi.",
        "Performans iddiaları Meta'nın kendi testleri.",
    ], footer="Kaynak: Meta AI Research, RuntimeWire (6 Kasım 2026)", tag_col=TEAL)
    story_card(D + "story_1700_hap_xr.png", "HAP HABER", "Akıllı gözlük [Aralık'ta]", [
        "İlk Android XR gözlükleri Aralık'ta çıkıyor.",
        "Warby Parker'a göre ön sipariş 12\u00a0Kasım'da.",
        "Fiyat ve ülke listesi henüz açıklanmadı.",
    ], footer="Kaynak: 9to5Google, The Gadgeteer (6 Kasım 2026)", tag_col=PINK)
    story_card(D + "story_1930_duyuru.png", "20:30'DA", "5000 TL neden ['orta']?", [
        "CASE WHEN'de sık yapılan bir sıra hatası.",
        "SQL Mülakat Sorusu #8, 20:30 Reels'inde.",
    ], footer="SQL öğrenen bir arkadaşına gönder.", tag_col=YELLOW)
    story_card(D + "story_2200_ozet.png", "GÜNÜN ÖZETİ", "Bugün ne [öğrendik]?", [
        "CASE ilk doğru koşulda durur.",
        "En dar koşulu en üste yaz.",
        "Meta AI'a yeni modeller dağıtılıyor.",
    ], footer="Yarın yeni Reels var.")
    story_greeting(D + "story_iyigeceler.png", "iyigeceler", "QR kod Go oyunundan ilham aldı",
                   "QR kodu 1994'te Denso Wave'den Masahiro Hara, araba parçalarını takip etmek için "
                   "geliştirdi. Hara'ya göre fikir Go oyununun siyah-beyaz taşlarından geldi.",
                   "Yarın yeni Reels var. İyi uykular.")
    print("stories ok")
