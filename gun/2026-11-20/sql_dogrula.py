import sqlite3
c = sqlite3.connect(':memory:')
c.executescript('''create table musteri(id int, ad text);
insert into musteri values(1,'Ali'),(2,'Ayşe'),(3,'Can'),(4,'Deniz');
create table siparis(id int, musteri_id int);
insert into siparis values(1,1),(2,2),(3,NULL);''')
# Reels: Eleyen Soru #1 NOT IN + NULL
q = '''SELECT ad FROM musteri
WHERE id NOT IN (
  SELECT musteri_id
  FROM siparis);'''
print('NOT IN:', c.execute(q).fetchall())  # []
q2 = '''SELECT ad FROM musteri m
WHERE NOT EXISTS (
  SELECT 1 FROM siparis s
  WHERE s.musteri_id = m.id);'''
print('NOT EXISTS:', c.execute(q2).fetchall())  # Can, Deniz
# Karusel: 5 soru
c.executescript('''create table s(musteri text, tutar int);
insert into s values('Ali',300),('Ali',250),('Ayşe',200),('Can',600);
create table m2(sehir text); insert into m2 values('Ankara'),('İzmir'),('Ankara'),(NULL);
create table a(x int); insert into a values(1),(2),(2);
create table b(x int); insert into b values(2),(3);
create table c(ad text, maas int); insert into c values('Ece',9000),('Mert',7000),('Selin',7000),('Tuna',5000);''')
print('S1 HAVING:', c.execute("SELECT musteri FROM s GROUP BY musteri HAVING SUM(tutar) > 500").fetchall())
try: c.execute("SELECT musteri FROM s WHERE SUM(tutar) > 500 GROUP BY musteri").fetchall()
except Exception as e: print('S1 WHERE hata:', e)
print('S2 COUNT DISTINCT:', c.execute("SELECT COUNT(DISTINCT sehir) FROM m2").fetchall())
print('S3 UNION:', c.execute("SELECT x FROM a UNION SELECT x FROM b").fetchall(), 'ALL:', len(c.execute("SELECT x FROM a UNION ALL SELECT x FROM b").fetchall()))
print('S5 OFFSET:', c.execute("SELECT ad, maas FROM c ORDER BY maas DESC LIMIT 1 OFFSET 1").fetchall())
# Anket story: <> ve NULL
c.executescript("create table k(sehir text); insert into k values('Ankara'),('İzmir'),(NULL);")
print('ANKET:', c.execute("SELECT COUNT(*) FROM k WHERE sehir <> 'Ankara'").fetchall())
