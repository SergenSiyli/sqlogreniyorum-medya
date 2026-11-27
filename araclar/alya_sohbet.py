"""Alya'nın Günlüğü sayfaları: günlük başlığı + mesaj balonları (1080x1350).
Kullanım: python3 araclar/alya_sohbet.py <bolum.json> <cikti_klasoru>
JSON: {"bolum":1,"kapak":{"baslik":"İki çizgi."},
       "sayfalar":[{"zaman":"Pazartesi · 08.10","gunluk":"...","mesajlar":[{"kim":"Alya","yazi":"..."},{"kim":"Selin","yazi":"..."}],"son":"Devamı pazartesi"}]}
Alya sağda (kiremit balon), diğerleri solda (beyaz balon, isim etiketi)."""
import sys, json, html
from pathlib import Path
d = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")); out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
e = html.escape
CSS = """*{margin:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:#F6EFE6;font-family:"Inter",sans-serif;color:#3B2A22;position:relative;overflow:hidden;
 background-image:repeating-linear-gradient(#F6EFE6 0 78px,#E8DCCD 78px 80px);}
body:before{content:"";position:absolute;left:96px;top:0;bottom:0;width:3px;background:#E7B9A8}
.ust{position:absolute;top:70px;left:140px;right:80px;display:flex;justify-content:space-between;align-items:center}
.seri{font-family:"Caladea",serif;font-style:italic;font-size:38px;color:#A0522D}
.zaman{font-size:30px;font-weight:600;color:#fff;background:#B5532E;padding:12px 26px;border-radius:40px}
.gunluk{white-space:pre-line;position:absolute;top:175px;left:150px;right:110px;font-family:"Caladea",serif;font-style:italic;font-size:50px;line-height:1.3;color:#4A3A55;background:#EFE7F7;border:3px dashed #B9A3D6;border-radius:60px;padding:34px 44px}
.gunluk:after{content:"";position:absolute;left:70px;bottom:-46px;width:34px;height:34px;border-radius:50%;background:#EFE7F7;border:3px dashed #B9A3D6}
.gunluk:before{content:"";position:absolute;left:40px;bottom:-78px;width:18px;height:18px;border-radius:50%;background:#EFE7F7;border:3px dashed #B9A3D6}
.ic{font-family:"Inter",sans-serif;font-style:normal;font-size:28px;font-weight:700;letter-spacing:1px;color:#7B5EA7;margin-bottom:10px}
.sohbet{position:absolute;left:120px;right:70px;bottom:190px;display:flex;flex-direction:column;gap:22px}
.m{max-width:78%;padding:24px 32px;border-radius:34px;font-size:42px;line-height:1.3;box-shadow:0 6px 16px #0000000f}
.sol{align-self:flex-start;background:#fff;border-bottom-left-radius:8px}
.sag{align-self:flex-end;background:#C8643D;color:#fff;border-bottom-right-radius:8px}
.kim{font-size:28px;font-weight:700;color:#A0522D;margin-bottom:6px}
.son{position:absolute;left:140px;right:90px;bottom:200px;text-align:center}
.son b{display:block;font-family:"Caladea",serif;font-style:italic;font-size:64px;color:#B5532E;margin-bottom:24px}
.son span{font-size:40px;color:#6B5A50;display:block}
.son i{display:block;margin-top:34px;font-style:normal;font-size:34px;font-weight:600;color:#fff;background:#B5532E;padding:16px 28px;border-radius:40px}
.alt{position:absolute;bottom:64px;left:0;right:0;text-align:center;font-size:28px;color:#8B7A70;letter-spacing:1px}
.kapak{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:0 140px}
.kapak .s{font-family:"Caladea",serif;font-style:italic;font-size:56px;color:#A0522D}
.kapak .b{font-size:34px;font-weight:700;letter-spacing:8px;color:#fff;background:#B5532E;padding:12px 34px;border-radius:40px;margin:36px 0}
.kapak .t{font-size:40px;font-weight:600;color:#6B5A50;margin-top:18px}
.kapak h1{font-family:"Caladea",serif;font-size:150px;line-height:1.05;color:#3B2A22}
.kapak h1.uzun{font-size:96px;line-height:1.12}
.kapak .k{font-size:38px;color:#6B5A50;margin-top:50px}"""
def sayfa(govde): return f'<!doctype html><html lang="tr"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{govde}<div class="alt">@utopikanne</div></body></html>'
pages = []
k = d["kapak"]
pages.append(sayfa(f'<div class="kapak"><div class="s">Alya\'nın Günlüğü</div><div class="t">{e(k.get("tur","🤰 Bir hamilelik hikâyesi"))}</div><div class="b">BÖLÜM {d["bolum"]}</div><h1 class="{"uzun" if len(k["baslik"])>20 else ""}">{e(k["baslik"])}</h1><div class="k">{e(k.get("alt","Kaydır →"))}</div></div>'))
for s in d["sayfalar"]:
    g = f'<div class="ust"><div class="seri">Alya\'nın Günlüğü</div><div class="zaman">{e(s["zaman"])}</div></div>'
    if s.get("gunluk"): g += f'<div class="gunluk"><div class="ic">💭 Alya\'nın içinden</div>{e(s["gunluk"])}</div>'
    if s.get("mesajlar"):
        g += '<div class="sohbet">' + "".join(
            f'<div class="m sag">{e(m["yazi"])}</div>' if m["kim"] == "Alya" else f'<div class="m sol"><div class="kim">{e(m["kim"])}</div>{e(m["yazi"])}</div>'
            for m in s["mesajlar"]) + '</div>'
    if s.get("son"): g += f'<div class="son"><b>{e(s["son"])}</b><span>{e(s.get("soru",""))}</span><i>Devamını kaçırmamak için takipte kal 🤍</i></div>'
    pages.append(sayfa(g))
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(viewport={"width":1080,"height":1350})
    for i, h in enumerate(pages, 1):
        pg.set_content(h); pg.wait_for_timeout(150); pg.screenshot(path=str(out/f"sayfa_{i}.png"))
    b.close()
print(len(pages), "sayfa ->", out)
