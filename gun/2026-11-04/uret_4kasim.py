"""4 Kasım 2026 (Çarşamba) içerikleri. Kullanım: python3 uret_4kasim.py news sql stories"""
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

D = "/home/claude/sqlogreniyorum-medya/gun/2026-11-04/"
which = sys.argv[1:]

if "news" in which:
    sc = news_with_hook("YAPAY ZEKÂ", [("Sohbet ettiğin", TEXT), ("yapay zekâ", YELLOW),
                                       ("işi de bitirecek.", TEXT)],
                        "ChatGPT'de Chat ve Work birleşiyor.", [
        "Masaüstü uygulamada Chat ve Work tek sekme oluyor.",
        "Dosyalarını ve eklentilerini sohbete getirebileceksin.",
        "Site, sunum ya da web'de iş yaptırabileceksin.",
        "Önce seçili kullanıcılara açılıyor.",
    ], "Şirketin açıklamasına göre ChatGPT ve Codex aynı kullanım hakkını paylaşacak; bazıları limite daha sık takılabilir.",
        "ChatGPT'yi en çok ne için kullanıyorsun?", "TechCrunch, tbreak (2 Kasım 2026)")
    print(reel("reel_chatgpt_chat_work", sc, D, seed=41))

if "sql" in which:
    H3 = ["id", "ad", "email"]
    ROWS = [(1, "Ali", "ali@x.com"), (2, "Ayse", "ayse@x.com"), (3, "Ali", "ali@x.com"),
            (4, "Can", "can@x.com"), (5, "Ayse", "ayse@x.com"), (6, "Ali", "ali@x.com")]

    def s_hook(d, t):
        pill(d, (70, 300), "SQL MÜLAKAT SORUSU #4", fill=YELLOW, size=40)
        y = hook_title(d, [("DISTINCT yazdım,", TEXT), ("tekrarlar", YELLOW), ("silinmedi.", PINK)], 410, 110)
        code_box(d, (40, y + 30), ["SELECT DISTINCT *", "FROM kayitlar;"], size=42, w=1000, title="sorgu.sql")
        R.caption(d, t, "6 satır vardı, yine 6 satır geldi.", y + 330, start=1.0, size=56, col=RED, weight="Black")

    def s_data(d, t):
        R.caption(d, t, "kayitlar", 330, size=52, weight="ExtraBold")
        table(d, (40, 420), H3, ROWS, [150, 300, 530], size=40, hl_rows=[2, 4, 5], hl_col=RED)
        R.caption(d, t, "Ali 3 kez, Ayse 2 kez [kayıtlı].", 1100, start=0.8, size=54, hl=YELLOW)

    def s_trap(d, t):
        pill(d, (70, 300), "NEDEN?", fill=RED, size=44)
        R.caption(d, t, "DISTINCT satırın [tüm sütunlarına] bakar.", 420, size=56, hl=YELLOW, weight="Bold")
        R.caption(d, t, "Ali'nin id'leri farklı: 1, 3, 6.", 680, start=0.9, size=56, weight="Bold")
        R.caption(d, t, "Bu yüzden 3 satır da \"farklı\" sayılır.", 850, start=1.6, size=52, col=RED, weight="Bold")
        R.caption(d, t, "Tekrarı belirleyen sütunu [sen] seçmelisin: email.", 1100, start=2.4, size=52,
                  hl=GREEN, weight="Bold")

    def s_fix(d, t):
        pill(d, (70, 300), "KOPYALARI BUL", fill=GREEN, size=40)
        code_box(d, (40, 400), ["SELECT id, ad,", "  ROW_NUMBER() OVER (", "    PARTITION BY email",
                                "    ORDER BY id) AS rn", "FROM kayitlar;"], size=38, w=1000, title="sorgu.sql")
        if R.visible(t, 1.0):
            table(d, (40, 930 + R.rise(t, 1.0)), ["id", "ad", "rn"],
                  [(1, "Ali", 1), (3, "Ali", 2), (6, "Ali", 3), (2, "Ayse", 1), (5, "Ayse", 2), (4, "Can", 1)],
                  [200, 400, 380], size=36, hl_rows=[1, 2, 4], hl_col=RED)
        R.caption(d, t, "rn > 1 olanlar [kopya]: id 3, 5, 6.", 1540, start=2.2, size=48, hl=YELLOW)

    def s_delete(d, t):
        pill(d, (70, 300), "SİL", fill=RED, size=44)
        code_box(d, (40, 400), ["WITH t AS (", "  SELECT id, ROW_NUMBER() OVER (", "    PARTITION BY email",
                                "    ORDER BY id) AS rn", "  FROM kayitlar)", "DELETE FROM kayitlar",
                                "WHERE id IN (SELECT id FROM t", "  WHERE rn > 1);"], size=34, w=1000,
                 title="temizle.sql")
        if R.visible(t, 1.2):
            table(d, (40, 1080 + R.rise(t, 1.2)), H3, [ROWS[0], ROWS[1], ROWS[3]], [150, 300, 530], size=38)
        R.caption(d, t, "Her kişiden [ilk kayıt] kaldı: 3 satır.", 1440, start=2.2, size=50, hl=GREEN)

    def s_rule(d, t):
        pill(d, (70, 330), "KURAL", fill=TEAL, size=44)
        y = 460
        for i, (a, b) in enumerate([("Tekrarı ne belirler?", "PARTITION BY"), ("Hangisi kalır?", "ORDER BY")]):
            st = 0.2 + i * 0.8
            if R.visible(t, st):
                yy = y + R.rise(t, st, 40)
                d.rounded_rectangle([50, yy, 1030, yy + 230], radius=26, fill=CARD, outline=LINE, width=2)
                d.text((90, yy + 40), a, font=font("Bold", 50), fill=TEXT)
                d.text((90, yy + 120), b, font=font("Black", 64), fill=YELLOW if i == 0 else TEAL)
            y += 270
        R.caption(d, t, "rn = 1 kalır, rn > 1 [silinir].", 1060, start=1.8, size=52, hl=PINK)

    sc = [(2.9, s_hook), (3.2, s_data), (4.2, s_trap), (4.6, s_fix), (4.2, s_delete), (3.6, s_rule), (3.2, sql_cta)]
    print(reel("reel_tekrar_kayit", sc, D, seed=43))

