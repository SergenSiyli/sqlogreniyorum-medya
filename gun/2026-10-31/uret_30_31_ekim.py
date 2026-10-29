import sys, os, json
sys.path.insert(0, "/home/claude/sqlogreniyorum-medya/araclar")
import reels as R
from uretim import reel, news_scenes, story_poll, story_card
from brand import *
G = "/home/claude/sqlogreniyorum-medya/gun/"
D30, D31 = G + "2026-10-30/", G + "2026-10-31/"
which = sys.argv[1:]

if "stories" in which:
    story_card(D30 + "story_1400_mcp_kart.png", "YAPAY ZEKÂ", "Numbers'a gelen [MCP] ne demek?", [
        "MCP, yapay zekâ ajanlarını uygulamalara bağlayan açık bir standart.",
        "Dış ajanlar Numbers, Pages ve Keynote içeriğini okuyup düzenleyebilecek.",
        "Güncelleme Kasım'da geliyor; şimdilik beta ve yalnızca ABD İngilizcesi.",
    ], footer="Detaylar öğlen Reels'inde.", tag_col=TEAL)
    story_card(D30 + "story_2130_ozet.png", "GÜNÜN ÖZETİ", "Bugün ne [öğrendik]?", [
        "Numbers, Pages ve Keynote'a yapay zekâ asistanı ve MCP desteği geliyor.",
        "DISTINCT yalnızca tekrar eden satırları atar.",
        "GROUP BY gruplar; COUNT, SUM, AVG ile hesap yaptırır.",
    ], footer="Yarın: Google'ın yeni modeli ve NULL tuzağı.")
    story_poll(D31 + "story_1000_soru.png", "GÜNÜN SORUSU",
               "Çok güçlü bir yapay zekâ herkese açılmalı mı?",
               ["Evet, hemen", "Önce test edilsin", "Hayır, açılmamalı"],
               note="Cevabını DM'den yaz. Konunun detayı 11:00 Reels'inde.")
    story_card(D31 + "story_1400_gemini_kart.png", "YAPAY ZEKÂ", "Gemini 4 Carbon [kimlere] açık?", [
        "Şimdilik yalnızca seçilmiş siber güvenlik ekiplerine.",
        "Erişim, Fairwind Programı ile genişleyecek.",
        "Model, yazılım açıklarını bulmaya odaklanıyor.",
        "Test puanları Google'ın kendi açıklaması.",
    ], footer="Kaynak: Google Blog, 9to5Google", tag_col=TEAL)
    story_card(D31 + "story_1730_duyuru.png", "18:30'DA", "WHERE telefon = NULL neden [boş] döner?", [
        "Tabloda telefonu NULL olan 2 müşteri var.",
        "Sorgu doğru görünüyor ama sonuç: 0 satır.",
    ], footer="Cevap 18:30 Reels'inde. Kaçırma.", tag_col=PINK)
    story_card(D31 + "story_2130_ozet.png", "GÜNÜN ÖZETİ", "Bugün ne [öğrendik]?", [
        "Google'ın Gemini 4 Carbon modeli şimdilik yalnızca siber güvenlik ekiplerine açık.",
        "= NULL hiçbir satır döndürmez; IS NULL kullan.",
        "COALESCE, NULL yerine varsayılan değer koyar.",
    ], footer="Kaydetmediysen Reels'e dön, mülakatta sorulur.")
    print("stories ok")

if "news" in which:
    sc = news_scenes("YAPAY ZEKÂ", [("Google'ın yeni", TEXT), ("modeli herkese", YELLOW), ("kapalı.", TEXT)], [
        "Gemini 4 Carbon, Argon'dan iki hafta sonra geldi.",
        "Google'a göre Artificial Analysis'te 59 puanla birinci.",
        "Açık bulma testi SEC-bench Pro'da %88,2.",
        "Şimdilik yalnızca seçilmiş siber savunuculara açık.",
    ], "Yapay zekâ, yazılım açıklarını bulan bir güvenlik aracına dönüşüyor.",
        "Bu kadar güçlü bir model herkese açılmalı mı?", "Google Blog, 9to5Google (28 Ekim 2026)")
    print(reel("reel_gemini4_carbon", sc, D31, seed=11))

