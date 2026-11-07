import sqlite3
c = sqlite3.connect(":memory:")
c.executescript("""
CREATE TABLE siparisler(id INT, tutar INT);
INSERT INTO siparisler VALUES (1,300),(2,1500),(3,5000);
""")
q1 = """SELECT id, tutar,
  CASE WHEN tutar > 1000 THEN 'orta'
       WHEN tutar > 4000 THEN 'büyük'
       ELSE 'küçük' END AS segment
FROM siparisler;"""
q2 = """SELECT id, tutar,
  CASE WHEN tutar > 4000 THEN 'büyük'
       WHEN tutar > 1000 THEN 'orta'
       ELSE 'küçük' END AS segment
FROM siparisler;"""
print("YANLIS:", c.execute(q1).fetchall())
print("DOGRU:", c.execute(q2).fetchall())
