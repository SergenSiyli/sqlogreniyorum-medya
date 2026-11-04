"""5 Kasım eksik story'leri + 6 Kasım 2026 (Cuma) içerikleri. Kullanım: python3 uret_6kasim.py ek5 news sql stories"""
import sys
sys.path.insert(0, "/home/claude/sqlogreniyorum-medya/araclar")
import reels as R
from uretim import reel, story_poll, story_card, story_greeting
from brand import *
_src = open("/home/claude/sqlogreniyorum-medya/gun/2026-11-01/uret_31ekim_1kasim.py").read().split(
    "# ------------------------------------------------------------------ 31 Ekim haber")[0]
_ns = {}
exec(_src.replace("which = sys.argv[1:]", "which = []"), _ns)
hook_title, news_with_hook, sql_cta = _ns["hook_title"], _ns["news_with_hook"], _ns["sql_cta"]

D5 = "/home/claude/sqlogreniyorum-medya/gun/2026-11-05/"
D = "/home/claude/sqlogreniyorum-medya/gun/2026-11-06/"
which = sys.argv[1:]

if "ek5" in which:
    story_card(D5 + "story_1330_mulakat_taktik.png", "TEKNİK MÜLAKAT TAKTİĞİ #1", "SQL'de [takıldın] mı?", [
        "Önce tabloyu ve beklenen sonucu sesli özetle.",
        "2-3 örnek satırla sonucu elle hesapla.",
        "Basit sorguyla başla, adım adım geliştir.",
        "Fonksiyon adını unuttuysan mantığını anlat.",
    ], footer="Veri analisti mülakatına hazırlanan bir arkadaşına gönder.", tag_col=BLUE)
    story_card(D5 + "story_1600_hap_whatsapp.png", "HAP HABER", "WhatsApp [son fotoğraf]", [
        "Sohbette galerideki son fotoğrafı öneriyor.",
        "Kendiliğinden gitmez, önce düzenleme ekranı açılır.",
        "Şimdilik bazı kullanıcılara kademeli geliyor.",
    ], footer="Kaynak: WABetaInfo, Dataconomy (3-4 Kasım 2026)", tag_col=PINK)
    print("ek5 ok")

if "news" in which:
    sc = news_with_hook("YAPAY ZEKÂ", [("Okul yapay zekâyı", TEXT), ("kapatırsa Google", YELLOW),
                                       ("Arama da kapanabilir.", TEXT)],
                        "ABD'de okullar için yeni kural tartışılıyor.", [
        "ABD'de okul hesaplarında Gemini ve Arama varsayılan kapalı.",
        "Açmak için okul yöneticisinin onayı gerekiyor.",
        "Yapay zekâyı kapatan okulda Arama da kapanıyor.",
        "Değişiklik 2027'de başlıyor; tepkiler büyüyor.",
    ], "Google'a göre Arama ve yapay zekâ artık iç içe; şirket ayarların ayrı açılabileceğini de söylüyor. "
       "Türkiye için açıklama yok.",
        "Okulda yapay zekâ + Arama paketi mantıklı mı?", "9to5Google, Forbes, CBS News, TechCrunch (3-4 Kasım 2026)")
    print(reel("reel_google_okul_arama", sc, D, seed=61))

if "sql" in which:
    ROWS = [("1 Kasım", 40), ("2 Kasım", 55), ("3 Kasım", 50), ("5 Kasım", 70), ("6 Kasım", 65)]

    def s_hook(d, t):
        pill(d, (70, 300), "SQL MÜLAKAT SORUSU #5", fill=YELLOW, size=40)
        y = hook_title(d, [("5 günlük satış,", TEXT), ("fark sorgusu", YELLOW), ("3 satır döndürdü.", PINK)], 410, 110)
        code_box(d, (40, y + 30), ["SELECT b.gun, b.adet - a.adet", "FROM satis a JOIN satis b",
                                   "ON b.gun = DATE(a.gun, '+1 day');"], size=40, w=1000, title="sorgu.sql")
        R.caption(d, t, "5 Kasım'ın +20'si kayboldu.", y + 380, start=1.0, size=56, col=RED, weight="Black")

    def s_data(d, t):
        R.caption(d, t, "satis", 330, size=52, weight="ExtraBold")
        table(d, (40, 420), ["gun", "adet"], ROWS, [560, 420], size=42, hl_rows=[3], hl_col=RED)
        R.caption(d, t, "4 Kasım'da [kayıt yok].", 1050, start=0.8, size=56, hl=YELLOW)

    def s_trap(d, t):
        pill(d, (70, 300), "NEDEN?", fill=RED, size=44)
        R.caption(d, t, "JOIN, [bir gün önceyi] arıyor.", 420, size=58, hl=YELLOW, weight="Bold")
        R.caption(d, t, "5 Kasım için 4 Kasım yok: satır düştü.", 640, start=0.9, size=54, weight="Bold")
        R.caption(d, t, "1 Kasım'ın da öncesi yok: o da düştü.", 860, start=1.7, size=54, col=RED, weight="Bold")
        R.caption(d, t, "İstediğin takvimdeki dün değil, [önceki satır].", 1100, start=2.5, size=52,
                  hl=GREEN, weight="Bold")

    def s_fix(d, t):
        pill(d, (70, 300), "ÇÖZÜM: LAG", fill=GREEN, size=40)
        code_box(d, (40, 400), ["SELECT gun, adet,", "  adet - LAG(adet) OVER (", "    ORDER BY gun) AS fark",
                                "FROM satis;"], size=40, w=1000, title="sorgu.sql")
        if R.visible(t, 1.0):
            table(d, (40, 860 + R.rise(t, 1.0)), ["gun", "adet", "fark"],
                  [("1 Kasım", 40, "NULL"), ("2 Kasım", 55, 15), ("3 Kasım", 50, -5), ("5 Kasım", 70, 20),
                   ("6 Kasım", 65, -5)], [420, 280, 280], size=38, hl_rows=[3], hl_col=GREEN)
        R.caption(d, t, "5 satır geldi, +20 [geri döndü].", 1500, start=2.2, size=50, hl=GREEN)

    def s_rule(d, t):
        pill(d, (70, 330), "KURAL", fill=TEAL, size=44)
        y = 460
        for i, (a, b) in enumerate([("Önceki satır", "LAG(sütun)"), ("Sonraki satır", "LEAD(sütun)")]):
            st = 0.2 + i * 0.8
            if R.visible(t, st):
                yy = y + R.rise(t, st, 40)
                d.rounded_rectangle([50, yy, 1030, yy + 230], radius=26, fill=CARD, outline=LINE, width=2)
                d.text((90, yy + 40), a, font=font("Bold", 50), fill=TEXT)
                d.text((90, yy + 120), b, font=font("Black", 64), fill=YELLOW if i == 0 else TEAL)
            y += 270
        R.caption(d, t, "Sırayı OVER içindeki [ORDER BY] belirler.", 1060, start=1.8, size=50, hl=PINK)
        R.caption(d, t, "İlk satırın öncesi yok: fark NULL.", 1240, start=2.4, size=48, col=MUTED)

    sc = [(2.9, s_hook), (3.2, s_data), (4.4, s_trap), (4.6, s_fix), (3.8, s_rule), (3.2, sql_cta)]
    print(reel("reel_lag_fark", sc, D, seed=63))

