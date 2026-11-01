"""@utopikanne: icerik JSON'undan (tarih -> [hikâye]) günlük PNG'leri üretir.
Kullanım: python3 araclar/anne_gun.py hesaplar/utopikanne/gun/icerik_XXXX.json"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import anne_story as A

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def dosya_adi(o):
    return f"story_{o['saat'].replace(':', '')}_{o['sablon']}.png"


def uret(tarih, o):
    klasor = os.path.join(ROOT, "hesaplar", "utopikanne", "gun", tarih)
    os.makedirs(klasor, exist_ok=True)
    p = os.path.join(klasor, dosya_adi(o))
    s = o["sablon"]
    if s == "gunaydin":
        A.gunaydin(p, o["bilgi"], o["kaynak"])
    elif s == "tarif":
        A.tarif_karti(p, o["seri"], o["ay"], o["baslik"], o["malzemeler"], o["adimlar"], o["saklama"], o["dikkat"],
                      o["kaynak"], cizim=o.get("cizim", "havuc"))
    elif s == "hamilelik":
        A.hamilelik_haftasi(p, o["seri"], o["hafta"], o["boy"], o["bilgi"], o["ipucu"], o["kaynak"])
    elif s == "efsane":
        A.efsane_gercek(p, o["efsane"], o["gercek"], o["kaynak"], seri=o.get("seri"))
    elif s in ("kontrol", "liste"):
        A.kontrol_listesi(p, o["etiket"], o["baslik"], o["maddeler"], o["kaynak"], numarali=(s == "liste"),
                          not_metni=o.get("not"))
    elif s == "dm":
        A.dm_cagrisi(p, o["soru"], o["secenekler"], o["cagri"])
    elif s == "iyi_geceler":
        A.iyi_geceler(p, o["baslik"], o["bilgi"], o["kaynak"])
    return p


if __name__ == "__main__":
    veri = json.load(open(sys.argv[1]))
    for tarih, liste in veri.items():
        for o in liste:
            print(uret(tarih, o))
