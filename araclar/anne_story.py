"""@utopikanne hikâye şablonları (1080x1920, güvenli alan y=250–1580). Sıcak, sade marka kiti."""
import math
from PIL import Image, ImageDraw, ImageFont

HANDLE = "@utopikanne"
KREM = (250, 243, 235)
SEFTALI = (240, 168, 138)
ADACAYI = (150, 178, 148)
KAHVE = (74, 54, 44)
SOLUK = (150, 128, 115)
GECE = (40, 36, 62)
GECE2 = (58, 52, 86)
AY = (250, 232, 196)
INTER = "/usr/share/fonts/opentype/inter/Inter-{}.otf"


def font(w="Bold", s=48):
    return ImageFont.truetype(INTER.format(w), s)


def wrap(d, text, fnt, max_w):
    out = []
    for para in text.split("\n"):
        cur = ""
        for w in para.split(" "):
            t = (cur + " " + w).strip()
            if d.textlength(t, font=fnt) <= max_w:
                cur = t
            else:
                out.append(cur)
                cur = w
        out.append(cur)
    return out


def yaz(d, xy, text, fnt, fill, max_w=920, sp=1.3, center=False, W=1080):
    x, y = xy
    for ln in wrap(d, text, fnt, max_w):
        xx = (W - d.textlength(ln, font=fnt)) / 2 if center else x
        d.text((xx, y), ln, font=fnt, fill=fill)
        y += int(fnt.size * sp)
    return y


def iyi_geceler(path, baslik, bilgi, kaynak, alt="Tatlı rüyalar, yarın sabah görüşmek üzere.", saglik=True):
    W, H = 1080, 1920
    img = Image.new("RGB", (W, H), GECE)
    d = ImageDraw.Draw(img)
    for i in range(H):  # yumuşak dikey geçiş
        t = i / H
        d.line([(0, i), (W, i)], fill=tuple(int(GECE[k] * (1 - t) + GECE2[k] * t) for k in range(3)))
    # hilal + yıldızlar
    cx, cy, r = 540, 470, 120
    m = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(m)
    md.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    md.ellipse([cx - r + 60, cy - r - 30, cx + r + 60, cy + r - 30], fill=0)  # hilal: daire eksi kaydırılmış daire
    img.paste(Image.new("RGB", (W, H), AY), (0, 0), m)
    for sx, sy, s in [(250, 330, 9), (820, 300, 7), (880, 560, 10), (200, 600, 6), (700, 250, 5), (380, 250, 4)]:
        d.polygon([(sx, sy - s * 2), (sx + s * .6, sy - s * .6), (sx + s * 2, sy), (sx + s * .6, sy + s * .6),
                   (sx, sy + s * 2), (sx - s * .6, sy + s * .6), (sx - s * 2, sy), (sx - s * .6, sy - s * .6)], fill=AY)
    y = yaz(d, (0, 680), "İyi geceler", font("Black", 118), AY, center=True)
    y = yaz(d, (0, y + 10), "anneler, babalar ve minikler", font("Medium", 44), (205, 196, 220), center=True)
    y += 60
    kart_y = y
    bl = wrap(d, bilgi, font("SemiBold", 46), 820)
    tl = wrap(d, baslik, font("ExtraBold", 54), 820)
    h = 130 + len(tl) * 70 + len(bl) * 62 + 70 + (38 if saglik else 0)
    d.rounded_rectangle([90, kart_y, 990, kart_y + h], radius=44, fill=(250, 243, 235))
    d.rounded_rectangle([130, kart_y + 40, 130 + d.textlength("BİLİYOR MUYDUN?", font=font("ExtraBold", 30)) + 44, kart_y + 92],
                        radius=26, fill=SEFTALI)
    d.text((152, kart_y + 50), "BİLİYOR MUYDUN?", font=font("ExtraBold", 30), fill=(74, 30, 42))
    yy = yaz(d, (130, kart_y + 125), baslik, font("ExtraBold", 54), KAHVE, max_w=820, sp=1.25)
    yy = yaz(d, (130, yy + 8), bilgi, font("SemiBold", 46), KAHVE, max_w=820, sp=1.3)
    d.text((130, kart_y + h - 60 - (38 if saglik else 0)), "Kaynak: " + kaynak, font=font("Medium", 28), fill=SOLUK)
    if saglik:
        d.text((130, kart_y + h - 60), "Bilgilendirme amaçlıdır, doktoruna danış.", font=font("Medium", 26), fill=SOLUK)
    y = kart_y + h + 50
    y = yaz(d, (0, y), alt, font("Medium", 42), (225, 218, 236), center=True)
    assert y <= 1580, ("story taşıyor", y)
    hw = d.textlength(HANDLE, font=font("Bold", 34))
    d.text(((W - hw) / 2, 1640), HANDLE, font=font("Bold", 34), fill=(205, 196, 220))
    img.save(path)
    return path