if "stories" in which:
    story_greeting(D + "story_gunaydin.png", "gunaydin", "\"Sadece bir hobi\" diyen Linux",
                   "1991'de 21 yaşındaki üniversite öğrencisi Linus Torvalds, projesini \"sadece bir hobi, "
                   "GNU gibi büyük ve profesyonel olmayacak\" diye duyurdu.",
                   "Küçük başlangıçları küçümseme. Bugün 11:00 ve 18:00'de yeni Reels var.")
    story_poll(D + "story_1000_soru.png", "GÜNÜN SORUSU", "Bir önceki satırın değerini hangisi getirir?",
               ["LEAD()", "LAG()", "ROW_NUMBER()"],
               note="Cevabını DM'den yaz. Cevap 18:00 Reels'inde.")
    story_card(D + "story_1330_ilham_15dk.png", "İLHAM", "Günde [15 dakika] SQL", [
        "Pzt-Sal: SELECT, WHERE, ORDER BY",
        "Çar-Per: GROUP BY, HAVING, JOIN",
        "Cuma: LAG ve ROW_NUMBER gibi pencere fonksiyonları",
        "Hafta sonu: kendi tablonla 5 soru çöz",
    ], footer="Küçük ama her gün. Kaydet, pazartesi başla.", tag_col=YELLOW)
    story_card(D + "story_1400_google_kart.png", "YAPAY ZEKÂ", "Neler [belli], neler değil?", [
        "Kural ABD'deki okul öğrenci hesapları için.",
        "Değişiklik 2027'de devreye girecek.",
        "Google: Gemini ve Arama ayrı ayrı açılabilecek.",
        "Türkiye için bir açıklama yok.",
    ], footer="Kaynak: 9to5Google, Forbes, CBS News, TechCrunch (3-4 Kasım 2026)", tag_col=TEAL)
    story_card(D + "story_1600_hap_fotograflar.png", "HAP HABER", "Anılarda [müzik] kapanıyor", [
        "Google Fotoğraflar'da Anılar müziği kapatılabiliyor.",
        "Tek ayar, yıl sonu özetini de kapsıyor.",
        "Videoların kendi sesi çalmaya devam ediyor.",
    ], footer="Kademeli geliyor. Kaynak: 9to5Google, Android Headlines (4 Kasım 2026)", tag_col=PINK)
    story_card(D + "story_1700_duyuru.png", "18:00'DE", "Fark sorgusu [satır] kaybetti.", [
        "5 günlük satış vardı, sonuç 3 satır.",
        "Suçlu: takvimdeki bir boşluk.",
    ], footer="SQL Mülakat Sorusu #5. Cevap 18:00 Reels'inde.", tag_col=PINK)
    story_card(D + "story_2130_ozet.png", "GÜNÜN ÖZETİ", "Bugün ne [öğrendik]?", [
        "ABD'de okulda yapay zekâ kapanırsa Arama da kapanabilir.",
        "LAG önceki satırı, LEAD sonraki satırı getirir.",
        "Takvimde boşluk varsa JOIN ile fark satır kaybeder.",
    ], footer="Yarın yeni Reels var.")
    story_greeting(D + "story_iyigeceler.png", "iyigeceler", "176 emoji, 12x12 piksel",
                   "1999'da Shigetaka Kurita, NTT DoCoMo için 12x12 piksellik 176 emoji tasarladı. "
                   "Bu orijinal set 2016'da MoMA koleksiyonuna girdi.",
                   "Yarın yeni Reels var. İyi uykular.")
    print("stories ok")
