"""v5 koyu kod editörü Reels ortak yardımcıları (gun/2026-11-01 şablonundan: hook_title, sql_cta)."""
import sys
sys.path.insert(0, "/home/claude/sqlogreniyorum-medya/araclar")
import reels as R
from brand import *
_src = open("/home/claude/sqlogreniyorum-medya/gun/2026-11-01/uret_31ekim_1kasim.py").read().split(
    "# ------------------------------------------------------------------ 31 Ekim haber")[0]
_ns = {}
exec(_src.replace("which = sys.argv[1:]", "which = []"), _ns)
hook_title, sql_cta = _ns["hook_title"], _ns["sql_cta"]


def hook_scene(seri, lines, code, wrong, code_size=40):
    """İlk kare: seri rozeti + hata hikâyesi + kod + kırmızı yanlış sonuç; hepsi t=0'da tam görünür."""
    def s(d, t):
        pill(d, (70, 300), seri, fill=YELLOW, size=40)
        y = hook_title(d, lines, 410, 104)
        y = code_box(d, (40, y + 30), code, size=code_size, w=1000, title="sorgu.sql")
        text_block(d, (70, y + 40), wrong, font("Black", 54), fill=RED, max_w=940)
    return s


def rule_scene(cards, cap, hl):
    def s(d, t):
        pill(d, (70, 330), "KURAL", fill=TEAL, size=44)
        y = 460
        for i, (a, b) in enumerate(cards):
            st = 0.2 + i * 0.8
            if R.visible(t, st):
                yy = y + R.rise(t, st, 40)
                d.rounded_rectangle([50, yy, 1030, yy + 230], radius=26, fill=CARD, outline=LINE, width=2)
                d.text((90, yy + 40), a, font=font("Bold", 50), fill=TEXT)
                d.text((90, yy + 120), b, font=font("Black", 64), fill=YELLOW if i == 0 else TEAL)
            y += 270
        R.caption(d, t, cap, 1060, start=1.8, size=52, hl=hl)
    return s
