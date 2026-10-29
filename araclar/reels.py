"""Hafta 1 Reels videoları ve quiz story görselleri (1080x1920, 30 fps, sessiz)."""
import os
import subprocess
import sys
from brand import *

OUT = os.path.join(os.path.dirname(__file__), "..", "out")
W, H, FPS = 1080, 1920, 30
BASE, _ = canvas(W, H)


def ease(t, start, dur=0.35):
    """0→1 arası yumuşak geçiş."""
    p = min(max((t - start) / dur, 0), 1)
    return 1 - (1 - p) ** 3


def rise(t, start, dist=60):
    return int((1 - ease(t, start)) * dist)


def visible(t, start):
    return t >= start


def frame_base(T_total, t_abs):
    img = BASE.copy()
    d = ImageDraw.Draw(img)
    # ilerleme çubuğu
    d.rectangle([0, 0, W, 10], fill=CARD)
    d.rectangle([0, 0, int(W * t_abs / T_total), 10], fill=YELLOW)
    d.text((70, 70), HANDLE, font=font("Bold", 34), fill=MUTED)
    return img, d


def render(name, scenes):
    total = sum(s[0] for s in scenes)
    path = os.path.join(OUT, f"{name}.mp4")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
           "-pix_fmt", "yuv420p", "-movflags", "+faststart", path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    t_abs = 0.0
    n = int(round(total * FPS))
    cover_saved = False
    for i in range(n):
        t_abs = i / FPS
        acc = 0
        for dur, fn in scenes:
            if t_abs < acc + dur or (dur, fn) == scenes[-1]:
                img, d = frame_base(total, t_abs)
                fn(d, t_abs - acc)
                break
            acc += dur
        if not cover_saved and t_abs >= 1.5:
            img.save(os.path.join(OUT, f"{name}_kapak.png"))
            cover_saved = True
        p.stdin.write(img.tobytes())
    p.stdin.close()
    p.wait()
    return path, total


def big_title(d, t, lines, y=620, size=104, start=0.0, step=0.25, hl=YELLOW):
    """Her satır sırayla yukarı kayarak gelir. lines: [(metin, renk)]"""
    fnt = font("Black", size)
    for i, (txt, col) in enumerate(lines):
        st = start + i * step
        if visible(t, st):
            d.text((70, y + rise(t, st)), txt, font=fnt, fill=col)
        y += int(size * 1.12)
    return y


def caption(d, t, text, y, start=0.0, size=48, col=TEXT, hl=None, max_w=940, weight="Bold"):
    if not visible(t, start):
        return y
    return text_block(d, (70, y + rise(t, start, 40)), text, font(weight, size), fill=col, max_w=max_w, highlight=hl)


def cta_scene(d, t, line1="Kaydet, lazım olacak.", line2="Her gün 1 SQL konusu için takip et"):
    y = big_title(d, t, [(line1.split(",")[0] + ",", TEXT), (line1.split(",")[1].strip(), YELLOW)], y=640, size=110)
    y = caption(d, t, line2, y + 60, start=0.5, size=50, col=MUTED, weight="SemiBold")
    if visible(t, 0.8):
        pill(d, (70, y + 60 + rise(t, 0.8)), HANDLE, fill=PINK, size=44)


# ------------------------------------------------------------ Reel 1
Q1 = ["SELECT bolum, COUNT(*) AS kisi", "FROM calisanlar", "WHERE maas > 30000", "GROUP BY bolum",
      "HAVING COUNT(*) >= 2", "ORDER BY kisi DESC;"]
ORDER = [(1, "FROM", "Önce tablo okunur"), (2, "WHERE", "Satırlar filtrelenir"), (3, "GROUP BY", "Satırlar gruplanır"),
         (4, "HAVING", "Gruplar filtrelenir"), (0, "SELECT", "Sütunlar seçilir, takma ad doğar"),
         (5, "ORDER BY", "En son sıralanır")]
COLS = [YELLOW, TEAL, PINK, BLUE, GREEN, YELLOW]


def r1_hook(d, t):
    big_title(d, t, [("SQL, sorgunu", TEXT), ("yazdığın sırayla", TEXT), ("çalıştırmaz.", YELLOW)], y=640, size=112)
    caption(d, t, "Bunu bilmeyen her gün aynı hatayı alıyor.", 1100, start=1.0, size=46, col=MUTED, weight="SemiBold")


