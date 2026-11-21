"""24 Kasım 2026 18:00 Reels (v5 koyu kod editörü): SQL Mülakat Sorusu #13 LIMIT ve eşitlik / DENSE_RANK.
Doğrulama: gun/2026-11-24/sql_dogrula.py"""
import sys
sys.path.insert(0, "/home/claude/sqlogreniyorum-medya/araclar")
from v5_ortak import *
from uretim import reel

D = "/home/claude/sqlogreniyorum-medya/gun/2026-11-24/"
ROWS = [("Ali", 90), ("Ayşe", 70), ("Can", 80), ("Deniz", 70), ("Ece", 60)]
QA = ["SELECT ad, satis", "FROM satici", "ORDER BY satis DESC", "LIMIT 3;"]
QB = ["SELECT ad, satis FROM (", "  SELECT ad, satis,", "    DENSE_RANK() OVER (", "      ORDER BY satis DESC)",
      "      AS sira", "  FROM satici) t", "WHERE sira <= 3;"]

s_hook = hook_scene("SQL MÜLAKAT SORUSU #13",
                    [("En iyi 3 satıcıya", TEXT), ("prim verdim.", YELLOW), ("Deniz itiraz etti.", PINK)],
                    QA, "Deniz de 70 sattı, listede yok. Neden?")


def s_data(d, t):
    R.caption(d, t, "satici", 300, size=52, weight="ExtraBold")
    table(d, (40, 390), ["ad", "satis"], ROWS, [500, 500], size=42, hl_rows=[1, 3], hl_col=RED)
    R.caption(d, t, "Ayşe ve Deniz [eşit]: ikisi de 70.", 900, start=0.8, size=52, hl=YELLOW)


def s_trap(d, t):
    pill(d, (70, 300), "NEDEN?", fill=RED, size=44)
    R.caption(d, t, "LIMIT eşitliğe bakmaz, [tam] 3 satır keser.", 420, size=56, hl=RED, weight="ExtraBold")
    if R.visible(t, 1.0):
        table(d, (40, 640 + R.rise(t, 1.0)), ["ad", "satis"], [("Ali", 90), ("Can", 80), ("Ayşe", 70)],
              [500, 500], size=42)
    R.caption(d, t, "Deniz 70 → dışarıda kaldı.", 1000, start=1.8, size=56, col=RED, weight="Black")
    R.caption(d, t, "Eşitlerden hangisinin kalacağı da garanti değil.", 1120, start=2.6, size=46, col=MUTED,
              weight="SemiBold")


def s_fix(d, t):
    pill(d, (70, 300), "DOĞRUSU", fill=GREEN, size=44)
    y = code_box(d, (40, 390), QB, size=36, w=1000, title="sorgu.sql")
    if R.visible(t, 1.2):
        table(d, (40, y + 30 + R.rise(t, 1.2)), ["ad", "satis"],
              [("Ali", 90), ("Can", 80), ("Ayşe", 70), ("Deniz", 70)], [500, 500], size=36, hl_rows=[3])
    R.caption(d, t, "Eşitler [aynı] sırayı alır: 4 kişi.", 1500, start=2.2, size=50, hl=GREEN)


s_rule = rule_scene([("LIMIT 3", "tam 3 satır"), ("DENSE_RANK <= 3", "ilk 3 değer")],
                    "Prim, ödül, sıralama: [eşitliği] unutma.", PINK)

sc = [(3.2, s_hook), (3.2, s_data), (4.8, s_trap), (5.2, s_fix), (3.6, s_rule), (3.2, sql_cta)]
print(reel("reel_mulakat_13_limit_esitlik", sc, D, seed=71))
