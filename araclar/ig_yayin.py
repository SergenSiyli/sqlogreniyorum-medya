"""@sqlogreniyorum: Instagram'a doğrudan (resmi Instagram API, ücretsiz) zamanında yayın.

GitHub Actions'ta çalışır (.github/workflows/instagram-yayin.yml). Erişim anahtarı
yalnızca depo sırrı IG_TOKEN'dan okunur; koda, kuyruğa ya da loglara yazılmaz.

Kuyruk: kuyruk/AAAA-AA-GG.json  ->  [{"id", "hedef": "AAAA-AA-GGTSS:DD" (İstanbul saati),
         "tur": "STORY"|"REEL", "medya": url, "kapak": url (REEL), "aciklama": str (REEL)}]
Durum : kuyruk/durum/<id>.json  (yayınlananlar; ikinci kez yayınlanmaz)

Kullanım:
  python3 araclar/ig_yayin.py kontrol      # anahtar ve hesap türünü doğrular
  python3 araclar/ig_yayin.py yayin        # önümüzdeki pencerede zamanı gelenleri tam saatinde yayınlar
"""
import datetime as dt
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo

API = "https://graph.instagram.com/v23.0"
TZ = ZoneInfo("Europe/Istanbul")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KUYRUK = os.path.join(ROOT, "kuyruk")
DURUM = os.path.join(KUYRUK, "durum")
PENCERE_DK = 80        # bu çalışmanın üstlendiği ileri pencere
GEC_KALMA_DK = 60      # bundan daha geç kalmış gönderi yayınlanmaz, "kaçırıldı" yazılır
HAZIRLIK_DK = {"REEL": 7, "STORY": 2}   # konteyner hedef saatten bu kadar önce hazırlanır


def token():
    t = os.environ.get("IG_TOKEN", "").strip()
    if not t:
        sys.exit("IG_TOKEN depo sırrı tanımlı değil (Settings > Secrets and variables > Actions).")
    return t


def istek(method, path, **params):
    params["access_token"] = token()
    data = urllib.parse.urlencode(params).encode()
    url = f"{API}/{path}"
    if method == "GET":
        req = urllib.request.Request(url + "?" + data.decode())
    else:
        req = urllib.request.Request(url, data=data, method="POST")
    for deneme in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            govde = e.read().decode(errors="replace")
            if e.code >= 500 and deneme < 3:
                time.sleep(5 * (deneme + 1))
                continue
            raise RuntimeError(f"API {e.code}: {govde[:400]}") from None
        except urllib.error.URLError:
            if deneme < 3:
                time.sleep(5 * (deneme + 1))
                continue
            raise


def simdi():
    return dt.datetime.now(TZ)


def bekle(hedef):
    while True:
        kalan = (hedef - simdi()).total_seconds()
        if kalan <= 0:
            return
        time.sleep(min(kalan, 30))


def kaydet(oge, sonuc):
    os.makedirs(DURUM, exist_ok=True)
    yol = os.path.join(DURUM, oge["id"] + ".json")
    with open(yol, "w") as f:
        json.dump({"id": oge["id"], "hedef": oge["hedef"], "tur": oge["tur"], **sonuc}, f, ensure_ascii=False, indent=1)
    for deneme in range(5):
        subprocess.run(["git", "add", yol], cwd=ROOT, check=True)
        subprocess.run(["git", "commit", "-qm", f"yayın durumu: {oge['id']} ({sonuc['durum']})"], cwd=ROOT)
        subprocess.run(["git", "pull", "--rebase", "-q"], cwd=ROOT)
        if subprocess.run(["git", "push", "-q"], cwd=ROOT).returncode == 0:
            return
        time.sleep(3)


def yapildi(oid):
    return os.path.exists(os.path.join(DURUM, oid + ".json"))


def adaylar():
    bugun = simdi().date()
    ogeler = []
    for g in (bugun - dt.timedelta(days=1), bugun, bugun + dt.timedelta(days=1)):
        yol = os.path.join(KUYRUK, f"{g.isoformat()}.json")
        if os.path.exists(yol):
            with open(yol) as f:
                ogeler += json.load(f)
    n = simdi()
    sec = []
    for o in ogeler:
        h = dt.datetime.fromisoformat(o["hedef"]).replace(tzinfo=TZ)
        o["_h"] = h
        if yapildi(o["id"]):
            continue
        if n - dt.timedelta(minutes=GEC_KALMA_DK) <= h <= n + dt.timedelta(minutes=PENCERE_DK):
            sec.append(o)
        elif dt.timedelta(minutes=GEC_KALMA_DK) < n - h < dt.timedelta(hours=12):
            kaydet(o, {"durum": "kacirildi", "not": "yayın penceresi kaçırıldı"})
    return sorted(sec, key=lambda o: o["_h"])


def konteyner(uid, o):
    if o["tur"] == "STORY":
        p = {"media_type": "STORIES"}
        p["video_url" if o["medya"].endswith(".mp4") else "image_url"] = o["medya"]
    elif o["tur"] == "REEL":
        p = {"media_type": "REELS", "video_url": o["medya"], "caption": o.get("aciklama", ""), "share_to_feed": "true"}
        if o.get("kapak"):
            p["cover_url"] = o["kapak"]
    else:
        raise ValueError("bilinmeyen tür " + o["tur"])
    cid = istek("POST", f"{uid}/media", **p)["id"]
    son = time.time() + 15 * 60
    while True:
        st = istek("GET", cid, fields="status_code,status").get("status_code")
        if st == "FINISHED":
            return cid
        if st in ("ERROR", "EXPIRED"):
            raise RuntimeError(f"konteyner {st}")
        if time.time() > son:
            raise RuntimeError("konteyner 15 dk içinde hazırlanmadı")
        time.sleep(10)


def yayin():
    uid = istek("GET", "me", fields="user_id,username")["user_id"]
    hatalar = 0
    for o in adaylar():
        hazirlik = o["_h"] - dt.timedelta(minutes=HAZIRLIK_DK.get(o["tur"], 3))
        print(f"{o['id']}: hedef {o['hedef']}, hazırlık {hazirlik:%H:%M}", flush=True)
        bekle(hazirlik)
        try:
            cid = konteyner(uid, o)
            bekle(o["_h"])
            mid = istek("POST", f"{uid}/media_publish", creation_id=cid)["id"]
            gecikme = round((simdi() - o["_h"]).total_seconds())
            print(f"  yayınlandı {mid}, sapma {gecikme} sn", flush=True)
            kaydet(o, {"durum": "yayinlandi", "media_id": mid, "zaman": simdi().isoformat(timespec="seconds"),
                       "sapma_sn": gecikme})
        except Exception as e:  # bir gönderinin hatası diğerlerini durdurmaz
            hatalar += 1
            print(f"  HATA: {e}", flush=True)
            kaydet(o, {"durum": "hata", "hata": str(e)[:500], "zaman": simdi().isoformat(timespec="seconds")})
    if hatalar:
        sys.exit(f"{hatalar} gönderi yayınlanamadı")


def kontrol():
    me = istek("GET", "me", fields="user_id,username,account_type,media_count")
    print(json.dumps(me, ensure_ascii=False))
    lim = istek("GET", f"{me['user_id']}/content_publishing_limit", fields="quota_usage,config")
    print(json.dumps(lim, ensure_ascii=False))


if __name__ == "__main__":
    {"kontrol": kontrol, "yayin": yayin}[sys.argv[1] if len(sys.argv) > 1 else "yayin"]()