# ---------------- Gündüz şablonları (krem zemin) ----------------
W, H = 1080, 1920
BEYAZ = (255, 255, 255)
SEFTALI_ACIK = (250, 222, 205)
ADACAYI_ACIK = (220, 232, 215)
TURUNCU = (232, 132, 72)
YESIL = (110, 150, 100)
SARI = (246, 196, 92)
SAGLIK_NOT = "Bilgilendirme amaçlıdır, doktoruna danış."


def zemin(ust=KREM, alt=(246, 232, 220)):
    img = Image.new("RGB", (W, H), ust)
    d = ImageDraw.Draw(img)
    for i in range(H):
        t = i / H
        d.line([(0, i), (W, i)], fill=tuple(int(ust[k] * (1 - t) + alt[k] * t) for k in range(3)))
    return img, d


def tr_buyuk(t):
    return t.replace("i", "İ").replace("ı", "I").upper()


def etiket(d, x, y, text, bg=SEFTALI, fg=BEYAZ, s=30, center=False):
    text = tr_buyuk(text)
    f = font("ExtraBold", s)
    w = d.textlength(text, font=f) + 48
    if center:
        x = (W - w) / 2
    d.rounded_rectangle([x, y, x + w, y + s + 26], radius=(s + 26) // 2, fill=bg)
    d.text((x + 24, y + 11), text, font=f, fill=fg)
    return y + s + 26


def alt_bilgi(d, kaynak=None, saglik=True, renk=SOLUK, y=1500):
    """Kaynak + sağlık notu güvenli alanın en altında (y..1580)."""
    if kaynak:
        t = "Kaynak: " + kaynak
        d.text(((W - d.textlength(t, font=font("Medium", 28))) / 2, y), t, font=font("Medium", 28), fill=renk)
    if saglik:
        d.text(((W - d.textlength(SAGLIK_NOT, font=font("Medium", 26))) / 2, y + 44), SAGLIK_NOT,
               font=font("Medium", 26), fill=renk)
    hw = d.textlength(HANDLE, font=font("Bold", 34))
    d.text(((W - hw) / 2, 1640), HANDLE, font=font("Bold", 34), fill=KAHVE)


def sinir(y, limit=1480):
    assert y <= limit, ("story taşıyor", y)


# --- basit vektör çizimler (yalnızca kendi çizimlerimiz) ---
def gunes(d, cx, cy, r=110):
    for a in range(0, 360, 30):
        rad = math.radians(a)
        x1, y1 = cx + math.cos(rad) * (r + 25), cy + math.sin(rad) * (r + 25)
        x2, y2 = cx + math.cos(rad) * (r + 70), cy + math.sin(rad) * (r + 70)
        d.line([(x1, y1), (x2, y2)], fill=SARI, width=16)
        d.ellipse([x2 - 8, y2 - 8, x2 + 8, y2 + 8], fill=SARI)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SARI)
    d.ellipse([cx - r + 22, cy - r + 22, cx + r - 22, cy + r - 22], fill=(250, 210, 120))


def kase(d, cx, cy, w=300, renk=ADACAYI, ici=TURUNCU):
    # püre, kase, kaşık
    d.ellipse([cx - w / 2 + 20, cy - 55, cx + w / 2 - 20, cy + 35], fill=ici)
    d.chord([cx - w / 2, cy - 120, cx + w / 2, cy + 150], 0, 180, fill=renk)
    d.rectangle([cx - w / 2, cy + 13, cx + w / 2, cy + 19], fill=(130, 158, 128))
    d.rounded_rectangle([cx - 60, cy + 140, cx + 60, cy + 160], radius=10, fill=renk)
    # kaşık
    d.line([(cx + 40, cy - 30), (cx + 125, cy - 105)], fill=KAHVE, width=16)
    d.ellipse([cx + 15, cy - 60, cx + 75, cy - 5], fill=KAHVE)


