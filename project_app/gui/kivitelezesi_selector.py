import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

def open_kivitelezesi_selector(parent, callback):
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    json_path = os.path.join(base_dir, 'project_app', 'data', 'kivitelezesi_tetelek.json')

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            items = json.load(f)
    except Exception as e:
        messagebox.showerror("Hiba", f"Nem sikerült betölteni a kivitelezési tételeket: {str(e)}")
        return 

    selector = tk.Toplevel(parent)
    selector.title("Kivitelezési munka kiválasztása")
    selector.geometry("600x400")

    search_var = tk.StringVar()
    search_entry = ttk.Entry(selector, textvariable=search_var)
    search_entry.pack(fill='x', padx=10, pady=(10, 0))

    columns = ("Tétel", "Egység", "Egységár")
    tree = ttk.Treeview(selector, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=180)
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    def update_list():
        query = search_var.get().lower()
        tree.delete(*tree.get_children())
        for item in items:
            if (query in item["nev"].lower() or 
                query in item["egyseg"].lower() or 
                query in str(item["egysegar"])):
                tree.insert("", tk.END, values=(item["nev"], item["egyseg"], item["egysegar"]))

    def on_select(event=None):
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Nincs kiválasztás", "Válassz ki egy tételt!")
            return
        values = tree.item(selected, "values")
        callback(values)
        selector.destroy()

    search_entry.bind("<Return>", lambda e: on_select())
    search_var.trace_add("write", lambda *a: update_list())
    ttk.Button(selector, text="✅ Hozzáadás", command=on_select).pack(pady=10)
    tree.bind("<Return>", on_select)
    tree.bind("<Double-Button-1>", on_select)

    update_list()