"""@utopikanne RENKLİ hikâye şablonları (2 Kasım 2026, hesap sahibinin isteği: kadın kitleye hitap eden, canlı, feminen).
1080x1920, içerik güvenli alanı y=250–1480, kaynak/not 1500–1580, @utopikanne y=1640.
Palet: pudra pembe, mercan, lila, nane, şeftali, limon, gök mavisi. Metin koyu mürdüm, açık kartlarda.
Yalnızca kendi vektör çizimlerimiz; fotoğraf, logo, emoji yok. İyi geceler şablonu anne_story.iyi_geceler (korunur)."""
import math
import random
import re
from PIL import Image, ImageDraw
from anne_story import font, tr_buyuk, iyi_geceler  # noqa: F401  (iyi_geceler dışarıya açılır)

W, H = 1080, 1920
HANDLE = "@utopikanne"
MURDUM = (74, 30, 64)
SOLUK = (112, 74, 100)       # alt notlar; açık zeminde ~6:1 kontrast
BEYAZ = (255, 255, 255)
KREM = (255, 250, 246)
SAGLIK_NOT = "Bilgilendirme amaçlıdır, doktorunuza danışın."

# temel pastel tonlar
PUDRA = (248, 196, 212)
MERCAN = (255, 135, 115)
LILA = (198, 172, 238)
NANE = (150, 222, 196)
SEFTALI = (255, 196, 158)
LIMON = (255, 228, 110)
GOK = (150, 204, 246)
# rozet/vurgu için koyu tonlar (beyaz metinle ≥ 4.5:1)
K_MERCAN = (184, 58, 46)
K_PEMBE = (172, 44, 98)
K_LILA = (104, 60, 160)
K_NANE = (18, 108, 82)
K_GOK = (24, 92, 150)
K_LIMON = (122, 88, 0)

# tema: (degrade üst, degrade alt, blob renkleri, koyu vurgu, açık kart tonu)
TEMA = {
    "gunaydin": ((255, 232, 214), (255, 244, 196), [SEFTALI, LIMON, PUDRA], K_MERCAN, (255, 238, 222)),
    "tarif": ((255, 226, 214), (255, 238, 222), [MERCAN, SEFTALI, LIMON], K_MERCAN, (255, 232, 222)),
    "hamilelik": ((240, 230, 255), (250, 236, 246), [LILA, PUDRA, GOK], K_LILA, (238, 228, 252)),
    "lohusa": ((255, 230, 238), (250, 236, 250), [PUDRA, LILA, SEFTALI], K_PEMBE, (255, 232, 240)),
    "emzirme": ((226, 240, 255), (240, 246, 255), [GOK, LILA, NANE], K_GOK, (228, 240, 254)),
    "temizlik": ((224, 248, 238), (236, 248, 252), [NANE, GOK, LIMON], K_NANE, (226, 246, 238)),
    "haber": ((255, 247, 206), (255, 238, 222), [LIMON, SEFTALI, NANE], K_LIMON, (255, 246, 210)),
    "efsane": ((255, 232, 240), (230, 248, 240), [PUDRA, NANE, LILA], K_PEMBE, (255, 232, 240)),
    "hap": ((255, 232, 222), (255, 246, 206), [MERCAN, LIMON, PUDRA], K_MERCAN, (255, 244, 206)),
    "kontrol": ((228, 248, 238), (242, 234, 255), [NANE, LILA, GOK], K_NANE, (230, 246, 238)),
    "liste": ((242, 234, 255), (228, 248, 238), [LILA, NANE, PUDRA], K_LILA, (240, 232, 254)),
    "dm": ((255, 230, 240), (240, 232, 255), [PUDRA, LILA, MERCAN], K_PEMBE, (255, 234, 242)),
}


class Tasma(Exception):
    pass


# ---------------- zemin, blob, dekor ----------------
def blob_poligon(cx, cy, R, seed, n=120):
    rnd = random.Random(seed)
    a, b, p1, p2 = rnd.uniform(.08, .14), rnd.uniform(.04, .08), rnd.uniform(0, 6.3), rnd.uniform(0, 6.3)
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        r = R * (1 + a * math.sin(3 * t + p1) + b * math.sin(5 * t + p2))
        pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    return pts


def zemin(tur):
    ust, alt, renkler, _, _ = TEMA[tur]
    img = Image.new("RGB", (W, H), ust)
    d = ImageDraw.Draw(img)
    for i in range(H):
        t = i / H
        d.line([(0, i), (W, i)], fill=tuple(int(ust[k] * (1 - t) + alt[k] * t) for k in range(3)))
    kat = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(kat)
    yerler = [(-60, 120, 330), (1120, 760, 360), (-40, 1500, 300), (1060, 1840, 280), (820, -40, 220)]
    seed = sum(map(ord, tur))
    for i, (x, y, r) in enumerate(yerler):
        c = renkler[i % len(renkler)]
        kd.polygon(blob_poligon(x, y, r, seed + i), fill=c + (120,))
    img = Image.alpha_composite(img.convert("RGBA"), kat).convert("RGB")
    d = ImageDraw.Draw(img)
    dekor(d, tur)
    return img, d


def yildiz(d, x, y, s, renk):
    d.polygon([(x, y - s * 2), (x + s * .55, y - s * .55), (x + s * 2, y), (x + s * .55, y + s * .55),
               (x, y + s * 2), (x - s * .55, y + s * .55), (x - s * 2, y), (x - s * .55, y - s * .55)], fill=renk)