def havuc(d, cx, cy, s=1.0):
    d.polygon([(cx - 34 * s, cy - 70 * s), (cx + 34 * s, cy - 70 * s), (cx, cy + 110 * s)], fill=TURUNCU)
    for k in (-1, 0, 1):
        d.ellipse([cx + k * 22 * s - 12 * s, cy - 125 * s, cx + k * 22 * s + 12 * s, cy - 62 * s], fill=YESIL)
    for yy in (-30, 5, 40):
        d.line([(cx - 14 * s, cy + yy * s), (cx + 2 * s, cy + yy * s)], fill=(205, 105, 50), width=int(5 * s))


def balkabagi(d, cx, cy, s=1.0):
    for dx, ww in ((-55, 90), (55, 90), (0, 100)):
        d.ellipse([cx + dx * s - ww * s, cy - 80 * s, cx + dx * s + ww * s, cy + 80 * s], fill=SARI)
    for dx in (-45, 45):
        d.arc([cx + dx * s - 40 * s, cy - 78 * s, cx + dx * s + 40 * s, cy + 78 * s], 100, 260 if dx < 0 else 440,
              fill=(205, 105, 50), width=int(5 * s))
    d.rounded_rectangle([cx - 10 * s, cy - 115 * s, cx + 10 * s, cy - 72 * s], radius=6, fill=YESIL)


def takvim(d, cx, cy, sayi, w=300):
    h = w * 1.0
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=36, fill=BEYAZ)
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy - h / 2 + 80], radius=36, fill=SEFTALI)
    d.rectangle([cx - w / 2, cy - h / 2 + 44, cx + w / 2, cy - h / 2 + 80], fill=SEFTALI)
    for dx in (-80, 80):
        d.rounded_rectangle([cx + dx - 12, cy - h / 2 - 28, cx + dx + 12, cy - h / 2 + 30], radius=10, fill=KAHVE)
    t = "HAFTA"
    d.text((cx - d.textlength(t, font=font("ExtraBold", 34)) / 2, cy - h / 2 + 22), t, font=font("ExtraBold", 34), fill=BEYAZ)
    f = font("Black", 150)
    t = str(sayi)
    d.text((cx - d.textlength(t, font=f) / 2, cy - 60), t, font=f, fill=KAHVE)


def tik(d, x, y, r=26, renk=ADACAYI):
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=renk)
    d.line([(x + r * .5, y + r * 1.0), (x + r * .9, y + r * 1.4), (x + r * 1.55, y + r * .65)], fill=BEYAZ, width=7)


def numara(d, x, y, n, r=28, renk=SEFTALI):
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=renk)
    f = font("ExtraBold", 32)
    t = str(n)
    d.text((x + r - d.textlength(t, font=f) / 2, y + r - 20), t, font=f, fill=BEYAZ)


def balon(d, cx, cy, w=420, h=250, renk=SEFTALI):
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=70, fill=renk)
    d.polygon([(cx - 60, cy + h / 2 - 5), (cx - 130, cy + h / 2 + 70), (cx + 10, cy + h / 2 - 5)], fill=renk)
    for dx in (-100, 0, 100):
        d.ellipse([cx + dx - 22, cy - 22, cx + dx + 22, cy + 22], fill=BEYAZ)


def kalp(d, cx, cy, s=40, renk=SEFTALI):
    d.ellipse([cx - s, cy - s * .8, cx, cy + s * .2], fill=renk)
    d.ellipse([cx, cy - s * .8, cx + s, cy + s * .2], fill=renk)
    d.polygon([(cx - s * .97, cy - s * .15), (cx + s * .97, cy - s * .15), (cx, cy + s * 1.05)], fill=renk)


# --- şablonlar ---
def gunaydin(path, bilgi, kaynak, baslik="Günaydın"):
    img, d = zemin(KREM, (250, 228, 205))
    gunes(d, 540, 470)
    y = yaz(d, (0, 690), baslik, font("Black", 124), KAHVE, center=True)
    y = yaz(d, (0, y + 6), "güzel bir gün olsun", font("Medium", 44), SOLUK, center=True)
    y += 60
    bl = wrap(d, bilgi, font("SemiBold", 48), 800)
    h = 150 + len(bl) * 64 + 30
    d.rounded_rectangle([90, y, 990, y + h], radius=44, fill=BEYAZ)
    etiket(d, 140, y + 44, "GÜNÜN BİLGİSİ", bg=ADACAYI)
    yy = yaz(d, (140, y + 130), bilgi, font("SemiBold", 48), KAHVE, max_w=800, sp=1.33)
    sinir(y + h)
    alt_bilgi(d, kaynak)
    img.save(path)
    return path


