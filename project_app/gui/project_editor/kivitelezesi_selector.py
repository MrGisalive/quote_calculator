import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from gui.utils import center_window

def open_kivitelezesi_selector(parent, callback):
    """
    Kivitelezési munkadíjtételek kiválasztó ablak, teljesen reszponzív és görgethető, fejlett stornóval.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    json_path = os.path.join(base_dir, 'data', 'kivitelezesi_tetelek.json')

    print(f"[DEBUG] Loading JSON from: {json_path}")

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            items = json.load(f)
        print(f"[DEBUG] {len(items)} kivitelezési tétel betöltve.")
    except Exception as e:
        print(f"[DEBUG] Hiba kivitelezési tételek betöltésekor: {e}")
        messagebox.showerror("Hiba", f"Nem sikerült betölteni a kivitelezési tételeket: {str(e)}")
        return

    selected_items = []
    selector = tk.Toplevel(parent)
    selector.title("Kivitelezési munkák kiválasztása")
    selector.geometry("900x600")
    center_window(selector, 900, 600)
    selector.minsize(700, 400)
    selector.grab_set()

    main_frame = ttk.Frame(selector)
    main_frame.pack(fill="both", expand=True)
    main_frame.rowconfigure(1, weight=4)
    main_frame.rowconfigure(3, weight=2)
    main_frame.columnconfigure(0, weight=1)

    # --- Topbar ---
    topbar = ttk.Frame(main_frame)
    topbar.grid(row=0, column=0, sticky="ew", pady=(8, 4))
    style = ttk.Style(selector)
    style.configure('Vissza.TButton', font=('Arial', 13, 'bold'))
    style.configure('ListButton.TButton', font=('Arial', 13, 'bold'), padding=8)
    style.configure('Remove.TButton', font=('Arial', 12, 'bold'), background="#f4c2c2", foreground="black")
    style.map('Remove.TButton', background=[('active', '#f29ca3')])
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
    def increment_qty():
        try:
            qty = int(qty_var.get())
            qty_var.set(qty + 1)
        except ValueError:
            qty_var.set(1)
    def decrement_qty():
        try:
            qty = int(qty_var.get())
            if qty > 1:
                qty_var.set(qty - 1)
        except ValueError:
            qty_var.set(1)
    def validate_qty(*args):
        try:
            val = int(qty_var.get())
            if val < 1:
                qty_var.set(1)
        except:
            qty_var.set(1)
    qty_var.trace_add("write", validate_qty)

    ttk.Label(action_frame, text="Darabszám:", font=('Arial', 13, 'bold')).pack(side="left", padx=(0, 8))
    qty_frame = ttk.Frame(action_frame)
    qty_frame.pack(side="left", padx=(0, 16))
    ttk.Button(qty_frame, text="➖", width=2, command=decrement_qty).pack(side="left")
    qty_entry = ttk.Entry(qty_frame, textvariable=qty_var, width=5, font=('Arial', 13, 'bold'), justify="center")
    qty_entry.pack(side="left", padx=4)
    ttk.Button(qty_frame, text="➕", width=2, command=increment_qty).pack(side="left")
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

    # --- Szoros szerkesztő frame a stornohoz ---
    edit_frame = ttk.Frame(bottom_frame)
    edit_frame.grid(row=2, column=0, sticky="ew", pady=(4, 0))

    btn_minus = ttk.Button(edit_frame, text="➖", width=2)
    btn_minus.pack(side="left", padx=(2, 2))

    edit_qty_var = tk.IntVar(value=1)
    edit_qty_entry = ttk.Entry(edit_frame, textvariable=edit_qty_var, width=4, font=('Arial', 12), justify="center")
    edit_qty_entry.pack(side="left", padx=(2, 2))

    btn_plus = ttk.Button(edit_frame, text="➕", width=2)
    btn_plus.pack(side="left", padx=(2, 8))

    btn_storno = ttk.Button(edit_frame, text="Storno", style='Remove.TButton')
    btn_storno.pack(side="left", padx=(2, 2))

    btn_delete = ttk.Button(edit_frame, text="Tétel törlése", style='Remove.TButton')
    btn_delete.pack(side="left", padx=(2, 2))

    # --- Funkciók a szerkesztéshez ---
    def update_selected_qty_entry(*args):
        sel = selected_list.curselection()
        if sel:
            idx = sel[0]
            _, _, _, qty = selected_items[idx]
            edit_qty_var.set(1)  # Mindig 1, ha új tétel, vagy ha rákattintunk visszaáll 1-re
        else:
            edit_qty_var.set(1)
    def set_selected_qty_from_entry():
        pass  # Most nem szükséges, a storno_gomb már elvégzi a logikát
    def increment_selected_qty():
        edit_qty_var.set(edit_qty_var.get() + 1)
    def decrement_selected_qty():
        if edit_qty_var.get() > 1:
            edit_qty_var.set(edit_qty_var.get() - 1)
    def storno_selected_qty():
        sel = selected_list.curselection()
        if not sel:
            return
        idx = sel[0]
        try:
            storno_amount = int(edit_qty_var.get())
            if storno_amount < 1:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Hibás érték", "Adj meg legalább 1 darabot stornozáshoz.")
            return
        name, unit, price, qty = selected_items[idx]
        new_qty = qty - storno_amount
        if new_qty > 0:
            selected_items[idx] = (name, unit, price, new_qty)
            update_selected_list()
            selected_list.selection_set(idx)
            selected_list.activate(idx)
        else:
            selected_items.pop(idx)
            update_selected_list()
            # ha maradt még sor, próbáljuk a következőt vagy az utolsót kijelölni
            if selected_list.size() > 0:
                new_idx = min(idx, selected_list.size()-1)
                selected_list.selection_set(new_idx)
                selected_list.activate(new_idx)
        edit_qty_var.set(1)
    def delete_selected_item():
        sel = selected_list.curselection()
        if sel:
            idx = sel[0]
            selected_items.pop(idx)
            update_selected_list()
            edit_qty_var.set(1)

    btn_minus.config(command=decrement_selected_qty)
    btn_plus.config(command=increment_selected_qty)
    btn_storno.config(command=storno_selected_qty)
    btn_delete.config(command=delete_selected_item)
    # Ha enterrel módosítanád az input mezőt
    edit_qty_entry.bind("<Return>", lambda e: storno_selected_qty())

    selected_list.bind("<<ListboxSelect>>", lambda e: update_selected_qty_entry())

    # --- Véglegesítés gomb ---
    finalize_btn = ttk.Button(main_frame, text="✅ Kiválasztottak hozzáadása",
                              style='ListButton.TButton',
                              command=lambda: (callback(selected_items), selector.destroy()))
    finalize_btn.grid(row=4, column=0, pady=6, sticky="ew", padx=180)

    # --- Lista szűrés, frissítés, hozzáadás ---
    def search_items(query):
        q = query.lower()
        filtered = [
            item for item in items
            if q in item.get('nev', '').lower()
            or q in item.get('egyseg', '').lower()
            or q in str(item.get('egysegar', ''))
        ]
        print(f"[DEBUG] {len(filtered)} tétel találat a keresésre: '{query}'")
        return filtered

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
                qty_var.set(1)  # Hozzáadás után reset
                return
        selected_items.append((item['nev'], item['egyseg'], item['egysegar'], qty))
        update_selected_list()
        qty_var.set(1)  # Hozzáadás után reset

    selected_list.config(font=("Consolas", 12))  # vagy Courier New
    def update_selected_list():
        selected_list.delete(0, tk.END)
        for name, unit, price, qty in selected_items:
            sor = f"{name:32.32} | {unit:^7} |  x{qty:>3} | {price:>7} Ft/db"
            selected_list.insert(tk.END, sor)

    # --- Eseménykötések ---
    add_btn.config(command=add_to_selected)
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