if "sql" in which:
    H = ["id", "ad", "telefon"]
    ROWS = [(1, "Ali", "5321"), (2, "Ayse", None), (3, "Can", "5442"), (4, "Ece", None), (5, "Mert", "5053")]
    QA = ["SELECT ad", "FROM musteriler", "WHERE telefon = NULL;"]
    QB = ["SELECT ad", "FROM musteriler", "WHERE telefon IS NULL;"]
    QC = ["SELECT ad,", "  COALESCE(telefon, 'yok')", "    AS telefon", "FROM musteriler;"]

    def s_hook(d, t):
        R.big_title(d, t, [("= NULL", TEXT), ("çalışmaz.", YELLOW), ("Neden?", PINK)], y=600, size=130, step=0.3)
        R.caption(d, t, "Mülakatların klasik NULL tuzağı.", 1110, start=1.1, size=48, col=MUTED, weight="SemiBold")

    def s_data(d, t):
        R.caption(d, t, "Elimizde bu tablo var:", 420, size=60, weight="ExtraBold")
        if R.visible(t, 0.4):
            y = table(d, (40, 560 + R.rise(t, 0.4)), H, ROWS, [180, 340, 480], size=40)
        R.caption(d, t, "2 müşterinin telefonu [NULL], yani bilinmiyor.", 1150, start=1.4, size=50, hl=RED)

    def s_trap(d, t):
        pill(d, (70, 380), "TUZAK", fill=RED, size=44)
        chars = int(max(t - 0.3, 0) * 34)
        code_box(d, (40, 500), QA, size=44, w=1000, chars=chars, title="sorgu.sql")
        if R.visible(t, 2.2):
            R.caption(d, t, "Sonuç: 0 satır", 860, start=2.2, size=80, col=RED, weight="Black")
        R.caption(d, t, "NULL ile = karşılaştırması TRUE olmaz, [bilinmiyor] döner. WHERE ise sadece TRUE satırları alır.",
                  1020, start=3.2, size=46, hl=YELLOW, weight="SemiBold")

    def s_ok(d, t):
        pill(d, (70, 380), "DOĞRU", fill=GREEN, size=44)
        code_box(d, (40, 500), QB, size=44, w=1000, title="sorgu.sql", line_marks=None)
        if R.visible(t, 1.2):
            table(d, (40, 860 + R.rise(t, 1.2)), ["ad"], [("Ayse",), ("Ece",)], [500], size=42)
        R.caption(d, t, "NULL kontrolü için = değil, [IS NULL] kullan.", 1200, start=2.2, size=52, hl=GREEN)

    def s_coal(d, t):
        pill(d, (70, 330), "BONUS: COALESCE", fill=TEAL, size=44)
        code_box(d, (40, 440), QC, size=42, w=1000, title="sorgu.sql")
        if R.visible(t, 1.4):
            table(d, (40, 830 + R.rise(t, 1.4)), ["ad", "telefon"],
                  [("Ali", "5321"), ("Ayse", "yok"), ("Can", "5442"), ("Ece", "yok"), ("Mert", "5053")],
                  [400, 500], size=38, hl_rows=[1, 3])
        R.caption(d, t, "NULL yerine [varsayılan] değer koyar.", 1320, start=2.6, size=50, hl=TEAL)

    def s_rules(d, t):
        R.caption(d, t, "Akılda kalsın:", 400, size=70, weight="Black")
        for i, (col, txt) in enumerate([(YELLOW, "NULL bir değer değil, \"bilinmiyor\" demektir."),
                                         (GREEN, "NULL kontrolü için = değil, IS NULL kullan."),
                                         (TEAL, "COALESCE, NULL yerine varsayılan değer koyar.")]):
            st = 0.4 + i * 1.1
            if R.visible(t, st):
                y = 560 + i * 280 + R.rise(t, st)
                d.rounded_rectangle([40, y, 1040, y + 240], radius=28, fill=CARD, outline=col, width=4)
                d.text((80, y + 70), str(i + 1), font=font("Black", 80), fill=col)
                text_block(d, (180, y + 60), txt, font("Bold", 48), max_w=820)

    def s_cta(d, t):
        y = R.big_title(d, t, [("Kaydet,", TEXT), ("mülakatta", YELLOW), ("sorulur.", YELLOW)], y=600, size=110)
        y = R.caption(d, t, "Takip et, her gün yeni teknoloji ve SQL", y + 60, start=0.5, size=50, col=MUTED, weight="SemiBold")
        if R.visible(t, 0.8):
            pill(d, (70, y + 60 + R.rise(t, 0.8)), HANDLE, fill=PINK, size=44)

    sc = [(3.2, s_hook), (4.5, s_data), (7.0, s_trap), (5.5, s_ok), (6.5, s_coal), (5.0, s_rules), (3.5, s_cta)]
    print(reel("reel_null_is_null", sc, D31, seed=5))