def tarif_karti(path, seri, ay, baslik, malzemeler, adimlar, saklama, dikkat, kaynak, cizim="havuc"):
    img, d = zemin(KREM, (247, 230, 216))
    etiket(d, 90, 250, seri, bg=ADACAYI)
    f = font("ExtraBold", 30)
    aw = d.textlength(ay, font=f) + 48
    etiket(d, 990 - aw, 250, ay, bg=SEFTALI)
    y = yaz(d, (90, 340), baslik, font("Black", 92), KAHVE, max_w=560, sp=1.1)
    kase(d, 840, 455, w=260)
    if cizim == "havuc":
        havuc(d, 680, 430, 0.55)
    else:
        balkabagi(d, 650, 545, 0.42)
    y = max(y, 600) + 10
    # malzemeler
    d.text((90, y), "Malzemeler", font=font("ExtraBold", 44), fill=TURUNCU)
    y += 66
    for m in malzemeler:
        d.ellipse([96, y + 16, 116, y + 36], fill=ADACAYI)
        y = yaz(d, (136, y), m, font("Medium", 40), KAHVE, max_w=840, sp=1.3)
    y += 20
    d.text((90, y), "Hazırlanışı", font=font("ExtraBold", 44), fill=TURUNCU)
    y += 70
    for i, a in enumerate(adimlar, 1):
        numara(d, 90, y - 4, i, r=24)
        y = yaz(d, (152, y), a, font("Medium", 37), KAHVE, max_w=830, sp=1.26) + 8
    y += 6
    y = yaz(d, (90, y), "Saklama: " + saklama, font("SemiBold", 34), SOLUK, max_w=900, sp=1.3) + 18
    lines = wrap(d, dikkat, font("SemiBold", 36), 800)
    h = 70 + len(lines) * 48 + 24
    d.rounded_rectangle([90, y, 990, y + h], radius=30, fill=SEFTALI_ACIK)
    d.text((130, y + 24), "DİKKAT", font=font("ExtraBold", 30), fill=TURUNCU)
    yaz(d, (130, y + 68), dikkat, font("SemiBold", 36), KAHVE, max_w=800, sp=1.3)
    sinir(y + h)
    alt_bilgi(d, kaynak)
    img.save(path)
    return path


def hamilelik_haftasi(path, seri, hafta, boy, bilgi, ipucu, kaynak):
    img, d = zemin((248, 238, 232), (240, 222, 214))
    etiket(d, 0, 250, seri, bg=ADACAYI, center=True)
    takvim(d, 540, 520, hafta, w=280)
    y = yaz(d, (0, 720), f"Hamileliğin {hafta}. haftası", font("Black", 74), KAHVE, center=True)
    y += 20
    # boy karşılaştırması: minik tohum çizimi + metin
    f = font("ExtraBold", 44)
    tw = d.textlength("Bebeğin boyu: " + boy, font=f)
    x0 = (W - tw - 60) / 2
    d.ellipse([x0, y + 14, x0 + 30, y + 44], fill=KAHVE)
    d.text((x0 + 60, y), "Bebeğin boyu: " + boy, font=f, fill=TURUNCU)
    y += 90
    y = yaz(d, (110, y), bilgi, font("Medium", 42), KAHVE, max_w=860, sp=1.35) + 30
    lines = wrap(d, ipucu, font("SemiBold", 40), 790)
    h = 80 + len(lines) * 54 + 30
    d.rounded_rectangle([90, y, 990, y + h], radius=36, fill=ADACAYI_ACIK)
    d.text((135, y + 28), "ANNE İÇİN İPUCU", font=font("ExtraBold", 30), fill=YESIL)
    yaz(d, (135, y + 76), ipucu, font("SemiBold", 40), KAHVE, max_w=790, sp=1.33)
    sinir(y + h)
    alt_bilgi(d, kaynak)
    img.save(path)
    return path


