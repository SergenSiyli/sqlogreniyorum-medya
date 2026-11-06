import sqlite3
c = sqlite3.connect(":memory:")
c.executescript("""
CREATE TABLE ekim(musteri TEXT, tutar INT);
CREATE TABLE kasim(musteri TEXT, tutar INT);
INSERT INTO ekim VALUES ('Ali',100),('Ayşe',200),('Can',150);
INSERT INTO kasim VALUES ('Ali',100),('Deniz',300),('Can',150);
""")
q1 = """SELECT SUM(tutar) FROM (
  SELECT musteri, tutar FROM ekim
  UNION
  SELECT musteri, tutar FROM kasim);"""
q2 = q1.replace("UNION\n", "UNION ALL\n")
print("UNION toplam:", c.execute(q1).fetchall())
print("UNION ALL toplam:", c.execute(q2).fetchall())
print("UNION satirlar:", c.execute("SELECT musteri, tutar FROM ekim UNION SELECT musteri, tutar FROM kasim").fetchall())
print("UNION ALL sayi:", c.execute("SELECT COUNT(*) FROM (SELECT musteri, tutar FROM ekim UNION ALL SELECT musteri, tutar FROM kasim)").fetchall())
