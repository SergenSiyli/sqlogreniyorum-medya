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
import re
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Europe/Istanbul")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Çoklu hesap: HESAP ortam değişkeni. Varsayılan sqlogreniyorum (kuyruk/ klasörü, IG_TOKEN sırrı).
# Diğer hesaplar: hesaplar/<hesap>/kuyruk/, hesaplar/<hesap>/hesap.json {"ig_id": ...}, sır IG_TOKEN_<HESAP>.
HESAP = os.environ.get("HESAP", "sqlogreniyorum").strip() or "sqlogreniyorum"
VARSAYILAN = HESAP == "sqlogreniyorum"
IG_ID = "17841460768999553"  # @sqlogreniyorum Instagram hesap kimliği (Meta panelinden)
if not VARSAYILAN:
    with open(os.path.join(ROOT, "hesaplar", HESAP, "hesap.json")) as _f:
        IG_ID = str(json.load(_f).get("ig_id", ""))
KUYRUK = os.path.join(ROOT, "kuyruk") if VARSAYILAN else os.path.join(ROOT, "hesaplar", HESAP, "kuyruk")
TOKEN_ADI = "IG_TOKEN" if VARSAYILAN else "IG_TOKEN_" + HESAP.upper()
WORKFLOW = os.environ.get("WORKFLOW_DOSYA", "instagram-yayin.yml")
DURUM = os.path.join(KUYRUK, "durum")
PENCERE_DK = 80        # bu çalışmanın üstlendiği ileri pencere
GEC_KALMA_DK = 60      # bundan daha geç kalmış gönderi yayınlanmaz, "kaçırıldı" yazılır
HAZIRLIK_DK = {"REEL": 7, "TRIAL_REEL": 7, "STORY": 2, "CAROUSEL": 5}   # konteyner hedef saatten bu kadar önce hazırlanır
ZINCIR_UYKU_DK = 25    # zincir: en fazla bu kadar bekleyip bir sonraki çalışmayı kendisi başlatır
ZINCIR_UFUK_SA = 14    # bu kadar saat içinde bekleyen gönderi varsa zincir sürer


def token():
    t = os.environ.get(TOKEN_ADI, "").strip()
    if not t:
        sys.exit(f"{TOKEN_ADI} depo sırrı tanımlı değil (Settings > Secrets and variables > Actions).")
    return t


def api():
    # IGAA... = Instagram girişi anahtarı; EAA... = Facebook/birleşik giriş anahtarı
    return "https://graph.facebook.com/v23.0" if token().startswith("EAA") else "https://graph.instagram.com/v23.0"


def hesap_id():
    if token().startswith("EAA"):
        if not IG_ID:
            raise RuntimeError(f"hesaplar/{HESAP}/hesap.json içinde ig_id yok")
        return IG_ID
    return istek("GET", "me", fields="user_id")["user_id"]


def istek(method, path, **params):
    params["access_token"] = token()
    API = api()
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
        subprocess.run(["git", "commit", "-qm", f"[{HESAP}] yayın durumu: {oge['id']} ({sonuc['durum']})"], cwd=ROOT)
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


JSDELIVR_RE = re.compile(r"cdn\.jsdelivr\.net/gh/SergenSiyli/sqlogreniyorum-medya@[0-9a-f]{7,40}/(.+)$")


def yerel_dosya(url):
    """Kendi depomuzdaki medyanın Actions çalışma kopyasındaki yolu (yoksa None).
    Videolar jsDelivr yerine buradan doğrudan Instagram'a yüklenir (jsDelivr kuralları toplu video barındırmayı yasaklıyor)."""
    m = JSDELIVR_RE.search(url or "")
    if not m:
        return None
    yol = os.path.join(ROOT, urllib.parse.unquote(m.group(1)))
    return yol if os.path.isfile(yol) else None


