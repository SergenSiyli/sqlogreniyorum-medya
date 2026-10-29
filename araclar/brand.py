"""@sqlogreniyorum marka kiti: renkler, fontlar ve çizim yardımcıları."""
import re
from PIL import Image, ImageDraw, ImageFont

HANDLE = "@sqlogreniyorum"

BG = (12, 16, 29)
CARD = (23, 30, 48)
CARD2 = (31, 40, 63)
LINE = (52, 63, 92)
TEXT = (236, 239, 246)
MUTED = (144, 153, 176)
YELLOW = (255, 199, 44)
TEAL = (45, 212, 191)
PINK = (247, 118, 170)
GREEN = (134, 239, 172)
RED = (255, 107, 107)
BLUE = (96, 165, 250)

INTER = "/usr/share/fonts/opentype/inter/Inter-{}.otf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono{}.ttf"

_cache = {}


def font(weight="Bold", size=48):
    key = ("i", weight, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(INTER.format(weight), size)
    return _cache[key]


def mono(size=36, bold=False):
    key = ("m", bold, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(MONO.format("-Bold" if bold else ""), size)
    return _cache[key]


def canvas(w=1080, h=1350):
    img = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(img)
    # ince ızgara dokusu
    for x in range(0, w, 54):
        d.line([(x, 0), (x, h)], fill=(16, 21, 37))
    for y in range(0, h, 54):
        d.line([(0, y), (w, y)], fill=(16, 21, 37))
    return img, d


def wrap(d, text, fnt, max_w):
    lines = []
    for para in text.split("\n"):
        words, cur = para.split(" "), ""
        for w in words:
            t = (cur + " " + w).strip()
            if d.textlength(t, font=fnt) <= max_w:
                cur = t
            else:
                if cur:
                    lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def text_block(d, xy, text, fnt, fill=TEXT, max_w=920, spacing=1.22, highlight=None):
    """Metni sarar; [köşeli parantez] içindeki kelimeleri highlight rengiyle boyar."""
    x, y = xy
    lh = int(fnt.size * spacing)
    plain = text.replace("[", "").replace("]", "")
    lines = wrap(d, plain, fnt, max_w)
    marks = set(m.lower() for m in re.findall(r"\[([^\]]+)\]", text))
    for ln in lines:
        cx = x
        for i, word in enumerate(ln.split(" ")):
            token = word.strip(".,:;!?'\"()").lower()
            col = highlight if highlight and any(token and token in m.split() for m in marks) else fill
            s = word + (" " if i < len(ln.split(" ")) - 1 else "")
            d.text((cx, y), s, font=fnt, fill=col)
            cx += d.textlength(s, font=fnt)
        y += lh
    return y


KEYWORDS = {
    "SELECT", "FROM", "WHERE", "GROUP", "BY", "HAVING", "ORDER", "JOIN", "INNER", "LEFT",
    "RIGHT", "FULL", "OUTER", "ON", "AS", "AND", "OR", "IS", "NULL", "NOT", "DESC", "ASC",
    "WITH", "OVER", "PARTITION", "LIMIT", "IN", "DISTINCT", "UNION", "ALL", "CASE", "WHEN", "THEN", "ELSE", "END", "EXISTS", "LIKE", "BETWEEN", "INSERT", "INTO", "VALUES", "UPDATE", "SET", "DELETE", "CREATE", "TABLE",
}
FUNCS = {"COUNT", "SUM", "AVG", "MIN", "MAX", "ROW_NUMBER", "RANK", "DENSE_RANK"}
TOKEN_RE = re.compile(r"('[^']*'|\d+|[A-Za-z_çğıöşüÇĞİÖŞÜ][\wçğıöşüÇĞİÖŞÜ]*|\s+|.)")


def code_colors(line):
    out = []
    for tok in TOKEN_RE.findall(line):
        u = tok.upper()
        if tok.startswith("'"):
            out.append((tok, GREEN))
        elif tok.isdigit():
            out.append((tok, PINK))
        elif u in KEYWORDS:
            out.append((tok, YELLOW))
        elif u in FUNCS:
            out.append((tok, TEAL))
        else:
            out.append((tok, TEXT))
    return out


def code_box(d, xy, lines, size=34, w=960, pad=34, chars=None, line_marks=None, title=None):
    """Kod kutusu çizer. chars: daktilo efekti için gösterilecek karakter sayısı.
    line_marks: {satır_no: (etiket, renk)} satır başına numara rozeti."""
    x, y = xy
    fnt = mono(size)
    lh = int(size * 1.5)
    top = 56 if title is not None else 0
    h = pad * 2 + lh * len(lines) + top
    d.rounded_rectangle([x, y, x + w, y + h], radius=26, fill=CARD, outline=LINE, width=2)
    if title is not None:
        for i, col in enumerate([RED, YELLOW, GREEN]):
            d.ellipse([x + 26 + i * 30, y + 22, x + 44 + i * 30, y + 40], fill=col)
        d.text((x + 130, y + 16), title, font=mono(22), fill=MUTED)
    left = 0
    remaining = chars
    gutter = 0
    if line_marks is not None:
        gutter = 64
    for i, ln in enumerate(lines):
        ly = y + pad + top + i * lh
        if line_marks is not None and i in line_marks:
            lab, col = line_marks[i]
            bx = x + pad - 6
            d.rounded_rectangle([bx, ly - 2, bx + 46, ly + size + 6], radius=12, fill=col)
            tw = d.textlength(lab, font=font("ExtraBold", 28))
            d.text((bx + 23 - tw / 2, ly + 2), lab, font=font("ExtraBold", 28), fill=BG)
        cx = x + pad + gutter
        for tok, col in code_colors(ln):
            if remaining is not None:
                if remaining <= 0:
                    break
                tok = tok[:remaining]
                remaining -= len(tok)
            d.text((cx, ly), tok, font=fnt, fill=col)
            cx += d.textlength(tok, font=fnt)
        if remaining is not None:
            remaining -= 1  # satır sonu
            if remaining < 0:
                break
    return y + h


def table(d, xy, headers, rows, col_w, size=32, hl_rows=None, hl_col=TEAL, null_col=RED):
    x, y = xy
    rh = int(size * 1.9)
    total_w = sum(col_w)
    d.rounded_rectangle([x, y, x + total_w, y + rh * (len(rows) + 1)], radius=20, fill=CARD, outline=LINE, width=2)
    d.rounded_rectangle([x, y, x + total_w, y + rh], radius=20, fill=CARD2)
    d.rectangle([x, y + rh - 20, x + total_w, y + rh], fill=CARD2)
    cx = x
    for h, cw in zip(headers, col_w):
        d.text((cx + 24, y + (rh - size) / 2 - 2), h, font=mono(size, True), fill=YELLOW)
        cx += cw
    for r, row in enumerate(rows):
        ry = y + rh * (r + 1)
        if hl_rows and r in hl_rows:
            if r == len(rows) - 1:
                d.rounded_rectangle([x + 2, ry, x + total_w - 2, ry + rh - 2], radius=18, fill=(28, 52, 64))
                d.rectangle([x + 2, ry, x + total_w - 2, ry + 20], fill=(28, 52, 64))
            else:
                d.rectangle([x + 2, ry, x + total_w - 2, ry + rh], fill=(28, 52, 64))
        if r < len(rows) - 1:
            d.line([(x + 16, ry + rh), (x + total_w - 16, ry + rh)], fill=LINE, width=1)
        cx = x
        for val, cw in zip(row, col_w):
            s = "NULL" if val is None else str(val)
            col = null_col if val is None else TEXT
            d.text((cx + 24, ry + (rh - size) / 2 - 2), s, font=mono(size), fill=col)
            cx += cw
    return y + rh * (len(rows) + 1)


def pill(d, xy, text, fill=YELLOW, fg=BG, size=28):
    fnt = font("ExtraBold", size)
    tw = d.textlength(text, font=fnt)
    x, y = xy
    d.rounded_rectangle([x, y, x + tw + 44, y + size + 26], radius=(size + 26) // 2, fill=fill)
    d.text((x + 22, y + 11), text, font=fnt, fill=fg)
    return x + tw + 44


def footer(d, w, h, page=None, total=None, swipe=True):
    d.text((70, h - 92), HANDLE, font=font("Bold", 30), fill=MUTED)
    if page is not None:
        s = f"{page}/{total}"
        tw = d.textlength(s, font=font("Bold", 30))
        right = w - 70
        if swipe and page < total:
            arrow = "kaydır  →"
            aw = d.textlength(arrow, font=font("SemiBold", 30))
            d.text((right - aw, h - 92), arrow, font=font("SemiBold", 30), fill=YELLOW)
            right -= aw + 40
        d.text((right - tw, h - 92), s, font=font("Bold", 30), fill=MUTED)


def venn(d, cx, cy, r, mode, labels=True):
    """JOIN Venn şeması. mode: inner/left/right/full/anti"""
    off = int(r * 0.62)
    a, b = (cx - off, cy), (cx + off, cy)
    fill_a = mode in ("left", "full", "anti")
    fill_b = mode in ("right", "full")
    fill_mid = mode in ("inner", "left", "right", "full")
    W, H = 2 * r + 2 * off + 20, 2 * r + 20
    mask_a = Image.new("L", (W, H), 0)
    mask_b = Image.new("L", (W, H), 0)
    ox, oy = cx - W // 2, cy - H // 2
    ImageDraw.Draw(mask_a).ellipse([a[0] - r - ox, a[1] - r - oy, a[0] + r - ox, a[1] + r - oy], fill=255)
    ImageDraw.Draw(mask_b).ellipse([b[0] - r - ox, b[1] - r - oy, b[0] + r - ox, b[1] + r - oy], fill=255)
    from PIL import ImageChops
    mid = ImageChops.multiply(mask_a, mask_b)
    only_a = ImageChops.subtract(mask_a, mid)
    only_b = ImageChops.subtract(mask_b, mid)
    layer = Image.new("RGB", (W, H), TEAL)
    base = d._image
    for m, on in ((only_a, fill_a), (only_b, fill_b), (mid, fill_mid)):
        if on:
            base.paste(layer, (ox, oy), m)
    d.ellipse([a[0] - r, a[1] - r, a[0] + r, a[1] + r], outline=TEXT, width=4)
    d.ellipse([b[0] - r, b[1] - r, b[0] + r, b[1] + r], outline=TEXT, width=4)
    if not labels:
        return
    lf = font("Bold", 26)
    d.text((a[0] - r * 0.55 - d.textlength("ogrenciler", font=lf) / 2, cy - r - 44), "ogrenciler", font=lf, fill=MUTED)
    d.text((b[0] + r * 0.55 - d.textlength("kayitlar", font=lf) / 2, cy - r - 44), "kayitlar", font=lf, fill=MUTED)


def venn_plain(d, cx, cy, r, mode):
    venn(d, cx, cy, r, mode, labels=False)
