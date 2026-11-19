import sqlite3
c = sqlite3.connect(':memory:')
c.executescript('''create table siparis(urun text, fiyat int, kargo int);
insert into siparis values('A',400,50),('B',300,NULL),('C',200,50);''')
# Reels: SQL TEST #11 SUM(fiyat + kargo) ve NULL
print('Beklenen (fiyat+kargo, NULL kargo 0):', 400+50+300+200+50)
print('Yanlış:', c.execute('''SELECT SUM(fiyat + kargo)
FROM siparis;''').fetchall())
print('B satırı:', c.execute("SELECT fiyat + kargo FROM siparis WHERE urun='B'").fetchall())
print('Doğru:', c.execute('''SELECT SUM(fiyat
  + COALESCE(kargo, 0))
FROM siparis;''').fetchall())
# Anket: GROUP BY ve NULL
c.executescript("create table k(sehir text); insert into k values('Ankara'),(NULL),(NULL),('İzmir');")
r = c.execute("SELECT sehir, COUNT(*) FROM k GROUP BY sehir").fetchall()
print('ANKET GROUP BY:', r, '->', len(r), 'satır')
# Günaydın mini soru: NULL = NULL
print('NULL = NULL:', c.execute("SELECT NULL = NULL").fetchall())
