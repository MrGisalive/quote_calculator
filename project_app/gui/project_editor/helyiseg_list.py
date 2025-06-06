import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

class HelyisegListManager:
    """
    Egy helyiség-kezelő lista (Listbox) + gombok panel, hozzáadás/szerkesztés/törlés funkciókkal.
    """

    def __init__(self, parent, helyisegek, open_helyseg_callback, update_total_callback, db_handler):
        self.helyisegek = helyisegek
        self.open_helyseg_callback = open_helyseg_callback
        self.update_total_callback = update_total_callback
        self.db_handler = db_handler

        # Külső keret/cím
        self.frame = ttk.LabelFrame(parent, text="Helyiségek", padding=(10,8,10,8))
        self.frame.columnconfigure(0, weight=1)

        # Listbox + görgető
        self.helyseg_listbox = tk.Listbox(self.frame, height=7, font=("Segoe UI", 10))
        self.helyseg_listbox.grid(row=0, column=0, sticky="ew")
        self.helyseg_listbox.bind("<Double-Button-1>", self.open_helyseg)

        listbox_scroll = ttk.Scrollbar(self.frame, orient="vertical", command=self.helyseg_listbox.yview)
        self.helyseg_listbox.configure(yscrollcommand=listbox_scroll.set)
        listbox_scroll.grid(row=0, column=1, sticky="ns")

        # Gombok egy sorban, szép elrendezésben
        btn_frame = ttk.Frame(self.frame)
        btn_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(7,0))
        for i in range(4):
            btn_frame.columnconfigure(i, weight=1)

        ttk.Button(btn_frame, text="🔎 Megnyitás", command=self.open_helyseg).grid(row=0, column=0, sticky="ew", padx=2)
        ttk.Button(btn_frame, text="➕ Hozzáadás", command=self.add_helyseg).grid(row=0, column=1, sticky="ew", padx=2)
        ttk.Button(btn_frame, text="✏️ Szerkesztés", command=self.edit_helyseg).grid(row=0, column=2, sticky="ew", padx=2)
        ttk.Button(btn_frame, text="🗑️ Törlés", command=self.delete_helyseg).grid(row=0, column=3, sticky="ew", padx=2)

        self.refresh_listbox()

    def add_helyseg(self):
        """
        Új helyiség hozzáadása felugró ablakból. Csak név kell, tételek listája üres.
        """
        nev = simpledialog.askstring("Helyiség hozzáadása", "Add meg a helyiség nevét:")
        if nev:
            self.helyisegek.append({"nev": nev, "tetel_lista": [], "kivitelezesi_tetelek": []})
            self.refresh_listbox()
            self.update_total_callback()

    def edit_helyseg(self):
        """
        Kijelölt helyiség nevének átírása.
        """
        idx = self.helyseg_listbox.curselection()
        if idx:
            current_name = self.helyisegek[idx[0]]["nev"]
            new_name = simpledialog.askstring("Szerkesztés", "Új helyiségnév:", initialvalue=current_name)
            if new_name:
                self.helyisegek[idx[0]]["nev"] = new_name
                self.refresh_listbox()

    def delete_helyseg(self):
        """
        Kijelölt helyiség törlése megerősítéssel.
        """
        idx = self.helyseg_listbox.curselection()
        if idx and messagebox.askyesno("Törlés", "Biztosan törli a kiválasztott helyiséget?"):
            del self.helyisegek[idx[0]]
            self.refresh_listbox()
            self.update_total_callback()

    def open_helyseg(self, event=None):
        """
        Részletező/munkaablak megnyitása a helyiséghez (dupla katt vagy gomb).
        """
        idx = self.helyseg_listbox.curselection()
        if idx:
            self.open_helyseg_callback(self.helyisegek[idx[0]], self.db_handler)

    def refresh_listbox(self):
        """
        A listbox frissítése, hogy minden helyiség aktuális neve megjelenjen.
        """
        self.helyseg_listbox.delete(0, tk.END)
        for helyseg in self.helyisegek:
            self.helyseg_listbox.insert(tk.END, helyseg['nev'])
