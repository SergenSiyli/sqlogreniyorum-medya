#!/usr/bin/env python3
"""utopikanne — renkli, 3D çizimli carousel + aynı içerikten animasyonlu Reels.

Kullanım:
  python3 araclar/anne_canli.py <icerik.json> <cikis_klasoru> [--reels] [--sadece-reels] [--story]

Çıktı:
  <cikis>/<ad>_01.jpg ... (1080x1350, JPEG)  -> CAROUSEL
  <cikis>/<ad>_reels.mp4 + <ad>_reels_kapak.jpg (1080x1920) -> TRIAL_REEL / REEL

İçerik JSON örneği: hesaplar/utopikanne/icerik_ornek/mikrodalga.json
Slayt tipleri: kapak, adim, liste, kiyas, not, son
  - Başlıkta *kelime* -> fosforlu kalemle vurgulanır.
  - ikon adları: hesaplar/utopikanne/marka/ikon/*.png (Microsoft Fluent Emoji 3D, MIT lisansı)
Kurallar (strateji.md): sen dili, uydurma kişisel deneyim yok, ürün/marka yok,
diyet dili yok; sağlık bilgisi resmî kaynaktan + "doktoruna danış".
"""
import base64, json, os, subprocess, sys, html, re
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
IKON = KOK / "hesaplar/utopikanne/marka/ikon"

TEMA = {  # bg1, bg2, vurgu, mürekkep, fosfor
    "seftali": ("#FFF1E6", "#FFD3BD", "#FF6B4A", "#3A2418", "#FFD166"),
    "nane":    ("#E8FBF3", "#BFEEDB", "#0E9F7A", "#173A30", "#FFE066"),
    "lila":    ("#F4EEFF", "#D9C8FF", "#7C4DEB", "#2A1D4A", "#FFC8E2"),
    "gok":     ("#EAF5FF", "#C6E2FF", "#2F7AE5", "#16304F", "#FFE27A"),
    "pembe":   ("#FFF0F5", "#FFCADD", "#E23D82", "#45172C", "#FFE08A"),
    "limon":   ("#FFFBE6", "#FFEB99", "#E08A00", "#3D2C00", "#B8F2C9"),
}


def ikon_uri(ad):
    p = IKON / f"{ad}.png"
    if not p.exists():
        raise SystemExit(f"ikon yok: {ad}  (bkz. {IKON})")
    return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode()


def vurgula(s):
    s = html.escape(s)
    return re.sub(r"\*(.+?)\*", r'<span class="hl">\1</span>', s).replace("\n", "<br>")


def img(ad, cls="", d=0.0, extra=""):
    return f'<img class="ik a pop {cls}" data-d="{d}" src="{ikon_uri(ad)}" {extra}>'


