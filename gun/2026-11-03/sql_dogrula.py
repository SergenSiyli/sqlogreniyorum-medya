import sqlite3
c = sqlite3.connect(":memory:")
c.executescript("""
CREATE TABLE musteriler(id INTEGER PRIMARY KEY, ad TEXT);
INSERT INTO musteriler VALUES (1,'Ali'),(2,'Ayse'),(3,'Can'),(4,'Ece');
CREATE TABLE siparisler(id INTEGER PRIMARY KEY, musteri_id INT, durum TEXT);
INSERT INTO siparisler VALUES (101,1,'teslim'),(102,2,'iptal'),(103,3,'teslim');
""")
for q in ["SELECT m.ad, s.durum FROM musteriler m LEFT JOIN siparisler s ON s.musteri_id = m.id;",
          "SELECT m.ad, s.durum FROM musteriler m LEFT JOIN siparisler s ON s.musteri_id = m.id WHERE s.durum = 'teslim';",
          "SELECT m.ad, s.durum FROM musteriler m LEFT JOIN siparisler s ON s.musteri_id = m.id AND s.durum = 'teslim';"]:
    print(q); print(c.execute(q).fetchall())
