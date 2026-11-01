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


def iyi_geceler(path, baslik, bilgi, kaynak, alt="Tatlı rüyalar, yarın sabah görüşmek üzere."):
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
    h = 130 + len(tl) * 70 + len(bl) * 62 + 70
    d.rounded_rectangle([90, kart_y, 990, kart_y + h], radius=44, fill=(250, 243, 235))
    d.rounded_rectangle([130, kart_y + 40, 130 + d.textlength("BİLİYOR MUYDUN?", font=font("ExtraBold", 30)) + 44, kart_y + 92],
                        radius=26, fill=SEFTALI)
    d.text((152, kart_y + 50), "BİLİYOR MUYDUN?", font=font("ExtraBold", 30), fill=(255, 255, 255))
    yy = yaz(d, (130, kart_y + 125), baslik, font("ExtraBold", 54), KAHVE, max_w=820, sp=1.25)
    yy = yaz(d, (130, yy + 8), bilgi, font("SemiBold", 46), KAHVE, max_w=820, sp=1.3)
    d.text((130, kart_y + h - 60), "Kaynak: " + kaynak, font=font("Medium", 28), fill=SOLUK)
    y = kart_y + h + 50
    y = yaz(d, (0, y), alt, font("Medium", 42), (225, 218, 236), center=True)
    assert y <= 1580, ("story taşıyor", y)
    hw = d.textlength(HANDLE, font=font("Bold", 34))
    d.text(((W - hw) / 2, 1640), HANDLE, font=font("Bold", 34), fill=(205, 196, 220))
    img.save(path)
    return path


if __name__ == "__main__":
    import sys
    iyi_geceler(sys.argv[1], "Yenidoğanlar çok uyur",
                "0–3 aylık bebeklerin günde 14–17 saat uyuması öneriliyor. Bu uyku gün boyunca kısa parçalara bölünür.",
                "National Sleep Foundation")
