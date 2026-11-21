"""22 Kasım 2026 18:00 Reels (v5 yeniden üretim, koyu kod editörü): SQL Mülakat Sorusu #11 tam sayı bölmesi.
Doğrulama: gun/2026-11-22/sql_dogrula_v5.py"""
import sys
sys.path.insert(0, "/home/claude/sqlogreniyorum-medya/araclar")
from v5_ortak import *
from uretim import reel

D = "/home/claude/sqlogreniyorum-medya/gun/2026-11-22/"
ROWS = [(1, 0), (2, 1), (3, 0), (4, 0), (5, 1), (6, 0), (7, 0), (8, 0)]
QA = ["SELECT SUM(iade) / COUNT(*)", "  * 100 AS iade_orani", "FROM siparis;"]
QB = ["SELECT SUM(iade) * 100.0", "  / COUNT(*) AS iade_orani", "FROM siparis;"]

s_hook = hook_scene("SQL MÜLAKAT SORUSU #11",
                    [("İade oranını hesapladım.", TEXT), ("%25 olmalıydı,", YELLOW), ("SQL %0 dedi.", PINK)],
                    QA, "Sonuç: 0. Müdür 'hiç iade yok' sandı. Neden?")


def s_data(d, t):
    R.caption(d, t, "siparis", 300, size=52, weight="ExtraBold")
    table(d, (40, 390), ["id", "iade"], ROWS, [400, 600], size=38, hl_rows=[1, 4], hl_col=RED)
    R.caption(d, t, "8 sipariş, 2 iade: oran [%25] olmalı.", 1080, start=0.8, size=52, hl=YELLOW)


def s_trap(d, t):
    pill(d, (70, 300), "NEDEN?", fill=RED, size=44)
    R.caption(d, t, "SUM(iade) = 2, COUNT(*) = 8.", 420, size=56, weight="Bold")
    R.caption(d, t, "2 / 8 = [0]", 560, start=0.8, size=90, hl=RED, weight="Black")
    R.caption(d, t, "İki tam sayı bölünürse sonuç da tam sayı olur: 0,25 → 0.", 740, start=1.6, size=52,
              weight="Bold")
    R.caption(d, t, "0 × 100 = 0. Çarpma çok geç geldi.", 960, start=2.6, size=52, col=PINK, weight="Bold")
    R.caption(d, t, "PostgreSQL, SQL Server ve SQLite'ta böyle. MySQL'de / ondalıklı böler.", 1160,
              start=3.2, size=38, col=MUTED, weight="SemiBold")


def s_fix(d, t):
    pill(d, (70, 300), "DOĞRUSU", fill=GREEN, size=44)
    y = code_box(d, (40, 400), QB, size=40, w=1000, title="sorgu.sql")
    if R.visible(t, 1.0):
        table(d, (40, y + 50 + R.rise(t, 1.0)), ["iade_orani"], [("25.0",)], [600], size=42, hl_rows=[0])
    R.caption(d, t, "Önce 100.0 ile çarp: bölme [ondalıklı] olur.", 1060, start=1.8, size=52, hl=GREEN)


s_rule = rule_scene([("Tam sayı / tam sayı", "= tam sayı"), ("Oran hesaplarken", "* 100.0 sonra böl")],
                    "Rapor %0 diyorsa önce [bölmeye] bak.", PINK)

sc = [(3.2, s_hook), (3.4, s_data), (5.2, s_trap), (4.4, s_fix), (3.6, s_rule), (3.2, sql_cta)]
print(reel("reel_mulakat_11_tamsayi_bolme", sc, D, seed=61))
