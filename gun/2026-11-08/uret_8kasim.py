"""8 Kasım 2026 (Pazar, A/B: Reels 13:00 SQL + 21:00 haber). Kullanım: python3 uret_8kasim.py sql news stories"""
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
D = "/home/claude/sqlogreniyorum-medya/gun/2026-11-08/"
which = sys.argv[1:]

EKIM = [("Ali", 100), ("Ayşe", 200), ("Can", 150)]
KASIM = [("Ali", 100), ("Deniz", 300), ("Can", 150)]

if "sql" in which:
    def s_hook(d, t):
        pill(d, (70, 300), "SQL MÜLAKAT SORUSU #7", fill=YELLOW, size=40)
        y = hook_title(d, [("Ciro 1000 TL", TEXT), ("olmalıydı.", TEXT), ("SQL 750 dedi.", PINK)], 410, 118)
        code_box(d, (40, y + 30), ["SELECT SUM(tutar) FROM (", "  SELECT musteri, tutar FROM ekim",
                                   "  UNION", "  SELECT musteri, tutar FROM kasim);"],
                 size=38, w=1000, title="sorgu.sql")
        R.caption(d, t, "250 TL nereye gitti?", y + 460, start=1.0, size=58, col=RED, weight="Black")

    def s_data(d, t):
        R.caption(d, t, "ekim", 300, size=50, weight="ExtraBold")
        table(d, (40, 380), ["musteri", "tutar"], EKIM, [500, 480], size=40, hl_rows=[0, 2], hl_col=YELLOW)
        R.caption(d, t, "kasim", 800, start=0.6, size=50, weight="ExtraBold")
        if R.visible(t, 0.6):
            table(d, (40, 880 + R.rise(t, 0.6)), ["musteri", "tutar"], KASIM, [500, 480], size=40,
                  hl_rows=[0, 2], hl_col=YELLOW)
        R.caption(d, t, "Ali ve Can iki ay da [aynı] tutarı ödedi.", 1340, start=1.4, size=48, hl=YELLOW)

    def s_trap(d, t):
        pill(d, (70, 300), "NEDEN?", fill=RED, size=44)
        R.caption(d, t, "UNION tekrar eden satırları [siler].", 420, size=56, hl=PINK, weight="Bold")
        R.caption(d, t, "(Ali, 100) iki kez var.", 620, start=0.8, size=56, col=YELLOW, weight="Black")
        R.caption(d, t, "(Can, 150) iki kez var.", 760, start=1.3, size=56, col=YELLOW, weight="Black")
        R.caption(d, t, "UNION ikisini de bire indirdi.", 940, start=2.0, size=52, weight="Bold")
        R.caption(d, t, "6 satır yerine 4 satır: 750 TL.", 1120, start=2.7, size=52, col=RED, weight="Bold")

    def s_fix(d, t):
        pill(d, (70, 300), "ÇÖZÜM: UNION ALL", fill=GREEN, size=40)
        code_box(d, (40, 400), ["SELECT SUM(tutar) FROM (", "  SELECT musteri, tutar FROM ekim",
                                "  UNION ALL", "  SELECT musteri, tutar FROM kasim);"],
                 size=38, w=1000, title="sorgu.sql")
        if R.visible(t, 1.0):
            table(d, (40, 860 + R.rise(t, 1.0)), ["SUM(tutar)"], [(1000,)], [980], size=46,
                  hl_rows=[0], hl_col=GREEN)
        R.caption(d, t, "6 satırın hepsi kaldı: [1000] TL.", 1150, start=2.0, size=52, hl=GREEN)

    def s_rule(d, t):
        pill(d, (70, 330), "KURAL", fill=TEAL, size=44)
        y = 460
        for i, (a, b) in enumerate([("Tekrarlar gerçek kayıtsa", "UNION ALL"),
                                    ("Tekil liste istiyorsan", "UNION")]):
            st = 0.2 + i * 0.8
            if R.visible(t, st):
                yy = y + R.rise(t, st, 40)
                d.rounded_rectangle([50, yy, 1030, yy + 230], radius=26, fill=CARD, outline=LINE, width=2)
                d.text((90, yy + 40), a, font=font("Bold", 46), fill=TEXT)
                d.text((90, yy + 120), b, font=font("Black", 62), fill=YELLOW if i == 0 else TEAL)
            y += 270
        R.caption(d, t, "UNION ALL tekrar aramaz, [daha hızlı].", 1060, start=1.8, size=48, hl=GREEN)

    sc = [(2.9, s_hook), (3.6, s_data), (4.8, s_trap), (4.2, s_fix), (3.8, s_rule), (3.2, sql_cta)]
    print(reel("reel_union_all", sc, D, seed=81))

