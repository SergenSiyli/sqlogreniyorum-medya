"""2 Kasım 2026 (Pazartesi) içerikleri. Kullanım: python3 uret_2kasim.py news sql stories"""
import sys
sys.path.insert(0, "/home/claude/sqlogreniyorum-medya/araclar")
sys.path.insert(0, "/home/claude/sqlogreniyorum-medya/gun/2026-11-01")
import reels as R
from uretim import reel, story_poll, story_card, story_greeting
from brand import *
import importlib.util
spec = importlib.util.spec_from_file_location("k", "/home/claude/sqlogreniyorum-medya/gun/2026-11-01/uret_31ekim_1kasim.py")
_src = open(spec.origin).read().split("# ------------------------------------------------------------------ 31 Ekim haber")[0]
_ns = {}
exec(_src.replace("which = sys.argv[1:]", "which = []"), _ns)
hook_title, news_with_hook, sql_cta = _ns["hook_title"], _ns["news_with_hook"], _ns["sql_cta"]

D = "/home/claude/sqlogreniyorum-medya/gun/2026-11-02/"
which = sys.argv[1:]

if "news" in which:
    sc = news_with_hook("TEKNOLOJİ", [("Profiline yakında", TEXT), ("kapak fotoğrafı", YELLOW),
                                      ("koyabileceksin.", TEXT)],
                        "WhatsApp'ta iPhone testi başladı.", [
        "Kapak fotoğrafı iPhone beta sürümünde test ediliyor.",
        "Android beta kullanıcılarında zaten görünüyor.",
        "Fotoğraf çek, galeriden seç ya da Meta AI ile üret.",
        "Kimin göreceğini profil fotoğrafı gibi sen seçiyorsun.",
        "Şimdilik sadece bazı beta kullanıcılarında.",
    ], "Profilin daha görünür olacak: gizlilik ayarını şimdiden düşün.",
        "Kapak fotoğrafını kimlere açarsın?", "WABetaInfo, dijitaliyidir (31 Ekim 2026)")
    print(reel("reel_whatsapp_kapak", sc, D, seed=21))

if "sql" in which:
    H = ["ad", "maas"]
    ROWS = [("Ali", "90000"), ("Ayse", "90000"), ("Can", "75000"), ("Ece", "75000"), ("Mert", "60000")]
    QA = ["SELECT maas", "FROM calisanlar", "ORDER BY maas DESC", "LIMIT 1 OFFSET 1;"]
    QB = ["SELECT MAX(maas)", "FROM calisanlar", "WHERE maas < (", "  SELECT MAX(maas)", "  FROM calisanlar);"]
    QC = ["SELECT DISTINCT maas FROM (", "  SELECT maas, DENSE_RANK()", "    OVER (ORDER BY maas DESC)", "    AS sira", "  FROM calisanlar)", "WHERE sira = 2;"]

    def s_hook(d, t):
        pill(d, (70, 320), "SQL MÜLAKAT SORUSU #2", fill=YELLOW, size=40)
        y = hook_title(d, [("İkinci en yüksek", TEXT), ("maaşı bul.", YELLOW), ("Çoğu kişi yanlış yazıyor.", PINK)], 430, 104)
        code_box(d, (40, y + 30), QA, size=42, w=1000, title="sorgu.sql")
        R.caption(d, t, "Sonuç: 90000. Yanlış!", y + 420, start=1.0, size=64, col=RED, weight="Black")

    def s_data(d, t):
        R.caption(d, t, "Tablomuz: calisanlar", 400, size=60, weight="ExtraBold")
        table(d, (40, 540), H, ROWS, [400, 400], size=42, hl_rows=[0, 1])
        R.caption(d, t, "En yüksek maaş [90000] ve 2 kişide var.", 1180, start=0.8, size=52, hl=YELLOW)

    def s_trap(d, t):
        pill(d, (70, 330), "NEDEN?", fill=RED, size=44)
        code_box(d, (40, 450), QA, size=42, w=1000, title="sorgu.sql")
        R.caption(d, t, "OFFSET 1 ikinci [satırı] verir, ikinci [değeri] değil.", 860, start=0.4, size=52,
                  hl=YELLOW, weight="Bold")
        R.caption(d, t, "İkinci satır da 90000.", 1110, start=1.8, size=52, col=RED, weight="Bold")

    def s_fix(d, t):
        pill(d, (70, 330), "DOĞRU", fill=GREEN, size=44)
        code_box(d, (40, 450), QB, size=42, w=1000, title="sorgu.sql")
        if R.visible(t, 1.0):
            table(d, (40, 900 + R.rise(t, 1.0)), ["MAX(maas)"], [("75000",)], [500], size=44)
        R.caption(d, t, "En yüksekten [küçük] olanların en büyüğü.", 1140, start=1.8, size=52, hl=GREEN)

    def s_bonus(d, t):
        pill(d, (70, 330), "BONUS: N. EN YÜKSEK", fill=TEAL, size=44)
        code_box(d, (40, 440), QC, size=40, w=1000, title="sorgu.sql")
        if R.visible(t, 1.0):
            table(d, (40, 930 + R.rise(t, 1.0)), ["maas"], [("75000",)], [500], size=44)
        R.caption(d, t, "[DENSE_RANK] eşitlere aynı sırayı verir. 3. için sira = 3 yaz.", 1170, start=2.0,
                  size=48, hl=TEAL)

    sc = [(2.8, s_hook), (3.4, s_data), (4.6, s_trap), (4.6, s_fix), (5.2, s_bonus), (3.2, sql_cta)]
    print(reel("reel_ikinci_en_yuksek_maas", sc, D, seed=23))

