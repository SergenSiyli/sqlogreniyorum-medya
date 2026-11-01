"""3 Kasım 2026 (Salı) içerikleri. Kullanım: python3 uret_3kasim.py news sql stories"""
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

D = "/home/claude/sqlogreniyorum-medya/gun/2026-11-03/"
which = sys.argv[1:]

if "news" in which:
    sc = news_with_hook("YAPAY ZEKÂ", [("Sen sormadan", TEXT), ("kod sorununa", YELLOW),
                                       ("çözüm öneren ajan.", TEXT)],
                        "DeepSeek açık kaynak prototipini duyurdu.", [
        "Adı Super-Agent, şimdilik bir prototip.",
        "Açık kaynak: geliştiriciler kodunu inceleyebiliyor.",
        "Geliştiricilerin grup sohbetlerini takip ediyor.",
        "Sohbette çıkan kodlama sorununu yakalıyor.",
        "Komut beklemeden çözüm öneriyor.",
    ], "Yapay zekâ, emir bekleyen asistandan kendisi iş bulan ekip arkadaşına dönüşüyor.",
        "Kodunu yapay zekâya izletir miydin?", "Investing.com, Seoul Economic Daily (1 Kasım 2026)")
    print(reel("reel_deepseek_superagent", sc, D, seed=31))

if "sql" in which:
    QA = ["SELECT m.ad, s.durum", "FROM musteriler m", "LEFT JOIN siparisler s", "  ON s.musteri_id = m.id",
          "WHERE s.durum = 'teslim';"]
    QB = ["SELECT m.ad, s.durum", "FROM musteriler m", "LEFT JOIN siparisler s", "  ON s.musteri_id = m.id",
          " AND s.durum = 'teslim';"]

    def s_hook(d, t):
        pill(d, (70, 300), "SQL MÜLAKAT SORUSU #3", fill=YELLOW, size=40)
        y = hook_title(d, [("LEFT JOIN yazdım,", TEXT), ("müşterilerin yarısı", YELLOW), ("kayboldu.", PINK)], 410, 100)
        code_box(d, (40, y + 30), QA, size=40, w=1000, title="sorgu.sql")
        R.caption(d, t, "4 müşteri vardı, 2 satır geldi.", y + 500, start=1.0, size=58, col=RED, weight="Black")

    def s_data(d, t):
        R.caption(d, t, "musteriler", 330, size=52, weight="ExtraBold")
        table(d, (40, 420), ["id", "ad"], [(1, "Ali"), (2, "Ayse"), (3, "Can"), (4, "Ece")], [200, 400], size=40)
        if R.visible(t, 0.8):
            yy = 900 + R.rise(t, 0.8)
            d.text((70, yy - 80), "siparisler", font=font("ExtraBold", 52), fill=TEXT)
            table(d, (40, yy), ["id", "musteri_id", "durum"],
                  [(101, 1, "teslim"), (102, 2, "iptal"), (103, 3, "teslim")], [200, 340, 380], size=40)
        R.caption(d, t, "Ece'nin hiç siparişi [yok].", 1330, start=1.8, size=52, hl=YELLOW)

    def s_trap(d, t):
        pill(d, (70, 300), "NEDEN?", fill=RED, size=44)
        R.caption(d, t, "Önce LEFT JOIN çalışır:", 410, size=52, weight="Bold")
        table(d, (40, 510), ["ad", "durum"], [("Ali", "teslim"), ("Ayse", "iptal"), ("Can", "teslim"), ("Ece", None)],
              [400, 500], size=42, hl_rows=[1, 3], hl_col=RED)
        R.caption(d, t, "Sonra WHERE çalışır: [iptal] ve [NULL] 'teslim' değil, satır atılır.", 1020, start=0.8,
                  size=50, hl=YELLOW, weight="Bold")
        R.caption(d, t, "LEFT JOIN sessizce INNER JOIN'e döndü.", 1270, start=2.2, size=50, col=RED, weight="Bold")

    def s_fix(d, t):
        pill(d, (70, 300), "DOĞRU", fill=GREEN, size=44)
        code_box(d, (40, 410), QB, size=40, w=1000, title="sorgu.sql")
        if R.visible(t, 1.0):
            table(d, (40, 900 + R.rise(t, 1.0)), ["ad", "durum"],
                  [("Ali", "teslim"), ("Ayse", None), ("Can", "teslim"), ("Ece", None)], [400, 500], size=40)
        R.caption(d, t, "Koşulu [ON] içine taşı: 4 müşteri de kalır.", 1400, start=2.0, size=50, hl=GREEN)

    def s_rule(d, t):
        pill(d, (70, 330), "KURAL", fill=TEAL, size=44)
        y = 460
        for i, (a, b) in enumerate([("Sağ tablonun filtresi", "ON içine"), ("Sol tablonun filtresi", "WHERE içine")]):
            st = 0.2 + i * 0.9
            if R.visible(t, st):
                yy = y + R.rise(t, st, 40)
                d.rounded_rectangle([50, yy, 1030, yy + 230], radius=26, fill=CARD, outline=LINE, width=2)
                d.text((90, yy + 40), a, font=font("Bold", 50), fill=TEXT)
                d.text((90, yy + 120), b, font=font("Black", 64), fill=YELLOW if i == 0 else TEAL)
            y += 270
        R.caption(d, t, "LEFT JOIN kullandıysan WHERE'deki [sağ tablo] koşuluna bak.", 1060, start=2.0, size=48,
                  hl=PINK)

    sc = [(2.9, s_hook), (3.8, s_data), (5.2, s_trap), (4.8, s_fix), (4.2, s_rule), (3.2, sql_cta)]
    print(reel("reel_left_join_where", sc, D, seed=33))