def video_yukle(uid, p, yol):
    """Resumable yükleme: konteyneri upload_type=resumable ile aç, dosyayı rupload'a gönder. Konteyner id döner."""
    p = dict(p)
    p.pop("video_url", None)
    p["upload_type"] = "resumable"
    r = istek("POST", f"{uid}/media", **p)
    cid, uri = r["id"], r.get("uri")
    if not uri:
        raise RuntimeError("resumable yükleme adresi dönmedi")
    with open(yol, "rb") as f:
        veri = f.read()
    for deneme in range(4):
        req = urllib.request.Request(uri, data=veri, method="POST", headers={
            "Authorization": "OAuth " + token(), "offset": "0", "file_size": str(len(veri))})
        try:
            with urllib.request.urlopen(req, timeout=300) as rr:
                sonuc = json.load(rr)
            if not sonuc.get("success", True):
                raise RuntimeError(f"yükleme başarısız: {sonuc}")
            return cid
        except urllib.error.HTTPError as e:
            govde = e.read().decode(errors="replace")
            if e.code >= 500 and deneme < 3:
                time.sleep(5 * (deneme + 1))
                continue
            raise RuntimeError(f"yükleme {e.code}: {govde[:300]}") from None


def bekle_hazir(cid):
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


def konteyner(uid, o):
    if o["tur"] == "STORY":
        p = {"media_type": "STORIES"}
        p["video_url" if o["medya"].endswith(".mp4") else "image_url"] = o["medya"]
    elif o["tur"] in ("REEL", "TRIAL_REEL"):
        p = {"media_type": "REELS", "video_url": o["medya"], "caption": o.get("aciklama", ""), "share_to_feed": "true"}
        if o.get("kapak"):
            p["cover_url"] = o["kapak"]
        if o["tur"] == "TRIAL_REEL":  # deneme Reels: önce yalnızca takip etmeyenlere gösterilir
            p.pop("share_to_feed")
            p["trial_params"] = json.dumps({"graduation_strategy": "SS_PERFORMANCE"})
    elif o["tur"] == "CAROUSEL":
        cocuklar = []
        for m in o["medya"]:
            q = {"is_carousel_item": "true"}
            if m.endswith(".mp4"):
                q.update(media_type="VIDEO", video_url=m)
            else:
                q["image_url"] = m
            cocuklar.append(istek("POST", f"{uid}/media", **q)["id"])
        p = {"media_type": "CAROUSEL", "children": ",".join(cocuklar), "caption": o.get("aciklama", "")}
    else:
        raise ValueError("bilinmeyen tür " + o["tur"])
    yol = yerel_dosya(p.get("video_url"))
    if yol:
        try:
            return bekle_hazir(video_yukle(uid, p, yol))
        except Exception as e:  # doğrudan yükleme olmazsa eski yol (URL) yedek
            print(f"  doğrudan video yükleme başarısız, URL ile denenecek: {e}", flush=True)
    return bekle_hazir(istek("POST", f"{uid}/media", **p)["id"])


def yayin_turu(uid):
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
    return hatalar


def siradaki():
    """Bugün/yarın bekleyen en yakın gönderinin hedef zamanı (yoksa None)."""
    n = simdi()
    bekleyen = []
    for g in (n.date(), n.date() + dt.timedelta(days=1)):
        yol = os.path.join(KUYRUK, f"{g.isoformat()}.json")
        if os.path.exists(yol):
            with open(yol) as f:
                for o in json.load(f):
                    h = dt.datetime.fromisoformat(o["hedef"]).replace(tzinfo=TZ)
                    if not yapildi(o["id"]) and h > n - dt.timedelta(minutes=GEC_KALMA_DK):
                        bekleyen.append(h)
    return min(bekleyen) if bekleyen else None


CALISMA_DK = 110   # bir çalışma en fazla bu kadar döngü kurar, sonra halefini başlatır (iş zaman aşımı 240 dk)


def yayin():
    """4 Kasım: zincir bir kez koptu (09:40Z'de halef başlamadı, cron da 2 saat gelmedi → 14:00 story kaçtı).
    Artık her çalışma ~110 dk boyunca kendi içinde döner (her turda git pull ile yeni kuyruğu okur),
    sonra halefini yeniden denemeli ve doğrulamalı başlatır; başlatamazsa kendisi dönmeye devam eder."""
    uid = hesap_id()
    basla = time.time()
    hatalar = 0
    while True:
        subprocess.run(["git", "pull", "--rebase", "-q"], cwd=ROOT)
        hatalar += yayin_turu(uid)
        subprocess.run(["git", "pull", "--rebase", "-q"], cwd=ROOT)
        s = siradaki()
        if not s or s - simdi() > dt.timedelta(hours=ZINCIR_UFUK_SA):
            print("yakında bekleyen gönderi yok; cron'a bırakıldı", flush=True)
            break
        if time.time() - basla > CALISMA_DK * 60:
            if halef_baslat():
                break
            if time.time() - basla > 200 * 60:  # iş zaman aşımına yaklaşıldı; cron yedek
                break
        uyan = min(simdi() + dt.timedelta(minutes=ZINCIR_UYKU_DK), s - dt.timedelta(minutes=PENCERE_DK - 10))
        print(f"sıradaki gönderi {s:%d.%m %H:%M}; {uyan:%H:%M}'de yeniden bakılacak", flush=True)
        bekle(uyan)
    if hatalar:
        sys.exit(f"{hatalar} gönderi yayınlanamadı")


