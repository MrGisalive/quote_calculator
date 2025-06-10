import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
from .exporter import export_project_to_word
from core.db_handler import DatabaseHandler
from .helyiseg_list import HelyisegListManager
from .helyiseg_window import open_helyseg_window
from gui.utils import center_window
from gui.utils import open_folder_in_explorer

# Központi útvonalak, hogy mindig a projekthez képest dolgozzunk
CURRENT_FILE = os.path.abspath(__file__)
PROJECT_EDITOR_DIR = os.path.dirname(CURRENT_FILE)
PROJECT_APP_DIR = os.path.abspath(os.path.join(PROJECT_EDITOR_DIR, '..', '..', '..'))
PROJECTS_DIR = os.path.join(PROJECT_APP_DIR, "projektek")

class ProjectEditor:
    """
    Egyetlen projekt szerkesztését lehetővé tevő ablak.
    Kezeli a projekt metaadatait, helyiségeit, mentést, exportálást.
    """
    def __init__(self, root, projektnev, megrendelo, cim, helyisegek=None):
        self.root = root
        self.helyisegek = helyisegek if helyisegek else []
        self.projektnev = projektnev
        self.megrendelo = megrendelo
        self.cim = cim
        self.db = DatabaseHandler()

        # Fő ablak létrehozása, alapbeállítások
        self.editor = tk.Toplevel(self.root)
        self.editor.title(f"Projekt: {self.projektnev}")
        self.editor.geometry("600x400")
        self.editor.minsize(650, 480)
        self.editor.grab_set()
        center_window(self.editor, 600, 400)
        self.editor.protocol("WM_DELETE_WINDOW", self.on_close)
        self.editor.columnconfigure(0, weight=1)
        self.editor.rowconfigure(0, weight=1)

        # --- Vissza gombos topbar ---
        style = ttk.Style(self.editor)
        style.configure('Vissza.TButton', font=('Arial', 13, 'bold'))
        topbar = ttk.Frame(self.editor)
        topbar.pack(side="top", fill="x", padx=0, pady=(0, 8))

        def on_vissza():
            self.editor.destroy()
            self.root.deiconify()
        btn_vissza = ttk.Button(topbar, text="⬅️ Vissza", command=on_vissza, style='Vissza.TButton')
        btn_vissza.pack(side="left", padx=12, pady=8)

        # --- Görgethető tartalom ---
        main_canvas = tk.Canvas(self.editor, background="#f9f9f9", borderwidth=0, highlightthickness=0)
        main_canvas.pack(fill="both", expand=True, side="top")
        main_scrollbar = ttk.Scrollbar(self.editor, orient="vertical", command=main_canvas.yview)
        main_canvas.configure(yscrollcommand=main_scrollbar.set)
        main_scrollbar.place(relx=1.0, rely=0, relheight=1.0, anchor="ne")

        # Tartalmi frame a canvason belül, dinamikus szélesség
        container = ttk.Frame(main_canvas)
        container_id = main_canvas.create_window((0, 0), window=container, anchor="nw")
        container.bind("<Configure>", lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all")))
        main_canvas.bind("<Configure>", lambda e: main_canvas.itemconfig(container_id, width=e.width))
        container.columnconfigure(0, weight=1)

        # --- Projekt adatok (név, megrendelő, cím) ---
        project_details = ttk.LabelFrame(container, text="Projekt információk", padding=10)
        project_details.grid(row=0, column=0, sticky='ew', pady=10, padx=10)
        project_details.columnconfigure(0, weight=1)
        ttk.Label(project_details, text=f"Projekt neve: {self.projektnev}", font=("Arial", 14, "bold")).grid(row=0, column=0, sticky='w', pady=(0, 5))
        ttk.Label(project_details, text=f"Megrendelő neve: {self.megrendelo}", font=("Arial", 10)).grid(row=1, column=0, sticky='w')
        ttk.Label(project_details, text=f"Lakcím: {self.cim}", font=("Arial", 10)).grid(row=2, column=0, sticky='w')

        # --- Szerkesztés gomb ---
        btn_edit = ttk.Button(
            project_details, text="✏️ Szerkesztés",
            command=self.edit_project_meta
        )
        btn_edit.grid(row=0, column=1, rowspan=3, padx=12, sticky="ne")

        # --- Helyiségek kezelő ---
        self.helyiseg_manager = HelyisegListManager(
            container, self.helyisegek,
            self.open_helyseg_window,
            self.update_project_total,
            self.db
        )
        self.helyiseg_manager.frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.helyiseg_manager.frame.columnconfigure(0, weight=1)

        # --- Alsó funkciógombok ---
        btn_frame = ttk.Frame(container)
        btn_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        btn_frame.columnconfigure((0, 1, 2, 3), weight=1)
        ttk.Button(btn_frame, text="📁 Mentés Másként", command=self.save_project).grid(row=0, column=0, sticky="ew", padx=2)
        ttk.Button(btn_frame, text="💾 Gyors Mentés", command=self.auto_save_project).grid(row=0, column=1, sticky="ew", padx=2)
        ttk.Button(btn_frame, text="📝 Dokumentum generálás", command=self.export_to_doc).grid(row=0, column=3, sticky="ew", padx=2)
        ttk.Button(btn_frame, text="📂 Dokumentumok mappa", command=lambda: open_folder_in_explorer(PROJECTS_DIR, self.editor)).grid(row=1, column=3, sticky="ew", padx=2)

        # --- Összeg kiírása ---
        self.osszeg_label = ttk.Label(
            container, text="Projekt teljes összege: 0 Ft", font=("Segoe UI", 12, "bold"))
        self.osszeg_label.grid(row=3, column=0, sticky="w", padx=15, pady=(6, 10))

        self.update_project_total()
    def edit_project_meta(self):
        eredmeny = open_project_meta_editor(
            self.editor, self.projektnev, self.megrendelo, self.cim
        )
        if eredmeny:
            self.projektnev, self.megrendelo, self.cim = eredmeny
            # Címkék frissítése:
            for widget in self.editor.winfo_children():
                widget.destroy()
            self.__init__(self.root, self.projektnev, self.megrendelo, self.cim, self.helyisegek)
    def open_helyseg_window(self, adat, db_handler):
        # Helyiség szerkesztő ablak megnyitása
        open_helyseg_window(self.editor, adat, db_handler, self.update_project_total)

    def update_project_total(self):
        """
        Teljes projektösszeg újraszámítása és megjelenítése.
        """
        total = 0
        for helyseg in self.helyisegek:
            for t in helyseg.get('tetel_lista', []):
                total += int(t.get("mennyiseg", 1)) * float(t.get("egysegar", 0))
            for t in helyseg.get('kivitelezesi_tetelek', []):
                total += int(t.get("mennyiseg", 1)) * float(t.get("egysegar", 0))
        self.osszeg_label.config(text=f"Projekt teljes összege: {total:,.0f} Ft")

    def save_project(self):
        """
        Projekt mentése másként – felhasználó által választott névvel, projektek mappába.
        """
        os.makedirs(PROJECTS_DIR, exist_ok=True)
        safe_name = "".join(c for c in self.projektnev if c.isalnum() or c in (" ", "_", "-")).rstrip()
        default_path = os.path.join(PROJECTS_DIR, f"{safe_name}.json")
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON fájl", "*.json")],
            initialdir=PROJECTS_DIR,
            initialfile=f"{safe_name}.json"
        )
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.get_project_data(), f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Siker", f"Projekt elmentve ide:\n{path}")

    def auto_save_project(self):
        """
        Gyors mentés, automatikusan a projektek mappába.
        """
        os.makedirs(PROJECTS_DIR, exist_ok=True)
        safe_name = "".join(c for c in self.projektnev if c.isalnum() or c in (" ", "_", "-")).rstrip()
        file_path = os.path.join(PROJECTS_DIR, f"{safe_name}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.get_project_data(), f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Mentve", f"Sikeres mentés ide:\n{file_path}")

    def get_project_data(self):
        """
        A projekt adatait egy JSON-menthető dict-ben adja vissza.
        """
        return {
            "projektnev": self.projektnev,
            "megrendelo": self.megrendelo,
            "cim": self.cim,
            "helyisegek": self.helyisegek
        }

    def on_close(self):
        """
        Szerkesztő ablak bezárása – vissza főmenübe.
        """
        self.editor.destroy()
        self.root.deiconify()

    def export_to_doc(self):
        """
        Word dokumentum generálás, projektek mappába.
        """
        os.makedirs(PROJECTS_DIR, exist_ok=True)
        safe_name = "".join(c for c in self.projektnev if c.isalnum() or c in (" ", "_", "-")).rstrip()
        file_path = filedialog.asksaveasfilename(
            defaultextension=".docx",
            filetypes=[("Word dokumentum", "*.docx")],
            initialdir=PROJECTS_DIR,
            initialfile=f"{safe_name}.docx"
        )
        if file_path:
            try:
                export_project_to_word(file_path, self.get_project_data())
                messagebox.showinfo("Siker", f"A dokumentum elkészült:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Hiba", f"Hiba történt: {e}")

