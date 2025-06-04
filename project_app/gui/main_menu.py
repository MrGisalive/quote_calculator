import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
from gui.project_editor import ProjectEditor

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Árajánlat Projektkezelő")
        self.root.geometry("400x400")

        self.title_label = ttk.Label(self.root, text="Árajánlat Projektkezelő", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=30)

        ttk.Button(self.root, text="➕ Új projekt", command=self.new_project).pack(pady=10)
        ttk.Button(self.root, text="📁 Projekt betöltése", command=self.load_project).pack(pady=10)
        ttk.Button(self.root, text="❌ Kilépés", command=self.root.quit).pack(pady=30)

    def new_project(self):
        window = tk.Toplevel(self.root)
        window.title("Új projekt létrehozása")
        window.geometry("400x250")

        ttk.Label(window, text="Projekt neve:").pack(pady=5)
        nev_entry = ttk.Entry(window, width=40)
        nev_entry.pack(pady=5)

        ttk.Label(window, text="Megrendelő neve:").pack(pady=5)
        megrendelo_entry = ttk.Entry(window, width=40)
        megrendelo_entry.pack(pady=5)

        ttk.Label(window, text="Lakcím:").pack(pady=5)
        cim_entry = ttk.Entry(window, width=40)
        cim_entry.pack(pady=5)

        def tovabb():
            self.root.withdraw()
            nev = nev_entry.get()
            megrendelo = megrendelo_entry.get()
            cim = cim_entry.get()
            window.destroy()
            ProjectEditor(self.root, nev, megrendelo, cim)

        ttk.Button(window, text="Tovább →", command=tovabb).pack(pady=15)

    def load_project(self):
        filepath = filedialog.askopenfilename(filetypes=[("JSON fájl", "*.json")])
        if filepath:
            self._open_project(filepath)

    def _open_project(self, filepath):
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
    MainMenu(root)