def slayt_html(s, i, n, meta):
    tip = s["tip"]
    rozet = f'<div class="rozet a" data-d="0">{html.escape(meta["seri"])}' + (f' · #{meta["no"]}' if meta.get("no") is not None else '') + '</div>'
    sayac = f'<div class="sayac">{i}/{n}</div>'
    el = '<div class="el">@utopikanne</div>'
    ic = ""
    if tip == "kapak":
        ik = s.get("ikonlar", [])
        bulut = "".join(img(a, f"k{j}", 0.35 + 0.15 * j) for j, a in enumerate(ik[:4]))
        ic = f'''<div class="ust a" data-d="0.05">{vurgula(s.get("ust",""))}</div>
        <h1 class="dev a" data-d="0.15">{vurgula(s["baslik"])}</h1>
        <div class="alt a" data-d="0.3">{vurgula(s.get("alt",""))}</div>
        <div class="bulut">{bulut}</div>
        <div class="kaydir a" data-d="0.9">Kaydır, öğren <b>→</b></div>'''
    elif tip == "adim":
        ik = "".join(img(a, "orta", 0.3 + 0.15 * j) for j, a in enumerate(s.get("ikonlar", [])[:3]))
        no = f'<div class="no a pop" data-d="0.05">{s["no"]}</div>' if "no" in s else ""
        ic = f'''{no}<h2 class="a" data-d="0.12">{vurgula(s["baslik"])}</h2>
        <div class="ikonlar">{ik}</div>
        <p class="metin a" data-d="0.45">{vurgula(s.get("metin",""))}</p>'''
    elif tip == "liste":
        m = "".join(
            f'<li class="a" data-d="{0.25 + 0.18*j}"><img class="mik" src="{ikon_uri(x["ikon"])}"><span>{vurgula(x["yazi"])}</span></li>'
            for j, x in enumerate(s["maddeler"]))
        ic = f'<h2 class="a" data-d="0.05">{vurgula(s["baslik"])}</h2><ul class="liste">{m}</ul>'
    elif tip == "kiyas":
        def taraf(t, d):
            adet = "".join(f'<img class="kik a pop" data-d="{d + 0.1*k}" src="{ikon_uri(t["ikon"])}">' for k in range(t.get("adet", 1)))
            return f'<div class="taraf"><div class="kikonlar">{adet}</div><div class="kyazi a" data-d="{d+0.2}">{vurgula(t["yazi"])}</div></div>'
        ic = f'''<h2 class="a" data-d="0.05">{vurgula(s["baslik"])}</h2>
        <div class="kiyas">{taraf(s["sol"],0.25)}<div class="esit a pop" data-d="0.6">{html.escape(s.get("isaret","≈"))}</div>{taraf(s["sag"],0.75)}</div>
        <p class="metin a" data-d="1.2">{vurgula(s.get("metin",""))}</p>'''
    elif tip == "not":
        ic = f'''<div class="notkutu a" data-d="0.1">{img(s.get("ikon","stethoscope"),"notik",0.25)}
        <h2>{vurgula(s["baslik"])}</h2><p class="metin">{vurgula(s.get("metin",""))}</p></div>'''
    elif tip == "son":
        ik = "".join(img(a, f"k{j}", 0.3 + 0.15 * j) for j, a in enumerate(s.get("ikonlar", ["smiling_face_with_hearts"])[:3]))
        g = s.get("gonder")
        gonder = f'<div class="cta3 a" data-d="0.95">📩 {html.escape(g)}</div>' if g else ""
        ic = f'''<div class="bulut kucuk">{ik}</div>
        <h1 class="dev a" data-d="0.1">{vurgula(s.get("baslik","Serinin devamı için *takip et*"))}</h1>
        <p class="metin a" data-d="0.35">{vurgula(s.get("metin","Her gün böyle pratik bilgiler burada."))}</p>
        <div class="cta a pop" data-d="0.6">+ Takip et</div>
        <div class="cta2 a" data-d="0.8">🔖 Kaydet, lazım olunca bul</div>{gonder}'''
    return f'<section class="sahne t-{tip}" data-i="{i-1}">{rozet}{sayac}<div class="govde">{ic}</div>{el}</section>'


