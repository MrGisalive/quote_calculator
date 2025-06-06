import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from gui.utils import center_window

def open_kivitelezesi_selector(parent, callback):
    """
    Kivitelezési munkadíjtételek kiválasztó ablak, teljesen reszponzív és görgethető.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    json_path = os.path.join(base_dir, 'project_app', 'data', 'kivitelezesi_tetelek.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            items = json.load(f)
    except Exception as e:
        messagebox.showerror("Hiba", f"Nem sikerült betölteni a kivitelezési tételeket: {str(e)}")
        return

    selector = tk.Toplevel(parent)
    selector.title("Kivitelezési munkák kiválasztása")
    selector.geometry("900x600")
    center_window(selector, 900, 600)
    selector.minsize(700, 400)

    # --- Fő frame, minden gridben! ---
    main_frame = ttk.Frame(selector)
    main_frame.pack(fill="both", expand=True)
    main_frame.rowconfigure(1, weight=4)   # fő lista
    main_frame.rowconfigure(3, weight=2)   # gyűjtőlista
    main_frame.columnconfigure(0, weight=1)

    # --- Topbar ---
    topbar = ttk.Frame(main_frame)
    topbar.grid(row=0, column=0, sticky="ew", pady=(8, 4))
    style = ttk.Style(selector)
    style.configure('Vissza.TButton', font=('Arial', 13, 'bold'))
    style.configure('ListButton.TButton', font=('Arial', 13, 'bold'), padding=8)
    btn_vissza = ttk.Button(topbar, text="⬅️ Vissza", command=selector.destroy, style='Vissza.TButton')
    btn_vissza.pack(side="left", padx=10, pady=4)

    # --- Kereső + fő lista ---
    top_frame = ttk.Frame(main_frame)
    top_frame.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 8))
    top_frame.rowconfigure(1, weight=1)
    top_frame.columnconfigure(0, weight=1)

    search_var = tk.StringVar()
    search_entry = ttk.Entry(top_frame, textvariable=search_var, width=40)
    search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8), pady=(0, 3))
    search_entry.focus()

    list_frame = ttk.Frame(top_frame)
    list_frame.grid(row=1, column=0, sticky="nsew")
    list_frame.rowconfigure(0, weight=1)
    list_frame.columnconfigure(0, weight=1)

    listbox = tk.Listbox(list_frame)
    listbox.grid(row=0, column=0, sticky="nsew")
    list_scroll = ttk.Scrollbar(list_frame, orient="vertical", command=listbox.yview)
    list_scroll.grid(row=0, column=1, sticky="ns")
    listbox.config(yscrollcommand=list_scroll.set)

    # --- Darabszám + hozzáadás a két lista között ---
    action_frame = ttk.Frame(main_frame)
    action_frame.grid(row=2, column=0, sticky="ew", padx=12, pady=(0, 6))
    qty_var = tk.IntVar(value=1)
    ttk.Label(action_frame, text="Darabszám:", font=('Arial', 13, 'bold')).pack(side="left", padx=(0, 8))
    qty_spin = ttk.Spinbox(action_frame, from_=1, to=999, textvariable=qty_var, width=7, font=('Arial', 13))
    qty_spin.pack(side="left", padx=(0, 16))
    add_btn = ttk.Button(action_frame, text="➕ Hozzáadás a listához", style='ListButton.TButton')
    add_btn.pack(side="left", padx=10)

    # --- Gyűjtőlista (alul) ---
    bottom_frame = ttk.Frame(main_frame)
    bottom_frame.grid(row=3, column=0, sticky="nsew", padx=12, pady=(0, 10))
    bottom_frame.rowconfigure(1, weight=1)
    bottom_frame.columnconfigure(0, weight=1)
    ttk.Label(bottom_frame, text="Gyűjtőlista: (kiválasztott tételek)").grid(row=0, column=0, sticky='w')
    selected_frame = ttk.Frame(bottom_frame)
    selected_frame.grid(row=1, column=0, sticky="nsew")
    selected_frame.rowconfigure(0, weight=1)
    selected_frame.columnconfigure(0, weight=1)
    selected_list = tk.Listbox(selected_frame)
    selected_list.grid(row=0, column=0, sticky="nsew")
    selected_scroll = ttk.Scrollbar(selected_frame, orient="vertical", command=selected_list.yview)
    selected_scroll.grid(row=0, column=1, sticky="ns")
    selected_list.config(yscrollcommand=selected_scroll.set)
    remove_btn = ttk.Button(bottom_frame, text="❌ Kijelölt törlése")
    remove_btn.grid(row=2, column=0, sticky="e", pady=(4, 0))

    # --- Véglegesítés gomb ---
    selected_items = []
    finalize_btn = ttk.Button(main_frame, text="✅ Kiválasztottak hozzáadása",
                              style='ListButton.TButton',
                              command=lambda: (callback(selected_items), selector.destroy()))
    finalize_btn.grid(row=4, column=0, pady=6, sticky="ew", padx=180)

    # --- Lista szűrés, frissítés, hozzáadás ---
    def search_items(query):
        q = query.lower()
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
    def add_to_selected():
        sel_idx = listbox.curselection()
        if not sel_idx:
            messagebox.showwarning("Nincs kiválasztva", "Előbb válassz ki egy tételt!")
            return
        filtered = search_items(search_var.get())
        item = filtered[sel_idx[0]]
        qty = qty_var.get()
        if qty < 1:
            messagebox.showwarning("Hibás mennyiség", "A darabszám legalább 1 legyen!")
            return
        for i, (name, unit, price, q) in enumerate(selected_items):
            if name == item['nev'] and unit == item['egyseg']:
                selected_items[i] = (name, unit, price, q + qty)
                update_selected_list()
                return
        selected_items.append((item['nev'], item['egyseg'], item['egysegar'], qty))
        update_selected_list()
    def update_selected_list():
        selected_list.delete(0, tk.END)
        for name, unit, price, qty in selected_items:
            selected_list.insert(tk.END, f"{name} ({unit}) x{qty} - {price} Ft/db")
    def remove_selected_item():
        sel = selected_list.curselection()
        if sel:
            selected_items.pop(sel[0])
            selected_list.delete(sel[0])

    # --- Eseménykötések ---
    add_btn.config(command=add_to_selected)
    remove_btn.config(command=remove_selected_item)
    listbox.bind("<Double-Button-1>", lambda e: add_to_selected())
    search_entry.bind("<Return>", lambda e: add_to_selected())
    search_var.trace_add("write", lambda *a: update_list())
    update_list()

    # Görgő támogatás (Listbox-on, platformfüggetlen)
    def on_mousewheel_listbox(event):
        if os.name == 'nt':
            listbox.yview_scroll(-1 * int(event.delta / 120), "units")
        else:
            listbox.yview_scroll(-1 if event.num == 4 else 1, "units")
        return "break"
    def on_mousewheel_selected(event):
        if os.name == 'nt':
            selected_list.yview_scroll(-1 * int(event.delta / 120), "units")
        else:
            selected_list.yview_scroll(-1 if event.num == 4 else 1, "units")
        return "break"
    listbox.bind("<MouseWheel>", on_mousewheel_listbox)
    listbox.bind("<Button-4>", on_mousewheel_listbox)
    listbox.bind("<Button-5>", on_mousewheel_listbox)
    selected_list.bind("<MouseWheel>", on_mousewheel_selected)
    selected_list.bind("<Button-4>", on_mousewheel_selected)
    selected_list.bind("<Button-5>", on_mousewheel_selected)
