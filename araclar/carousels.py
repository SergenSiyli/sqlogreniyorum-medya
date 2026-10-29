"""Hafta 1 carousel'leri: JOIN türleri ve sıralama fonksiyonları (1080x1350)."""
import os
from brand import *

OUT = os.path.join(os.path.dirname(__file__), "..", "out")
W, H = 1080, 1350


def save(img, folder, i):
    p = os.path.join(OUT, folder)
    os.makedirs(p, exist_ok=True)
    img.save(os.path.join(p, f"{i:02d}.png"))


def hook(folder, total, tag, title, sub, art=None):
    img, d = canvas(W, H)
    pill(d, (70, 120), tag)
    y = text_block(d, (70, 260), title, font("Black", 92), max_w=940, spacing=1.12, highlight=YELLOW)
    y = text_block(d, (70, y + 40), sub, font("Medium", 40), fill=MUTED, max_w=900)
    if art:
        art(d, y)
    footer(d, W, H, 1, total)
    save(img, folder, 1)


def join_art(d, y):
    """Kapak için 2x2 mini Venn ızgarası."""
    top = max(y + 70, 720)
    for i, (mode, lab) in enumerate([("inner", "INNER"), ("left", "LEFT"), ("right", "RIGHT"), ("full", "FULL")]):
        cx = 290 + (i % 2) * 500
        cy = top + 90 + (i // 2) * 230
        venn_plain(d, cx, cy, 62, mode)
        tw = d.textlength(lab, font=mono(28, True))
        d.text((cx - tw / 2, cy + 74), lab, font=mono(28, True), fill=YELLOW)


def rank_art(d, y):
    top = max(y + 80, 760)
    cols = [("ROW_NUMBER", YELLOW, "1 2 3 4"), ("RANK", TEAL, "1 2 2 4"), ("DENSE_RANK", PINK, "1 2 2 3")]
    for i, (name, col, seq) in enumerate(cols):
        yy = top + i * 120
        d.rounded_rectangle([70, yy, 1010, yy + 96], radius=22, fill=CARD, outline=LINE, width=2)
        d.text((104, yy + 26), name, font=mono(36, True), fill=col)
        sw = d.textlength(seq, font=mono(40, True))
        d.text((976 - sw, yy + 22), seq.replace("2 2", "? ?") if i else seq, font=mono(40, True), fill=TEXT)


def heading(d, step, title, y=110):
    pill(d, (70, y), step, fill=CARD2, fg=YELLOW, size=26)
    return text_block(d, (70, y + 80), title, font("ExtraBold", 60), max_w=940, spacing=1.15, highlight=YELLOW)


# ---------------------------------------------------------------- JOIN
def joins():
    F, T = "carousel_join", 8
    hook(F, T, "SQL TEMELLERİ", "JOIN'leri hâlâ [karıştırıyor] musun?",
         "4 JOIN türü, tek örnek tabloyla. Kaydet, ihtiyacın olduğunda aç.", join_art)

    img, d = canvas(W, H)
    y = heading(d, "ÖRNEK VERİ", "İki tablomuz var")
    top = y + 40
    y = table(d, (50, top), ["id", "ad"], [(1, "Ayşe"), (2, "Mehmet"), (3, "Zeynep")], [110, 330], size=30)
    d.text((50, y + 14), "ogrenciler", font=mono(26), fill=MUTED)
    y2 = table(d, (530, top), ["ogrenci_id", "kurs"], [(1, "SQL"), (1, "Python"), (2, "SQL"), (4, "Excel")],
               [250, 200], size=30)
    d.text((560, y2 + 14), "kayitlar", font=mono(26), fill=MUTED)
    text_block(d, (70, y2 + 90), "Dikkat: [Zeynep] hiçbir kursa kayıtlı değil, [4] numaralı öğrenci ise tabloda yok.",
               font("Medium", 38), fill=TEXT, max_w=940, highlight=PINK)
    d.rounded_rectangle([60, 960, 1020, 1130], radius=24, fill=CARD, outline=YELLOW, width=3)
    text_block(d, (100, 995), "Bu iki tabloyu 4 farklı şekilde birleştireceğiz. Sonuçlar nasıl değişiyor, izle.",
               font("SemiBold", 36), max_w=880)
    footer(d, W, H, 2, T)
    save(img, F, 2)

    q_base = ["SELECT o.ad, k.kurs", "FROM ogrenciler o", "{J} kayitlar k", "  ON o.id = k.ogrenci_id;"]
    items = [
        ("inner", "INNER JOIN", "Sadece [iki] tabloda da eşleşenler.", [("Ayşe", "SQL"), ("Ayşe", "Python"), ("Mehmet", "SQL")], []),
        ("left", "LEFT JOIN", "Soldaki [tüm] satırlar + eşleşen kısım. Eşleşme yoksa NULL.",
         [("Ayşe", "SQL"), ("Ayşe", "Python"), ("Mehmet", "SQL"), ("Zeynep", None)], [3]),
        ("right", "RIGHT JOIN", "Sağdaki [tüm] satırlar + eşleşen kısım. LEFT'in aynası.",
         [("Ayşe", "SQL"), ("Ayşe", "Python"), ("Mehmet", "SQL"), (None, "Excel")], [3]),
        ("full", "FULL OUTER JOIN", "İki tablonun da [tüm] satırları. Eşleşmeyen taraf NULL.",
         [("Ayşe", "SQL"), ("Ayşe", "Python"), ("Mehmet", "SQL"), ("Zeynep", None), (None, "Excel")], [3, 4]),
    ]
    for n, (mode, J, desc, rows, hl) in enumerate(items, start=3):
        img, d = canvas(W, H)
        pill(d, (70, 100), J, size=30)
        venn(d, 820, 175, 78, mode)
        y = text_block(d, (70, 290), desc, font("Bold", 44), max_w=940, highlight=TEAL)
        q = [l.replace("{J}", J) for l in q_base]
        y = code_box(d, (60, y + 30), q, size=33, w=960)
        y = table(d, (60, y + 36), ["ad", "kurs"], rows, [360, 300], size=31, hl_rows=hl)
        footer(d, W, H, n, T)
        save(img, F, n)

    img, d = canvas(W, H)
    y = heading(d, "BONUS: ANTI JOIN", "Hiç kursa kaydolmayanları bul")
    venn(d, 540, y + 170, 110, "anti")
    y = code_box(d, (60, y + 340), ["SELECT o.ad", "FROM ogrenciler o", "LEFT JOIN kayitlar k",
                                     "  ON o.id = k.ogrenci_id", "WHERE k.ogrenci_id IS NULL;"], size=33)
    y = table(d, (60, y + 30), ["ad"], [("Zeynep",)], [360], size=31, hl_rows=[0])
    text_block(d, (460, y - 100), "Mülakatlarda çok sorulur.", font("SemiBold", 36), fill=MUTED, max_w=560)
    footer(d, W, H, 7, T)
    save(img, F, 7)

    cta(F, 8, T, "Sen en çok hangisini kullanıyorsun?",
        "Yorumlara JOIN türünü yaz. Bir sonraki konuyu sizin sorularınızdan seçiyoruz.")


# ---------------------------------------------------------------- RANK
def ranks():
    F, T = "carousel_rank", 7
    hook(F, T, "MÜLAKAT SORUSU", "ROW_NUMBER, RANK ve DENSE_RANK [farkı] ne?",
         "Eşit değerlerde üçü farklı davranır. 7 slaytta netleştirelim.", rank_art)

    img, d = canvas(W, H)
    y = heading(d, "ÖRNEK VERİ", "Ece ile Can [aynı] puanı almış")
    table(d, (70, y + 50), ["ad", "puan"], [("Ali", 95), ("Ece", 90), ("Can", 90), ("Deniz", 85)], [420, 300],
          size=36, hl_rows=[1, 2])
    callout(d, 820, "Soru: Ece ve Can'a kaçıncı sıra verilmeli? Cevap, hangi fonksiyonu kullandığına bağlı.")
    footer(d, W, H, 2, T)
    save(img, F, 2)

    img, d = canvas(W, H)
    y = heading(d, "SORGU", "Üçünü yan yana çalıştıralım")
    code_box(d, (40, y + 50), ["SELECT ad, puan,", "  ROW_NUMBER() OVER (", "    ORDER BY puan DESC, ad) AS rn,",
                               "  RANK() OVER (", "    ORDER BY puan DESC) AS rnk,", "  DENSE_RANK() OVER (",
                               "    ORDER BY puan DESC) AS drnk", "FROM puanlar;"], size=32, w=1000, title="sorgu.sql")
    callout(d, 900, "İpucu: ROW_NUMBER'a eklediğimiz \", ad\" eşitlikte sırayı sabitler. Yazmazsan her çalıştırmada farklı sonuç alabilirsin.")
    footer(d, W, H, 3, T)
    save(img, F, 3)

    img, d = canvas(W, H)
    y = heading(d, "SONUÇ", "Farkı [eşitlikte] görürsün")
    y = table(d, (40, y + 40), ["ad", "puan", "rn", "rnk", "drnk"],
              [("Ali", 95, 1, 1, 1), ("Can", 90, 2, 2, 2), ("Ece", 90, 3, 2, 2), ("Deniz", 85, 4, 4, 3)],
              [230, 190, 170, 190, 220], size=34, hl_rows=[1, 2])
    text_block(d, (70, y + 50), "Deniz'e bak: RANK 4 verdi, DENSE_RANK 3 verdi.", font("Bold", 40), max_w=940)
    callout(d, 880, "RANK, eşit iki kişiyi 2. sayıp 3. sırayı atlar. DENSE_RANK hiçbir sırayı atlamaz.")
    footer(d, W, H, 4, T)
    save(img, F, 4)

    img, d = canvas(W, H)
    y = heading(d, "ÖZET", "Hangisi ne yapar?")
    y += 40
    for name, col, desc in [
        ("ROW_NUMBER", YELLOW, "Eşitlik umursamaz. Her satıra benzersiz numara: 1, 2, 3, 4"),
        ("RANK", TEAL, "Eşitlere aynı sıra, sonra boşluk bırakır: 1, 2, 2, 4"),
        ("DENSE_RANK", PINK, "Eşitlere aynı sıra, boşluk yok: 1, 2, 2, 3"),
    ]:
        d.rounded_rectangle([60, y, 1020, y + 230], radius=24, fill=CARD, outline=LINE, width=2)
        d.rectangle([60, y + 24, 70, y + 206], fill=col)
        d.text((100, y + 30), name, font=mono(42, True), fill=col)
        text_block(d, (100, y + 98), desc, font("Medium", 36), max_w=880)
        y += 260
    footer(d, W, H, 5, T)
    save(img, F, 5)

    img, d = canvas(W, H)
    y = heading(d, "GERÇEK HAYAT", "Her kategoride en çok satan [2] ürün")
    y = code_box(d, (40, y + 30), ["WITH sirali AS (", "  SELECT kategori, urun, satis,", "    ROW_NUMBER() OVER (",
                                   "      PARTITION BY kategori", "      ORDER BY satis DESC) AS sira",
                                   "  FROM urunler)", "SELECT kategori, urun, satis", "FROM sirali WHERE sira <= 2;"],
                 size=31, w=1000)
    table(d, (40, y + 30), ["kategori", "urun", "satis"],
          [("Kitap", "Roman", 120), ("Kitap", "Dergi", 90), ("Oyun", "Puzzle", 85), ("Oyun", "Zeka", 70)],
          [330, 370, 300], size=29)
    footer(d, W, H, 6, T)
    save(img, F, 6)

    cta(F, 7, T, "Mülakatta bu soru geldi mi?",
        "Yaşadığın SQL mülakat sorusunu yorumlara yaz, çözümünü videoyla anlatalım.")


def callout(d, y, text):
    fnt = font("SemiBold", 36)
    lines = wrap(d, text, fnt, 860)
    h = len(lines) * int(36 * 1.22) + 70
    d.rounded_rectangle([60, y, 1020, y + h], radius=24, fill=CARD, outline=YELLOW, width=3)
    text_block(d, (100, y + 35), text, fnt, max_w=860)


def cta(F, n, T, title, sub):
    img, d = canvas(W, H)
    y = text_block(d, (70, 330), title, font("Black", 78), max_w=940, spacing=1.12)
    y = text_block(d, (70, y + 40), sub, font("Medium", 40), fill=MUTED, max_w=920)
    y += 80
    for i, (lab, col) in enumerate([("KAYDET", YELLOW), ("PAYLAŞ", TEAL), ("TAKİP ET", PINK)]):
        pill(d, (70 + i * 300, y), lab, fill=col, size=32)
    d.text((70, y + 150), "Her gün 1 SQL konusu.", font=font("Bold", 40), fill=TEXT)
    footer(d, W, H, n, T, swipe=False)
    save(img, F, n)


if __name__ == "__main__":
    joins()
    ranks()
    print("ok")
