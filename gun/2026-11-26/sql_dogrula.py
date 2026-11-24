import sqlite3
c = sqlite3.connect(':memory:')
# Reels 26 Kasım 18:00: 30 Günde SQL · Gün 2/30 WHERE — '=' büyük/küçük harfe duyarlı (İzmir vs izmir)
c.executescript('''create table musteri(id int, ad text, sehir text);
insert into musteri values (1,'Ayşe','İzmir'),(2,'Mert','Ankara'),(3,'Zeynep','İzmir'),(4,'Can','Bursa');''')
print('26 tablo:', c.execute('select * from musteri').fetchall())
print('26 YANLIS:', c.execute("""SELECT ad FROM musteri
WHERE sehir = 'izmir';""").fetchall())
print('26 DOGRU:', c.execute("""SELECT ad FROM musteri
WHERE sehir = 'İzmir';""").fetchall())
print('26 yorum sorusu (<> İzmir):', c.execute("SELECT ad FROM musteri WHERE sehir <> 'İzmir';").fetchall())
print('26 LOWER Türkçe İ (önerilmez):', c.execute("SELECT LOWER('İzmir')").fetchall())
# Anket 26
cur = c.execute("SELECT ad AS isim FROM musteri;"); print('ANKET26 sütun adı:', [d[0] for d in cur.description])
print('MINI26 SELECT * sütun sayısı:', len(c.execute("SELECT * FROM musteri").description))