def sayfa(icerik, W, H, reels):
    b1, b2, v, ink, fos = TEMA[icerik.get("tema", "seftali")]
    sl = icerik["slaytlar"]
    sahneler = "".join(slayt_html(s, i + 1, len(sl), icerik) for i, s in enumerate(sl))
    olcek = 1.0
    pad_top = 250 if reels else 120
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;font-family:Inter,sans-serif;color:{ink}}}
.sahne{{position:absolute;inset:0;background:radial-gradient(circle at 18% 12%,#ffffffcc 0,transparent 38%),linear-gradient(160deg,{b1},{b2});overflow:hidden}}
.sahne:before,.sahne:after{{content:"";position:absolute;border-radius:50%;background:{v};opacity:.10}}
.sahne:before{{width:520px;height:520px;right:-180px;top:-160px}}
.sahne:after{{width:380px;height:380px;left:-150px;bottom:-120px;opacity:.08}}
.rozet{{position:absolute;left:64px;top:{pad_top-70}px;background:{v};color:#fff;font-weight:800;font-size:30px;letter-spacing:1.5px;padding:12px 26px;border-radius:40px;box-shadow:0 8px 24px {v}55}}
.sayac{{display:{'none' if reels else 'block'};position:absolute;right:64px;top:{pad_top-62}px;font-weight:700;font-size:28px;opacity:.55}}
.el{{position:absolute;bottom:{70 if not reels else 300}px;width:100%;text-align:center;font-weight:700;font-size:30px;opacity:.6}}
.govde{{position:absolute;left:72px;right:72px;top:{pad_top+20}px;bottom:{150 if not reels else 380}px;display:flex;flex-direction:column;justify-content:center;gap:30px}}
.ust{{font-size:46px;font-weight:800;color:{v}}}
.dev{{font-size:{104 if not reels else 112}px;line-height:1.04;font-weight:900;letter-spacing:-2px}}
h2{{font-size:70px;line-height:1.08;font-weight:900;letter-spacing:-1px}}
.alt{{font-size:44px;font-weight:600;line-height:1.25}}
.metin{{font-size:42px;line-height:1.36;font-weight:500}}
.hl{{background:linear-gradient(transparent 52%,{fos} 52%,{fos} 92%,transparent 92%);padding:0 6px;border-radius:6px}}
.bulut{{position:relative;height:330px}}
.bulut.kucuk{{height:260px}}
.ik{{width:250px;height:250px;object-fit:contain;filter:drop-shadow(0 18px 22px rgba(0,0,0,.18))}}
.bulut .ik{{position:absolute}}
.k0{{left:0;top:30px;width:270px;height:270px}} .k1{{left:300px;top:0}} .k2{{left:590px;top:50px;width:230px;height:230px}} .k3{{left:760px;top:-10px;width:180px;height:180px}}
.kaydir{{display:{'none' if reels else 'block'};font-size:38px;font-weight:800;color:{v}}}
.no{{width:120px;height:120px;border-radius:50%;background:{v};color:#fff;font-size:68px;font-weight:900;display:flex;align-items:center;justify-content:center;box-shadow:0 10px 26px {v}66}}
.ikonlar{{display:flex;gap:30px;justify-content:center}}
.ikonlar .ik{{width:270px;height:270px}}
.liste{{list-style:none;display:flex;flex-direction:column;gap:26px}}
.liste li{{display:flex;align-items:center;gap:28px;background:#ffffffb8;border-radius:34px;padding:22px 30px;font-size:40px;font-weight:600;line-height:1.25;box-shadow:0 8px 20px rgba(0,0,0,.06)}}
.mik{{width:110px;height:110px;flex:none;object-fit:contain}}
.kiyas{{display:flex;align-items:center;justify-content:space-between;gap:20px;background:#ffffffb8;border-radius:44px;padding:40px 30px}}
.taraf{{flex:1;text-align:center}}
.kikonlar{{display:flex;flex-wrap:wrap;justify-content:center;gap:4px;min-height:200px;align-items:center}}
.kik{{width:150px;height:150px;object-fit:contain;filter:drop-shadow(0 10px 12px rgba(0,0,0,.15))}}
.kyazi{{font-size:40px;font-weight:800;margin-top:14px}}
.esit{{font-size:110px;font-weight:900;color:{v}}}
.notkutu{{background:#ffffffd0;border-radius:48px;padding:56px 50px;display:flex;flex-direction:column;gap:26px;border:4px dashed {v}66}}
.notik{{width:180px;height:180px}}
.cta{{align-self:flex-start;background:{v};color:#fff;font-size:54px;font-weight:900;padding:24px 56px;border-radius:60px;box-shadow:0 14px 30px {v}66}}
.cta2,.cta3{{font-size:40px;font-weight:700;background:#ffffffb8;border-radius:30px;padding:18px 30px;align-self:flex-start}}
</style></head><body>{sahneler}
<script>
const R={str(reels).lower()};
const S=[...document.querySelectorAll('.sahne')];
const DUR={json.dumps([s.get("sure", 3.6 if s["tip"] in ("kapak","son") else (3.2 + 0.25*len(s.get("maddeler",[])) if s["tip"]=="liste" else 3.3)) for s in sl])};
const BAS=[];let a=0;for(const d of DUR){{BAS.push(a);a+=d;}}
window.TOPLAM=a;
function e(x){{x=Math.min(1,Math.max(0,x));return 1-Math.pow(1-x,3)}}
function pop(x){{x=Math.min(1,Math.max(0,x));const c=1.70158*1.4;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)}}
window.goster=function(i){{S.forEach((s,k)=>{{s.style.display=k==i?'block':'none';s.style.opacity=1;s.style.transform='none'}});
 document.querySelectorAll('.a').forEach(x=>{{x.style.opacity=1;x.style.transform='none'}})}};
window.ciz=function(t){{
 S.forEach((s,k)=>{{const t0=BAS[k],t1=t0+DUR[k];
  if(t<t0-0.01||t>t1+0.3){{s.style.display='none';return}}
  s.style.display='block';const lt=t-t0;
  const giris=k==0?1:e(lt/0.35);const cikis=k==S.length-1?1:1-e((t-t1)/0.3);
  s.style.opacity=Math.min(giris,cikis);s.style.transform=`translateX(${{(1-giris)*90}}px)`;s.style.zIndex=k;
  s.querySelectorAll('.a').forEach((x,j)=>{{const d=parseFloat(x.dataset.d||0);const p=(lt-d)/0.5;
   if(x.classList.contains('pop')){{const q=pop(p);const f=Math.sin((t+j)*2.2)*8;
     x.style.opacity=e(p*1.6);x.style.transform=`translateY(${{(1-e(p))*40+(p>1?f:0)}}px) scale(${{0.4+0.6*q}})`}}
   else{{x.style.opacity=e(p);x.style.transform=`translateY(${{(1-e(p))*50}}px)`}}}})
 }})}};
</script></body></html>'''


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    story = "--story" in sys.argv
    reels = ("--reels" in sys.argv or "--sadece-reels" in sys.argv) and not story
    post = "--sadece-reels" not in sys.argv and not story
    src, out = Path(args[0]), Path(args[1])
    out.mkdir(parents=True, exist_ok=True)
    icerik = json.loads(src.read_text(encoding="utf-8"))
    ad = icerik.get("ad", src.stem)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        br = p.chromium.launch()
        if post:
            pg = br.new_page(viewport={"width": 1080, "height": 1350})
            pg.set_content(sayfa(icerik, 1080, 1350, False)); pg.wait_for_timeout(300)
            for i in range(len(icerik["slaytlar"])):
                pg.evaluate(f"goster({i})")
                pg.screenshot(path=str(out / f"{ad}_{i+1:02d}.jpg"), type="jpeg", quality=92)
            print("carousel:", len(icerik["slaytlar"]), "slayt")
        if story:  # tek kare hikâye (1080x1920 PNG), ilk slayt
            pg = br.new_page(viewport={"width": 1080, "height": 1920})
            pg.set_content(sayfa(icerik, 1080, 1920, True)); pg.wait_for_timeout(300)
            pg.evaluate("goster(0)")
            pg.screenshot(path=str(out / f"{ad}.png")); print("story:", out / f"{ad}.png")
        if reels:
            pg = br.new_page(viewport={"width": 1080, "height": 1920})
            pg.set_content(sayfa(icerik, 1080, 1920, True)); pg.wait_for_timeout(300)
            T = pg.evaluate("TOPLAM"); fps = 30; n = int(T * fps)
            wav = out / f"{ad}_muzik.wav"
            subprocess.run([sys.executable, str(KOK / "araclar/music.py"), str(wav), str(T)], check=True, capture_output=True)
            mp4 = out / f"{ad}_reels.mp4"
            ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(fps), "-c:v", "mjpeg", "-i", "-",
                                   "-i", str(wav), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
                                   "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", str(mp4)], stdin=subprocess.PIPE)
            for f in range(n):
                pg.evaluate(f"ciz({f / fps})")
                ff.stdin.write(pg.screenshot(type="jpeg", quality=88))
            ff.stdin.close(); ff.wait(); wav.unlink()
            pg.evaluate("goster(0)")
            pg.screenshot(path=str(out / f"{ad}_reels_kapak.jpg"), type="jpeg", quality=92)
            print("reels:", mp4, f"{T:.1f}s")
        br.close()


if __name__ == "__main__":
    main()
