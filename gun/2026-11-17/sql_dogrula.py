import sqlite3
c=sqlite3.connect(':memory:')
c.executescript("""
CREATE TABLE musteri(id INTEGER, ad TEXT, telefon TEXT);
INSERT INTO musteri VALUES (1,'Ali','0532'),(2,'Ayşe',NULL),(3,'Can','0544'),(4,'Deniz',NULL),(5,'Ece','0505');
""")
q1="""SELECT ad FROM musteri
WHERE telefon = NULL;"""
print('Q1 = NULL',c.execute(q1).fetchall())
q2="""SELECT ad FROM musteri
WHERE telefon IS NULL;"""
print('Q2 IS NULL',c.execute(q2).fetchall())
print('NULL = NULL ->',c.execute("SELECT NULL = NULL").fetchall())
print('<> NULL',c.execute("SELECT ad FROM musteri WHERE telefon <> NULL").fetchall())
print('IS NOT NULL',c.execute("SELECT ad FROM musteri WHERE telefon IS NOT NULL").fetchall())