def kalp(d, cx, cy, s, renk):
    d.ellipse([cx - s, cy - s * .8, cx, cy + s * .2], fill=renk)
    d.ellipse([cx, cy - s * .8, cx + s, cy + s * .2], fill=renk)
    d.polygon([(cx - s * .97, cy - s * .15), (cx + s * .97, cy - s * .15), (cx, cy + s * 1.05)], fill=renk)


def yaprak(d, cx, cy, s, renk, aci=30):
    m = Image.new("L", (int(4 * s), int(4 * s)), 0)
    md = ImageDraw.Draw(m)
    md.ellipse([s * .4, s * 1.3, s * 3.6, s * 2.7], fill=255)
    m = m.rotate(aci, resample=Image.BICUBIC)
    d._image.paste(Image.new("RGB", m.size, renk), (int(cx - 2 * s), int(cy - 2 * s)), m)


def dalga(d, x, y, w, renk, gen=8):
    pts = [(x + i, y + 10 * math.sin(i / 18)) for i in range(0, int(w), 3)]
    d.line(pts, fill=renk, width=gen, joint="curve")


def dekor(d, tur):
    """Küçük dekorlar yalnızca üst bant (y<230) ve alt bant (y>1690) içinde: metne asla girmez."""
    _, _, renkler, koyu, _ = TEMA[tur]
    c1, c2 = renkler[0], renkler[1]
    koyu_a = tuple(min(255, int(v * .6 + 255 * .4)) for v in koyu)
    yildiz(d, 140, 150, 14, koyu_a)
    yildiz(d, 930, 110, 10, koyu_a)
    kalp(d, 860, 190, 20, c1 if tur != "kontrol" else PUDRA)
    for x, y, r in [(250, 90, 8), (330, 170, 6), (700, 120, 7), (990, 210, 6)]:
        d.ellipse([x - r, y - r, x + r, y + r], fill=koyu_a)
    dalga(d, 420, 160, 200, c2 if c2 != LIMON else SEFTALI)
    yaprak(d, 200, 1790, 22, NANE if tur not in ("temizlik", "kontrol") else LILA, 35)
    yildiz(d, 880, 1760, 12, koyu_a)
    kalp(d, 300, 1840, 16, c1)
    for x, y, r in [(760, 1830, 7), (960, 1860, 6), (120, 1720, 6)]:
        d.ellipse([x - r, y - r, x + r, y + r], fill=koyu_a)


# ---------------- metin yardımcıları ----------------
def sar(d, text, f, max_w):
    out = []
    for para in text.split("\n"):
        cur = ""
        kel = []
        for w_ in para.split(" "):
            # "6." gibi sıra sayısı satır sonunda yalnız kalmasın: sonraki kelimeyle birlikte taşınır
            if kel and re.fullmatch(r"\d+\.", kel[-1]) and w_:
                kel[-1] += " " + w_
            else:
                kel.append(w_)
        for w_ in kel:
            t = (cur + " " + w_).strip()
            if d.textlength(t, font=f) <= max_w:
                cur = t
            else:
                if cur:
                    out.append(cur)
                cur = w_
        out.append(cur)
    for ln in out:
        if d.textlength(ln, font=f) > max_w:
            raise Tasma("uzun kelime: " + ln)
    return out


def yaz(d, x, y, text, f, renk, max_w, sp=1.3, center=False, cx=W / 2):
    for ln in sar(d, text, f, max_w):
        xx = cx - d.textlength(ln, font=f) / 2 if center else x
        d.text((xx, y), ln, font=f, fill=renk)
        y += int(f.size * sp)
    return y


def yukseklik(d, text, f, max_w, sp=1.3):
    return len(sar(d, text, f, max_w)) * int(f.size * sp)


