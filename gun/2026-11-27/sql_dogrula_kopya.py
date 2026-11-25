import sqlite3
c = sqlite3.connect(':memory:')
# Karusel 27 Kasım 12:30: SQL Kopya Kâğıdı #3 — sorgu çalışma sırası
c.executescript('''create table siparis(id int, sehir text, tutar int);
insert into siparis values (1,'Ankara',300),(2,'İzmir',80),(3,'Ankara',150),(4,'Bursa',500),(5,'İzmir',60),(6,'Ankara',40);''')
print('tablo:', c.execute('select * from siparis').fetchall())
try: print(c.execute("SELECT sehir FROM siparis\nWHERE COUNT(*) > 1\nGROUP BY sehir;").fetchall())
except Exception as e: print('K1 HATA:', e)
print('K1 DOGRU:', c.execute("SELECT sehir, COUNT(*)\nFROM siparis\nGROUP BY sehir\nHAVING COUNT(*) > 1;").fetchall())
print('K2 WHERE once:', c.execute("SELECT sehir, COUNT(*)\nFROM siparis\nWHERE tutar > 100\nGROUP BY sehir;").fetchall())
print('K3 ORDER BY takma ad:', c.execute("SELECT sehir, SUM(tutar) AS ciro\nFROM siparis\nGROUP BY sehir\nORDER BY ciro DESC;").fetchall())
print('K4 LIMIT en son:', c.execute("SELECT sehir, SUM(tutar) AS ciro\nFROM siparis\nGROUP BY sehir\nORDER BY ciro DESC\nLIMIT 1;").fetchall())
print('anket LENGTH:', c.execute("SELECT LENGTH('SQL ');").fetchall())
print('gunaydin COUNT bos:', c.execute("create table bos(x int)").fetchall(), c.execute("SELECT COUNT(*), SUM(x) FROM bos").fetchall())
