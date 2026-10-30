"""31 Ekim Reels'lerinin kanca yenilemesi (t=0'da tam görünen kanca) + 1 Kasım içerikleri.
Kullanım: python3 uret_31ekim_1kasim.py r31news r31sql news sql stories
"""
import sys
sys.path.insert(0, "/home/claude/sqlogreniyorum-medya/araclar")
import reels as R
from uretim import reel, news_scenes, story_poll, story_card, story_greeting
from brand import *

G = "/home/claude/sqlogreniyorum-medya/gun/"
D31, D01 = G + "2026-10-31/", G + "2026-11-01/"
which = sys.argv[1:]


def fit_size(lines, size, max_w=940):
    """Kanca satırları ekrana sığana kadar punto küçült."""
    from PIL import Image, ImageDraw
    d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    while size > 60 and max(d.textlength(t, font=font("Black", size)) for t, _ in lines) > max_w:
        size -= 4
    return size


def hook_title(d, lines, y, size):
    """Animasyonsuz: ilk karede tam görünür."""
    size = fit_size(lines, size)
    fnt = font("Black", size)
    for txt, col in lines:
        d.text((70, y), txt, font=fnt, fill=col)
        y += int(size * 1.12)
    return y


def news_with_hook(tag, hook_lines, sub, points, takeaway, question, source):
    sc = news_scenes(tag, hook_lines, points, takeaway, question, source)

    def s_hook(d, t):
        pill(d, (70, 330), tag, fill=TEAL, size=38)
        y = hook_title(d, hook_lines, 450, 112)
        R.caption(d, t, sub, y + 50, start=1.0, size=52, col=PINK, weight="ExtraBold")

    def s_cta(d, t):
        y = hook_title(d, [("Bunu bilmesi", TEXT), ("gereken birine", YELLOW), ("gönder.", YELLOW)], 520, 104)
        y = R.caption(d, t, "Kaydet, sonra lazım olur.", y + 50, start=0.4, size=54, col=TEXT, weight="Bold")
        y = R.caption(d, t, "Her gün yapay zekâ ve SQL için takip et", y + 30, start=0.7, size=44, col=MUTED,
                      weight="SemiBold")
        if R.visible(t, 0.9):
            pill(d, (70, y + 50 + R.rise(t, 0.9)), HANDLE, fill=PINK, size=44)

    sc[0] = (2.5, s_hook)
    sc[-1] = (3.2, s_cta)
    return sc


def sql_cta(d, t):
    y = hook_title(d, [("SQL öğrenen bir", TEXT), ("arkadaşına", YELLOW), ("gönder.", YELLOW)], 520, 110)
    y = R.caption(d, t, "Kaydet, mülakatta sorulur.", y + 50, start=0.4, size=56, weight="Bold")
    y = R.caption(d, t, "Her gün yeni SQL ve teknoloji için takip et", y + 30, start=0.7, size=44, col=MUTED,
                  weight="SemiBold")
    if R.visible(t, 0.9):
        pill(d, (70, y + 50 + R.rise(t, 0.9)), HANDLE, fill=PINK, size=44)


# ------------------------------------------------------------------ 31 Ekim haber (yeniden)
if "r31news" in which:
    sc = news_with_hook("YAPAY ZEKÂ", [("Yapay zekâ artık", TEXT), ("güvenlik açığı", YELLOW), ("avlıyor.", TEXT)],
                        "Ama bu modeli henüz kullanamazsın.", [
        "Gemini 4 Carbon, Argon'dan iki hafta sonra geldi.",
        "Google'a göre Artificial Analysis'te 59 puanla birinci.",
        "Açık bulma testi SEC-bench Pro'da %88,2.",
        "Şimdilik yalnızca seçilmiş siber savunuculara açık.",
    ], "Yapay zekâ, yazılım açıklarını bulan bir güvenlik aracına dönüşüyor.",
        "Bu kadar güçlü bir model herkese açılmalı mı?", "Google Blog, 9to5Google (28 Ekim 2026)")
    print(reel("reel_gemini4_carbon_v2", sc, D31, seed=11))