def rozet(d, x, y, text, bg, fg=BEYAZ, s=30, center=False, cx=W / 2):
    text = tr_buyuk(text)
    f = font("ExtraBold", s)
    w = d.textlength(text, font=f) + 52
    if center:
        x = cx - w / 2
    d.rounded_rectangle([x, y, x + w, y + s + 28], radius=(s + 28) // 2, fill=bg)
    d.text((x + 26, y + 12), text, font=f, fill=fg)
    return y + s + 28, x + w


def kart(d, y1, y2, fill=BEYAZ, x1=80, x2=1000, r=44, golge=None):
    if golge:
        d.rounded_rectangle([x1 + 8, y1 + 12, x2 + 8, y2 + 12], radius=r, fill=golge)
    d.rounded_rectangle([x1, y1, x2, y2], radius=r, fill=fill)


def golge_rengi(tur):
    _, alt, renkler, _, _ = TEMA[tur]
    c = renkler[0]
    return tuple(int(c[k] * .55 + alt[k] * .45) for k in range(3))


def alt_bilgi(d, kaynak=None, not_metni=SAGLIK_NOT):
    if kaynak:
        f = font("SemiBold", 28)
        t = "Kaynak: " + kaynak
        while d.textlength(t, font=f) > 960 and f.size > 20:
            f = font("SemiBold", f.size - 2)
        d.text(((W - d.textlength(t, font=f)) / 2, 1500), t, font=f, fill=SOLUK)
    if not_metni:
        f = font("Medium", 26)
        d.text(((W - d.textlength(not_metni, font=f)) / 2, 1544), not_metni, font=f, fill=SOLUK)
    f = font("Bold", 32)
    d.text(((W - d.textlength(HANDLE, font=f)) / 2, 1640), HANDLE, font=f, fill=MURDUM)


def seri_no(seri, onek):
    m = re.search(r"#\s*(\d+)", seri or "")
    return f"{onek} #{m.group(1)}" if m else (seri or onek)


def sigdir(cizici, path, *args):
    """Yerleşimi ölçek k ile dener; güvenli alana sığan ilk ölçeği kaydeder."""
    son = None
    for k in (1.2, 1.12, 1.06, 1.0, .95, .9, .85, .8, .75, .7):
        try:
            img, y = cizici(k, *args)
            if y <= 1480:
                img.save(path)
                return path
            son = y
        except Tasma as e:
            son = str(e)
    raise AssertionError(("story taşıyor", path, son))


def F(w, s, k):
    return font(w, max(24, int(s * k)))


# ---------------- vektör çizimler ----------------
def gunes(d, cx, cy, r=105):
    for a in range(0, 360, 30):
        rad = math.radians(a)
        x1, y1 = cx + math.cos(rad) * (r + 24), cy + math.sin(rad) * (r + 24)
        x2, y2 = cx + math.cos(rad) * (r + 66), cy + math.sin(rad) * (r + 66)
        d.line([(x1, y1), (x2, y2)], fill=(255, 186, 60), width=16)
        d.ellipse([x2 - 8, y2 - 8, x2 + 8, y2 + 8], fill=(255, 186, 60))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 196, 70))
    d.ellipse([cx - r + 20, cy - r + 20, cx + r - 20, cy + r - 20], fill=(255, 220, 110))
    # yanak + gülümseme
    for dx in (-48, 48):
        d.ellipse([cx + dx - 16, cy + 6, cx + dx + 16, cy + 30], fill=(255, 160, 140))
        d.ellipse([cx + dx * .55 - 8, cy - 28, cx + dx * .55 + 8, cy - 12], fill=MURDUM)
    d.arc([cx - 32, cy - 10, cx + 32, cy + 40], 20, 160, fill=MURDUM, width=7)


PURE = {"havuc": (255, 150, 60), "balkabagi": (255, 176, 60), "brokoli": (120, 190, 90), "elma": (250, 220, 150),
        "armut": (228, 226, 140), "avokado": (170, 210, 110), "kabak": (190, 220, 130), "patates": (240, 214, 150),
        "muz": (255, 228, 140), "karnabahar": (240, 226, 186)}


def kase(d, cx, cy, w=270, renk=NANE, ici=(255, 150, 60), koyu=K_NANE):
    d.ellipse([cx - w / 2 + 18, cy - 52, cx + w / 2 - 18, cy + 32], fill=ici)
    d.chord([cx - w / 2, cy - 115, cx + w / 2, cy + 145], 0, 180, fill=renk)
    d.line([(cx - w / 2 + 30, cy + 55), (cx + w / 2 - 30, cy + 55)], fill=BEYAZ, width=8)
    for dx in (-60, 0, 60):
        kalp(d, cx + dx, cy + 88, 12, BEYAZ)
    d.rounded_rectangle([cx - 58, cy + 136, cx + 58, cy + 156], radius=10, fill=renk)
    d.line([(cx + 40, cy - 28), (cx + 120, cy - 100)], fill=koyu, width=15)
    d.ellipse([cx + 14, cy - 58, cx + 72, cy - 6], fill=koyu)


