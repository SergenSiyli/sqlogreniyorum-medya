import sqlite3
c = sqlite3.connect(':memory:')
c.executescript('''create table sinav(ogrenci text, puan int);
insert into sinav values('Ali',100),('Ayşe',80),('Can',NULL),('Deniz',NULL);''')
q = '''SELECT AVG(puan)
FROM sinav;'''
print('AVG:', c.execute(q).fetchall())          # 90.0
q2 = '''SELECT AVG(COALESCE(puan, 0))
FROM sinav;'''
print('COALESCE:', c.execute(q2).fetchall())   # 45.0
print('SUM/COUNT(*):', c.execute('select sum(puan), count(*), count(puan) from sinav').fetchall())
