"""@utopikanne: icerik JSON'undan (tarih -> [hikâye]) günlük PNG'leri üretir (RENKLİ şablonlar, anne_renkli.py).
Kullanım: python3 araclar/anne_gun.py <icerik.json> [--cikis DIR] [--saat-sonra HH:MM] [--tarih AAAA-AA-GG]
  --cikis: PNG'leri hesaplar/utopikanne/gun/<tarih>/ yerine DIR/<tarih>/ altına yazar (deneme için).
  --saat-sonra: yalnızca bu saatten (dahil) sonraki hikâyeleri üretir.  --tarih: yalnızca o günü üretir."""
import argparse
import json
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import anne_renkli as R

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def dosya_adi(o):
    return f"story_{o['saat'].replace(':', '')}_{o['sablon']}.png"


def uret(tarih, o, cikis=None):
    klasor = os.path.join(cikis, tarih) if cikis else os.path.join(ROOT, "hesaplar", "utopikanne", "gun", tarih)
    os.makedirs(klasor, exist_ok=True)
    p = os.path.join(klasor, dosya_adi(o))
    s = o["sablon"]
    R.CTA = o.get("cta")
    if s == "gunaydin":
        R.gunaydin(p, o["bilgi"], o["kaynak"])
    elif s == "tarif":
        R.tarif_karti(p, o["seri"], o["ay"], o["baslik"], o["malzemeler"], o["adimlar"], o["saklama"], o["dikkat"],
                      o["kaynak"], cizim=o.get("cizim", "havuc"))
    elif s == "hamilelik":
        R.hamilelik_haftasi(p, o["seri"], o["hafta"], o["boy"], o["bilgi"], o["ipucu"], o["kaynak"])
    elif s == "lohusa":
        R.lohusa(p, o.get("seri"), o["baslik"], o.get("bilgi"), o["kaynak"], o.get("maddeler"), o.get("not"))
    elif s == "emzirme":
        R.emzirme(p, o.get("seri"), o["baslik"], o.get("bilgi"), o["kaynak"], o.get("maddeler"), o.get("not"))
    elif s == "temizlik":
        R.temizlik(p, o.get("seri"), o["baslik"], o["maddeler"], o.get("uyari"), o["kaynak"])
    elif s == "haber":
        R.haber(p, o["baslik"], o["ozet"], o.get("tarih"), o["kaynak"])
    elif s == "efsane":
        R.efsane_gercek(p, o["efsane"], o["gercek"], o["kaynak"], seri=o.get("seri"))
    elif s == "hap":
        R.hap(p, o.get("seri"), o["baslik"], o["bilgi"], o["kaynak"])
    elif s in ("kontrol", "liste"):
        R.kontrol_listesi(p, o["etiket"], o["baslik"], o["maddeler"], o["kaynak"], numarali=(s == "liste"),
                          not_metni=o.get("not"))
    elif s == "kalori":
        R.kalori(p, o.get("seri"), o["baslik"], o["formul"], o["ornek"], o["bilgi"], o["kaynak"],
                 o.get("not", "Bilgilendirme amaçlıdır."))
    elif s == "dm":
        R.dm_cagrisi(p, o["soru"], o["secenekler"], o["cagri"])
    elif s == "iyi_geceler":
        R.iyi_geceler(p, o["baslik"], o["bilgi"], o["kaynak"])  # korunan gece şablonu (anne_story)
    else:
        raise ValueError("bilinmeyen şablon: " + s)
    return p


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("icerik")
    ap.add_argument("--cikis")
    ap.add_argument("--saat-sonra")
    ap.add_argument("--tarih")
    a = ap.parse_args()
    veri = json.load(open(a.icerik))
    for tarih, liste in veri.items():
        if a.tarih and tarih != a.tarih:
            continue
        for o in liste:
            if a.saat_sonra and o["saat"] < a.saat_sonra:
                continue
            print(uret(tarih, o, a.cikis))