if "stories" in which:
    story_greeting(D + "story_gunaydin.png", "gunaydin", "İlk spam e-posta: 1978",
                   "3 Mayıs 1978'de DEC çalışanı Gary Thuerk, ARPANET üzerinden yaklaşık 400 kişiye aynı reklam "
                   "e-postasını gönderdi. Bu, bilinen ilk toplu spam e-postası sayılıyor.",
                   "Bugün 11:00 ve 18:00'de yeni Reels, 12:30'da JOIN rehberi var.")
    story_poll(D + "story_1000_soru.png", "GÜNÜN SORUSU", "Kodunu yapay zekâya izletir miydin?",
               ["Evet, hemen", "Sadece önerilerine bakarım", "Asla"],
               note="Cevabını DM'den yaz. Detaylar 11:00 Reels'inde.")
    story_card(D + "story_1400_deepseek_kart.png", "YAPAY ZEKÂ", "Ajan [nasıl] çalışıyor?", [
        "Yönlendiriciler sohbet ve e-postadan bilgi topluyor.",
        "Çalışan ajanlar kod incelemesi gibi işleri aynı anda yürütüyor.",
        "Sen tek bir ajanla konuşuyorsun, arkada birçoğu çalışıyor.",
        "Şirkete göre insan aynı anda ancak 3-5 sohbeti yönetebiliyor.",
    ], footer="Kaynak: Investing.com, Seoul Economic Daily (1 Kasım 2026)", tag_col=TEAL)
    story_card(D + "story_1700_duyuru.png", "18:00'DE", "LEFT JOIN yazdım, müşterilerin [yarısı] kayboldu.", [
        "4 müşteri vardı, sorgu 2 satır döndürdü.",
        "Suçlu tek bir satır: WHERE s.durum = 'teslim'",
    ], footer="SQL Mülakat Sorusu #3. Cevap 18:00 Reels'inde.", tag_col=PINK)
    story_card(D + "story_2130_ozet.png", "GÜNÜN ÖZETİ", "Bugün ne [öğrendik]?", [
        "DeepSeek, komut beklemeden çözüm öneren bir ajan duyurdu.",
        "WHERE'deki sağ tablo koşulu, eşleşmeyen satırları da atar.",
        "Sağ tablonun filtresini ON içine yaz.",
    ], footer="Yarın 11:00 ve 18:00'de yeni Reels.")
    story_greeting(D + "story_iyigeceler.png", "iyigeceler", "İlk solucan: Creeper (1971)",
                   "1971'de BBN'de Bob Thomas'ın yazdığı Creeper, ARPANET'te bilgisayardan bilgisayara geçip "
                   "\"I'M THE CREEPER: CATCH ME IF YOU CAN\" yazdı. Onu silmek için Reaper yazıldı.",
                   "Yarın 11:00 ve 18:00'de yeni Reels var. İyi uykular.")
    print("stories ok")
