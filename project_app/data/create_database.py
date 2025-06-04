import sqlite3
import os

def create_items_table():
    db_path = os.path.join(os.path.dirname(__file__), 'items.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nev TEXT NOT NULL,
            egyseg TEXT DEFAULT 'db',
            egysegar INTEGER
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_items_table()