def sebze(d, ad, cx, cy, s=1.0):
    Y = (110, 170, 80)
    if ad == "havuc":
        d.polygon([(cx - 34 * s, cy - 70 * s), (cx + 34 * s, cy - 70 * s), (cx, cy + 110 * s)], fill=(255, 140, 50))
        for k in (-1, 0, 1):
            d.ellipse([cx + k * 22 * s - 12 * s, cy - 125 * s, cx + k * 22 * s + 12 * s, cy - 62 * s], fill=Y)
        for yy in (-30, 5, 40):
            d.line([(cx - 14 * s, cy + yy * s), (cx + 2 * s, cy + yy * s)], fill=(214, 100, 40), width=max(3, int(5 * s)))
    elif ad == "balkabagi":
        for dx, ww in ((-55, 90), (55, 90), (0, 100)):
            d.ellipse([cx + dx * s - ww * s, cy - 80 * s, cx + dx * s + ww * s, cy + 80 * s], fill=(255, 166, 60))
        for dx in (-40, 40):
            d.arc([cx + dx * s - 38 * s, cy - 76 * s, cx + dx * s + 38 * s, cy + 76 * s], 270 if dx > 0 else 90,
                  90 if dx > 0 else 270, fill=(220, 120, 40), width=max(3, int(5 * s)))
        d.rounded_rectangle([cx - 10 * s, cy - 115 * s, cx + 10 * s, cy - 72 * s], radius=6, fill=Y)
    elif ad == "brokoli":
        d.polygon([(cx - 22 * s, cy + 10 * s), (cx + 22 * s, cy + 10 * s), (cx + 16 * s, cy + 110 * s),
                   (cx - 16 * s, cy + 110 * s)], fill=(150, 200, 110))
        for dx, dy, r in ((-55, -10, 48), (55, -10, 48), (0, -55, 58), (-30, 15, 40), (30, 15, 40)):
            d.ellipse([cx + (dx - r) * s, cy + (dy - r) * s, cx + (dx + r) * s, cy + (dy + r) * s], fill=(84, 160, 80))
        for dx, dy in ((-40, -30), (20, -70), (45, -5), (-5, -20)):
            d.ellipse([cx + (dx - 8) * s, cy + (dy - 8) * s, cx + (dx + 8) * s, cy + (dy + 8) * s], fill=(120, 190, 100))
    elif ad == "karnabahar":
        for dx, dy, a in ((-80, 40, -35), (80, 40, 35), (0, 70, 0)):
            d.ellipse([cx + (dx - 40) * s, cy + (dy - 22) * s, cx + (dx + 40) * s, cy + (dy + 22) * s],
                      fill=(110, 180, 100))
        for dx, dy, r in ((-55, -5, 50), (55, -5, 50), (0, -50, 58), (-28, 25, 42), (28, 25, 42)):
            d.ellipse([cx + (dx - r) * s, cy + (dy - r) * s, cx + (dx + r) * s, cy + (dy + r) * s],
                      fill=(250, 240, 214), outline=(214, 196, 150), width=max(2, int(4 * s)))
        for dx, dy in ((-40, -25), (20, -65), (45, 0), (-5, -15), (0, 30)):
            d.ellipse([cx + (dx - 9) * s, cy + (dy - 9) * s, cx + (dx + 9) * s, cy + (dy + 9) * s], fill=(236, 222, 186))
    elif ad == "elma":
        d.ellipse([cx - 95 * s, cy - 70 * s, cx + 5 * s, cy + 90 * s], fill=(236, 80, 90))
        d.ellipse([cx - 5 * s, cy - 70 * s, cx + 95 * s, cy + 90 * s], fill=(236, 80, 90))
        d.ellipse([cx - 60 * s, cy - 40 * s, cx - 30 * s, cy - 5 * s], fill=(250, 150, 150))
        d.line([(cx, cy - 60 * s), (cx + 8 * s, cy - 110 * s)], fill=(120, 80, 50), width=max(4, int(9 * s)))
        yaprak(d, cx + 38 * s, cy - 100 * s, 22 * s, Y, 20)
    elif ad == "armut":
        c = (196, 210, 90)
        d.ellipse([cx - 90 * s, cy - 10 * s, cx + 90 * s, cy + 120 * s], fill=c)
        d.ellipse([cx - 55 * s, cy - 90 * s, cx + 55 * s, cy + 40 * s], fill=c)
        d.line([(cx, cy - 85 * s), (cx + 6 * s, cy - 125 * s)], fill=(120, 80, 50), width=max(4, int(9 * s)))
        yaprak(d, cx + 34 * s, cy - 118 * s, 20 * s, Y, 20)
    elif ad == "avokado":
        d.ellipse([cx - 80 * s, cy - 110 * s, cx + 80 * s, cy + 110 * s], fill=(70, 130, 60))
        d.ellipse([cx - 62 * s, cy - 88 * s, cx + 62 * s, cy + 92 * s], fill=(200, 230, 140))
        d.ellipse([cx - 34 * s, cy - 2 * s, cx + 34 * s, cy + 66 * s], fill=(150, 96, 60))
    elif ad == "kabak":
        m = Image.new("L", (int(300 * s), int(300 * s)), 0)
        md = ImageDraw.Draw(m)
        md.rounded_rectangle([20 * s, 115 * s, 280 * s, 185 * s], radius=int(35 * s), fill=255)
        m = m.rotate(28, resample=Image.BICUBIC)
        d._image.paste(Image.new("RGB", m.size, (96, 160, 80)), (int(cx - 150 * s), int(cy - 150 * s)), m)
        d.ellipse([cx + 98 * s, cy - 82 * s, cx + 122 * s, cy - 58 * s], fill=(150, 110, 60))
        for k in (-60, 0, 60):
            d.ellipse([cx + k * s - 6 * s, cy - k * .53 * s - 4 * s, cx + k * s + 6 * s, cy - k * .53 * s + 4 * s],
                      fill=(150, 200, 120))
    elif ad == "patates":
        d.polygon(blob_poligon(cx, cy, 90 * s, 7), fill=(214, 168, 110))
        for dx, dy in ((-30, -20), (25, 10), (-5, 40), (40, -35)):
            d.ellipse([cx + (dx - 6) * s, cy + (dy - 5) * s, cx + (dx + 6) * s, cy + (dy + 5) * s], fill=(170, 124, 76))
    elif ad == "muz":
        m = Image.new("L", (int(320 * s), int(320 * s)), 0)
        md = ImageDraw.Draw(m)
        md.ellipse([20 * s, 20 * s, 300 * s, 300 * s], fill=255)
        md.ellipse([20 * s, -30 * s, 300 * s, 230 * s], fill=0)  # hilal maske
        d._image.paste(Image.new("RGB", m.size, (255, 206, 60)), (int(cx - 160 * s), int(cy - 160 * s)), m)
        d.ellipse([cx - 135 * s, cy - 10 * s, cx - 115 * s, cy + 12 * s], fill=(120, 90, 40))
        d.ellipse([cx + 115 * s, cy - 10 * s, cx + 135 * s, cy + 12 * s], fill=(120, 90, 40))


def takvim(d, cx, cy, sayi, w=280, ust=K_LILA):
    h = w
    d.rounded_rectangle([cx - w / 2 + 10, cy - h / 2 + 14, cx + w / 2 + 10, cy + h / 2 + 14], radius=36, fill=LILA)
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=36, fill=BEYAZ)
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy - h / 2 + 80], radius=36, fill=ust)
    d.rectangle([cx - w / 2, cy - h / 2 + 44, cx + w / 2, cy - h / 2 + 80], fill=ust)
    for dx in (-80, 80):
        d.rounded_rectangle([cx + dx - 12, cy - h / 2 - 28, cx + dx + 12, cy - h / 2 + 30], radius=10, fill=MURDUM)
    f = font("ExtraBold", 34)
    d.text((cx - d.textlength("HAFTA", font=f) / 2, cy - h / 2 + 22), "HAFTA", font=f, fill=BEYAZ)
    f = font("Black", 140)
    t = str(sayi)
    d.text((cx - d.textlength(t, font=f) / 2, cy - 55), t, font=f, fill=MURDUM)


