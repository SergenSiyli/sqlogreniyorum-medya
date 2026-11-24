import sqlite3
c = sqlite3.connect(':memory:')
# Reels 26 Kasım 18:00: 30 Günde SQL · Gün 3/30 ORDER BY — fiyat metin (TEXT) sütunda, sıralama harf harf
c.executescript('''create table urun(id int, ad text, fiyat text);
insert into urun values (1,'Kulaklık','900'),(2,'Klavye','450'),(3,'Monitör','1250'),(4,'Mouse','250');''')
print('tablo:', c.execute('select * from urun').fetchall())
print('YANLIS:', c.execute("""SELECT ad, fiyat FROM urun
ORDER BY fiyat DESC;""").fetchall())
print('DOGRU:', c.execute("""SELECT ad, fiyat FROM urun
ORDER BY CAST(fiyat AS INTEGER) DESC;""").fetchall())
print('ASC varsayilan:', c.execute("SELECT ad FROM urun ORDER BY CAST(fiyat AS INTEGER);").fetchall())
print("'1250' < '900':", c.execute("select '1250' < '900'").fetchall())
# yorum sorusu: sayısal sütunlu tabloda ORDER BY fiyat (DESC yok) → ilk satır
c.executescript('''create table urun2(ad text, fiyat int);
insert into urun2 values ('Kulaklık',900),('Klavye',450),('Monitör',1250),('Mouse',250);''')
print('YORUM (ORDER BY fiyat) ilk:', c.execute("SELECT ad FROM urun2 ORDER BY fiyat;").fetchall()[0])
# Ekrandaki kodun birebiri
print('EKRAN YANLIS:', c.execute("SELECT ad, fiyat FROM urun\nORDER BY fiyat DESC;").fetchall())
print('EKRAN DOGRU:', c.execute("SELECT ad, fiyat FROM urun\nORDER BY CAST(fiyat\n  AS INTEGER) DESC;").fetchall())
print('EKRAN YORUM:', c.execute("SELECT ad FROM urun\nORDER BY CAST(fiyat\n  AS INTEGER);").fetchall())
