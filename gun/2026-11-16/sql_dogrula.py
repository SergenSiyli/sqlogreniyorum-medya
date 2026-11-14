import sqlite3
c=sqlite3.connect(':memory:')
c.executescript("""
CREATE TABLE siparis(id INTEGER, sehir TEXT, tutar INTEGER);
INSERT INTO siparis VALUES (1,'Ankara',50),(2,'Ankara',300),(3,'İzmir',80),(4,'İzmir',250),(5,'Bursa',400);
CREATE TABLE musteri(id INTEGER, ad TEXT);
INSERT INTO musteri VALUES (1,'Ali'),(2,'Ayşe'),(3,'Can');
""")
q1="""SELECT id FROM siparis
WHERE sehir = 'Ankara'
   OR sehir = 'İzmir'
  AND tutar > 100;"""
print('Q1',c.execute(q1).fetchall())
q1b="""SELECT id FROM siparis
WHERE (sehir = 'Ankara'
    OR sehir = 'İzmir')
  AND tutar > 100;"""
print('Q1 düzeltilmiş',c.execute(q1b).fetchall())
q1c="""SELECT id FROM siparis
WHERE sehir IN ('Ankara', 'İzmir')
  AND tutar > 100;"""
print('Q1 IN',c.execute(q1c).fetchall())
q2="""SELECT m.ad, COUNT(*) AS adet
FROM musteri m
LEFT JOIN siparis s
  ON s.musteri_id = m.id
GROUP BY m.ad;"""
c2=sqlite3.connect(':memory:')
c2.executescript("CREATE TABLE musteri(id INTEGER, ad TEXT); INSERT INTO musteri VALUES (1,'Ali'),(2,'Ayşe'),(3,'Can'); CREATE TABLE siparis(id INTEGER, musteri_id INTEGER); INSERT INTO siparis VALUES (1,1),(2,1),(3,2);")
print('Q2',c2.execute(q2).fetchall())
q2b=q2.replace('COUNT(*)','COUNT(s.id)')
print('Q2 düzeltilmiş',c2.execute(q2b).fetchall())
