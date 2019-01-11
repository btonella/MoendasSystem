import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
	CREATE TABLE pedidos(
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		mesa INTEGER,
		comanda TEXT,
		pedido TEXT,
		quantidade REAL,
		valor REAL
	);
	""")
print("Tabela pedidos criadas com sucesso")

cursor.execute("""
	CREATE TABLE mesas(
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		mesa INTEGER,
		comanda TEXT,
		total REAL
	);
""")
print("Tabela mesas criadas com sucesso")

cursor.execute("""
	CREATE TABLE relatorio(
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		mesa INTEGER,
		comanda TEXT,
		pedido TEXT,
		quantidade REAL,
		valor REAL,
		data DATE
	);

	""")

print("Tabela relatorio criadas com sucesso")
cursor.close()