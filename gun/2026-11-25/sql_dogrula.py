import sqlite3
c = sqlite3.connect(':memory:')
# Reels 25 Kasım: SQL Mülakat Sorusu #14 ay sonu tarih tuzağı
c.executescript('''create table siparis(id int, tarih text, tutar int);
insert into siparis values
(1,'2026-11-03 10:15',1200),(2,'2026-11-17 09:40',800),(3,'2026-11-29 16:05',500),
(4,'2026-11-30 11:30',700),(5,'2026-11-30 19:45',900),(6,'2026-12-01 08:10',400);''')
print('25 tablo:', c.execute('select * from siparis').fetchall())
print('25 YANLIS:', c.execute('''SELECT SUM(tutar)
FROM siparis
WHERE tarih >= '2026-11-01'
  AND tarih <= '2026-11-30';''').fetchall())
print('25 YANLIS satirlar:', c.execute("SELECT id FROM siparis WHERE tarih >= '2026-11-01' AND tarih <= '2026-11-30'").fetchall())
print('25 DOGRU:', c.execute('''SELECT SUM(tutar)
FROM siparis
WHERE tarih >= '2026-11-01'
  AND tarih < '2026-12-01';''').fetchall())
print("25 karsilastirma:", c.execute("SELECT '2026-11-30 11:30' <= '2026-11-30', '2026-11-30' <= '2026-11-30'").fetchall())
# Anket 25
print('ANKET25 DATE:', c.execute("SELECT DATE('2026-11-30 19:45');").fetchall())
# Günaydın mini soru: NULL + 5 / COALESCE(NULL, 5)
print('MINI25:', c.execute("SELECT NULL + 5, COALESCE(NULL, 5);").fetchall())
# Karusel NULL kopya kâğıdı
c.executescript("""create table calisan(ad text, prim int);
insert into calisan values('Ali',100),('Ayşe',NULL),('Can',300),('Ece',NULL);""")
q = {
 'K1 = NULL': "SELECT COUNT(*) FROM calisan WHERE prim = NULL;",
 'K1 IS NULL': "SELECT ad FROM calisan WHERE prim IS NULL;",
 'K2 count': "SELECT COUNT(*), COUNT(prim) FROM calisan;",
 'K3 avg': "SELECT AVG(prim), SUM(prim) FROM calisan;",
 'K3 avg coalesce': "SELECT AVG(COALESCE(prim, 0)) FROM calisan;",
 'K4 arit': "SELECT ad, prim + 50 FROM calisan;",
 'K4 coalesce': "SELECT ad, COALESCE(prim, 0) + 50 FROM calisan;",
 'K5 not in': "SELECT COUNT(*) FROM calisan WHERE prim NOT IN (100, NULL);",
 'K5 <>': "SELECT ad FROM calisan WHERE prim <> 100;",
}
for k, s in q.items(): print(k, c.execute(s).fetchall())
print('25 BETWEEN:', c.execute("SELECT SUM(tutar) FROM siparis WHERE tarih BETWEEN '2026-11-01' AND '2026-11-30';").fetchall())
# Karusel ekranındaki sorgular birebir
for s in ["SELECT ad FROM calisan\nWHERE prim = NULL;", "SELECT ad FROM calisan WHERE prim IS NULL;",
          "SELECT COUNT(*),\n       COUNT(prim)\nFROM calisan;", "SELECT AVG(prim)\nFROM calisan;",
          "SELECT AVG(COALESCE(prim, 0)) FROM calisan;", "SELECT prim + 50 FROM calisan;",
          "SELECT COALESCE(prim, 0) + 50 FROM calisan;", "SELECT ad FROM calisan\nWHERE prim NOT IN (100, NULL);",
          "SELECT ad FROM calisan\nWHERE prim <> 100;"]:
    print('KARUSEL', s.replace("\n"," "), c.execute(s).fetchall())
