import sqlite3
c=sqlite3.connect(":memory:")
c.executescript("""CREATE TABLE kayitlar(id INT, ad TEXT, email TEXT);
INSERT INTO kayitlar VALUES (1,'Ali','ali@x.com'),(2,'Ayse','ayse@x.com'),(3,'Ali','ali@x.com'),(4,'Can','can@x.com'),(5,'Ayse','ayse@x.com'),(6,'Ali','ali@x.com');""")
q={"distinct":"SELECT DISTINCT * FROM kayitlar;",
"count_distinct":"SELECT COUNT(*) FROM (SELECT DISTINCT * FROM kayitlar);",
"rn":"""SELECT id, ad, ROW_NUMBER() OVER (PARTITION BY email ORDER BY id) AS rn FROM kayitlar ORDER BY email, id;""",
"tekrar":"""WITH t AS (SELECT id, ROW_NUMBER() OVER (PARTITION BY email ORDER BY id) AS rn FROM kayitlar) SELECT id FROM t WHERE rn > 1 ORDER BY id;"""}
for k,s in q.items(): print(k, c.execute(s).fetchall())
c.execute("DELETE FROM kayitlar WHERE id IN (SELECT id FROM (SELECT id, ROW_NUMBER() OVER (PARTITION BY email ORDER BY id) AS rn FROM kayitlar) WHERE rn > 1);")
print("sonra", c.execute("SELECT * FROM kayitlar ORDER BY id").fetchall())
