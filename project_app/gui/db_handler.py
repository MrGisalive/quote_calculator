import sqlite3
import os

class DatabaseHandler:
    def __init__(self, db_path=None):
        if db_path is None:
            # Mindig megtalálja a data/items.db-t, bárhonnan is indítod
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_path = os.path.join(base_dir, "data", "items.db")
        self.db_path = db_path
        print("Adatbázis elérési út:", self.db_path)   # DEBUG PRINT
        if not os.path.isfile(self.db_path):
            raise FileNotFoundError(f"Nem található az adatbázis: {self.db_path}")
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

    def search_items(self, search_term=""):
        c = self.conn.cursor()
        query = "SELECT nev, egyseg, egysegar FROM items WHERE nev LIKE ?"
        c.execute(query, (f"%{search_term}%",))
        return [dict(row) for row in c.fetchall()]

    def close(self):
        self.conn.close()
