"""28 Kasım 2026 18:00 Reels (v5 koyu kod editörü + v6 "30 Günde SQL"): Gün 5/30 DISTINCT — DISTINCT tek sütuna değil tüm satıra bakar.
Doğrulama: gun/2026-11-28/sql_dogrula.py. Sabah nöbeti 26 Kasım: ÇÖZÜM EN SONDA (DOĞRUSU ≥10. sn, KURAL kartı yok,
gönder + "Yarın Gün 6" DOĞRUSU sahnesinin son 2 sn'sinde 1.150-1.450 px), süre 14-17 sn."""
import sys
sys.path.insert(0, "/home/claude/sqlogreniyorum-medya/araclar")
from v5_ortak import *
from uretim import reel

D = "/home/claude/sqlogreniyorum-medya/gun/2026-11-28/"
QA = ["SELECT DISTINCT sehir, musteri", "FROM siparis;"]
QB = ["SELECT DISTINCT sehir", "FROM siparis;"]
WRONG = [("İstanbul", "Ayşe"), ("Ankara", "Mert"), ("İstanbul", "Can"), ("İzmir", "Ece"), ("İstanbul", "Deniz")]
RIGHT = [("İstanbul",), ("Ankara",), ("İzmir",)]


def s_hook(d, t):
    pill(d, (70, 280), "30 GÜNDE SQL · GÜN 5/30", fill=YELLOW, size=44)
    y = hook_title(d, [("Şehir listesi istedim,", TEXT), ("DISTINCT yazdım.", TEXT), ("İstanbul 3 kez geldi.", PINK)], 400, 100)
    y = code_box(d, (40, y + 40), QA, size=50, w=1000, title="sehirler.sql")
    d.rounded_rectangle([40, y + 40, 1040, y + 330], radius=26, fill=CARD, outline=RED, width=3)
    d.text((80, y + 65), "İstanbul, Ankara, İstanbul,", font=mono(52, True), fill=RED)
    d.text((80, y + 140), "İzmir, İstanbul", font=mono(52, True), fill=RED)
    d.text((80, y + 225), "3 şehir yerine 5 satır", font=font("Black", 60), fill=RED)
    text_block(d, (70, y + 370), "Neden?", font("Black", 96), fill=TEXT, max_w=940)


def s_neden(d, t):
    pill(d, (70, 280), "NEDEN?", fill=RED, size=46)
    y = table(d, (40, 390), ["sehir", "musteri"], WRONG, [520, 480], size=48, hl_rows=[0, 2, 4])
    y = R.caption(d, t, "DISTINCT tek sütuna değil, [tüm satıra] bakar.", y + 40, start=0.4, size=60,
                  hl=YELLOW, weight="ExtraBold")
    y = R.caption(d, t, "İstanbul+Ayşe ile İstanbul+Can farklı satır, ikisi de kalır.", y + 30, start=2.2,
                  size=52, col=TEXT, weight="Bold")
    R.caption(d, t, "Silinen tek satır: 2. kez gelen [Ayşe · İstanbul].", y + 30, start=4.2, size=52,
              hl=PINK, weight="Bold")


def s_dogru(d, t):
    pill(d, (70, 280), "DOĞRUSU", fill=GREEN, size=46)
    y = code_box(d, (40, 390), QB, size=54, w=1000, title="sehirler.sql")
    if R.visible(t, 0.6):
        yy = y + 40 + R.rise(t, 0.6, 40)
        y2 = table(d, (40, yy), ["sehir"], RIGHT, [560], size=52)
        if R.visible(t, 1.2):
            d.text((660, yy + 150 + R.rise(t, 1.2, 30)), "3 şehir", font=font("Black", 96), fill=GREEN)
            d.text((660, yy + 270 + R.rise(t, 1.2, 30)), "✓", font=font("Black", 96), fill=GREEN)
        R.caption(d, t, "Sadece [istediğin sütunu] yaz.", y2 + 30, start=1.8, size=52, hl=YELLOW,
                  weight="ExtraBold")
    if R.visible(t, 4.0):
        yy = 1300 + R.rise(t, 4.0, 40)
        d.rounded_rectangle([40, yy, 1040, yy + 190], radius=26, fill=CARD, outline=TEAL, width=3)
        d.text((80, yy + 25), "30 günü tek başına yapma:", font=font("ExtraBold", 54), fill=TEXT)
        d.text((80, yy + 105), "1 kişiye gönder →", font=font("Black", 58), fill=TEAL)
        pill(d, (70, yy + 220), "Yarın Gün 6/30: AND / OR", fill=YELLOW, size=50)


sc = [(3.2, s_hook), (6.8, s_neden), (6.0, s_dogru)]
print(reel("reel_30gun_sql_gun05_distinct", sc, D, seed=95))