def biberon(d, cx, cy, s=1.0):
    d.rounded_rectangle([cx - 55 * s, cy - 40 * s, cx + 55 * s, cy + 150 * s], radius=int(40 * s), fill=BEYAZ,
                        outline=K_GOK, width=max(4, int(7 * s)))
    d.rounded_rectangle([cx - 50 * s, cy + 40 * s, cx + 50 * s, cy + 144 * s], radius=int(34 * s), fill=(214, 236, 255))
    d.rounded_rectangle([cx - 66 * s, cy - 75 * s, cx + 66 * s, cy - 35 * s], radius=int(16 * s), fill=PUDRA)
    d.ellipse([cx - 30 * s, cy - 140 * s, cx + 30 * s, cy - 70 * s], fill=SEFTALI)
    d.rectangle([cx - 30 * s, cy - 105 * s, cx + 30 * s, cy - 72 * s], fill=SEFTALI)
    for i in range(3):
        yy = cy + (10 + i * 38) * s
        d.line([(cx + 20 * s, yy), (cx + 48 * s, yy)], fill=K_GOK, width=max(3, int(5 * s)))


def damla(d, cx, cy, s, renk):
    d.ellipse([cx - 40 * s, cy - 20 * s, cx + 40 * s, cy + 60 * s], fill=renk)
    d.polygon([(cx - 36 * s, cy + 8 * s), (cx + 36 * s, cy + 8 * s), (cx, cy - 70 * s)], fill=renk)
    d.ellipse([cx - 22 * s, cy + 5 * s, cx - 8 * s, cy + 25 * s], fill=BEYAZ)


def baloncuklar(d, cx, cy, s=1.0):
    for dx, dy, r in ((-70, 20, 70), (40, -40, 55), (75, 55, 40), (-10, -95, 30), (-110, -70, 22)):
        d.ellipse([cx + (dx - r) * s, cy + (dy - r) * s, cx + (dx + r) * s, cy + (dy + r) * s], fill=(255, 255, 255),
                  outline=K_NANE, width=max(3, int(6 * s)))
        d.arc([cx + (dx - r * .65) * s, cy + (dy - r * .65) * s, cx + (dx + r * .65) * s, cy + (dy + r * .65) * s],
              200, 260, fill=GOK, width=max(3, int(6 * s)))
    yildiz(d, cx + 130 * s, cy - 90 * s, 16 * s, LIMON)
    yildiz(d, cx - 150 * s, cy + 70 * s, 12 * s, K_NANE)


def kalp_cicek(d, cx, cy, s=1.0):
    for a in range(0, 360, 72):
        r = math.radians(a)
        x, y = cx + math.cos(r) * 62 * s, cy + math.sin(r) * 62 * s
        d.ellipse([x - 48 * s, y - 48 * s, x + 48 * s, y + 48 * s], fill=PUDRA)
    kalp(d, cx, cy + 4 * s, 46 * s, K_PEMBE)
    yildiz(d, cx + 140 * s, cy - 70 * s, 14 * s, LILA)
    yildiz(d, cx - 140 * s, cy + 60 * s, 11 * s, SEFTALI)


def tik(d, x, y, r=28, renk=K_NANE):
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=renk)
    d.line([(x + r * .5, y + r * 1.0), (x + r * .9, y + r * 1.4), (x + r * 1.55, y + r * .65)], fill=BEYAZ,
           width=max(5, int(r * .26)))


def numara(d, x, y, n, r=28, renk=K_MERCAN):
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=renk)
    f = font("ExtraBold", int(r * 1.1))
    t = str(n)
    bb = d.textbbox((0, 0), t, font=f)
    d.text((x + r - (bb[2] + bb[0]) / 2, y + r - (bb[3] + bb[1]) / 2), t, font=f, fill=BEYAZ)


def carpi(d, cx, cy, r=30, renk=K_PEMBE):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=renk)
    q = r * .42
    d.line([(cx - q, cy - q), (cx + q, cy + q)], fill=BEYAZ, width=8)
    d.line([(cx - q, cy + q), (cx + q, cy - q)], fill=BEYAZ, width=8)


def konusma(d, cx, cy, w=360, h=190):
    d.rounded_rectangle([cx - w / 2 + 10, cy - h / 2 + 14, cx + w / 2 + 10, cy + h / 2 + 14], radius=70, fill=LILA)
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=70, fill=K_PEMBE)
    d.polygon([(cx - 60, cy + h / 2 - 5), (cx - 130, cy + h / 2 + 70), (cx + 10, cy + h / 2 - 5)], fill=K_PEMBE)
    for dx in (-90, 0, 90):
        d.ellipse([cx + dx - 22, cy - 22, cx + dx + 22, cy + 22], fill=BEYAZ)


