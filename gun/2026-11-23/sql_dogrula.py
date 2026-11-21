import sqlite3
c = sqlite3.connect(':memory:')
# Reels 23 Kasım: SQL Mülakat Sorusu #12 LAG PARTITION BY'sız
c.executescript('''create table satis(sube text, gun text, ciro int);
insert into satis values('Beşiktaş','01.11',500),('Beşiktaş','02.11',650),('Beşiktaş','03.11',600),
('Kadıköy','01.11',900),('Kadıköy','02.11',950),('Kadıköy','03.11',1000);''')
print('23 tablo:', c.execute('select * from satis').fetchall())
print('23 YANLIS:', c.execute('''SELECT sube, gun, ciro,
  ciro - LAG(ciro) OVER (
    ORDER BY sube, gun) AS fark
FROM satis;''').fetchall())
print('23 DOGRU:', c.execute('''SELECT sube, gun, ciro,
  ciro - LAG(ciro) OVER (
    PARTITION BY sube
    ORDER BY gun) AS fark
FROM satis;''').fetchall())
# Anket 23: COALESCE
print('ANKET23 COALESCE(NULL,0,5):', c.execute('SELECT COALESCE(NULL, 0, 5);').fetchall())
# Ekrandaki kodun birebiri
print('EKRAN YANLIS:', c.execute('''SELECT sube, gun,
  ciro - LAG(ciro) OVER (
    ORDER BY sube, gun) AS fark
FROM satis;''').fetchall())
print('EKRAN DOGRU:', c.execute('''SELECT sube, gun,
  ciro - LAG(ciro) OVER (
    PARTITION BY sube
    ORDER BY gun) AS fark
FROM satis;''').fetchall())
