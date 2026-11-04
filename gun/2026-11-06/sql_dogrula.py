import sqlite3
c=sqlite3.connect(":memory:")
c.executescript("""CREATE TABLE satis(gun TEXT, adet INT);
INSERT INTO satis VALUES ('2026-11-01',40),('2026-11-02',55),('2026-11-03',50),('2026-11-05',70),('2026-11-06',65);""")
q={"selfjoin":"""SELECT b.gun, b.adet - a.adet AS fark FROM satis a JOIN satis b ON b.gun = DATE(a.gun, '+1 day') ORDER BY b.gun;""",
"lag":"""SELECT gun, adet, adet - LAG(adet) OVER (ORDER BY gun) AS fark FROM satis ORDER BY gun;""",
"lead":"""SELECT gun, LEAD(adet) OVER (ORDER BY gun) AS sonraki FROM satis ORDER BY gun;"""}
for k,s in q.items(): print(k, c.execute(s).fetchall())
