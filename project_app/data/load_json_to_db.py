import sqlite3
import os
import json


def load_items_from_json_to_db():
    db_path = os.path.join(os.path.dirname(__file__), 'items.db')
    json_path = os.path.join(os.path.dirname(__file__), 'items.json')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    with open(json_path, 'r', encoding='utf-8') as file:
        items = json.load(file)

    for item in items:
        name = item.get("name")
        price = item.get("price")
        if name and price is not None:
            cursor.execute('''
                INSERT INTO items (nev, egyseg, egysegar)
                VALUES (?, 'db', ?)
            ''', (name, price))

    conn.commit()
    conn.close()


if __name__ == '__main__':
    load_items_from_json_to_db()
