import sqlite3

def init_db():
    conn = sqlite3.connect('kniffel.db')
    cursor = conn.cursor()

    # Benutzertabelle
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        salt TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()