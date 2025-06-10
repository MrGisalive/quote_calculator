import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
from gui.project_editor import ProjectEditor
from gui.utils import center_window
import os
from gui.utils import open_folder_in_explorer

# Központi útvonalak, hogy mindig a projekthez képest dolgozzunk
CURRENT_FILE = os.path.abspath(__file__)
PROJECT_EDITOR_DIR = os.path.dirname(CURRENT_FILE)
PROJECT_APP_DIR = os.path.abspath(os.path.join(PROJECT_EDITOR_DIR, '..', '..', '..'))
PROJECTS_DIR = os.path.join(PROJECT_APP_DIR, "projektek")

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Árajánlat Projektkezelő")
        self.root.geometry("400x500")
        center_window(self.root, 400, 500)

        # ---- Menü gombstílus egységesítése ----
        style = ttk.Style(self.root)
        style.configure(
            'Menu.TButton',
            font=('Arial', 12, 'bold'),
            padding=10,
            foreground='#272c34',
            background='#e6e9ef',
            borderwidth=0,
        )
        style.map(
            'Menu.TButton',
            background=[('active', '#b2c0e0'), ('pressed', '#d1e0f7')],
            foreground=[('active', '#194f8c')]
        )

        # ---- Főcím ----
        self.title_label = ttk.Label(
            self.root, text="Árajánlat Projektkezelő", font=("Arial", 19, "bold")
        )
        self.title_label.pack(pady=32)

        # ---- Főmenü gombok ----
        ttk.Button(
            self.root, text="➕ Új projekt",
            command=self.new_project, style='Menu.TButton'
        ).pack(pady=15, fill='x', padx=50)

        ttk.Button(
            self.root, text="📁 Projekt betöltése",
            command=self.load_project, style='Menu.TButton'
        ).pack(pady=15, fill='x', padx=50)

        # Dokumentumok mappa megnyitása
        ttk.Button(
            self.root,
            text="📂 Dokumentumok mappa megnyitása",
            command=lambda: open_folder_in_explorer(PROJECTS_DIR, self.root),
            style='Menu.TButton'
        ).pack(pady=15, fill='x', padx=50)


        ttk.Button(
            self.root, text="❌ Kilépés",
            command=self.root.quit, style='Menu.TButton'
        ).pack(pady=28, fill='x', padx=80)

    def new_project(self):
        """
        Új projekt létrehozása ablak – hibajelzéssel, piros kiemeléssel.
        """
        window = tk.Toplevel(self.root)
        window.title("Új projekt létrehozása")
        window.geometry("400x250")
        center_window(window, 400, 250)
        window.grab_set()


        # ---- Topbar: Vissza és Tovább gombok ----
        style = ttk.Style(window)
        style.configure('Vissza.TButton', font=('Arial', 13, 'bold'))
        style.configure('Tovabb.TButton', font=('Arial', 13, 'bold'))

        topbar = ttk.Frame(window)
        topbar.pack(side="top", fill="x", padx=0, pady=(0, 10))

        btn_vissza = ttk.Button(
            topbar, text="⬅️ Vissza", command=window.destroy, style='Vissza.TButton'
        )
        btn_vissza.pack(side="left", padx=12, pady=8)

        # --- Adatbeviteli mezők ---
        ttk.Label(window, text="Projekt neve:").pack(pady=(10, 2))
        nev_entry = tk.Entry(window, width=40, font=('Arial', 11))
        nev_entry.pack(pady=2)

        ttk.Label(window, text="Megrendelő neve:").pack(pady=2)
        megrendelo_entry = tk.Entry(window, width=40, font=('Arial', 11))
        megrendelo_entry.pack(pady=2)

        ttk.Label(window, text="Lakcím:").pack(pady=2)
        cim_entry = tk.Entry(window, width=40, font=('Arial', 11))
        cim_entry.pack(pady=2)

        # --- Visszaállítja fehérre a mezőt gépeléskor ---
        def reset_entry_bg(event):
            event.widget.config(background="white")

        for entry in (nev_entry, megrendelo_entry, cim_entry):
            entry.bind("<Key>", reset_entry_bg)

        # --- Tovább gomb logika ---
        def tovabb():
            nev = nev_entry.get().strip()
            megrendelo = megrendelo_entry.get().strip()
            cim = cim_entry.get().strip()
            # Minden mező vissza fehér
            nev_entry.config(background="white")
            megrendelo_entry.config(background="white")
            cim_entry.config(background="white")

            # Ellenőrizzük, hogy mindhárom mező ki van-e töltve
            if nev and megrendelo and cim:
                window.destroy()
                self.root.withdraw()
                ProjectEditor(self.root, nev, megrendelo, cim)
            else:
                messagebox.showwarning("Hiányzó adat", "Minden mező kitöltése kötelező!", parent=window)
                if not nev:
                    nev_entry.config(background="#ffcccc")
                if not megrendelo:
                    megrendelo_entry.config(background="#ffcccc")
                if not cim:
                    cim_entry.config(background="#ffcccc")

        btn_tovabb = ttk.Button(
            topbar, text="Tovább →", command=tovabb, style='Tovabb.TButton'
        )
        btn_tovabb.pack(side="right", padx=12, pady=8)
        
    def load_project(self):
        """
        Meglévő projekt betöltése JSON-ból, mindig a projektek mappájából.
        """
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        projects_dir = os.path.join(base_dir, 'projektek')

        if not os.path.exists(projects_dir):
            os.makedirs(projects_dir)

        # --- Fájlkiválasztó, alapértelmezett mappa a projektek mappa ---
        filepath = filedialog.askopenfilename(
            filetypes=[("JSON fájl", "*.json")],
            initialdir=projects_dir,
            title="Projekt betöltése"
        )
        if filepath:
            self._open_project(filepath)

    def _open_project(self, filepath):
        """
        Fájl olvasása és ProjectEditor indítása.
        """
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                projekt = json.load(f)
            self.root.withdraw()
            ProjectEditor(
                self.root,
                projekt.get("projektnev", ""),
                projekt.get("megrendelo", ""),
                projekt.get("cim", ""),
                projekt.get("helyisegek", [])
            )
        except Exception as e:
            messagebox.showerror("Hiba", f"Nem sikerült a projekt betöltése: {e}")

def open_main_menu(root):
    """
    MainMenu osztály példányosítása.
    """
    MainMenu(root)
