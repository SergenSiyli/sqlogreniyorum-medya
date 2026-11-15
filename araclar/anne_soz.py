"""Tek kare söz/mizah postu (bitutamburcu tarzı): krem kağıt zemin, serif yazı, kiremit vurgu, altta küçük çizim.
Kullanım: python3 araclar/anne_soz.py <json> <cikti.png>
JSON: {"ust":"...", "satirlar":["...","*vurgu*..."], "alt":"...", "ikon":"hot_beverage", "hesap":"utopikanne"}"""
import sys, json, html, re, base64
from pathlib import Path
KOK = Path(__file__).resolve().parent.parent
d = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")); out = sys.argv[2]
def v(s): return re.sub(r"\*(.+?)\*", r'<em>\1</em>', html.escape(s)).replace("\n", "<br>")
ik = ""
if d.get("ikon"):
    for k in (KOK/"hesaplar/utopikanne/marka/ikon", KOK/"marka/ikon"):
        p = k/f'{d["ikon"]}.png'
        if p.exists(): ik = f'<img class="ik" src="data:image/png;base64,{base64.b64encode(p.read_bytes()).decode()}">'; break
satir = "".join(f"<p>{v(s)}</p>" for s in d["satirlar"])
H = f'''<!doctype html><html lang="tr"><head><meta charset="utf-8"><style>
*{{margin:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;background:#F4EDE3;font-family:"Caladea","DejaVu Serif",serif;color:#3B2A22;
 display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 110px;
 background-image:radial-gradient(#00000008 1px,transparent 1px);background-size:6px 6px}}
.ust{{font-size:36px;letter-spacing:6px;color:#A0522D;margin-bottom:48px;text-transform:uppercase}}
p{{font-size:74px;line-height:1.22;margin:6px 0}}
em{{font-style:italic;color:#B5532E}}
.alt{{font-size:40px;margin-top:44px;color:#6B5A50;line-height:1.35}}
.ik{{width:170px;height:170px;margin-top:70px;opacity:.95;filter:saturate(.75) drop-shadow(0 10px 14px #0002)}}
.el{{position:absolute;bottom:56px;font-size:28px;color:#8B7A70;letter-spacing:2px}}
</style></head><body>
{f'<div class="ust">{html.escape(d["ust"])}</div>' if d.get("ust") else ""}{satir}
{f'<div class="alt">{v(d["alt"])}</div>' if d.get("alt") else ""}{ik}
<div class="el">@{d.get("hesap","utopikanne")}</div></body></html>'''
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(viewport={"width":1080,"height":1350})
    pg.set_content(H); pg.wait_for_timeout(200); pg.screenshot(path=out); b.close()
print(out)
