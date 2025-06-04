# 💡 Villanyszerelési árajánlat készítő (Quote Calculator)

Ez a Python alapú, Tkinteres grafikus felülettel rendelkező alkalmazás egy villanyszerelési projekt anyag- és munkadíj alapú árajánlatainak összeállítását segíti.

## 🎯 Funkciók

- Helyiségek és projektek kezelése
- Anyagköltségek kiválasztása adatbázisból
- Kivitelezési munkák kiválasztása JSON listából
- Egységáras számítások automatikusan
- Word dokumentumba exportálás (python-docx)

## 🗂️ Mappastruktúra (részlet)

```
quote_calculator/
│
├── project_app/
│ ├── main.py # Alkalmazás belépési pontja
│ ├── data/ # Adatbázis és kivitelezési tételek
│ │ ├── items.db # SQLite adatbázis anyagköltségekhez
│ │ └── kivitelezesi_tetelek.json # Előre definiált munkadíjtételek
│ └── gui/ # GUI logika
│ ├── main_menu.py
│ ├── item_selector.py
│ ├── kivitelezesi_selector.py
│ └── project_editor/
│ ├── editor_window.py
│ ├── helyiseg_list.py
│ └── exporter.py
```

## 🛠️ Fejlesztői követelmények

### Telepítés

1. Klónozd a repót:
```bash
git clone https://github.com/felhasznalonev/quote_calculator.git
cd quote_calculator
```

2. Hozz létre virtuális környezetet:
```bash
python -m venv .venv
.venv\Scripts\activate     # Windows
```

3. Telepítsd a függőségeket:
```bash
pip install -r requirements.txt
```

### Követelmények

- Python 3.10+
- pip
- Tkinter (a legtöbb Python telepítéssel együtt jön)
- Függőségek:
  - `python-docx`

## ▶️ Futás

```bash
python project_app/main.py
```

Ez megnyitja a főmenüt, ahonnan új projektet hozhatsz létre, anyagot és munkát adhatsz hozzá, majd exportálhatod az ajánlatot Word formátumban.

## 📦 Adatok

- **Adatbázis fájl**: `data/items.db`
- **Kivitelezési munkák**: `data/kivitelezesi_tetelek.json`

## 📤 Export

Az ajánlatok automatikusan `projektek/` mappába kerülnek `.docx` formátumban.

## 📄 Licenc

Ez a projekt szabadon használható tanulási és egyéni célokra. Kereskedelmi felhasználáshoz kérlek keress meg.
