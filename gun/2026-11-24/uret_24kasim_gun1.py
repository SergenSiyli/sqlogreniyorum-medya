"""24 Kasım 18:00 · 30 GÜNDE SQL · GÜN 1/30: SELECT (virgül unutunca sütun adı olur). sqlite3 ile doğrulandı."""
import sys
sys.path.insert(0, "/home/claude/sqlogreniyorum-medya/araclar")
from v5_ortak import *
from v5_ortak import hook_title
from uretim import reel
D = "/home/claude/sqlogreniyorum-medya/gun/2026-11-24/"
ROWS = [(1, "Ali", "Kaya"), (2, "Ayşe", "Demir"), (3, "Can", "Yıldız")]
s_hook = hook_scene("30 GÜNDE SQL · GÜN 1/30",
    [("Ad ve soyadı istedim,", TEXT), ("tek sütun geldi.", YELLOW), ("Adı da 'soyad'.", PINK)],
    ["SELECT ad soyad", "FROM musteri;"], "Sonuç: soyad = Ali, Ayşe, Can. Neden?")
def s_data(d, t):
    R.caption(d, t, "musteri", 300, size=52, weight="ExtraBold")
    table(d, (40, 390), ["id", "ad", "soyad"], ROWS, [200, 380, 420], size=38)
    R.caption(d, t, "İstediğim: [ad] ve [soyad] yan yana.", 900, start=0.8, size=52, hl=YELLOW)
def s_trap(d, t):
    pill(d, (70, 300), "NEDEN?", fill=RED, size=44)
    R.caption(d, t, "Araya virgül koymadım.", 420, size=56, weight="Bold")
    R.caption(d, t, "SQL 'soyad'ı [takma ad] sandı.", 560, start=0.8, size=64, hl=RED, weight="Black")
    R.caption(d, t, "SELECT ad soyad = SELECT ad AS soyad", 760, start=1.6, size=48, weight="Bold")
    R.caption(d, t, "Hata vermez, sessizce yanlış sonuç verir.", 900, start=2.4, size=52, col=PINK, weight="Bold")
def s_fix(d, t):
    pill(d, (70, 300), "DOĞRUSU", fill=GREEN, size=44)
    y = code_box(d, (40, 400), ["SELECT ad, soyad", "FROM musteri;"], size=44, w=1000, title="sorgu.sql")
    if R.visible(t, 1.0):
        table(d, (40, y + 50 + R.rise(t, 1.0)), ["ad", "soyad"], [(a, b) for _, a, b in ROWS], [480, 520], size=40)
    R.caption(d, t, "Sütunların arasına [virgül].", 1100, start=1.8, size=56, hl=GREEN)
def s_end(d, t):
    pill(d, (70, 300), "GÜN 1/30 BİTTİ", fill=TEAL, size=44)
    y = hook_title(d, [("Yarın Gün 2:", TEXT), ("WHERE", YELLOW), ("ile süzme.", TEXT)], 440, 110)
    y = R.caption(d, t, "Kaçırmamak için takip et.", y + 50, start=0.4, size=60, weight="Bold")
    y = R.caption(d, t, "Sen hiç virgül unuttun mu? Evet/hayır yaz.", y + 40, start=0.8, size=46, col=MUTED, weight="SemiBold")
    if R.visible(t, 1.0):
        pill(d, (70, y + 50 + R.rise(t, 1.0)), HANDLE, fill=PINK, size=44)
sc = [(3.4, s_hook), (3.0, s_data), (4.6, s_trap), (4.0, s_fix), (3.6, s_end)]
print(reel("reel_30gun_sql_gun1_select", sc, D, seed=71))
