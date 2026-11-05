"""7 Kasım 2026 (Cumartesi, A/B: Reels 13:00 + 21:00). Kullanım: python3 uret_7kasim.py news sql stories"""
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
D = "/home/claude/sqlogreniyorum-medya/gun/2026-11-07/"
which = sys.argv[1:]

if "news" in which:
    sc = news_with_hook("YAPAY ZEKÂ", [("Yazdığın bir cümle", TEXT), ("hareketli bir", YELLOW),
                                       ("GIF'e dönüşebilir.", TEXT)],
                        "ChatGPT'ye GIF üretimi geliyor.", [
        "Metinden ya da fotoğraftan animasyonlu GIF.",
        "Hız ayarlanıyor, kareler tek tek düzenleniyor.",
        "Kendi ve evcil hayvan görselin saklanabiliyor.",
        "Özellik kullanıcılara kademeli açılıyor.",
    ], "Sticker ve meme tek komutla yapılabilecek. OpenAI'a göre yeni model Images 2.6; herkese ne zaman açılacağı belli değil.",
        "İlk GIF'ini ne yapardın?", "The Decoder, Thurrott, OpenAI (4-5 Kasım 2026)")
    print(reel("reel_chatgpt_gif", sc, D, seed=71))

if "sql" in which:
    MUS = [(1, "Ali"), (2, "Ayşe"), (3, "Can"), (4, "Deniz")]

    def s_hook(d, t):
        pill(d, (70, 300), "SQL MÜLAKAT SORUSU #6", fill=YELLOW, size=40)
        y = hook_title(d, [("Bu sorgu neden", TEXT), ("HİÇ satır", PINK), ("döndürmüyor?", TEXT)], 410, 118)
        code_box(d, (40, y + 30), ["SELECT ad FROM musteri", "WHERE id NOT IN (", "  SELECT musteri_id",
                                   "  FROM siparis);"], size=40, w=1000, title="sorgu.sql")
        R.caption(d, t, "Sonuç: 0 satır. Yanlış!", y + 460, start=1.0, size=58, col=RED, weight="Black")

    def s_data(d, t):
        R.caption(d, t, "musteri", 300, size=50, weight="ExtraBold")
        table(d, (40, 380), ["id", "ad"], MUS, [300, 680], size=40, hl_rows=[1, 3], hl_col=GREEN)
        R.caption(d, t, "siparis", 900, start=0.6, size=50, weight="ExtraBold")
        if R.visible(t, 0.6):
            table(d, (40, 980 + R.rise(t, 0.6)), ["id", "musteri_id"], [(10, 1), (11, 3), (12, "NULL")],
                  [300, 680], size=40, hl_rows=[2], hl_col=RED)
        R.caption(d, t, "Ayşe ve Deniz [sipariş] vermedi.", 1460, start=1.4, size=52, hl=YELLOW)

    def s_trap(d, t):
        pill(d, (70, 300), "NEDEN?", fill=RED, size=44)
        R.caption(d, t, "Listede bir [NULL] var.", 420, size=60, hl=PINK, weight="Bold")
        R.caption(d, t, "2 NOT IN (1, 3, NULL)", 620, start=0.8, size=58, col=YELLOW, weight="Black")
        R.caption(d, t, "SQL, NULL 2 mi bilemez.", 800, start=1.6, size=54, weight="Bold")
        R.caption(d, t, "Sonuç NULL olur, satır elenir.", 980, start=2.3, size=54, col=RED, weight="Bold")
        R.caption(d, t, "Tek NULL tüm sonucu [siler].", 1200, start=3.0, size=54, hl=PINK, weight="Bold")

    def s_fix(d, t):
        pill(d, (70, 300), "ÇÖZÜM: NOT EXISTS", fill=GREEN, size=40)
        code_box(d, (40, 400), ["SELECT ad FROM musteri m", "WHERE NOT EXISTS (", "  SELECT 1 FROM siparis s",
                                "  WHERE s.musteri_id = m.id);"], size=40, w=1000, title="sorgu.sql")
        if R.visible(t, 1.0):
            table(d, (40, 860 + R.rise(t, 1.0)), ["ad"], [("Ayşe",), ("Deniz",)], [980], size=42,
                  hl_rows=[0, 1], hl_col=GREEN)
        R.caption(d, t, "2 satır geldi. [Doğru] cevap.", 1250, start=2.0, size=52, hl=GREEN)

    def s_rule(d, t):
        pill(d, (70, 330), "KURAL", fill=TEAL, size=44)
        y = 460
        for i, (a, b) in enumerate([("Alt sorguda NULL olabilir mi?", "NOT EXISTS"),
                                    ("NOT IN kullanacaksan", "IS NOT NULL ekle")]):
            st = 0.2 + i * 0.8
            if R.visible(t, st):
                yy = y + R.rise(t, st, 40)
                d.rounded_rectangle([50, yy, 1030, yy + 230], radius=26, fill=CARD, outline=LINE, width=2)
                d.text((90, yy + 40), a, font=font("Bold", 46), fill=TEXT)
                d.text((90, yy + 120), b, font=font("Black", 62), fill=YELLOW if i == 0 else TEAL)
            y += 270
        R.caption(d, t, "IN'de sorun yok: Ali ve Can [gelir].", 1060, start=1.8, size=48, hl=GREEN)

    sc = [(2.9, s_hook), (3.4, s_data), (4.8, s_trap), (4.2, s_fix), (3.8, s_rule), (3.2, sql_cta)]
    print(reel("reel_not_in_null", sc, D, seed=73))

