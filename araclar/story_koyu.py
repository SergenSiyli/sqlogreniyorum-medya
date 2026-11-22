"""sqlogreniyorum hikâyeleri: v5 koyu kod editörü stili (uretim.py). Kullanım: python3 araclar/story_koyu.py 2026-11-23 [--atla 0900,...]
Kaynak: icerik/<tarih>_{gunaydin,anket,duyuru,cevap_kart,iyigeceler}.json (anne_canli formatı). *vurgu* -> [vurgu]."""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from uretim import story_poll, story_card, story_greeting
from brand import *
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
t = sys.argv[1]; atla = sys.argv[3].split(",") if len(sys.argv) > 3 else []
def j(k): return json.load(open(f"{KOK}/icerik/{t}_{k}.json"))["slaytlar"][0]
EMO = re.compile("[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F\u200D]+")
def temiz(s): return re.sub(r"\s+([.,!?])", r"\1", EMO.sub("", s or "")).strip()
def v(s): return re.sub(r"\*(.+?)\*", r"[\1]", temiz(s))
def duz(s): return temiz(s).replace("*", "")
D = f"{KOK}/gun/{t}/"; out = {}
def yap(slot, fn):
    if slot in atla: return
    out[slot] = fn()
s = j("gunaydin")
yap("0900", lambda: story_greeting(D + "story_0900_gunaydin_v5.png", "gunaydin", duz(s["baslik"]), temiz(s["alt"]), "Kaynak: " + s.get("kaynak", "")))
s2 = j("anket")
yap("1300", lambda: story_poll(D + "story_1300_anket_v5.png", "ANKET · HANGİSİ DÖNER?", temiz(s2["ust"]) + "\n" + duz(s2["baslik"]), s2["secenekler"], "Cevap 21:00'de. Tahminini aklında tut."))
s3 = j("duyuru")
yap("1805", lambda: story_card(D + "story_1805_duyuru_v5.png", "ŞİMDİ REELS'TE · " + s3["ust"].upper(), v(s3["baslik"]), [temiz(s3["alt"])], tag_col=PINK))
s4 = j("cevap_kart")
yap("2100", lambda: story_card(D + "story_2100_cevap_kart_v5.png", "BUGÜNÜN CEVAPLARI", v(s4["baslik"]), [temiz(s4["alt"])], footer=s4["ust"]))
s5 = j("iyigeceler")
yap("2300", lambda: story_greeting(D + "story_2300_iyigeceler_v5.png", "iyigeceler", duz(s5["baslik"]), temiz(s5["alt"]), "Kaynak: " + s5.get("kaynak", "")))
print(json.dumps(out))
