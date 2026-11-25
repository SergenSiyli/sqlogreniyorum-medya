"""27 Kasım 2026 18:00 Reels (v5 koyu kod editörü + v6 "30 Günde SQL"): Gün 4/30 LIMIT — ORDER BY'sız LIMIT 3 "en çok satan 3"ü vermez.
Doğrulama: gun/2026-11-27/sql_dogrula.py. Sabah nöbeti 25 Kasım: son sahne "Arkadaşınla 30 gün" gönderme çağrısı, süre ≤14 sn."""
import sys
sys.path.insert(0, "/home/claude/sqlogreniyorum-medya/araclar")
from v5_ortak import *
from uretim import reel

D = "/home/claude/sqlogreniyorum-medya/gun/2026-11-27/"
ROWS = [(1, "Defter", 120), (2, "Kalem", 340), (3, "Silgi", 45), (4, "Çanta", 510), (5, "Cetvel", 80)]
QA = ["SELECT ad, satis", "FROM kirtasiye", "LIMIT 3;"]
QB = ["SELECT ad, satis", "FROM kirtasiye", "ORDER BY satis DESC", "LIMIT 3;"]


def s_hook(d, t):
    pill(d, (70, 280), "30 GÜNDE SQL · GÜN 4/30", fill=YELLOW, size=44)
    y = hook_title(d, [("En çok satan 3 ürünü", TEXT), ("istedim. 510 satan", TEXT), ("Çanta listede yok.", PINK)], 400, 92)
    y = code_box(d, (40, y + 40), QA, size=54, w=1000, title="top3.sql")
    d.rounded_rectangle([40, y + 40, 1040, y + 250], radius=26, fill=CARD, outline=RED, width=3)
    d.text((80, y + 70), "Defter · Kalem · Silgi", font=mono(64, True), fill=RED)
    d.text((80, y + 165), "Silgi 45 satışla 3. oldu", font=font("Black", 56), fill=RED)
    text_block(d, (70, y + 290), "LIMIT 3 yazdım. Neden?", font("ExtraBold", 64), fill=TEXT, max_w=940)


def s_fix(d, t):
    pill(d, (70, 280), "NEDEN?", fill=RED, size=46)
    y = table(d, (40, 390), ["id", "ad", "satis"], ROWS, [140, 480, 380], size=50, hl_rows=[3])
    y = R.caption(d, t, "LIMIT sıralamaz, [ilk gelen] 3 satırı keser.", y + 40, start=0.4, size=60,
                  hl=YELLOW, weight="ExtraBold")
    if R.visible(t, 1.5):
        yy = y + 30 + R.rise(t, 1.5, 40)
        pill(d, (70, yy), "DOĞRUSU", fill=GREEN, size=46)
        y2 = code_box(d, (40, yy + 100), QB, size=54, w=1000, title="top3.sql")
        if R.visible(t, 2.4):
            d.text((70, y2 + 25 + R.rise(t, 2.4, 30)), "Çanta · Kalem · Defter ✓", font=font("Black", 70), fill=GREEN)


def s_rule(d, t):
    pill(d, (70, 280), "KURAL", fill=TEAL, size=46)
    cards = [("LIMIT 3", "sırası garanti değil", RED), ("ORDER BY ... LIMIT 3", "gerçek ilk 3", GREEN),
             ("ORDER BY satis DESC LIMIT 1", "en çok satan: Çanta", YELLOW)]
    y = 400
    for i, (a, b, col) in enumerate(cards):
        st = 0.1 + i * 0.4
        if R.visible(t, st):
            yy = y + R.rise(t, st, 40)
            d.rounded_rectangle([40, yy, 1040, yy + 270], radius=26, fill=CARD, outline=LINE, width=2)
            d.text((80, yy + 40), a, font=mono(52, True), fill=TEXT)
            d.text((80, yy + 145), b, font=font("Black", 72), fill=col)
        y += 300
    R.caption(d, t, "LIMIT her zaman [ORDER\u00a0BY] ile gelir.", y + 30, start=1.4, size=72, hl=PINK, weight="ExtraBold")


def s_soru(d, t):
    pill(d, (70, 280), "YARIN · GÜN 5/30: DISTINCT", fill=YELLOW, size=46)
    yy = 400
    d.rounded_rectangle([40, yy, 1040, yy + 700], radius=26, fill=CARD, outline=LINE, width=2)
    for i, ln in enumerate(["SELECT ad", "FROM kirtasiye", "ORDER BY satis", "LIMIT 1;"]):
        d.text((80, yy + 40 + i * 88), ln, font=mono(64, True), fill=TEXT)
    text_block(d, (80, yy + 420), "Hangi ürün gelir? Yoruma sadece adını yaz.", font("ExtraBold", 72),
               fill=YELLOW, max_w=920)
    y = R.caption(d, t, "Kaçırmamak için takip et", yy + 760, start=0.3, size=68, weight="Black")
    if R.visible(t, 0.6):
        pill(d, (70, y + 40 + R.rise(t, 0.6)), HANDLE, fill=PINK, size=62)


def s_cta(d, t):
    pill(d, (70, 280), "ARKADAŞINLA 30 GÜN", fill=TEAL, size=46)
    y = hook_title(d, [("30 günü tek", TEXT), ("başına yapma.", TEXT)], 420, 116)
    y = hook_title(d, [("SQL'e başlamak", YELLOW), ("isteyen 1 kişiye", YELLOW), ("gönder.", YELLOW)], y + 60, 116)
    y = text_block(d, (70, y + 60), "Gün 1'den birlikte gidin.", font("ExtraBold", 84), fill=TEXT, max_w=940)
    pill(d, (70, y + 70), "Gönder", fill=TEAL, size=76)


sc = [(3.0, s_hook), (4.2, s_fix), (2.4, s_rule), (2.4, s_soru), (2.0, s_cta)]
print(reel("reel_30gun_sql_gun04_limit", sc, D, seed=94))
