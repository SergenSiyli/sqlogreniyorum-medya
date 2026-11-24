import sqlite3
c = sqlite3.connect(':memory:')
# Reels 26 Kasım: 30 Günde SQL · Gün 1/30 SELECT — tek tırnaklı sütun adı tuzağı
c.executescript('''create table musteri(id int, ad text, sehir text);
insert into musteri values (1,'Ayşe','İzmir'),(2,'Mert','Ankara'),(3,'Zeynep','Bursa'),(4,'Can','Antalya');''')
print('26 tablo:', c.execute('select * from musteri').fetchall())
print('26 YANLIS:', c.execute("""SELECT 'ad'
FROM musteri;""").fetchall())
print('26 DOGRU:', c.execute("""SELECT ad
FROM musteri;""").fetchall())
print('26 cift tirnak:', c.execute('SELECT "ad" FROM musteri;').fetchall())
print('26 yorum sorusu:', c.execute("SELECT 'merhaba' FROM musteri;").fetchall())
# Anket 26: SELECT 2 + 3; ne döner
print('ANKET26:', c.execute("SELECT 2 + 3;").fetchall(), c.execute("SELECT '2' || '3';").fetchall())
# Günaydın mini soru 26: SELECT * kaç sütun getirir (musteri 3 sütun)
print('MINI26:', len(c.execute("SELECT * FROM musteri").description))
