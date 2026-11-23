"""25 Kasım 2026 18:00 Reels (v5 koyu kod editörü, EKRANI DOLDUR kuralı): SQL Mülakat Sorusu #14 ay sonu tarih tuzağı.
Doğrulama: gun/2026-11-25/sql_dogrula.py"""
import sys
sys.path.insert(0, "/home/claude/sqlogreniyorum-medya/araclar")
from v5_ortak import *
from uretim import reel

D = "/home/claude/sqlogreniyorum-medya/gun/2026-11-25/"
ROWS = [(1, "2026-11-03 10:15", 1200), (2, "2026-11-17 09:40", 800), (3, "2026-11-29 16:05", 500),
        (4, "2026-11-30 11:30", 700), (5, "2026-11-30 19:45", 900), (6, "2026-12-01 08:10", 400)]
QA = ["SELECT SUM(tutar)", "FROM siparis", "WHERE tarih >= '2026-11-01'", "  AND tarih <= '2026-11-30';"]
QB = ["SELECT SUM(tutar)", "FROM siparis", "WHERE tarih >= '2026-11-01'", "  AND tarih < '2026-12-01';"]


def s_hook(d, t):
    pill(d, (70, 290), "SQL MÜLAKAT SORUSU #14", fill=YELLOW, size=42)
    y = hook_title(d, [("Kasım cirosunu çektim.", TEXT), ("30 Kasım'ın hepsi", YELLOW), ("eksik geldi.", PINK)], 420, 92)
    y = code_box(d, (40, y + 50), QA, size=54, w=1000, title="kasim_ciro.sql")
    y = text_block(d, (70, y + 50), "Rapor: 2.500 TL", font("Black", 88), fill=RED, max_w=940)
    y = text_block(d, (70, y + 16), "Olması gereken: 4.100 TL.", font("ExtraBold", 62), fill=TEXT, max_w=940)
    text_block(d, (70, y + 16), "1.600 TL nereye gitti?", font("ExtraBold", 62), fill=YELLOW, max_w=940)


def s_data(d, t):
    R.caption(d, t, "siparis", 290, size=64, weight="ExtraBold")
    y = table(d, (40, 400), ["id", "tarih", "tutar"], ROWS, [150, 580, 270], size=52, hl_rows=[3, 4])
    y = R.caption(d, t, "30 Kasım'da [2] sipariş var: 700 + 900 TL.", y + 70, start=0.6, size=70, hl=YELLOW,
                  weight="ExtraBold")
    R.caption(d, t, "Sorgu ikisini de saymadı.", y + 50, start=1.4, size=76, col=RED, weight="Black")


def s_trap(d, t):
    pill(d, (70, 290), "NEDEN?", fill=RED, size=46)
    y = R.caption(d, t, "Sütunda [saat] de var. Karşılaştırma metin gibi yapılıyor:", 410, size=62, hl=YELLOW,
                  weight="ExtraBold")
    if R.visible(t, 0.9):
        yy = y + 40 + R.rise(t, 0.9)
        d.rounded_rectangle([40, yy, 1040, yy + 330], radius=26, fill=CARD, outline=LINE, width=2)
        d.text((70, yy + 45), "'2026-11-30 11:30'", font=mono(70, True), fill=TEXT)
        d.text((70, yy + 180), "  <= '2026-11-30'", font=mono(70, True), fill=TEXT)
        y = yy + 330
    else:
        y = y + 370
    if R.visible(t, 1.7):
        d.text((70, y + 40 + R.rise(t, 1.7, 40)), "→ YANLIŞ", font=font("Black", 150), fill=RED)
    R.caption(d, t, "Saatli değer, saatsiz tarihten büyük sayılır. 30 Kasım'ın tamamı rapordan düşer.", y + 270,
              start=2.6, size=58, col=MUTED, weight="SemiBold")


def s_fix(d, t):
    pill(d, (70, 290), "DOĞRUSU", fill=GREEN, size=46)
    y = code_box(d, (40, 400), QB, size=54, w=1000, title="kasim_ciro.sql", line_marks=None)
    if R.visible(t, 1.0):
        d.text((70, y + 70 + R.rise(t, 1.0, 40)), "4.100 TL", font=font("Black", 160), fill=GREEN)
    y2 = R.caption(d, t, "Kasım'ın 5 siparişi geldi, 1 Aralık (400 TL) dışarıda kaldı.", y + 340, start=1.8,
                   size=60, weight="Bold")
    R.caption(d, t, "Bitiş: [<] sonraki ayın 1'i.", y2 + 60, start=2.8, size=76, hl=YELLOW,
              weight="ExtraBold")


def s_rule(d, t):
    pill(d, (70, 290), "KURAL", fill=TEAL, size=46)
    cards = [("<= '2026-11-30'", "30 Kasım düşer", RED), ("< '2026-12-01'", "ay tam gelir", GREEN),
             ("BETWEEN ... '2026-11-30'", "aynı tuzak", YELLOW)]
    y = 410
    for i, (a, b, col) in enumerate(cards):
        st = 0.2 + i * 0.7
        if R.visible(t, st):
            yy = y + R.rise(t, st, 40)
            d.rounded_rectangle([40, yy, 1040, yy + 270], radius=26, fill=CARD, outline=LINE, width=2)
            d.text((80, yy + 40), a, font=mono(52, True), fill=TEXT)
            d.text((80, yy + 140), b, font=font("Black", 80), fill=col)
        y += 305
    R.caption(d, t, "Ay sonu, prim, fatura raporu: [saatli] tarihe dikkat.", y + 30, start=2.4, size=62, hl=PINK,
              weight="ExtraBold")


def s_cta(d, t):
    y = hook_title(d, [("Ay sonu raporunu", TEXT), ("hazırlayan iş", TEXT), ("arkadaşına", YELLOW),
                       ("gönder.", YELLOW)], 400, 124)
    if R.visible(t, 0.3):
        pill(d, (70, y + 60 + R.rise(t, 0.3, 30)), "Gönder", fill=TEAL, size=66)
    y = R.caption(d, t, "Kaydet, mülakatta sorulur.", y + 290, start=0.6, size=64, weight="Bold")
    y = R.caption(d, t, "Her gün yeni SQL için takip et", y + 40, start=0.8, size=52, col=MUTED, weight="SemiBold")
    if R.visible(t, 1.0):
        pill(d, (70, y + 80 + R.rise(t, 1.0)), HANDLE, fill=PINK, size=56)


sc = [(3.4, s_hook), (3.6, s_data), (5.0, s_trap), (5.2, s_fix), (3.8, s_rule), (3.4, s_cta)]
print(reel("reel_mulakat_14_ay_sonu", sc, D, seed=73))
