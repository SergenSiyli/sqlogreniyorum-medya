import sqlite3
c=sqlite3.connect(":memory:")
c.executescript("""CREATE TABLE musteri(id INT, ad TEXT);
INSERT INTO musteri VALUES (1,'Ali'),(2,'Ayşe'),(3,'Can'),(4,'Deniz');
CREATE TABLE siparis(id INT, musteri_id INT);
INSERT INTO siparis VALUES (10,1),(11,3),(12,NULL);""")
q={"not_in":"SELECT ad FROM musteri WHERE id NOT IN (SELECT musteri_id FROM siparis);",
"not_exists":"SELECT ad FROM musteri m WHERE NOT EXISTS (SELECT 1 FROM siparis s WHERE s.musteri_id = m.id);",
"in":"SELECT ad FROM musteri WHERE id IN (SELECT musteri_id FROM siparis);",
"not_in_null_filtre":"SELECT ad FROM musteri WHERE id NOT IN (SELECT musteri_id FROM siparis WHERE musteri_id IS NOT NULL);",
"2_not_in_null":"SELECT 2 NOT IN (1,3,NULL);"}
for k,s in q.items(): print(k, c.execute(s).fetchall())
