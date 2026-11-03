"""5 Kasım 2026 (Perşembe) içerikleri. Kullanım: python3 uret_5kasim.py news stories"""
import sys
sys.path.insert(0, "/home/claude/sqlogreniyorum-medya/araclar")
import reels as R
from uretim import reel, story_poll, story_card, story_greeting
from brand import *
_src = open("/home/claude/sqlogreniyorum-medya/gun/2026-11-01/uret_31ekim_1kasim.py").read().split(
    "# ------------------------------------------------------------------ 31 Ekim haber")[0]
_ns = {}
exec(_src.replace("which = sys.argv[1:]", "which = []"), _ns)
hook_title, news_with_hook = _ns["hook_title"], _ns["news_with_hook"]

D = "/home/claude/sqlogreniyorum-medya/gun/2026-11-05/"
which = sys.argv[1:]

if "news" in which:
    sc = news_with_hook("YAPAY ZEKÂ", [("Ne izleyeceğini", TEXT), ("artık yapay zekâ", YELLOW),
                                       ("seçiyor.", TEXT)],
                        "Netflix, AI Discover sekmesini test ediyor.", [
        "Şimdilik ABD'de, TV uygulamasında test ediliyor.",
        "\"Scare Me\" gibi temalarla öneri listesi sunuyor.",
        "Her temada kısa bir klip önizlemesi var.",
        "Beğenmediğini işaretlersen tercihini hatırlıyor.",
    ], "Şirket bunu bir test olarak tanımlıyor; özellikler geri bildirime göre korunabilir ya da geliştirilebilir. Türkiye için tarih yok.",
        "Ne izleyeceğini yapay zekâya bırakır mısın?", "What's on Netflix, TheWrap (3 Kasım 2026)")

    def s_cta(d, t):
        # Bu tur değişikliği: paylaşım çağrısı hedef kişiye özel
        y = hook_title(d, [("Ne izleyeceğini", TEXT), ("seçemeyen birine", YELLOW), ("gönder.", YELLOW)], 520, 104)
        y = R.caption(d, t, "Kaydet, sonra lazım olur.", y + 50, start=0.4, size=54, col=TEXT, weight="Bold")
        y = R.caption(d, t, "Her gün yapay zekâ ve SQL için takip et", y + 30, start=0.7, size=44, col=MUTED,
                      weight="SemiBold")
        if R.visible(t, 0.9):
            pill(d, (70, y + 50 + R.rise(t, 0.9)), HANDLE, fill=PINK, size=44)

    sc[-1] = (3.2, s_cta)
    print(reel("reel_netflix_ai_discover", sc, D, seed=51))

if "stories" in which:
    story_greeting(D + "story_gunaydin.png", "gunaydin", "İlk .com adresi: 1985",
                   "15 Mart 1985'te kaydedilen symbolics.com, internetteki ilk .com alan adı. "
                   "Adres, bilgisayar şirketi Symbolics'e aitti.",
                   "Bugün 11:00 ve 18:00'de yeni Reels var.")
    story_poll(D + "story_1000_soru.png", "GÜNÜN SORUSU", "Ne izleyeceğini yapay zekâya bırakır mısın?",
               ["Evet, bırakırım", "Hayır, ben seçerim", "Arkadaşıma sorarım"],
               note="Cevabını DM'den yaz. Haber 18:00 Reels'inde.")
    story_card(D + "story_1400_where_having_kart.png", "SQL", "WHERE mi, [HAVING] mi?", [
        "WHERE: gruplamadan önce satırları süzer.",
        "HAVING: gruplamadan sonra grupları süzer.",
        "WHERE COUNT(*) > 1 yazarsan sorgu hata verir.",
        "Toplama sonucuna göre süzüyorsan HAVING kullan.",
    ], footer="Ekran görüntüsünü al, mülakattan önce bak.", tag_col=TEAL)
    story_card(D + "story_1700_duyuru.png", "18:00'DE", "Ne izleyeceğini [yapay zekâ] seçiyor.", [
        "Netflix yeni bir sekmeyi test ediyor.",
        "Neler yapıyor, kimlere açık?",
    ], footer="Haber 18:00 Reels'inde.", tag_col=PINK)
    story_card(D + "story_2130_ozet.png", "GÜNÜN ÖZETİ", "Bugün ne [öğrendik]?", [
        "WHERE satırları, HAVING grupları süzer.",
        "COUNT(*) gibi toplamalar WHERE'de kullanılamaz.",
        "Netflix ABD'de AI Discover sekmesini test ediyor.",
    ], footer="Yarın 11:00 ve 18:00'de yeni Reels.")
    story_greeting(D + "story_iyigeceler.png", "iyigeceler", "İlk tweet 2006'da atıldı",
                   "21 Mart 2006'da Jack Dorsey ilk tweeti attı: \"just setting up my twttr\". "
                   "Platformun o günkü adı Twttr'dı.",
                   "Yarın 11:00 ve 18:00'de yeni Reels var. İyi uykular.")
    print("stories ok")