# ------------------------------------------------------------------ 31 Ekim NULL (yeniden)
if "r31sql" in which:
    H = ["id", "ad", "telefon"]
    ROWS = [(1, "Ali", "5321"), (2, "Ayse", None), (3, "Can", "5442"), (4, "Ece", None), (5, "Mert", "5053")]
    QA = ["SELECT ad", "FROM musteriler", "WHERE telefon = NULL;"]
    QB = ["SELECT ad", "FROM musteriler", "WHERE telefon IS NULL;"]
    QC = ["SELECT ad,", "  COALESCE(telefon, 'yok')", "    AS telefon", "FROM musteriler;"]

    def s_hook(d, t):
        pill(d, (70, 330), "SQL TUZAĞI", fill=RED, size=40)
        y = hook_title(d, [("Bu sorgu neden", TEXT), ("HİÇ satır", YELLOW), ("döndürmüyor?", TEXT)], 440, 112)
        code_box(d, (40, y + 40), QA, size=44, w=1000, title="sorgu.sql")
        R.caption(d, t, "Sonuç: 0 satır", y + 380, start=1.0, size=72, col=RED, weight="Black")

    def s_data(d, t):
        R.caption(d, t, "Elimizde bu tablo var:", 420, size=60, weight="ExtraBold")
        table(d, (40, 560 + R.rise(t, 0.0)), H, ROWS, [180, 340, 480], size=40)
        R.caption(d, t, "2 müşterinin telefonu [NULL], yani bilinmiyor.", 1150, start=1.0, size=50, hl=RED)

    def s_trap(d, t):
        pill(d, (70, 380), "NEDEN?", fill=RED, size=44)
        code_box(d, (40, 500), QA, size=44, w=1000, title="sorgu.sql")
        R.caption(d, t, "NULL ile = karşılaştırması TRUE olmaz, [bilinmiyor] döner.", 860, start=0.4, size=50,
                  hl=YELLOW, weight="Bold")
        R.caption(d, t, "WHERE ise sadece TRUE olan satırları alır.", 1120, start=1.8, size=50, weight="Bold")

    def s_ok(d, t):
        pill(d, (70, 380), "DOĞRU", fill=GREEN, size=44)
        code_box(d, (40, 500), QB, size=44, w=1000, title="sorgu.sql")
        if R.visible(t, 1.0):
            table(d, (40, 860 + R.rise(t, 1.0)), ["ad"], [("Ayse",), ("Ece",)], [500], size=42)
        R.caption(d, t, "NULL kontrolü için = değil, [IS NULL] kullan.", 1200, start=1.8, size=52, hl=GREEN)

    def s_coal(d, t):
        pill(d, (70, 330), "BONUS: COALESCE", fill=TEAL, size=44)
        code_box(d, (40, 440), QC, size=42, w=1000, title="sorgu.sql")
        if R.visible(t, 1.0):
            table(d, (40, 830 + R.rise(t, 1.0)), ["ad", "telefon"],
                  [("Ali", "5321"), ("Ayse", "yok"), ("Can", "5442"), ("Ece", "yok"), ("Mert", "5053")],
                  [400, 500], size=38, hl_rows=[1, 3])
        R.caption(d, t, "NULL yerine [varsayılan] değer koyar.", 1320, start=2.2, size=50, hl=TEAL)

    sc = [(2.8, s_hook), (3.8, s_data), (5.0, s_trap), (4.5, s_ok), (5.5, s_coal), (3.2, sql_cta)]
    print(reel("reel_null_is_null_v2", sc, D31, seed=5))

# ------------------------------------------------------------------ 1 Kasım haber
if "news" in which:
    sc = news_with_hook("YAPAY ZEKÂ", [("Artık dosyanı", TEXT), ("sohbetten çıkmadan", YELLOW),
                                       ("düzenleyebilirsin.", TEXT)],
                        "PDF, belge, tablo, sunum.", [
        "PDF, Docs, Sheets ve sunumlar sohbet içinde düzenleniyor.",
        "Dosyayı tam ekrana açıp kendin yazabiliyorsun.",
        "Metni seç, Gemini'ye sor ya da düzelttir.",
        "PDF web ve mobilde, diğerleri şimdilik sadece webde.",
    ], "Ödev ve sunum hazırlarken uygulamalar arasında gidip gelme derdi azalıyor.",
        "En çok hangi dosyayı düzenletirdin?", "Google Workspace Blog, Digital Trends (29 Ekim 2026)")
    print(reel("reel_gemini_dosya_duzenleme", sc, D01, seed=13))

