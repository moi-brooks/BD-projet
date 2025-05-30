import sqlite3
import os

print("Creating database at:", os.path.abspath("hotel_db.sqlite"))

conn = sqlite3.connect("hotel_db.sqlite")
cursor = conn.cursor()

try:
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS Hotel (
        id INTEGER PRIMARY KEY,
        ville TEXT,
        pays TEXT,
        code_postal INTEGER
    );

    CREATE TABLE IF NOT EXISTS Client (
        id INTEGER PRIMARY KEY,
        adresse TEXT,
        ville TEXT,
        code_postal INTEGER,
        email TEXT,
        telephone TEXT,
        nom TEXT
    );

    CREATE TABLE IF NOT EXISTS Prestation (
        id INTEGER PRIMARY KEY,
        prix REAL,
        description TEXT
    );

    CREATE TABLE IF NOT EXISTS TypeChambre (
        id INTEGER PRIMARY KEY,
        nom TEXT,
        prix REAL
    );

    CREATE TABLE IF NOT EXISTS Chambre (
        id INTEGER PRIMARY KEY,
        numero INTEGER,
        etage INTEGER,
        fumeur INTEGER,
        type_chambre_id INTEGER,
        hotel_id INTEGER,
        FOREIGN KEY(type_chambre_id) REFERENCES TypeChambre(id),
        FOREIGN KEY(hotel_id) REFERENCES Hotel(id)
    );

    CREATE TABLE IF NOT EXISTS Reservation (
        id INTEGER PRIMARY KEY,
        date_debut DATE,
        date_fin DATE,
        client_id INTEGER,
        chambre_id INTEGER,
        FOREIGN KEY(client_id) REFERENCES Client(id),
        FOREIGN KEY(chambre_id) REFERENCES Chambre(id)
    );

    CREATE TABLE IF NOT EXISTS Evaluation (
        id INTEGER PRIMARY KEY,
        date DATE,
        note INTEGER,
        commentaire TEXT,
        client_id INTEGER,
        FOREIGN KEY(client_id) REFERENCES Client(id)
    );
    """)
    conn.commit()
    print("✅ All tables created successfully!")

except sqlite3.Error as e:
    print("❌ SQL Error:", e)

# Show all created tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("📋 Tables in DB:", cursor.fetchall())

conn.close()
