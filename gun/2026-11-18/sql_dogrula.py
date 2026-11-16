import sqlite3
c = sqlite3.connect(':memory:')
c.executescript('''create table musteri(id int, ad text);insert into musteri values(1,'Ali'),(2,'Ayşe'),(3,'Can');
create table siparis(id int, musteri_id int, tutar int);insert into siparis values(1,1,100),(2,1,250),(3,1,80),(4,2,300);''')
r = c.execute('''SELECT m.ad, s.tutar
FROM musteri m
JOIN siparis s
  ON s.musteri_id = m.id;''').fetchall()
print(len(r), r)  # 4 satır: Ali x3, Ayşe x1, Can yok