# ------------------------------------------------------------------ 1 Kasım SQL: LIKE tuzağı (SQL Mülakat Sorusu #1)
if "sql" in which:
    TAB = [(1, "ali_veli"), (2, "alixveli"), (3, "aliveli"), (4, "ali.veli")]
    QA = ["SELECT kullanici_adi", "FROM kullanicilar", "WHERE kullanici_adi", "  LIKE 'ali_veli';"]
    QB = ["SELECT kullanici_adi", "FROM kullanicilar", "WHERE kullanici_adi", "  LIKE 'ali!_veli' ESCAPE '!';"]

    def s_hook(d, t):
        pill(d, (70, 320), "SQL MÜLAKAT SORUSU #1", fill=YELLOW, size=40)
        y = hook_title(d, [("Tek kişiyi aradım,", TEXT), ("3 kişi geldi.", YELLOW), ("Neden?", PINK)], 430, 112)
        code_box(d, (40, y + 30), QA, size=40, w=1000, title="sorgu.sql")
        R.caption(d, t, "ali_veli, alixveli, ali.veli", y + 420, start=1.0, size=56, col=RED, weight="Black")

    def s_data(d, t):
        R.caption(d, t, "Tablomuz:", 400, size=60, weight="ExtraBold")
        table(d, (40, 540), ["id", "kullanici_adi"], TAB, [200, 600], size=42)
        R.caption(d, t, "Aradığımız sadece [ali_veli].", 1060, start=0.8, size=54, hl=YELLOW)

    def s_trap(d, t):
        pill(d, (70, 330), "NEDEN?", fill=RED, size=44)
        R.caption(d, t, "LIKE içinde [_] alt çizgi değil,", 450, size=58, hl=RED, weight="ExtraBold")
        R.caption(d, t, "herhangi TEK bir karakter demek.", 540, size=58, weight="ExtraBold")
        if R.visible(t, 1.0):
            table(d, (40, 720 + R.rise(t, 1.0)), ["kullanici_adi", "_ yerine gelen"],
                  [("ali_veli", "_"), ("alixveli", "x"), ("ali.veli", ".")], [520, 440], size=42)
        R.caption(d, t, "aliveli gelmedi: _ tam 1 karakter ister.", 1180, start=2.4, size=48, col=MUTED,
                  weight="SemiBold")

    def s_fix(d, t):
        pill(d, (70, 330), "DOĞRU", fill=GREEN, size=44)
        code_box(d, (40, 450), QB, size=40, w=1000, title="sorgu.sql")
        if R.visible(t, 1.0):
            table(d, (40, 860 + R.rise(t, 1.0)), ["kullanici_adi"], [("ali_veli",)], [600], size=42)
        R.caption(d, t, "[ESCAPE] ile _ joker olmaktan çıkar, gerçek alt çizgi aranır.", 1080, start=1.8,
                  size=50, hl=GREEN)

    def s_rules(d, t):
        R.caption(d, t, "Akılda kalsın:", 380, size=70, weight="Black")
        for i, (col, txt) in enumerate([(YELLOW, "_ = tam 1 karakter"),
                                         (TEAL, "% = 0 ya da daha fazla karakter"),
                                         (PINK, "'%veli' gibi başta % olan arama index'i kullanamaz.")]):
            st = 0.2 + i * 0.9
            if R.visible(t, st):
                y = 540 + i * 270 + R.rise(t, st)
                d.rounded_rectangle([40, y, 1040, y + 230], radius=28, fill=CARD, outline=col, width=4)
                d.text((80, y + 65), str(i + 1), font=font("Black", 80), fill=col)
                text_block(d, (180, y + 55), txt, font("Bold", 48), max_w=820)

    sc = [(2.8, s_hook), (3.4, s_data), (5.5, s_trap), (5.0, s_fix), (4.6, s_rules), (3.2, sql_cta)]
    print(reel("reel_like_joker", sc, D01, seed=17))

# ------------------------------------------------------------------ 1 Kasım story'leri
if "stories" in which:
    story_greeting(D01 + "story_gunaydin.png", "gunaydin", "İlk web sitesi CERN'de doğdu",
                   "Dünyanın ilk web sitesi info.cern.ch, 1990'ın sonunda CERN'de Tim Berners-Lee'nin NeXT "
                   "bilgisayarında yayına girdi. Site, WWW projesinin kendisini anlatıyordu.",
                   "Bugün 11:00 ve 18:30'da yeni Reels var. İyi pazarlar.")
    story_poll(D01 + "story_1000_soru.png", "GÜNÜN SORUSU", "Dosyalarını yapay zekâya düzenletir misin?",
               ["Evet", "Hayır", "Bazen"], note="Cevabını DM'den yaz. Konunun detayı 11:00 Reels'inde.")
    story_card(D01 + "story_1400_gemini_kart.png", "YAPAY ZEKÂ", "Sohbette dosya [düzenleme]", [
        "Google'a göre kişisel Google hesaplarına da açık.",
        "LaTeX, Markdown ve TXT dosyalarını da destekliyor.",
        "Sonucu PPTX ya da PDF olarak indirebiliyorsun.",
        "Gemini'nin desteklediği tüm dillerde çalışıyor.",
    ], footer="Kaynak: Google Workspace Blog, Digital Trends", tag_col=TEAL)
    story_card(D01 + "story_1730_duyuru.png", "18:30'DA", "Tek kişiyi aradım, [3 kişi] geldi.", [
        "Sorgu: WHERE kullanici_adi LIKE 'ali_veli'",
        "Tabloda ali_veli adında tek kullanıcı var.",
    ], footer="Cevap 18:30 Reels'inde. Kaçırma.", tag_col=PINK)
    story_card(D01 + "story_2130_ozet.png", "GÜNÜN ÖZETİ", "Bugün ne [öğrendik]?", [
        "Gemini'de PDF, belge ve sunumlar artık sohbetin içinde düzenlenebiliyor.",
        "LIKE'ta _ tam 1 karakter, % ise 0 ya da daha fazla karakter.",
        "Gerçek _ aramak için ESCAPE kullan.",
    ], footer="Yarın 11:00 ve 18:00'de yeni Reels.")
    story_greeting(D01 + "story_iyigeceler.png", "iyigeceler", "İlk bilgisayar faresi tahtadandı",
                   "Douglas Engelbart'ın 1960'larda geliştirdiği ilk farenin gövdesi ahşaptı, altında iki metal "
                   "tekerlek vardı. Patentteki adı: ekran için X-Y konum göstergesi.",
                   "Yarın 11:00 ve 18:00'de yeni Reels var. İyi uykular.")
    print("stories ok")