def r1_code(d, t):
    caption(d, t, "Bu sorguya bak:", 420, size=60, weight="ExtraBold")
    chars = int(max(t - 0.4, 0) * 38)
    code_box(d, (40, 560), Q1, size=40, w=1000, chars=chars, title="sorgu.sql", line_marks={})
    if t > 4.6:
        caption(d, t, "Sence ilk hangi satır çalışır?", 1230, start=4.6, size=50, col=YELLOW)


def r1_order(d, t):
    step_len = 1.6
    k = min(int(t / step_len), len(ORDER) - 1)
    marks = {}
    for j in range(k + 1):
        line, kw, _ = ORDER[j]
        marks[line] = (str(j + 1), COLS[j])
    caption(d, t, "Gerçek çalışma sırası:", 420, size=60, weight="ExtraBold")
    code_box(d, (40, 560), Q1, size=40, w=1000, line_marks=marks, title="sorgu.sql")
    line, kw, desc = ORDER[k]
    st = k * step_len
    y = 1210 + rise(t, st, 30)
    pill(d, (70, y), f"{k + 1}. {kw}", fill=COLS[k], size=52)
    text_block(d, (70, y + 120), desc, font("Bold", 56), max_w=940)


def r1_payoff(d, t):
    caption(d, t, "Peki bu neden önemli?", 360, size=64, weight="ExtraBold")
    y = caption(d, t, "Takma ad ([kisi]) SELECT'te doğar. WHERE ondan önce çalıştığı için çoğu veritabanında onu tanımaz.",
                500, start=0.4, size=48, hl=YELLOW, weight="SemiBold")
    if visible(t, 1.6):
        yy = y + 50 + rise(t, 1.6)
        pill(d, (70, yy), "HATA", fill=RED, size=34)
        code_box(d, (40, yy + 80), ["WHERE kisi >= 2"], size=42, w=1000)
    if visible(t, 2.8):
        yy = y + 360 + rise(t, 2.8)
        pill(d, (70, yy), "ÇALIŞIR", fill=GREEN, size=34)
        code_box(d, (40, yy + 80), ["ORDER BY kisi DESC"], size=42, w=1000)


# ------------------------------------------------------------ Reel 2
def r2_hook(d, t):
    big_title(d, t, [("WHERE mi,", TEXT), ("HAVING mi?", YELLOW)], y=660, size=130)
    caption(d, t, "Farkı 25 saniyede öğren, bir daha karıştırma.", 1020, start=0.8, size=48, col=MUTED, weight="SemiBold")


def r2_where(d, t):
    pill(d, (70, 360), "WHERE", fill=YELLOW, size=48)
    caption(d, t, "Gruplamadan [ÖNCE] çalışır. Tek tek [satırları] filtreler.", 480, start=0.2, size=54, hl=YELLOW)
    if visible(t, 1.2):
        code_box(d, (40, 700 + rise(t, 1.2)), ["SELECT ad, bolum, maas", "FROM calisanlar", "WHERE maas > 40000;"], size=40, w=1000)
    if visible(t, 3.0):
        table(d, (40, 1040 + rise(t, 3.0)), ["ad", "bolum", "maas"],
              [("B", "Satış", 42000), ("E", "IT", 55000), ("F", "IT", 48000)], [240, 360, 400], size=38)


def r2_having(d, t):
    pill(d, (70, 360), "HAVING", fill=TEAL, size=48)
    caption(d, t, "Gruplamadan [SONRA] çalışır. [Grupları] filtreler.", 480, start=0.2, size=54, hl=TEAL)
    if visible(t, 1.2):
        code_box(d, (40, 700 + rise(t, 1.2)), ["SELECT bolum, AVG(maas) AS ort", "FROM calisanlar", "GROUP BY bolum",
                                               "HAVING AVG(maas) > 35000;"], size=40, w=1000)
    if visible(t, 3.0):
        table(d, (40, 1100 + rise(t, 3.0)), ["bolum", "ort"], [("IT", 44000)], [400, 400], size=40)
        caption(d, t, "Satış (33.250) ve İK (34.500) elendi.", 1330, start=3.4, size=42, col=MUTED, weight="SemiBold")