def open_project_meta_editor(parent, projektnev, megrendelo, cim):
    """
    Visszaadja a (projektnev, megrendelo, cim) tuple-t vagy None-t ha Cancel.
    Hibavisszajelzéssel, modal, középre helyezve.
    """
    result = {}

    editor = tk.Toplevel(parent)
    editor.title("Projekt adatok szerkesztése")
    editor.geometry("400x230")
    editor.transient(parent)
    editor.grab_set()
    try:
        # Ha van ilyen függvényed, használd!
        center_window(editor, 400, 230)
    except:
        pass

    # --- Adatmezők ---
    ttk.Label(editor, text="Projekt neve:").pack(pady=(12,2), anchor="w", padx=12)
    entry_projnev = tk.Entry(editor, width=38, font=('Arial', 11))
    entry_projnev.pack(fill="x", padx=12)
    entry_projnev.insert(0, projektnev)

    ttk.Label(editor, text="Megrendelő neve:").pack(pady=(10,2), anchor="w", padx=12)
    entry_megrendelo = tk.Entry(editor, width=38, font=('Arial', 11))
    entry_megrendelo.pack(fill="x", padx=12)
    entry_megrendelo.insert(0, megrendelo)

    ttk.Label(editor, text="Lakcím:").pack(pady=(10,2), anchor="w", padx=12)
    entry_cim = tk.Entry(editor, width=38, font=('Arial', 11))
    entry_cim.pack(fill="x", padx=12)
    entry_cim.insert(0, cim)

    # --- Reset szín gépeléskor ---
    def reset_entry_bg(event):
        event.widget.config(background="white")

    for entry in (entry_projnev, entry_megrendelo, entry_cim):
        entry.bind("<Key>", reset_entry_bg)

    # --- Gombok ---
    btn_frame = ttk.Frame(editor)
    btn_frame.pack(pady=16)
    
    def on_ok():
        nev = entry_projnev.get().strip()
        megr = entry_megrendelo.get().strip()
        address = entry_cim.get().strip()

        # Reset színek
        entry_projnev.config(background="white")
        entry_megrendelo.config(background="white")
        entry_cim.config(background="white")

        if nev and megr and address:
            result["projektnev"] = nev
            result["megrendelo"] = megr
            result["cim"] = address
            editor.destroy()
        else:
            messagebox.showwarning("Hiányzó adat", "Minden mező kitöltése kötelező!", parent=editor)
            if not nev:
                entry_projnev.config(background="#ffcccc")
            if not megr:
                entry_megrendelo.config(background="#ffcccc")
            if not address:
                entry_cim.config(background="#ffcccc")

    def on_cancel():
        editor.destroy()

    ttk.Button(btn_frame, text="OK", command=on_ok, width=12).pack(side="left", padx=8)
    ttk.Button(btn_frame, text="Mégse", command=on_cancel, width=12).pack(side="left", padx=8)

    entry_projnev.focus_set()
    editor.wait_window()
    if "projektnev" in result:
        return result["projektnev"], result["megrendelo"], result["cim"]
    return None
