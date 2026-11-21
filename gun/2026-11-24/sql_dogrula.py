import sqlite3
c = sqlite3.connect(':memory:')
# Reels 24 Kasım: SQL Mülakat Sorusu #13 LIMIT eşitlik / DENSE_RANK
c.executescript('''create table satici(ad text, satis int);
insert into satici values('Ali',90),('Ayşe',70),('Can',80),('Deniz',70),('Ece',60);''')
print('24 tablo:', c.execute('select * from satici').fetchall())
print('24 YANLIS:', c.execute('''SELECT ad, satis
FROM satici
ORDER BY satis DESC
LIMIT 3;''').fetchall())
print('24 DOGRU:', c.execute('''SELECT ad, satis FROM (
  SELECT ad, satis,
    DENSE_RANK() OVER (
      ORDER BY satis DESC) AS sira
  FROM satici) t
WHERE sira <= 3;''').fetchall())
print('24 siralar:', c.execute('SELECT ad, satis, DENSE_RANK() OVER (ORDER BY satis DESC), RANK() OVER (ORDER BY satis DESC) FROM satici').fetchall())
# Anket 24: COUNT(DISTINCT)
c.executescript("create table urun(renk text); insert into urun values('mavi'),('mavi'),(NULL),('kırmızı');")
print('ANKET24 COUNT(DISTINCT renk):', c.execute('SELECT COUNT(DISTINCT renk) FROM urun;').fetchall())
c.executescript("create table satici2 as select * from satici;")
print('EKRAN DOGRU:', c.execute('''SELECT ad, satis FROM (
  SELECT ad, satis,
    DENSE_RANK() OVER (
      ORDER BY satis DESC)
      AS sira
  FROM satici) t
WHERE sira <= 3;''').fetchall())
