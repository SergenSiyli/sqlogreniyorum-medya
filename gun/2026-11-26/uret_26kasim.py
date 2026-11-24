"""26 Kasım 2026 18:00 Reels (v5 koyu kod editörü + v6 "30 Günde SQL" serisi): Gün 1/30 SELECT, tek tırnaklı sütun adı tuzağı.
Doğrulama: gun/2026-11-26/sql_dogrula.py (tablo, yanlış ve doğru sonuç oradan)."""
import sys
sys.path.insert(0, "/home/claude/sqlogreniyorum-medya/araclar")
from v5_ortak import *
from uretim import reel

D = "/home/claude/sqlogreniyorum-medya/gun/2026-11-26/"
QA = ["SELECT 'ad'", "FROM musteri;"]
QB = ["SELECT ad", "FROM musteri;"]
WRONG = [("ad",), ("ad",), ("ad",), ("ad",)]
RIGHT = [("Ayşe",), ("Mert",), ("Zeynep",), ("Can",)]


def s_hook(d, t):
    pill(d, (70, 280), "30 GÜNDE SQL · GÜN 1/30", fill=YELLOW, size=44)
    y = hook_title(d, [("Müşteri adlarını", TEXT), ("istedim. Her satırda", YELLOW), ("'ad' yazdı.", PINK)], 400, 92)
    y = code_box(d, (40, y + 40), QA, size=60, w=1000, title="musteriler.sql")
    y = table(d, (40, y + 40), ["'ad'"], WRONG, [1000], size=50, hl_rows=[0, 1, 2, 3], hl_col=RED)
    text_block(d, (70, y + 30), "4 müşteri, 4 kez 'ad'. Neden?", font("Black", 66), fill=RED, max_w=940)


def s_fix(d, t):
    pill(d, (70, 280), "NEDEN?", fill=RED, size=46)
    y = R.caption(d, t, "Tek tırnak = [metin]. SQL her satıra aynı yazıyı basar.", 390, size=66, hl=YELLOW,
                  weight="ExtraBold")
    if R.visible(t, 1.4):
        yy = y + 50 + R.rise(t, 1.4, 40)
        pill(d, (70, yy), "DOĞRUSU: TIRNAKSIZ", fill=GREEN, size=46)
        y2 = code_box(d, (40, yy + 110), QB, size=60, w=1000, title="musteriler.sql")
        if R.visible(t, 2.2):
            table(d, (40, y2 + 40 + R.rise(t, 2.2, 30)), ["ad"], RIGHT, [1000], size=50, hl_rows=[0, 1, 2, 3],
                  hl_col=GREEN)


def s_rule(d, t):
    pill(d, (70, 280), "KURAL", fill=TEAL, size=46)
    cards = [("SELECT 'ad'", "metin: hep aynı", RED), ("SELECT ad", "sütun: gerçek veri", GREEN),
             ('SELECT "ad"', "sütun (çift tırnak)", YELLOW)]
    y = 400
    for i, (a, b, col) in enumerate(cards):
        st = 0.1 + i * 0.6
        if R.visible(t, st):
            yy = y + R.rise(t, st, 40)
            d.rounded_rectangle([40, yy, 1040, yy + 280], radius=26, fill=CARD, outline=LINE, width=2)
            d.text((80, yy + 40), a, font=mono(66, True), fill=TEXT)
            d.text((80, yy + 150), b, font=font("Black", 78), fill=col)
        y += 315
    R.caption(d, t, "Tek tırnak [değer] içindir, sütun adı için değil.", y + 30, start=2.0, size=62, hl=PINK,
              weight="ExtraBold")


def s_cta(d, t):
    pill(d, (70, 280), "YARIN · GÜN 2/30: WHERE", fill=YELLOW, size=46)
    y = hook_title(d, [("SQL'e yeni başlayan", TEXT), ("arkadaşına", YELLOW), ("gönder.", YELLOW)], 400, 112)
    pill(d, (70, y + 40), "Gönder", fill=TEAL, size=62)
    yy = y + 190
    d.rounded_rectangle([40, yy, 1040, yy + 420], radius=26, fill=CARD, outline=LINE, width=2)
    d.text((80, yy + 35), "SELECT 'merhaba'", font=mono(56, True), fill=TEXT)
    d.text((80, yy + 115), "FROM musteri;", font=mono(56, True), fill=TEXT)
    text_block(d, (80, yy + 215), "4 müşteri var. Kaç satır döner? Yoruma sadece sayıyı yaz.", font("ExtraBold", 54),
               fill=YELLOW, max_w=920)
    y = R.caption(d, t, "Kaçırmamak için takip et", yy + 470, start=0.4, size=60, weight="Black")
    if R.visible(t, 0.7):
        pill(d, (70, y + 40 + R.rise(t, 0.7)), HANDLE, fill=PINK, size=54)


sc = [(3.2, s_hook), (4.6, s_fix), (3.2, s_rule), (4.0, s_cta)]
print(reel("reel_30gun_sql_gun01_select", sc, D, seed=91))