if "stories" in which:
    story_greeting(D + "story_gunaydin.png", "gunaydin", "İlk bilgisayar şifresi: 1961",
                   "1961'de MIT'nin CTSS sisteminde aynı bilgisayarı paylaşan kullanıcıların dosyalarını ayırmak "
                   "için şifre kullanıldı. Fernando Corbató bilgisayar şifresinin öncüsü sayılıyor.",
                   "Bugün 11:00 ve 18:00'de yeni Reels var.")
    story_poll(D + "story_1000_soru.png", "GÜNÜN SORUSU", "ChatGPT'yi en çok ne için kullanıyorsun?",
               ["Sohbet ve soru", "Ödev ya da iş", "Kod yazmak"],
               note="Cevabını DM'den yaz. Haber 11:00 Reels'inde.")
    story_card(D + "story_1400_chatgpt_kart.png", "YAPAY ZEKÂ", "Neler [belli], neler değil?", [
        "OpenAI değişikliği kullanıcılara e-postayla duyurdu.",
        "Codex masaüstünde ayrı bölüm olarak kalıyor.",
        "Ortak kullanım hakkının büyüklüğü açıklanmadı.",
        "Web ve mobile gelip gelmeyeceği belli değil.",
    ], footer="Kaynak: TechCrunch, tbreak (2 Kasım 2026)", tag_col=TEAL)
    story_card(D + "story_1700_duyuru.png", "18:00'DE", "DISTINCT yazdım, tekrarlar [silinmedi].", [
        "6 kayıt vardı, 3'ü kopya. Sonuç yine 6 satır.",
        "Suçlu: her satırın farklı bir id'si var.",
    ], footer="SQL Mülakat Sorusu #4. Cevap 18:00 Reels'inde.", tag_col=PINK)
    story_card(D + "story_2130_ozet.png", "GÜNÜN ÖZETİ", "Bugün ne [öğrendik]?", [
        "ChatGPT masaüstünde Chat ve Work sekmeleri birleşiyor.",
        "id farklıysa DISTINCT kopyaları göremez.",
        "ROW_NUMBER() OVER (PARTITION BY email) kopyaları bulur.",
    ], footer="Yarın 11:00 ve 18:00'de yeni Reels.")
    story_greeting(D + "story_iyigeceler.png", "iyigeceler", "İlk webcam bir kahve makinesiydi",
                   "1991'de Cambridge Üniversitesi'nde araştırmacılar, kahve kalmış mı diye görmek için kahve "
                   "makinesine kamera bağladı. Görüntü 1993'te web'e açıldı ve ilk webcam sayıldı.",
                   "Yarın 11:00 ve 18:00'de yeni Reels var. İyi uykular.")
    print("stories ok")
