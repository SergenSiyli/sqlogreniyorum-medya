import sqlite3
c = sqlite3.connect(':memory:')
# Reels 29 Kasım 18:00: 30 Günde SQL · Gün 6/30 AND / OR — AND, OR'dan önce çalışır
c.executescript('''create table urunler(urun text, kategori text, stok int);
insert into urunler values ('Telefon Pro','Telefon',4),('Telefon Mini','Telefon',0),('Telefon Lite','Telefon',0),
('Tablet 11','Tablet',3),('Tablet 8','Tablet',0),('Kulaklık X','Kulaklık',7);''')
print('tablo:', c.execute('select * from urunler').fetchall())
print('EKRAN YANLIS:', c.execute("SELECT urun, stok FROM urunler\nWHERE kategori = 'Telefon'\n   OR kategori = 'Tablet'\n  AND stok > 0;").fetchall())
print('EKRAN DOGRU:', c.execute("SELECT urun, stok FROM urunler\nWHERE (kategori = 'Telefon'\n    OR kategori = 'Tablet')\n  AND stok > 0;").fetchall())
print('EKRAN YORUM:', c.execute("SELECT COUNT(*) FROM urunler WHERE kategori = 'Tablet' OR kategori = 'Telefon' AND stok > 0;").fetchall())
print('GUNAYDIN ||:', c.execute("SELECT 'a' || 'b'").fetchall())
print('ANKET 1 OR 0 AND 0:', c.execute("SELECT 1 OR 0 AND 0").fetchall())
