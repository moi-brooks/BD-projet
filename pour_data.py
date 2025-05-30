import sqlite3

conn = sqlite3.connect("hotel_db.sqlite")

with open("data.sql", "r", encoding="utf-8") as f:
    sql = f.read()
    conn.executescript(sql)

conn.commit()
conn.close()
print("✅ data inserted successfully!")