if "news" in which:
    sc = news_with_hook("YAPAY ZEKÂ", [("Akıllı Siri", TEXT), ("Türkçe", YELLOW), ("öğreniyor.", TEXT)],
                        "iOS 27.3 ile gelmesi bekleniyor.", [
        "Apple, Siri AI'a Türkçe desteğini duyurdu.",
        "Türkçe, eklenecek 4 yeni dilden biri.",
        "iOS 27.3 herkese açık betası 5 Kasım'da çıktı.",
        "Kararlı sürüm Aralık'ta bekleniyor.",
    ], "Tarih resmî değil; Türkçenin betada açılıp açılmadığı kaynaklarda net değil. Beta hata içerebilir, denemeden önce yedek al.",
        "Siri'yi Türkçe kullanır mısın?", "9to5Mac, iCulture, ShiftDelete (26 Ekim-5 Kasım 2026)")
    print(reel("reel_siri_turkce", sc, D, seed=83))

if "stories" in which:
    story_greeting(D + "story_gunaydin.png", "gunaydin", "Bluetooth adını bir kraldan aldı",
                   "Ad, 10. yüzyıl Danimarka kralı Harald \"Blåtand\" Gormsson'dan geliyor. 1996'da geçici "
                   "kod adı olarak önerildi ve kaldı.",
                   "Bugün 13:00 ve 21:00'de yeni Reels var.")
    story_poll(D + "story_1000_soru.png", "GÜNÜN SORUSU", "UNION, tekrar eden satırları ne yapar?",
               ["Hepsini tutar", "Birini bırakır", "Hata verir"], note="Cevabını DM'den yaz. Cevap 13:00 Reels'inde.")
    story_card(D + "story_1400_ilham.png", "TEKNOLOJİ TARİHİNDEN #1", "Codd'un [tablo] fikri", [
        "1970'te ilişkisel veri modelini yayımladı.",
        "Veriyi birbirine bağlı tablolarla düzenledi.",
        "Bu fikir System R'nin ve SQL'in temeli oldu.",
        "1981'de Turing Ödülü'nü kazandı.",
    ], footer="Kaynak: IBM, Britannica", tag_col=YELLOW)
    story_card(D + "story_1500_union_kart.png", "EKRAN GÖRÜNTÜSÜNÜ AL", "UNION mı, [UNION ALL] mı?", [
        "UNION: tekrar eden satırları bire indirir.",
        "UNION ALL: tüm satırları olduğu gibi tutar.",
        "Tekrarlar gerçek kayıtsa (ciro) UNION ALL.",
        "UNION ALL tekrar aramaz, genelde daha hızlı.",
    ], footer="SQL öğrenen bir arkadaşına gönder.", tag_col=TEAL)
    story_card(D + "story_1700_hap_findhub.png", "HAP HABER", "Unutursan [uyaracak]", [
        "Find Hub, takip cihazından uzaklaşınca uyarıyor.",
        "Takip cihazının Find Hub ayarlarından açılıyor.",
        "Şimdilik ABD ve Avrupa'nın bazı bölgelerinde.",
    ], footer="Kaynak: Engadget, 9to5Google (5-6 Kasım 2026)", tag_col=PINK)
    story_card(D + "story_2000_duyuru.png", "21:00'DE", "Siri [Türkçe] öğreniyor", [
        "Apple, Siri AI'a Türkçe desteğini duyurdu.",
        "Ne zaman herkese gelecek? 21:00 Reels'inde.",
    ], footer="Bunu bilmesi gereken birine gönder.", tag_col=PINK)
    story_card(D + "story_2200_ozet.png", "GÜNÜN ÖZETİ", "Bugün ne [öğrendik]?", [
        "UNION tekrar eden satırları siler.",
        "Ciro ve toplamda UNION ALL kullan.",
        "Siri AI'a Türkçe geliyor (iOS 27.3).",
    ], footer="Yarın yeni Reels var.")
    story_greeting(D + "story_iyigeceler.png", "iyigeceler", "Google bir yazım hatasıyla doğdu",
                   "Anlatılana göre 1997'de Stanford'da önerilen ad \"googol\"du (10 üzeri 100). Alan adı "
                   "aranırken \"google\" yazıldı; boştu ve kaydedildi.",
                   "Yarın yeni Reels var. İyi uykular.")
    print("stories ok")
