"""23 Kasım 2026 18:00 Reels (v5 koyu kod editörü): SQL Mülakat Sorusu #12 LAG ve PARTITION BY.
Doğrulama: gun/2026-11-23/sql_dogrula.py"""
import sys
sys.path.insert(0, "/home/claude/sqlogreniyorum-medya/araclar")
from v5_ortak import *
from uretim import reel

D = "/home/claude/sqlogreniyorum-medya/gun/2026-11-23/"
ROWS = [("Beşiktaş", "01.11", 500), ("Beşiktaş", "02.11", 650), ("Beşiktaş", "03.11", 600),
        ("Kadıköy", "01.11", 900), ("Kadıköy", "02.11", 950), ("Kadıköy", "03.11", 1000)]
QA = ["SELECT sube, gun,", "  ciro - LAG(ciro) OVER (", "    ORDER BY sube, gun) AS fark", "FROM satis;"]
QB = ["SELECT sube, gun,", "  ciro - LAG(ciro) OVER (", "    PARTITION BY sube", "    ORDER BY gun) AS fark",
      "FROM satis;"]
FIX = [("Beşiktaş", "01.11", None), ("Beşiktaş", "02.11", 150), ("Beşiktaş", "03.11", -50),
       ("Kadıköy", "01.11", None), ("Kadıköy", "02.11", 50), ("Kadıköy", "03.11", 50)]

s_hook = hook_scene("SQL MÜLAKAT SORUSU #12",
                    [("Şubelerin günlük", TEXT), ("farkını çıkardım.", TEXT), ("Kadıköy ilk gün +300!", PINK)],
                    QA, "Kadıköy'ün dünü yok, fark 300 çıktı. Neden?", code_size=38)


def s_data(d, t):
    R.caption(d, t, "satis", 300, size=52, weight="ExtraBold")
    table(d, (40, 390), ["sube", "gun", "ciro"], ROWS, [400, 300, 300], size=40, hl_rows=[3], hl_col=RED)
    R.caption(d, t, "Kadıköy'ün ilk günü: fark [NULL] olmalı.", 1000, start=0.8, size=52, hl=YELLOW)


def s_trap(d, t):
    pill(d, (70, 300), "NEDEN?", fill=RED, size=44)
    R.caption(d, t, "PARTITION BY yok: tablo [tek] sıra oldu.", 420, size=56, hl=RED, weight="ExtraBold")
    if R.visible(t, 1.0):
        table(d, (40, 640 + R.rise(t, 1.0)), ["sube", "gun", "ciro"], [ROWS[2], ROWS[3]], [400, 300, 300],
              size=42, hl_rows=[1], hl_col=RED)
    R.caption(d, t, "LAG, Beşiktaş'ın son gününü aldı:", 940, start=1.8, size=52, weight="Bold")
    R.caption(d, t, "900 − 600 = [300]", 1040, start=2.5, size=80, hl=RED, weight="Black")


def s_fix(d, t):
    pill(d, (70, 300), "DOĞRUSU", fill=GREEN, size=44)
    y = code_box(d, (40, 390), QB, size=38, w=1000, title="sorgu.sql")
    if R.visible(t, 1.0):
        table(d, (40, y + 30 + R.rise(t, 1.0)), ["sube", "gun", "fark"], FIX, [400, 300, 300], size=36,
              hl_rows=[3])
    R.caption(d, t, "Her şube [kendi] içinde sayılır.", 1440, start=2.0, size=50, hl=GREEN)


s_rule = rule_scene([("Kimin içinde?", "PARTITION BY"), ("Hangi sırayla?", "ORDER BY")],
                    "Şube, müşteri, ürün: LAG'e [PARTITION] şart.", YELLOW)

sc = [(3.2, s_hook), (3.4, s_data), (4.8, s_trap), (4.8, s_fix), (3.6, s_rule), (3.2, sql_cta)]
print(reel("reel_mulakat_12_lag_partition", sc, D, seed=67))
