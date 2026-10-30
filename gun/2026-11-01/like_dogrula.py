import sqlite3
c = sqlite3.connect(':memory:')
c.execute('create table kullanicilar(id int, kullanici_adi text)')
c.executemany('insert into kullanicilar values(?,?)', [(1,'ali_veli'),(2,'alixveli'),(3,'aliveli'),(4,'ali.veli')])
for q in ["SELECT kullanici_adi FROM kullanicilar WHERE kullanici_adi LIKE 'ali_veli'",
          "SELECT kullanici_adi FROM kullanicilar WHERE kullanici_adi LIKE 'ali!_veli' ESCAPE '!'",
          "SELECT kullanici_adi FROM kullanicilar WHERE kullanici_adi LIKE 'ali%veli'"]:
    print(q, '->', [r[0] for r in c.execute(q)])