def efsane_gercek(path, efsane, gercek, kaynak, seri=None):
    img, d = zemin(KREM, (244, 232, 222))
    y = etiket(d, 0, 250, (seri or "Efsane mi, gerçek mi?"), bg=KAHVE, center=True)
    y = yaz(d, (0, y + 40), "Efsane mi,\ngerçek mi?", font("Black", 96), KAHVE, center=True, sp=1.1) + 30
    # efsane kartı
    el = wrap(d, efsane, font("SemiBold", 44), 780)
    h = 100 + len(el) * 60 + 30
    d.rounded_rectangle([90, y, 990, y + h], radius=40, fill=SEFTALI_ACIK)
    cx, cy = 150, y + 62
    d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=TURUNCU)
    d.line([(cx - 13, cy - 13), (cx + 13, cy + 13)], fill=BEYAZ, width=8)
    d.line([(cx - 13, cy + 13), (cx + 13, cy - 13)], fill=BEYAZ, width=8)
    d.text((200, y + 38), "EFSANE", font=font("ExtraBold", 38), fill=TURUNCU)
    yaz(d, (140, y + 104), efsane, font("SemiBold", 44), KAHVE, max_w=780, sp=1.33)
    y += h + 36
    gl = wrap(d, gercek, font("SemiBold", 44), 780)
    h = 100 + len(gl) * 60 + 30
    d.rounded_rectangle([90, y, 990, y + h], radius=40, fill=ADACAYI_ACIK)
    tik(d, 120, y + 32, r=30, renk=YESIL)
    d.text((200, y + 38), "GERÇEK", font=font("ExtraBold", 38), fill=YESIL)
    yaz(d, (140, y + 104), gercek, font("SemiBold", 44), KAHVE, max_w=780, sp=1.33)
    sinir(y + h)
    alt_bilgi(d, kaynak)
    img.save(path)
    return path


def kontrol_listesi(path, etiket_metni, baslik, maddeler, kaynak, numarali=False, not_metni=None):
    img, d = zemin(KREM, (238, 236, 222))
    etiket(d, 0, 250, etiket_metni, bg=ADACAYI if not numarali else SEFTALI, center=True)
    y = yaz(d, (0, 345), baslik, font("Black", 78), KAHVE, center=True, max_w=900, sp=1.12) + 40
    for i, m in enumerate(maddeler, 1):
        lines = wrap(d, m, font("SemiBold", 42), 740)
        h = len(lines) * 56 + 50
        d.rounded_rectangle([90, y, 990, y + h], radius=32, fill=BEYAZ)
        cy = y + h / 2
        if numarali:
            numara(d, 120, cy - 30, i, r=30)
        else:
            tik(d, 120, cy - 30, r=30)
        yaz(d, (205, y + 25), m, font("SemiBold", 42), KAHVE, max_w=740, sp=1.33)
        y += h + 22
    if not_metni:
        y = yaz(d, (100, y + 10), not_metni, font("Medium", 36), SOLUK, max_w=880, sp=1.3, center=True)
    sinir(y)
    alt_bilgi(d, kaynak)
    img.save(path)
    return path


def dm_cagrisi(path, soru, secenekler, cagri):
    img, d = zemin(SEFTALI_ACIK, KREM)
    etiket(d, 0, 250, "SİZE SORUYORUZ", bg=KAHVE, center=True)
    balon(d, 540, 470, w=360, h=190, renk=SEFTALI)
    y = yaz(d, (0, 650), soru, font("Black", 80), KAHVE, center=True, max_w=900, sp=1.12) + 40
    f = font("ExtraBold", 46)
    if len(secenekler) > 2 and all(d.textlength(x, font=f) <= 340 for x in secenekler):
        for i, s_ in enumerate(secenekler):  # 2 sütunlu ızgara
            x0 = 120 if i % 2 == 0 else 555
            yy = y + (i // 2) * 128
            d.rounded_rectangle([x0, yy, x0 + 405, yy + 106], radius=53, fill=BEYAZ, outline=SEFTALI, width=4)
            d.text((x0 + (405 - d.textlength(s_, font=f)) / 2, yy + 26), s_, font=f, fill=KAHVE)
        y += ((len(secenekler) + 1) // 2) * 128
    else:
        for s_ in secenekler:
            lines = wrap(d, s_, f, 700)
            h = len(lines) * 58 + 54
            d.rounded_rectangle([170, y, 910, y + h], radius=h // 2 if len(lines) == 1 else 40, fill=BEYAZ,
                                outline=SEFTALI, width=4)
            yaz(d, (0, y + 27), s_, f, KAHVE, center=True, max_w=700, sp=1.25)
            y += h + 22
    y += 20
    kalp(d, 540, y + 20, s=28)
    y = yaz(d, (0, y + 75), cagri, font("SemiBold", 42), KAHVE, center=True, max_w=880, sp=1.3)
    sinir(y, 1580)
    alt_bilgi(d, None, saglik=False)
    img.save(path)
    return path

if __name__ == "__main__":
    import sys
    iyi_geceler(sys.argv[1], "Yenidoğanlar çok uyur",
                "0–3 aylık bebeklerin günde 14–17 saat uyuması öneriliyor. Bu uyku gün boyunca kısa parçalara bölünür.",
                "National Sleep Foundation")
