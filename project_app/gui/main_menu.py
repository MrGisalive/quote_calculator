import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
from gui.project_editor import ProjectEditor
from gui.utils import center_window

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
            padding=16,
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

        ttk.Button(
            self.root, text="❌ Kilépés",
            command=self.root.quit, style='Menu.TButton'
        ).pack(pady=28, fill='x', padx=80)

    def new_project(self):
        """
        Új projekt létrehozása ablak – egyszerű topbarral, vissza és tovább gombbal.
        """
        window = tk.Toplevel(self.root)
        window.title("Új projekt létrehozása")
        window.geometry("400x250")
        center_window(window, 400, 250)

        # ---- Topbar: Vissza és Tovább gombok ----
        style = ttk.Style(window)
        style.configure('Vissza.TButton', font=('Arial', 13, 'bold'))
        style.configure('Tovabb.TButton', font=('Arial', 13, 'bold'))

        topbar = ttk.Frame(window)
        topbar.pack(side="top", fill="x", padx=0, pady=(0, 10))

        # Vissza gomb (bal felső sarok)
        btn_vissza = ttk.Button(
            topbar, text="⬅️ Vissza", command=window.destroy, style='Vissza.TButton'
        )
        btn_vissza.pack(side="left", padx=12, pady=8)

        # Tovább gomb (jobb felső sarok)
        def tovabb():
            nev = nev_entry.get().strip()
            megrendelo = megrendelo_entry.get().strip()
            cim = cim_entry.get().strip()
            # Kötelező mezők ellenőrzése
            if not nev or not megrendelo or not cim:
                messagebox.showwarning("Hiányzó adat", "Minden mező kitöltése kötelező!")
                return
            window.destroy()
            self.root.withdraw()
            ProjectEditor(self.root, nev, megrendelo, cim)

        btn_tovabb = ttk.Button(
            topbar, text="Tovább →", command=tovabb, style='Tovabb.TButton'
        )
        btn_tovabb.pack(side="right", padx=12, pady=8)

        # ---- Projekt adatai mezők ----
        ttk.Label(window, text="Projekt neve:").pack(pady=(10, 2))
        nev_entry = ttk.Entry(window, width=40)
        nev_entry.pack(pady=2)

        ttk.Label(window, text="Megrendelő neve:").pack(pady=2)
        megrendelo_entry = ttk.Entry(window, width=40)
        megrendelo_entry.pack(pady=2)

        ttk.Label(window, text="Lakcím:").pack(pady=2)
        cim_entry = ttk.Entry(window, width=40)
        cim_entry.pack(pady=2)

    def load_project(self):
        """
        Meglévő projekt betöltése JSON-ból.
        """
        filepath = filedialog.askopenfilename(filetypes=[("JSON fájl", "*.json")])
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
