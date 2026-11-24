"""26 Kasım 2026 18:00 Reels (v5 koyu kod editörü + v6 "30 Günde SQL"): Gün 3/30 ORDER BY — metin sütunda sayı sıralaması ('900' > '1250').
Doğrulama: gun/2026-11-26/sql_dogrula_gun3.py (tablo, yanlış ve doğru sonuç oradan)."""
import sys
sys.path.insert(0, "/home/claude/sqlogreniyorum-medya/araclar")
from v5_ortak import *
from uretim import reel

D = "/home/claude/sqlogreniyorum-medya/gun/2026-11-26/"
ROWS = [(1, "Kulaklık", "'900'"), (2, "Klavye", "'450'"), (3, "Monitör", "'1250'"), (4, "Mouse", "'250'")]
QA = ["SELECT ad, fiyat FROM urun", "ORDER BY fiyat DESC;"]
QB = ["SELECT ad, fiyat FROM urun", "ORDER BY CAST(fiyat", "  AS INTEGER) DESC;"]


def s_hook(d, t):
    pill(d, (70, 280), "30 GÜNDE SQL · GÜN 3/30", fill=YELLOW, size=44)
    y = hook_title(d, [("En pahalıdan ucuza", TEXT), ("sıraladım. En pahalısı", TEXT), ("en altta çıktı.", PINK)], 400, 92)
    y = code_box(d, (40, y + 40), QA, size=56, w=1000, title="fiyat.sql")
    d.rounded_rectangle([40, y + 40, 1040, y + 250], radius=26, fill=CARD, outline=RED, width=3)
    d.text((80, y + 70), "900 · 450 · 250 · 1250", font=mono(70, True), fill=RED)
    d.text((80, y + 165), "Monitör (1250) en sonda", font=font("Black", 56), fill=RED)
    text_block(d, (70, y + 290), "DESC yazdım. Neden?", font("ExtraBold", 64), fill=TEXT, max_w=940)


def s_fix(d, t):
    pill(d, (70, 280), "NEDEN?", fill=RED, size=46)
    y = table(d, (40, 390), ["id", "ad", "fiyat"], ROWS, [140, 440, 420], size=50, hl_rows=[0, 2])
    y = R.caption(d, t, "fiyat [metin] sütunu. Metin harf harf sıralanır: '9' > '1'.", y + 40, start=0.5, size=58,
                  hl=YELLOW, weight="ExtraBold")
    if R.visible(t, 1.8):
        yy = y + 30 + R.rise(t, 1.8, 40)
        pill(d, (70, yy), "DOĞRUSU", fill=GREEN, size=46)
        y2 = code_box(d, (40, yy + 100), QB, size=54, w=1000, title="fiyat.sql")
        if R.visible(t, 2.6):
            d.text((70, y2 + 25 + R.rise(t, 2.6, 30)), "Monitör 1250 en üstte ✓", font=font("Black", 70), fill=GREEN)


def s_rule(d, t):
    pill(d, (70, 280), "KURAL", fill=TEAL, size=46)
    cards = [("ORDER BY fiyat", "küçükten büyüğe (ASC)", YELLOW), ("ORDER BY fiyat DESC", "büyükten küçüğe", GREEN),
             ("metinde '1250' < '900'", "sayıyı sayı sakla", RED)]
    y = 400
    for i, (a, b, col) in enumerate(cards):
        st = 0.1 + i * 0.6
        if R.visible(t, st):
            yy = y + R.rise(t, st, 40)
            d.rounded_rectangle([40, yy, 1040, yy + 270], radius=26, fill=CARD, outline=LINE, width=2)
            d.text((80, yy + 40), a, font=mono(58, True), fill=TEXT)
            d.text((80, yy + 145), b, font=font("Black", 72), fill=col)
        y += 300
    R.caption(d, t, "ASC varsayılan; yazmasan da küçükten büyüğe [sıralar].", y + 30, start=2.0, size=60, hl=PINK,
              weight="ExtraBold")


def s_cta(d, t):
    pill(d, (70, 280), "YARIN · GÜN 4/30: LIMIT", fill=YELLOW, size=46)
    y = hook_title(d, [("SQL'e yeni başlayan", TEXT), ("arkadaşına", YELLOW), ("gönder.", YELLOW)], 400, 112)
    pill(d, (70, y + 40), "Gönder", fill=TEAL, size=62)
    yy = y + 190
    d.rounded_rectangle([40, yy, 1040, yy + 470], radius=26, fill=CARD, outline=LINE, width=2)
    for i, ln in enumerate(["SELECT ad FROM urun", "ORDER BY CAST(fiyat", "  AS INTEGER);"]):
        d.text((80, yy + 35 + i * 72), ln, font=mono(52, True), fill=TEXT)
    text_block(d, (80, yy + 270), "İlk satırda hangi ürün? Yoruma sadece adını yaz.", font("ExtraBold", 54),
               fill=YELLOW, max_w=920)
    y = R.caption(d, t, "Kaçırmamak için takip et", yy + 520, start=0.4, size=60, weight="Black")
    if R.visible(t, 0.7):
        pill(d, (70, y + 40 + R.rise(t, 0.7)), HANDLE, fill=PINK, size=54)


sc = [(3.2, s_hook), (4.8, s_fix), (3.2, s_rule), (4.0, s_cta)]
print(reel("reel_30gun_sql_gun03_order_by", sc, D, seed=93))
