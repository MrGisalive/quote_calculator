import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

class HelyisegListManager:
    def __init__(self, parent, helyisegek, open_helyseg_callback, update_total_callback, db_handler):
        self.helyisegek = helyisegek
        self.open_helyseg_callback = open_helyseg_callback
        self.update_total_callback = update_total_callback
        self.db_handler = db_handler

        self.frame = ttk.LabelFrame(parent, text="Helyiségek", padding=(10,8,10,8))
        self.frame.columnconfigure(0, weight=1)

        self.helyseg_listbox = tk.Listbox(self.frame, height=7, font=("Segoe UI", 10))
        self.helyseg_listbox.grid(row=0, column=0, sticky="ew")
        self.helyseg_listbox.bind("<Double-Button-1>", self.open_helyseg)
        listbox_scroll = ttk.Scrollbar(self.frame, orient="vertical", command=self.helyseg_listbox.yview)
        self.helyseg_listbox.configure(yscrollcommand=listbox_scroll.set)
        listbox_scroll.grid(row=0, column=1, sticky="ns")

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
        nev = simpledialog.askstring("Helyiség hozzáadása", "Add meg a helyiség nevét:")
        if nev:
            self.helyisegek.append({"nev": nev, "tetel_lista": [], "kivitelezesi_tetelek": []})
            self.refresh_listbox()
            self.update_total_callback()

    def edit_helyseg(self):
        idx = self.helyseg_listbox.curselection()
        if idx:
            current_name = self.helyisegek[idx[0]]["nev"]
            new_name = simpledialog.askstring("Szerkesztés", "Új helyiségnév:", initialvalue=current_name)
            if new_name:
                self.helyisegek[idx[0]]["nev"] = new_name
                self.refresh_listbox()

    def delete_helyseg(self):
        idx = self.helyseg_listbox.curselection()
        if idx and messagebox.askyesno("Törlés", "Biztos törli a kiválasztott helyiséget?"):
            del self.helyisegek[idx[0]]
            self.refresh_listbox()
            self.update_total_callback()

    def open_helyseg(self, event=None):
        idx = self.helyseg_listbox.curselection()
        if idx:
            self.open_helyseg_callback(self.helyisegek[idx[0]], self.db_handler)

    def refresh_listbox(self):
        self.helyseg_listbox.delete(0, tk.END)
        for helyseg in self.helyisegek:
            self.helyseg_listbox.insert(tk.END, helyseg['nev'])
