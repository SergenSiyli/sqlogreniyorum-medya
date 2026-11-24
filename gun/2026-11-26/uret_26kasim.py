"""26 Kasım 2026 18:00 Reels (v5 koyu kod editörü + v6 "30 Günde SQL"): Gün 2/30 WHERE, '=' harfi harfine karşılaştırır (izmir ≠ İzmir).
Doğrulama: gun/2026-11-26/sql_dogrula.py (tablo, yanlış ve doğru sonuç oradan)."""
import sys
sys.path.insert(0, "/home/claude/sqlogreniyorum-medya/araclar")
from v5_ortak import *
from uretim import reel

D = "/home/claude/sqlogreniyorum-medya/gun/2026-11-26/"
ROWS = [(1, "Ayşe", "İzmir"), (2, "Mert", "Ankara"), (3, "Zeynep", "İzmir"), (4, "Can", "Bursa")]
QA = ["SELECT ad FROM musteri", "WHERE sehir = 'izmir';"]
QB = ["SELECT ad FROM musteri", "WHERE sehir = 'İzmir';"]


def s_hook(d, t):
    pill(d, (70, 280), "30 GÜNDE SQL · GÜN 2/30", fill=YELLOW, size=44)
    y = hook_title(d, [("İzmirli müşterileri", TEXT), ("istedim.", TEXT), ("0 satır geldi.", PINK)], 400, 96)
    y = code_box(d, (40, y + 40), QA, size=56, w=1000, title="izmir.sql")
    d.rounded_rectangle([40, y + 40, 1040, y + 230], radius=26, fill=CARD, outline=RED, width=3)
    d.text((80, y + 80), "Sonuç: 0 satır", font=font("Black", 88), fill=RED)
    text_block(d, (70, y + 270), "Tabloda 2 İzmirli var. Neden?", font("ExtraBold", 64), fill=TEXT, max_w=940)


def s_fix(d, t):
    pill(d, (70, 280), "NEDEN?", fill=RED, size=46)
    y = table(d, (40, 390), ["id", "ad", "sehir"], ROWS, [160, 420, 420], size=50, hl_rows=[0, 2])
    y = R.caption(d, t, "Tabloda [İzmir] yazıyor. = harfi harfine bakar: izmir ≠ İzmir.", y + 40, start=0.5, size=60,
                  hl=YELLOW, weight="ExtraBold")
    if R.visible(t, 1.8):
        yy = y + 40 + R.rise(t, 1.8, 40)
        pill(d, (70, yy), "DOĞRUSU", fill=GREEN, size=46)
        y2 = code_box(d, (40, yy + 100), QB, size=56, w=1000, title="izmir.sql")
        if R.visible(t, 2.6):
            d.text((70, y2 + 30 + R.rise(t, 2.6, 30)), "Ayşe, Zeynep ✓", font=font("Black", 96), fill=GREEN)


def s_rule(d, t):
    pill(d, (70, 280), "KURAL", fill=TEAL, size=46)
    cards = [("sehir = 'izmir'", "0 satır", RED), ("sehir = 'İzmir'", "2 satır", GREEN),
             ("PostgreSQL, SQLite", "harfe duyarlı", YELLOW)]
    y = 400
    for i, (a, b, col) in enumerate(cards):
        st = 0.1 + i * 0.6
        if R.visible(t, st):
            yy = y + R.rise(t, st, 40)
            d.rounded_rectangle([40, yy, 1040, yy + 270], radius=26, fill=CARD, outline=LINE, width=2)
            d.text((80, yy + 40), a, font=mono(62, True), fill=TEXT)
            d.text((80, yy + 145), b, font=font("Black", 74), fill=col)
        y += 300
    R.caption(d, t, "MySQL ve SQL Server çoğu ayarda duyarsız. Yine de metni [tablodaki] gibi yaz.", y + 30, start=2.0, size=60, hl=PINK,
              weight="ExtraBold")


def s_cta(d, t):
    pill(d, (70, 280), "YARIN · GÜN 3/30: ORDER BY", fill=YELLOW, size=46)
    y = hook_title(d, [("SQL'e yeni başlayan", TEXT), ("arkadaşına", YELLOW), ("gönder.", YELLOW)], 400, 112)
    pill(d, (70, y + 40), "Gönder", fill=TEAL, size=62)
    yy = y + 190
    d.rounded_rectangle([40, yy, 1040, yy + 420], radius=26, fill=CARD, outline=LINE, width=2)
    d.text((80, yy + 35), "SELECT ad FROM musteri", font=mono(52, True), fill=TEXT)
    d.text((80, yy + 110), "WHERE sehir <> 'İzmir';", font=mono(52, True), fill=TEXT)
    text_block(d, (80, yy + 210), "Kaç satır döner? Yoruma sadece sayıyı yaz.", font("ExtraBold", 56),
               fill=YELLOW, max_w=920)
    y = R.caption(d, t, "Kaçırmamak için takip et", yy + 470, start=0.4, size=60, weight="Black")
    if R.visible(t, 0.7):
        pill(d, (70, y + 40 + R.rise(t, 0.7)), HANDLE, fill=PINK, size=54)


sc = [(3.2, s_hook), (4.8, s_fix), (3.2, s_rule), (4.0, s_cta)]
print(reel("reel_30gun_sql_gun02_where", sc, D, seed=92))