# ---------------- ortak bloklar ----------------
def bilgi_karti(d, y, etiket_metni, metin, k, tur, fill=BEYAZ, s=46, wgt="SemiBold", etiket_bg=None):
    koyu = TEMA[tur][3]
    f = F(wgt, s, k)
    th = yukseklik(d, metin, f, 820, 1.33)
    ust = 40 + (64 if etiket_metni else 0)
    h = ust + th + 34
    kart(d, y, y + h, fill=fill, golge=golge_rengi(tur) if fill == BEYAZ else None)
    if etiket_metni:
        rozet(d, 130, y + 38, etiket_metni, etiket_bg or koyu, s=28)
    yaz(d, 130, y + ust + (20 if etiket_metni else 0), metin, f, MURDUM, 820, 1.33)
    return y + h + (20 if etiket_metni else 0)


def madde_kartlari(d, y, maddeler, k, tur, numarali=False, isaret=None, s=42):
    koyu = TEMA[tur][3]
    f = F("SemiBold", s, k)
    for i, m in enumerate(maddeler, 1):
        th = yukseklik(d, m, f, 730, 1.3)
        h = max(th + 46, 104)
        kart(d, y, y + h, fill=BEYAZ, r=34)
        cy = y + h / 2
        if numarali:
            numara(d, 112, cy - 30, i, r=30, renk=isaret or koyu)
        else:
            tik(d, 112, cy - 30, r=30, renk=isaret or koyu)
        yaz(d, 200, y + (h - th) / 2 + 4, m, f, MURDUM, 730, 1.3)
        y += h + 18
    return y


# ---------------- şablonlar ----------------
def gunaydin(path, bilgi, kaynak, baslik="Günaydın"):
    def ciz(k):
        img, d = zemin("gunaydin")
        gunes(d, 540, 470)
        y = yaz(d, 0, 680, baslik, F("Black", 132, 1), MURDUM, 960, center=True)
        y = yaz(d, 0, y + 4, "güzel bir gün dileriz", F("SemiBold", 44, 1), K_MERCAN, 960, center=True) + 50
        y = bilgi_karti(d, y, "GÜNÜN BİLGİSİ", bilgi, k, "gunaydin", s=50)
        alt_bilgi(d, kaynak)
        return img, y
    return sigdir(ciz, path)


def tarif_karti(path, seri, ay, baslik, malzemeler, adimlar, saklama, dikkat, kaynak, cizim="havuc"):
    def ciz(k):
        img, d = zemin("tarif")
        _, x2 = rozet(d, 80, 250, seri_no(seri, "Tarif"), K_MERCAN)
        f = font("ExtraBold", 30)
        aw = d.textlength(tr_buyuk(ay), font=f) + 52
        rozet(d, 1000 - aw, 250, ay, LIMON, fg=MURDUM)
        y = yaz(d, 80, 345, baslik, F("Black", 96, min(1, k + .1)), MURDUM, 560, 1.08)
        kase(d, 870, 480, w=230, renk=NANE, ici=PURE.get(cizim, (255, 150, 60)), koyu=K_NANE)
        sebze(d, cizim, 680, 450, 0.48)
        y = max(y, 640) + 10
        # malzeme + adım kartı
        fm, fa = F("Medium", 40, k), F("Medium", 37, k)
        fh = F("ExtraBold", 42, k)
        ih = int(fh.size * 1.6)
        for m in malzemeler:
            ih += yukseklik(d, m, fm, 820, 1.28)
        ih += 24 + int(fh.size * 1.6)
        for a in adimlar:
            ih += yukseklik(d, a, fa, 800, 1.26) + 10
        h = ih + 60
        kart(d, y, y + h, golge=golge_rengi("tarif"))
        yy = y + 32
        d.text((120, yy), "Malzemeler", font=fh, fill=K_MERCAN)
        yy += int(fh.size * 1.6)
        for m in malzemeler:
            d.ellipse([122, yy + fm.size * .4, 142, yy + fm.size * .4 + 20], fill=SEFTALI)
            yy = yaz(d, 162, yy, m, fm, MURDUM, 820, 1.28)
        yy += 24
        d.text((120, yy), "Hazırlanışı", font=fh, fill=K_MERCAN)
        yy += int(fh.size * 1.6)
        for i, a in enumerate(adimlar, 1):
            numara(d, 116, yy - 2, i, r=int(23 * k) + 1, renk=K_MERCAN)
            yy = yaz(d, 180, yy, a, fa, MURDUM, 800, 1.26) + 10
        y += h + 24
        fs = F("SemiBold", 34, k)
        y = yaz(d, 90, y, "Saklama: " + saklama, fs, MURDUM, 900, 1.3) + 18
        fd = F("SemiBold", 36, k)
        th = yukseklik(d, dikkat, fd, 800, 1.3)
        h = 76 + th + 26
        kart(d, y, y + h, fill=(255, 226, 232), r=32)
        d.text((125, y + 26), "DİKKAT", font=font("ExtraBold", 30), fill=K_PEMBE)
        yaz(d, 125, y + 72, dikkat, fd, MURDUM, 800, 1.3)
        alt_bilgi(d, kaynak)
        return img, y + h
    return sigdir(ciz, path)


