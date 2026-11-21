import sqlite3
c = sqlite3.connect(':memory:')
# Reels 22 Kasım (yeniden, koyu): SQL Mülakat Sorusu #11 tam sayı bölmesi
c.executescript('''create table siparis(id int, iade int);
insert into siparis values(1,0),(2,1),(3,0),(4,0),(5,1),(6,0),(7,0),(8,0);''')
print('22 tablo:', c.execute('select * from siparis').fetchall())
print('22 YANLIS:', c.execute('SELECT SUM(iade) / COUNT(*) * 100 FROM siparis;').fetchall())
print('22 ara SUM, COUNT, bolum:', c.execute('SELECT SUM(iade), COUNT(*), SUM(iade)/COUNT(*) FROM siparis').fetchall())
print('22 DOGRU:', c.execute('SELECT SUM(iade) * 100.0 / COUNT(*) FROM siparis;').fetchall())
# Ekrandaki kodun birebiri
print('EKRAN YANLIS:', c.execute('''SELECT SUM(iade) / COUNT(*)
  * 100 AS iade_orani
FROM siparis;''').fetchall())
print('EKRAN DOGRU:', c.execute('''SELECT SUM(iade) * 100.0
  / COUNT(*) AS iade_orani
FROM siparis;''').fetchall())