def halef_baslat():
    """Sonraki çalışmayı workflow_dispatch ile başlatır; 5 deneme, oluştuğunu runs listesinden doğrular."""
    tok, repo = os.environ.get("GITHUB_TOKEN"), os.environ.get("GITHUB_REPOSITORY")
    if not tok or not repo:
        return False
    h = {"Authorization": f"Bearer {tok}", "Accept": "application/vnd.github+json"}
    for deneme in range(5):
        oncesi = dt.datetime.now(dt.timezone.utc) - dt.timedelta(seconds=5)
        try:
            req = urllib.request.Request(
                f"https://api.github.com/repos/{repo}/actions/workflows/{WORKFLOW}/dispatches",
                data=json.dumps({"ref": "main", "inputs": {"mod": "yayin"}}).encode(), method="POST", headers=h)
            urllib.request.urlopen(req, timeout=30).close()
            time.sleep(15)
            with urllib.request.urlopen(urllib.request.Request(
                    f"https://api.github.com/repos/{repo}/actions/workflows/{WORKFLOW}/runs?event=workflow_dispatch&per_page=5",
                    headers=h), timeout=30) as r:
                runs = json.load(r)["workflow_runs"]
            mevcut = os.environ.get("GITHUB_RUN_ID")
            if any(str(x["id"]) != mevcut and dt.datetime.fromisoformat(x["created_at"].replace("Z", "+00:00")) >= oncesi
                   for x in runs):
                print("halef çalışma başlatıldı ve doğrulandı", flush=True)
                return True
            print(f"halef doğrulanamadı (deneme {deneme + 1})", flush=True)
        except Exception as e:
            print(f"halef başlatma hatası (deneme {deneme + 1}): {e}", flush=True)
        time.sleep(20 * (deneme + 1))
    return False


def kontrol():
    """Sonucu kuyruk/kontrol.json'a yazar ve depoya gönderir (Actions loglarına erişilemeyen ortamlar için)."""
    sonuc = {"zaman": simdi().isoformat(timespec="seconds")}
    try:
        t = token()
        sonuc["anahtar_turu"] = "facebook" if t.startswith("EAA") else ("instagram" if t.startswith("IG") else "bilinmiyor:" + t[:3])
        sonuc["anahtar_uzunlugu"] = len(t)
        uid = hesap_id()
        sonuc["hesap"] = istek("GET", uid, fields="username,media_count")
        sonuc["kota"] = istek("GET", f"{uid}/content_publishing_limit", fields="quota_usage,config")
        sonuc["durum"] = "ok"
        for u in sys.argv[2:]:  # medya adreslerinin içerik türünü kontrol et
            try:
                with urllib.request.urlopen(urllib.request.Request(u, method="HEAD"), timeout=30) as r:
                    sonuc.setdefault("medya", {})[u] = r.headers.get("Content-Type")
            except Exception as e2:
                sonuc.setdefault("medya", {})[u] = "HATA " + str(e2)[:100]
    except Exception as e:
        sonuc["durum"] = "hata"
        sonuc["hata"] = str(e)[:800]
    yol = os.path.join(KUYRUK, "kontrol.json")
    with open(yol, "w") as f:
        json.dump(sonuc, f, ensure_ascii=False, indent=1)
    print(json.dumps(sonuc, ensure_ascii=False))
    subprocess.run(["git", "add", yol], cwd=ROOT, check=True)
    subprocess.run(["git", "commit", "-qm", f"[{HESAP}] API bağlantı kontrolü: " + sonuc["durum"]], cwd=ROOT)
    for _ in range(5):
        subprocess.run(["git", "pull", "--rebase", "-q"], cwd=ROOT)
        if subprocess.run(["git", "push", "-q"], cwd=ROOT).returncode == 0:
            break
        time.sleep(3)
    if sonuc["durum"] != "ok":
        sys.exit(1)