def hamilelik_haftasi(path, seri, hafta, boy, bilgi, ipucu, kaynak):
    def ciz(k):
        img, d = zemin("hamilelik")
        rozet(d, 0, 250, f"Hafta {hafta}", K_LILA, center=True)
        takvim(d, 540, 500, hafta, w=260)
        y = yaz(d, 0, 680, f"Hamileliğin {hafta}. haftası", F("Black", 76, min(1, k + .1)), MURDUM, 940, 1.1,
                center=True) + 14
        fb = F("ExtraBold", 40, k)
        t = "Bebeğin boyu: " + boy
        tw = d.textlength(t, font=fb)
        if tw > 860:
            raise Tasma("boy")
        x0 = (W - tw - 70) / 2
        d.rounded_rectangle([x0 - 10, y, x0 + tw + 80, y + fb.size + 34], radius=(fb.size + 34) // 2, fill=BEYAZ)
        d.ellipse([x0 + 14, y + (fb.size + 34) / 2 - 13, x0 + 40, y + (fb.size + 34) / 2 + 13], fill=K_LILA)
        d.text((x0 + 56, y + 14), t, font=fb, fill=K_LILA)
        y += fb.size + 34 + 30
        y = bilgi_karti(d, y, None, bilgi, k, "hamilelik", s=42, wgt="Medium") + 20
        y = bilgi_karti(d, y, "Anne için ipucu", ipucu, k, "hamilelik", fill=(236, 226, 252), s=40,
                        etiket_bg=K_LILA)
        alt_bilgi(d, kaynak)
        return img, y
    return sigdir(ciz, path)


def _bilgi_maddeli(path, tur, onek, seri, baslik, bilgi, maddeler, not_metni, kaynak, cizim):
    def ciz(k):
        img, d = zemin(tur)
        koyu = TEMA[tur][3]
        rozet(d, 0, 250, seri_no(seri, onek), koyu, center=True)
        cizim(d)
        y = yaz(d, 0, 600, baslik, F("Black", 78, min(1, k + .1)), MURDUM, 920, 1.1, center=True) + 30
        if bilgi:
            y = bilgi_karti(d, y, None, bilgi, k, tur, s=42, wgt="Medium") + 18
        if maddeler:
            y = madde_kartlari(d, y, maddeler, k, tur, s=40)
        if not_metni:
            y = yaz(d, 0, y + 6, not_metni, F("SemiBold", 34, k), koyu, 880, 1.3, center=True)
        alt_bilgi(d, kaynak)
        return img, y
    return sigdir(ciz, path)


def lohusa(path, seri, baslik, bilgi, kaynak, maddeler=None, not_metni=None):
    return _bilgi_maddeli(path, "lohusa", "Doğum sonrası", seri, baslik, bilgi, maddeler, not_metni, kaynak,
                          lambda d: kalp_cicek(d, 540, 450, 1.0))


def emzirme(path, seri, baslik, bilgi, kaynak, maddeler=None, not_metni=None):
    def c(d):
        biberon(d, 470, 455, 0.85)  # emzik ucu rozete değmesin
        damla(d, 640, 470, 1.0, (120, 180, 240))
        damla(d, 720, 380, .6, LILA)
    return _bilgi_maddeli(path, "emzirme", "Bebek beslenmesi", seri, baslik, bilgi, maddeler, not_metni, kaynak, c)


def temizlik(path, seri, baslik, maddeler, uyari, kaynak):
    def ciz(k):
        img, d = zemin("temizlik")
        rozet(d, 0, 250, seri_no(seri, "Temizlik tüyosu"), K_NANE, center=True)
        baloncuklar(d, 540, 455, 1.0)
        y = yaz(d, 0, 600, baslik, F("Black", 78, min(1, k + .1)), MURDUM, 920, 1.1, center=True) + 30
        y = madde_kartlari(d, y, maddeler, k, "temizlik", numarali=True, s=40)
        if uyari:
            fd = F("SemiBold", 36, k)
            th = yukseklik(d, uyari, fd, 800, 1.3)
            h = 76 + th + 26
            kart(d, y, y + h, fill=(255, 226, 232), r=32)
            d.text((125, y + 26), "DİKKAT", font=font("ExtraBold", 30), fill=K_PEMBE)
            yaz(d, 125, y + 72, uyari, fd, MURDUM, 800, 1.3)
            y += h
        alt_bilgi(d, kaynak, "Bilgilendirme amaçlıdır.")
        return img, y
    return sigdir(ciz, path)


def haber(path, baslik, ozet, tarih, kaynak):
    def ciz(k):
        img, d = zemin("haber")
        yb, x2 = rozet(d, 80, 250, "Güncel", K_LIMON)
        if tarih:
            rozet(d, x2 + 16, 250, tarih, BEYAZ, fg=K_LIMON)
        # gazete çizimi
        d.rounded_rectangle([700, 360, 960, 560], radius=24, fill=BEYAZ, outline=K_LIMON, width=6)
        d.rectangle([730, 392, 930, 420], fill=LIMON)
        for i in range(4):
            d.line([(730, 450 + i * 28), (930 if i % 2 == 0 else 870, 450 + i * 28)], fill=(230, 200, 120), width=8)
        yildiz(d, 975, 350, 14, K_LIMON)
        y = yaz(d, 80, 350, baslik, F("Black", 74, min(1, k + .1)), MURDUM, 590, 1.1)
        y = max(y, 600) + 24
        y = bilgi_karti(d, y, None, ozet, k, "haber", s=42, wgt="Medium") + 16
        fk = F("ExtraBold", 34, k)
        t = "Kaynak: " + kaynak
        th = yukseklik(d, t, fk, 820, 1.3)
        kart(d, y, y + th + 40, fill=LIMON, r=30)
        yaz(d, 130, y + 20, t, fk, MURDUM, 820, 1.3)
        y += th + 40
        alt_bilgi(d, None, "Ayrıntılar için resmi duyuruyu inceleyin.")
        return img, y
    return sigdir(ciz, path)


def efsane_gercek(path, efsane, gercek, kaynak, seri=None):
    def ciz(k):
        img, d = zemin("efsane")
        y, _ = rozet(d, 0, 250, seri or "Efsane mi, gerçek mi?", K_PEMBE, center=True)
        y = yaz(d, 0, y + 36, "Efsane mi,\ngerçek mi?", F("Black", 100, min(1, k + .1)), MURDUM, 960, 1.08,
                center=True) + 28
        f = F("SemiBold", 44, k)
        for etk, metin, fill, ikon, renk in (("EFSANE", efsane, (255, 222, 234), "x", K_PEMBE),
                                             ("GERÇEK", gercek, (214, 244, 230), "t", K_NANE)):
            th = yukseklik(d, metin, f, 800, 1.33)
            h = 108 + th + 34
            kart(d, y, y + h, fill=fill, r=40)
            if ikon == "x":
                carpi(d, 150, y + 62, 30, renk)
            else:
                tik(d, 120, y + 32, r=30, renk=renk)
            d.text((200, y + 40), etk, font=font("ExtraBold", 38), fill=renk)
            yaz(d, 130, y + 110, metin, f, MURDUM, 800, 1.33)
            y += h + 32
        alt_bilgi(d, kaynak)
        return img, y - 32
    return sigdir(ciz, path)


def hap(path, seri, baslik, bilgi, kaynak):
    def ciz(k):
        img, d = zemin("hap")
        rozet(d, 0, 250, seri_no(seri, "Hap bilgi"), K_MERCAN, center=True)
        # büyük vurgu: limon blob üzerinde dev başlık
        kat = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(kat).polygon(blob_poligon(540, 640, 330, 3), fill=LIMON + (235,))
        img = Image.alpha_composite(img.convert("RGBA"), kat).convert("RGB")
        d = ImageDraw.Draw(img)
        dekor(d, "hap")
        rozet(d, 0, 250, seri_no(seri, "Hap bilgi"), K_MERCAN, center=True)
        for s in (190, 170, 150, 130, 112, 96, 84, 74):
            fb = font("Black", s)
            try:
                lns = sar(d, baslik, fb, 760)
            except Tasma:
                continue
            if len(lns) * s * 1.05 <= 400:
                break
        else:
            raise Tasma("hap başlık")
        th = len(lns) * int(fb.size * 1.05)
        y = yaz(d, 0, 640 - th / 2 - fb.size * .1, baslik, fb, K_MERCAN, 760, 1.05, center=True)
        y = max(y, 1000) + 10
        y = bilgi_karti(d, y, None, bilgi, k, "hap", s=46, wgt="SemiBold")
        alt_bilgi(d, kaynak)
        return img, y
    return sigdir(ciz, path)


def kontrol_listesi(path, etiket_metni, baslik, maddeler, kaynak, numarali=False, not_metni=None):
    tur = "liste" if numarali else "kontrol"

    def ciz(k):
        img, d = zemin(tur)
        koyu = TEMA[tur][3]
        rozet(d, 0, 250, etiket_metni, koyu, center=True)
        y = yaz(d, 0, 350, baslik, F("Black", 80, min(1, k + .1)), MURDUM, 920, 1.12, center=True) + 40
        y = madde_kartlari(d, y, maddeler, k, tur, numarali=numarali, s=42,
                           isaret=K_LILA if numarali else K_NANE)
        if not_metni:
            y = yaz(d, 0, y + 10, not_metni, F("SemiBold", 36, k), koyu, 880, 1.3, center=True)
        alt_bilgi(d, kaynak)
        return img, y
    return sigdir(ciz, path)


def dm_cagrisi(path, soru, secenekler, cagri):
    def ciz(k):
        img, d = zemin("dm")
        rozet(d, 0, 250, "Size soruyoruz", K_LILA, center=True)
        konusma(d, 540, 460)
        y = yaz(d, 0, 640, soru, F("Black", 82, min(1, k + .1)), MURDUM, 920, 1.12, center=True) + 40
        f = F("ExtraBold", 46, k)
        renk = [PUDRA, LILA, (255, 214, 196), NANE]
        if len(secenekler) > 2 and all(d.textlength(x, font=f) <= 350 for x in secenekler):
            for i, s_ in enumerate(secenekler):
                x0 = 110 if i % 2 == 0 else 555
                yy = y + (i // 2) * 130
                d.rounded_rectangle([x0, yy, x0 + 415, yy + 108], radius=54, fill=BEYAZ, outline=renk[i % 4], width=8)
                d.text((x0 + (415 - d.textlength(s_, font=f)) / 2, yy + (108 - f.size) / 2 - 6), s_, font=f,
                       fill=MURDUM)
            y += ((len(secenekler) + 1) // 2) * 130
        else:
            for i, s_ in enumerate(secenekler):
                th = yukseklik(d, s_, f, 700, 1.25)
                h = th + 50
                d.rounded_rectangle([160, y, 920, y + h], radius=min(54, h // 2), fill=BEYAZ, outline=renk[i % 4],
                                    width=8)
                yaz(d, 0, y + 25, s_, f, MURDUM, 700, 1.25, center=True)
                y += h + 22
        y += 20
        kalp(d, 540, y + 22, 28, K_PEMBE)
        y = yaz(d, 0, y + 78, cagri, F("SemiBold", 42, k), MURDUM, 880, 1.3, center=True)
        alt_bilgi(d, None, None)
        return img, y
    return sigdir(ciz, path)