if "stories" in which:
    story_greeting(D + "story_gunaydin.png", "gunaydin", "Python adını yılandan almadı",
                   "Guido van Rossum Python'u yazmaya başlarken BBC'nin komedi dizisi Monty Python's Flying "
                   "Circus'ın senaryolarını okuyordu. Kısa, benzersiz bir isim istedi.",
                   "Bugün 13:00 ve 21:00'de yeni Reels var.")
    story_poll(D + "story_1000_soru.png", "GÜNÜN SORUSU", "2 NOT IN (1, 3, NULL) ne döndürür?",
               ["TRUE", "FALSE", "NULL"], note="Cevabını DM'den yaz. Cevap 21:00 Reels'inde.")
    story_card(D + "story_1400_kariyer.png", "TEKNİK MÜLAKAT TAKTİĞİ #2", "SQL sorusunda [NULL] sor", [
        "Önce sor: bu sütunda NULL olabilir mi?",
        "COUNT(*) ile COUNT(sütun) farkını söyle.",
        "NOT IN yerine NOT EXISTS'i neden seçtiğini anlat.",
        "Kenar durumları sesli söylemek artı puandır.",
    ], footer="Veri analisti mülakatına hazırlanan bir arkadaşına gönder.", tag_col=BLUE)
    story_card(D + "story_1500_gif_kart.png", "YAPAY ZEKÂ", "Neler [belli], neler değil?", [
        "Yeni görsel modeli: ChatGPT Images 2.6.",
        "Metinden ya da fotoğraftan GIF üretiyor.",
        "Özellik kullanıcılara kademeli açılıyor.",
        "Plan ve ülke bilgisi açıklanmadı.",
    ], footer="Kaynak: The Decoder, Thurrott, OpenAI (4-5 Kasım 2026)", tag_col=TEAL)
    story_card(D + "story_1700_hap_edits.png", "HAP HABER", "Edits artık [Mac'te]", [
        "Instagram'ın video kurgu uygulaması masaüstünde.",
        "Ücretsiz, filigransız 4K dışa aktarma var.",
        "Şimdilik yalnızca Mac; Windows için tarih yok.",
    ], footer="Kaynak: TechCrunch, Gulf News (5 Kasım 2026)", tag_col=PINK)
    story_card(D + "story_2000_duyuru.png", "21:00'DE", "Sorgu [HİÇ] satır vermedi.", [
        "4 müşteri vardı, 2'si sipariş vermemişti.",
        "Suçlu: listedeki tek bir NULL.",
    ], footer="SQL Mülakat Sorusu #6. Cevap 21:00 Reels'inde.", tag_col=PINK)
    story_card(D + "story_2200_ozet.png", "GÜNÜN ÖZETİ", "Bugün ne [öğrendik]?", [
        "ChatGPT'ye GIF üretimi kademeli geliyor.",
        "NOT IN listesinde NULL varsa sonuç boş kalır.",
        "Güvenli yol: NOT EXISTS.",
    ], footer="Yarın yeni Reels var.")
    story_greeting(D + "story_iyigeceler.png", "iyigeceler", "eBay'in ilk satışı: bozuk lazer",
                   "1995'te sitenin adı AuctionWeb'di. Pierre Omidyar bozuk lazer işaretçisini "
                   "satışa koydu. Ürün 14,83 dolara satıldı.",
                   "Yarın yeni Reels var. İyi uykular.")
    print("stories ok")