def videotest():
    """Yayınlamadan doğrudan video yüklemeyi dener: konteyner FINISHED olursa başarı. Sonuç <kuyruk>/videotest.json."""
    yol = os.path.join(ROOT, sys.argv[2])
    sonuc = {"zaman": simdi().isoformat(timespec="seconds"), "dosya": sys.argv[2]}
    try:
        uid = hesap_id()
        t0 = time.time()
        cid = bekle_hazir(video_yukle(uid, {"media_type": "REELS", "caption": "test"}, yol))
        sonuc.update(durum="ok", konteyner=cid, sure_sn=round(time.time() - t0), not_="yayınlanmadı (test)")
    except Exception as e:
        sonuc.update(durum="hata", hata=str(e)[:600])
    out = os.path.join(KUYRUK, "videotest.json")
    with open(out, "w") as f:
        json.dump(sonuc, f, ensure_ascii=False, indent=1)
    print(json.dumps(sonuc, ensure_ascii=False), flush=True)
    subprocess.run(["git", "add", out], cwd=ROOT, check=True)
    subprocess.run(["git", "commit", "-qm", f"[{HESAP}] video yükleme testi: {sonuc['durum']}"], cwd=ROOT)
    for _ in range(5):
        subprocess.run(["git", "pull", "--rebase", "-q"], cwd=ROOT)
        if subprocess.run(["git", "push", "-q"], cwd=ROOT).returncode == 0:
            break
        time.sleep(3)


def analiz():
    """Hesap analizi için ham veri: profil + son 200 gönderi (+ erişilebilirse içgörüler) -> <kuyruk>/../analiz/."""
    uid = hesap_id()
    out = {"zaman": simdi().isoformat(timespec="seconds"), "hesap": HESAP}
    try:
        out["profil"] = istek("GET", uid, fields="username,name,biography,followers_count,follows_count,media_count,website")
    except Exception as e:
        out["profil_hata"] = str(e)[:300]
    medya, sonraki, sayfa = [], None, 0
    alanlar = "id,caption,media_type,media_product_type,timestamp,like_count,comments_count,permalink"
    while sayfa < 8:
        p = {"fields": alanlar, "limit": 25}
        if sonraki:
            p["after"] = sonraki
        r = istek("GET", f"{uid}/media", **p)
        medya += r.get("data", [])
        sonraki = r.get("paging", {}).get("cursors", {}).get("after")
        sayfa += 1
        if not r.get("paging", {}).get("next"):
            break
    for m in medya[:60]:
        metr = "reach,saved,shares,total_interactions" + (",views" if m.get("media_product_type") == "REELS" else "")
        try:
            m["icgoru"] = {d["name"]: d["values"][0]["value"] for d in istek("GET", f"{m['id']}/insights", metric=metr)["data"]}
        except Exception as e:
            m["icgoru_hata"] = str(e)[:160]
    out["medya"] = medya
    try:
        out["hesap_icgoru"] = istek("GET", f"{uid}/insights", metric="reach,follower_count", period="day")
    except Exception as e:
        out["hesap_icgoru_hata"] = str(e)[:300]
    try:
        out["kitle"] = istek("GET", f"{uid}/insights", metric="follower_demographics", period="lifetime",
                             metric_type="total_value", breakdown="age,gender")
    except Exception as e:
        out["kitle_hata"] = str(e)[:300]
    d = os.path.join(os.path.dirname(KUYRUK), "analiz")
    os.makedirs(d, exist_ok=True)
    yol = os.path.join(d, f"veri_{simdi():%Y-%m-%d}.json")
    with open(yol, "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    subprocess.run(["git", "add", yol], cwd=ROOT, check=True)
    subprocess.run(["git", "commit", "-qm", f"[{HESAP}] analiz verisi ({len(medya)} gönderi)"], cwd=ROOT)
    subprocess.run(["git", "pull", "--rebase", "-q"], cwd=ROOT)
    subprocess.run(["git", "push", "-q"], cwd=ROOT)
    print(f"analiz: {len(medya)} gönderi yazıldı -> {yol}", flush=True)


if __name__ == "__main__":
    {"kontrol": kontrol, "yayin": yayin, "analiz": analiz, "videotest": videotest}[sys.argv[1] if len(sys.argv) > 1 else "yayin"]()
