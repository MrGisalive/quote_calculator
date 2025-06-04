import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
from .exporter import export_project_to_word
from gui.db_handler import DatabaseHandler
from .helyiseg_list import HelyisegListManager
from .helyiseg_window import open_helyseg_window

CURRENT_FILE = os.path.abspath(__file__)
PROJECT_EDITOR_DIR = os.path.dirname(CURRENT_FILE)
PROJECT_APP_DIR = os.path.abspath(os.path.join(PROJECT_EDITOR_DIR, '..', '..', '..'))

class ProjectEditor:
    def __init__(self, root, projektnev, megrendelo, cim, helyisegek=None):
        self.root = root
        self.helyisegek = helyisegek if helyisegek else []
        self.projektnev = projektnev
        self.megrendelo = megrendelo
        self.cim = cim
        self.db = DatabaseHandler()

        self.editor = tk.Toplevel(self.root)
        self.editor.title(f"Projekt: {self.projektnev}")
        self.editor.geometry("600x400")
        self.editor.minsize(650, 480)
        self.editor.protocol("WM_DELETE_WINDOW", self.on_close)
        self.editor.columnconfigure(0, weight=1)
        self.editor.rowconfigure(0, weight=1)

        # --- Canvas + Scrollbar + Container ---
        main_canvas = tk.Canvas(self.editor, background="#f9f9f9", borderwidth=0, highlightthickness=0)
        main_canvas.grid(row=0, column=0, sticky="nsew")
        main_scrollbar = ttk.Scrollbar(self.editor, orient="vertical", command=main_canvas.yview)
        main_scrollbar.grid(row=0, column=1, sticky="ns")
        main_canvas.configure(yscrollcommand=main_scrollbar.set)

        container = ttk.Frame(main_canvas)
        container_id = main_canvas.create_window((0, 0), window=container, anchor="nw")

        # Keep scroll region in sync
        container.bind("<Configure>", lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all")))
        main_canvas.bind("<Configure>", lambda e: main_canvas.itemconfig(container_id, width=e.width))
        container.columnconfigure(0, weight=1)

        # --- Project Details ---
        project_details = ttk.LabelFrame(container, text="Projekt információk", padding=10)
        project_details.grid(row=0, column=0, sticky='ew', pady=10, padx=10)
        project_details.columnconfigure(0, weight=1)
        ttk.Label(project_details, text=f"Projekt neve: {self.projektnev}", font=("Arial", 14, "bold")).grid(row=0, column=0, sticky='w', pady=(0, 5))
        ttk.Label(project_details, text=f"Megrendelő neve: {self.megrendelo}", font=("Arial", 10)).grid(row=1, column=0, sticky='w')
        ttk.Label(project_details, text=f"Lakcím: {self.cim}", font=("Arial", 10)).grid(row=2, column=0, sticky='w')

        # --- Helyiseg Manager ---
        self.helyiseg_manager = HelyisegListManager(
            container, self.helyisegek,
            self.open_helyseg_window,
            self.update_project_total,
            self.db
        )
        self.helyiseg_manager.frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.helyiseg_manager.frame.columnconfigure(0, weight=1)

        # --- Buttons ---
        btn_frame = ttk.Frame(container)
        btn_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        btn_frame.columnconfigure((0, 1, 2, 3), weight=1)
        ttk.Button(btn_frame, text="📁 Mentés Másként", command=self.save_project).grid(row=0, column=0, sticky="ew", padx=2)
        ttk.Button(btn_frame, text="💾 Gyors Mentés", command=self.auto_save_project).grid(row=0, column=1, sticky="ew", padx=2)
        ttk.Button(btn_frame, text="❌ Projekt bezárása", command=self.on_close).grid(row=0, column=2, sticky="ew", padx=2)
        ttk.Button(btn_frame, text="📝 Dokumentum generálás", command=self.export_to_doc).grid(row=0, column=3, sticky="ew", padx=2)

        # --- Total Amount ---
        self.osszeg_label = ttk.Label(
            container, text="Projekt teljes összege: 0 Ft", font=("Segoe UI", 12, "bold"))
        self.osszeg_label.grid(row=3, column=0, sticky="w", padx=15, pady=(6, 10))

        self.update_project_total()

    def open_helyseg_window(self, adat, db_handler):
        open_helyseg_window(self.editor, adat, db_handler, self.update_project_total)

    def update_project_total(self):
        total = 0
        for helyseg in self.helyisegek:
            for t in helyseg.get('tetel_lista', []):
                total += int(t.get("mennyiseg", 1)) * float(t.get("egysegar", 0))
            for t in helyseg.get('kivitelezesi_tetelek', []):
                total += int(t.get("mennyiseg", 1)) * float(t.get("egysegar", 0))
        self.osszeg_label.config(text=f"Projekt teljes összege: {total:,.0f} Ft")

    def save_project(self):
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON fájl", "*.json")])
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.get_project_data(), f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Siker", "Projekt elmentve JSON fájlba!")

    def auto_save_project(self):
        os.makedirs(PROJECT_APP_DIR, exist_ok=True)
        safe_name = "".join(c for c in self.projektnev if c.isalnum() or c in (" ", "_", "-")).rstrip()
        file_path = os.path.join(PROJECT_APP_DIR, f"{safe_name}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.get_project_data(), f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Mentve", f"Sikeres mentés ide: {file_path}")

    def get_project_data(self):
        return {
            "projektnev": self.projektnev,
            "megrendelo": self.megrendelo,
            "cim": self.cim,
            "helyisegek": self.helyisegek
        }

    def on_close(self):
        self.editor.destroy()
        self.root.deiconify()

    def export_to_doc(self):
        os.makedirs(PROJECT_APP_DIR, exist_ok=True)
        safe_name = "".join(c for c in self.projektnev if c.isalnum() or c in (" ", "_", "-")).rstrip()
        file_path = filedialog.asksaveasfilename(
            defaultextension=".docx",
            filetypes=[("Word dokumentum", "*.docx")],
            initialdir=PROJECT_APP_DIR,
            initialfile=f"{safe_name}.docx"
        )
        if file_path:
            try:
                export_project_to_word(file_path, self.get_project_data())
                messagebox.showinfo("Siker", f"A dokumentum elkészült:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Hiba", f"Hiba történt: {e}")