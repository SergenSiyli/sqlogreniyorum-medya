import sqlite3
c = sqlite3.connect(':memory:')
# Reels 27 Kasım 18:00: 30 Günde SQL · Gün 4/30 LIMIT — ORDER BY'sız LIMIT "ilk 3"ü değil, rastgele/eklenme sırasını verir
c.executescript('''create table kirtasiye(id int, ad text, satis int);
insert into kirtasiye values (1,'Defter',120),(2,'Kalem',340),(3,'Silgi',45),(4,'Çanta',510),(5,'Cetvel',80);''')
print('tablo:', c.execute('select * from kirtasiye').fetchall())
print('EKRAN YANLIS:', c.execute("SELECT ad, satis FROM kirtasiye\nLIMIT 3;").fetchall())
print('EKRAN DOGRU:', c.execute("SELECT ad, satis FROM kirtasiye\nORDER BY satis DESC\nLIMIT 3;").fetchall())
print('EKRAN YORUM:', c.execute("SELECT ad FROM kirtasiye\nORDER BY satis\nLIMIT 1;").fetchall())