def r2_rule(d, t):
    caption(d, t, "Tek kural:", 420, size=70, weight="Black")
    for i, (lab, col, txt) in enumerate([
        ("HAVING", TEAL, "COUNT, SUM, AVG gibi bir toplama sonucuna göre filtreliyorsan"),
        ("WHERE", YELLOW, "Ham satır değerine göre filtreliyorsan"),
    ]):
        st = 0.5 + i * 1.3
        if visible(t, st):
            y = 600 + i * 380 + rise(t, st)
            d.rounded_rectangle([40, y, 1040, y + 320], radius=30, fill=CARD, outline=col, width=4)
            pill(d, (80, y + 36), lab, fill=col, size=40)
            text_block(d, (80, y + 140), txt, font("Bold", 46), max_w=920)


def r2_both(d, t):
    caption(d, t, "Bonus: İkisi [birlikte] de olur", 380, size=60, hl=YELLOW, weight="ExtraBold")
    if visible(t, 0.4):
        code_box(d, (40, 560 + rise(t, 0.4)), ["SELECT bolum, COUNT(*) AS kisi", "FROM calisanlar",
                                               "WHERE maas > 30000", "GROUP BY bolum", "HAVING COUNT(*) >= 2;"],
                 size=40, w=1000, line_marks={2: ("1", YELLOW), 4: ("2", TEAL)})
    if visible(t, 2.0):
        caption(d, t, "Önce 30.000 altı maaşlar elenir, sonra 2'den az kişisi kalan bölümler.", 1080, start=2.0,
                size=46, weight="SemiBold")


# ------------------------------------------------------------ Quiz story
def quiz():
    img, d = canvas(W, H)
    d.text((70, 120), HANDLE, font=font("Bold", 34), fill=MUTED)
    pill(d, (70, 220), "QUIZ", fill=PINK, size=40)
    y = text_block(d, (70, 330), "Bu sorgu ne döndürür?", font("Black", 84), max_w=940)
    y = table(d, (40, y + 30), ["id", "ad", "telefon"],
              [(1, "Ada", "555-01"), (2, "Bora", None), (3, "Cem", "555-03"), (4, "Duru", None), (5, "Efe", "555-05")],
              [150, 330, 520], size=36)
    y = code_box(d, (40, y + 40), ["SELECT COUNT(*),", "       COUNT(telefon)", "FROM musteriler;"], size=42, w=1000)
    d.rounded_rectangle([40, y + 50, 1040, y + 430], radius=30, outline=LINE, width=3)
    lab = "Quiz çıkartmasını buraya ekle"
    tw = d.textlength(lab, font=font("SemiBold", 32))
    d.text((540 - tw / 2, y + 220), lab, font=font("SemiBold", 32), fill=(60, 70, 98))
    img.save(os.path.join(OUT, "story_quiz_1_soru.png"))

    img, d = canvas(W, H)
    d.text((70, 120), HANDLE, font=font("Bold", 34), fill=MUTED)
    pill(d, (70, 220), "CEVAP", fill=GREEN, size=40)
    y = text_block(d, (70, 330), "5 ve 3", font("Black", 150), max_w=940, fill=YELLOW)
    y = text_block(d, (70, y + 20), "COUNT(*) tüm [satırları] sayar: 5", font("Bold", 52), max_w=940, highlight=YELLOW)
    y = text_block(d, (70, y + 30), "COUNT(telefon) [NULL] olanları saymaz: 3", font("Bold", 52), max_w=940, highlight=RED)
    d.rounded_rectangle([40, y + 70, 1040, y + 400], radius=30, fill=CARD, outline=YELLOW, width=3)
    text_block(d, (90, y + 115), "Gerçek hayatta: \"Telefonu kayıtlı kaç müşterim var?\" sorusunun cevabı COUNT(telefon).",
               font("SemiBold", 42), max_w=900)
    text_block(d, (70, 1560), "Bildin mi? Story'yi bir arkadaşına gönder.", font("Bold", 44), fill=MUTED, max_w=940)
    img.save(os.path.join(OUT, "story_quiz_2_cevap.png"))


if __name__ == "__main__":
    which = sys.argv[1:] or ["r1", "r2", "quiz"]
    if "r1" in which:
        print(render("reel_sql_calisma_sirasi",
                     [(3.2, r1_hook), (6.0, r1_code), (9.8, r1_order), (5.5, r1_payoff), (3.5, cta_scene)]))
    if "r2" in which:
        print(render("reel_where_vs_having",
                     [(3.0, r2_hook), (6.0, r2_where), (6.5, r2_having), (4.5, r2_rule), (5.5, r2_both),
                      (3.5, cta_scene)]))
    if "quiz" in which:
        quiz()
        print("quiz ok")
