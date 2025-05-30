import sqlite3

conn = sqlite3.connect("hotel_db.sqlite")
with open("data.sql", "r", encoding="utf-8") as f:
    conn.executescript(f.read())
conn.commit()
conn.close()
