import tkinter as tk
from tkinter import ttk

def open_item_selector(parent, db_handler, callback):
    selector = tk.Toplevel(parent)
    selector.title("Tételek kiválasztása")
    selector.geometry("800x500")

    search_var = tk.StringVar()
    search_entry = ttk.Entry(selector, textvariable=search_var)
    search_entry.pack(fill='x', padx=10, pady=(10, 0))

    listbox = tk.Listbox(selector, height=12)
    listbox.pack(fill="both", expand=True, padx=10, pady=5)

    # 🔍 Valós idejű adatbázis keresés
    def search_items(query):
        q = query.lower()
        items = db_handler.search_items(q)
        return [
            item for item in items
            if q in item.get('nev', '').lower()
            or q in item.get('egyseg', '').lower()
            or q in str(item.get('egysegar', ''))
        ]

    def update_list():
        filtered = search_items(search_var.get())
        listbox.delete(0, tk.END)
        for item in filtered:
            listbox.insert(tk.END, f"{item['nev']} ({item['egyseg']} - {item['egysegar']} Ft)")

    def on_select(event=None):
        sel_idx = listbox.curselection()
        if sel_idx:
            filtered = search_items(search_var.get())
            val = filtered[sel_idx[0]]
            callback((val['nev'], val['egyseg'], val['egysegar']))
            selector.destroy()

    ttk.Button(selector, text="➕ Hozzáadás", command=on_select).pack(pady=5)
    listbox.bind("<Double-Button-1>", on_select)
    listbox.bind("<Return>", on_select)
    search_entry.bind("<Return>", lambda e: on_select())
    search_var.trace_add("write", lambda *a: update_list())
    update_list()
