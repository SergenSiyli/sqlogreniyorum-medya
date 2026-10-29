"""İlk haftanın tüm SQL örneklerini SQLite'ta çalıştırıp sonuçları yazdırır."""
import sqlite3

db = sqlite3.connect(":memory:")
c = db.cursor()
c.executescript("""
CREATE TABLE ogrenciler (id INTEGER, ad TEXT);
INSERT INTO ogrenciler VALUES (1,'Ayşe'),(2,'Mehmet'),(3,'Zeynep');
CREATE TABLE kayitlar (ogrenci_id INTEGER, kurs TEXT);
INSERT INTO kayitlar VALUES (1,'SQL'),(1,'Python'),(2,'SQL'),(4,'Excel');

CREATE TABLE puanlar (ad TEXT, puan INTEGER);
INSERT INTO puanlar VALUES ('Ali',95),('Ece',90),('Can',90),('Deniz',85);

CREATE TABLE urunler (kategori TEXT, urun TEXT, satis INTEGER);
INSERT INTO urunler VALUES
 ('Kitap','Roman',120),('Kitap','Sözlük',40),('Kitap','Atlas',75),('Kitap','Dergi',90),
 ('Oyun','Satranç',60),('Oyun','Puzzle',85),('Oyun','Kart',30),('Oyun','Zeka',70);

CREATE TABLE musteriler (id INTEGER, ad TEXT, telefon TEXT);
INSERT INTO musteriler VALUES (1,'Ada','555-01'),(2,'Bora',NULL),(3,'Cem','555-03'),
 (4,'Duru',NULL),(5,'Efe','555-05');

CREATE TABLE calisanlar (ad TEXT, bolum TEXT, maas INTEGER);
INSERT INTO calisanlar VALUES
 ('A','Satış',35000),('B','Satış',42000),('C','Satış',31000),('D','Satış',25000),
 ('E','IT',55000),('F','IT',48000),('G','IT',29000),
 ('H','İK',33000),('I','İK',36000);
""")

Q = {
 "INNER": "SELECT o.ad, k.kurs FROM ogrenciler o INNER JOIN kayitlar k ON o.id = k.ogrenci_id",
 "LEFT": "SELECT o.ad, k.kurs FROM ogrenciler o LEFT JOIN kayitlar k ON o.id = k.ogrenci_id",
 "RIGHT": "SELECT o.ad, k.kurs FROM ogrenciler o RIGHT JOIN kayitlar k ON o.id = k.ogrenci_id",
 "FULL": "SELECT o.ad, k.kurs FROM ogrenciler o FULL OUTER JOIN kayitlar k ON o.id = k.ogrenci_id",
 "ANTI": "SELECT o.ad FROM ogrenciler o LEFT JOIN kayitlar k ON o.id = k.ogrenci_id WHERE k.ogrenci_id IS NULL",
 "RANK": """SELECT ad, puan,
   ROW_NUMBER() OVER (ORDER BY puan DESC, ad) AS rn,
   RANK()       OVER (ORDER BY puan DESC) AS rnk,
   DENSE_RANK() OVER (ORDER BY puan DESC) AS drnk
 FROM puanlar ORDER BY puan DESC, ad""",
 "TOP2": """WITH sirali AS (
   SELECT kategori, urun, satis,
     ROW_NUMBER() OVER (PARTITION BY kategori ORDER BY satis DESC) AS sira
   FROM urunler)
 SELECT kategori, urun, satis FROM sirali WHERE sira <= 2""",
 "COUNT": "SELECT COUNT(*), COUNT(telefon) FROM musteriler",
 "ORDER": """SELECT bolum, COUNT(*) AS kisi FROM calisanlar WHERE maas > 30000
   GROUP BY bolum HAVING COUNT(*) >= 2 ORDER BY kisi DESC""",
 "WHERE": "SELECT ad, bolum, maas FROM calisanlar WHERE maas > 40000",
 "HAVING": "SELECT bolum, AVG(maas) AS ort FROM calisanlar GROUP BY bolum HAVING AVG(maas) > 35000",
 "BOTH": """SELECT bolum, COUNT(*) AS kisi FROM calisanlar WHERE maas > 30000
   GROUP BY bolum HAVING COUNT(*) >= 2""",
}
for k, q in Q.items():
    print(f"--- {k}")
    for r in c.execute(q).fetchall():
        print("   ", r)
