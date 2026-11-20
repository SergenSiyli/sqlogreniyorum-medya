import sqlite3
c = sqlite3.connect(':memory:')
c.executescript('''create table siparis(id int, iade int);
insert into siparis values(1,0),(2,1),(3,0),(4,0),(5,1),(6,0),(7,0),(8,0);''')
# Reels: Eleyen Soru #2 tam sayı bölmesi (8 sipariş, 2 iade)
print('Beklenen: 2/8 = %', 2/8*100)
print('Yanlış:', c.execute('''SELECT SUM(iade) / COUNT(*)
  * 100
FROM siparis;''').fetchall())
print('Ara adım SUM(iade)/COUNT(*):', c.execute('SELECT SUM(iade) / COUNT(*) FROM siparis').fetchall())
print('Doğru:', c.execute('''SELECT SUM(iade) * 100.0
  / COUNT(*)
FROM siparis;''').fetchall())
# Anket: 4 satırlı tabloda LIMIT 3 OFFSET 2
c.executescript("create table urun(ad text); insert into urun values('a'),('b'),('c'),('d');")
r = c.execute("SELECT ad FROM urun ORDER BY ad LIMIT 3 OFFSET 2").fetchall()
print('ANKET LIMIT 3 OFFSET 2:', r, '->', len(r), 'satır')
