import sqlite3
c = sqlite3.connect(':memory:')
# Reels 28 Kasım 18:00: 30 Günde SQL · Gün 5/30 DISTINCT — DISTINCT tek sütuna değil tüm satıra bakar
c.executescript('''create table siparis(id int, musteri text, sehir text);
insert into siparis values (1,'Ayşe','İstanbul'),(2,'Mert','Ankara'),(3,'Can','İstanbul'),(4,'Ayşe','İstanbul'),(5,'Ece','İzmir'),(6,'Deniz','İstanbul');''')
print('tablo:', c.execute('select * from siparis').fetchall())
print('EKRAN YANLIS:', c.execute("SELECT DISTINCT sehir, musteri\nFROM siparis;").fetchall())
print('EKRAN DOGRU:', c.execute("SELECT DISTINCT sehir\nFROM siparis;").fetchall())
print('EKRAN YORUM:', c.execute("SELECT COUNT(DISTINCT musteri) FROM siparis;").fetchall())
print('GUNAYDIN NULL=NULL:', c.execute("SELECT NULL = NULL").fetchall())
print('ANKET COALESCE:', c.execute("SELECT COALESCE(NULL, 0, 5)").fetchall())
