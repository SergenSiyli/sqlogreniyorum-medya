"""29 Kasım 2026 18:00 Reels (v5 koyu kod editörü + v6 "30 Günde SQL"): Gün 6/30 AND / OR — AND, OR'dan önce çalışır.
Doğrulama: gun/2026-11-29/sql_dogrula.py (çıktı sql_dogrula_cikti.txt). 26 Kasım kuralı: ÇÖZÜM EN SONDA (DOĞRUSU ≥10. sn,
KURAL kartı yok, gönder + "Yarın Gün 7" DOĞRUSU sahnesinin son 2 sn'sinde 1.150-1.450 px), süre 14-17 sn."""
import sys
sys.path.insert(0, "/home/claude/sqlogreniyorum-medya/araclar")
from v5_ortak import *
from uretim import reel

D = "/home/claude/sqlogreniyorum-medya/gun/2026-11-29/"
QA = ["SELECT urun, stok FROM urunler", "WHERE kategori = 'Telefon'", "   OR kategori = 'Tablet'", "  AND stok > 0;"]
QB = ["SELECT urun, stok FROM urunler", "WHERE (kategori = 'Telefon'", "    OR kategori = 'Tablet')", "  AND stok > 0;"]
WRONG = [("Telefon Pro", "4"), ("Telefon Mini", "0"), ("Telefon Lite", "0"), ("Tablet 11", "3")]
RIGHT = [("Telefon Pro", "4"), ("Tablet 11", "3")]


def s_hook(d, t):
    pill(d, (70, 260), "30 GÜNDE SQL · GÜN 6/30", fill=YELLOW, size=44)
    y = hook_title(d, [("Stoktaki telefon ve", TEXT), ("tabletleri istedim.", TEXT), ("Stoğu 0 olanlar geldi.", PINK)], 370, 92)
    y = code_box(d, (40, y + 36), QA, size=50, w=1000, title="stok.sql")
    d.rounded_rectangle([40, y + 36, 1040, y + 250], radius=26, fill=CARD, outline=RED, width=3)
    d.text((80, y + 60), "Telefon Mini · 0", font=mono(52, True), fill=RED)
    d.text((80, y + 145), "Telefon Lite · 0", font=mono(52, True), fill=RED)
    text_block(d, (70, y + 290), "Neden?", font("Black", 96), fill=TEXT, max_w=940)


def s_neden(d, t):
    pill(d, (70, 260), "NEDEN?", fill=RED, size=46)
    y = table(d, (40, 370), ["urun", "stok"], WRONG, [640, 360], size=54, hl_rows=[1, 2])
    y = R.caption(d, t, "[AND] önce çalışır, OR sonra.", y + 40, start=0.4, size=66, hl=YELLOW, weight="ExtraBold")
    if R.visible(t, 2.0):
        yy = y + 30 + R.rise(t, 2.0, 30)
        d.text((70, yy), "SQL'in okuduğu:", font=font("Bold", 48), fill=MUTED)
        y = code_box(d, (40, yy + 70), ["kategori = 'Telefon'", "OR (kategori = 'Tablet'", "    AND stok > 0)"], size=50, w=1000)
    R.caption(d, t, "Telefonların [hepsi] geldi, stoğa bakılmadı.", y + 30, start=4.0, size=54,
              hl=PINK, weight="Bold")


def s_dogru(d, t):
    pill(d, (70, 260), "DOĞRUSU", fill=GREEN, size=46)
    y = code_box(d, (40, 370), QB, size=50, w=1000, title="stok.sql")
    if R.visible(t, 0.6):
        yy = y + 36 + R.rise(t, 0.6, 40)
        y2 = table(d, (40, yy), ["urun", "stok"], RIGHT, [640, 360], size=50)
        R.caption(d, t, "OR'u [parantezle] grupla.", y2 + 26, start=1.4, size=54, hl=YELLOW, weight="ExtraBold")
    if R.visible(t, 4.0):
        yy = 1300 + R.rise(t, 4.0, 40)
        d.rounded_rectangle([40, yy, 1040, yy + 190], radius=26, fill=CARD, outline=TEAL, width=3)
        d.text((80, yy + 25), "30 günü tek başına yapma:", font=font("ExtraBold", 54), fill=TEXT)
        d.text((80, yy + 105), "1 kişiye gönder →", font=font("Black", 58), fill=TEAL)
        pill(d, (70, yy + 220), "Yarın Gün 7/30: IN", fill=YELLOW, size=50)


sc = [(3.2, s_hook), (6.8, s_neden), (6.0, s_dogru)]
print(reel("reel_30gun_sql_gun06_and_or", sc, D, seed=96))