if "stories" in which:
    story_greeting(D + "story_gunaydin.png", "gunaydin", "İlk SMS: Merry Christmas",
                   "3 Aralık 1992'de Neil Papworth, dünyanın ilk SMS'ini bir bilgisayardan telefona gönderdi. "
                   "Alıcı cevap veremedi: telefonlar o gün mesaj yazamıyordu.",
                   "Bugün 11:00 ve 18:00'de yeni Reels var. İyi haftalar.")
    story_poll(D + "story_1000_soru.png", "GÜNÜN SORUSU", "WhatsApp profiline kapak fotoğrafı koyar mısın?",
               ["Evet, hemen", "Sadece kişilerime", "Hayır"], note="Cevabını DM'den yaz. Detaylar 11:00 Reels'inde.")
    story_card(D + "story_1400_whatsapp_kart.png", "TEKNOLOJİ", "Kapak fotoğrafı [gizliliği]", [
        "Seçenekler: Herkes, Kişilerim, Kişilerim hariç, Hiç kimse.",
        "Varsayılan: Herkes. Değiştirmezsen herkes görür.",
        "Görsel yatay banta kırpılıp profilin üstünde durur.",
        "Kapak koymayanlar varsayılan bir görsel görür.",
    ], footer="Kaynak: WABetaInfo (31 Ekim 2026)", tag_col=TEAL)
    story_card(D + "story_1700_duyuru.png", "18:00'DE", "İkinci en yüksek maaş [90000] çıktı. Neden?", [
        "Sorgu: ORDER BY maas DESC LIMIT 1 OFFSET 1",
        "Tabloda en yüksek maaş 2 kişide var.",
    ], footer="SQL Mülakat Sorusu #2. Cevap 18:00 Reels'inde.", tag_col=PINK)
    story_card(D + "story_2130_ozet.png", "GÜNÜN ÖZETİ", "Bugün ne [öğrendik]?", [
        "WhatsApp kişisel profillere kapak fotoğrafını test ediyor.",
        "OFFSET 1 ikinci satırı verir, ikinci değeri değil.",
        "N. en yüksek değer için DENSE_RANK kullan.",
    ], footer="Yarın 11:00 ve 18:00'de yeni Reels.")
    story_greeting(D + "story_iyigeceler.png", "iyigeceler", "İlk YouTube videosu 19 saniye",
                   "YouTube'a yüklenen ilk video 'Me at the zoo', 23 Nisan 2005'te kurucu ortak Jawed Karim'in "
                   "hesabından yayınlandı. Konusu: hayvanat bahçesindeki filler.",
                   "Yarın 11:00 ve 18:00'de yeni Reels var. İyi uykular.")
    print("stories ok")
