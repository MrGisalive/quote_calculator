import sqlite3
import os

class DatabaseHandler:
    """
    Egyetlen feladatú adatbázis-kezelő osztály.
    Az 'items.db' SQLite adatbázist kezeli (alapértelmezett elérési úton).
    Csak olvasás, keresés támogatott.
    """

    def __init__(self, db_path=None):
        # Ha nincs megadva, alapértelmezetten a 'data/items.db' a project_app alatt
        if db_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_path = os.path.join(base_dir, "data", "items.db")
        self.db_path = db_path

        if not os.path.isfile(self.db_path):
            # Emberi, jól olvasható hiba, ha hiányzik az adatbázis
            raise FileNotFoundError(f"Nem található az adatbázis: {self.db_path}")
        
        # SQLite kapcsolat megnyitása, sor-visszaadásra állítva
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

    def search_items(self, search_term=""):
        """
        Tételkeresés név alapján. Részleges egyezés ('LIKE'), ékezetre érzékeny.
        Visszaad egy listát dict-ként: {'nev': ..., 'egyseg': ..., 'egysegar': ...}
        """
        c = self.conn.cursor()
        query = "SELECT nev, egyseg, egysegar FROM items WHERE nev LIKE ?"
        c.execute(query, (f"%{search_term}%",))
        return [dict(row) for row in c.fetchall()]

    def close(self):
        """Kapcsolat lezárása (ha szükséges)."""
        self.conn.close()
