import tkinter as tk
from tkinter import ttk, messagebox
from gui.item_selector import open_item_selector
from gui.kivitelezesi_selector import open_kivitelezesi_selector

def open_helyseg_window(parent, adat, db_handler, update_total_callback):
    win = tk.Toplevel(parent)
    win.title(adat['nev'])
    win.geometry("850x600")
    win.columnconfigure(0, weight=1)
    win.rowconfigure(0, weight=1)

    canvas = tk.Canvas(win)
    scrollbar = ttk.Scrollbar(win, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    inner_frame = ttk.Frame(canvas, padding=10)
    inner_frame.columnconfigure(0, weight=1)
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")
    inner_frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    ttk.Label(inner_frame, text=f"Helyiség: {adat['nev']}", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, sticky="w", pady=10)

    columns = ("Tétel", "Egység", "Ár", "Mennyiség", "Összesen", "Megjegyzés")

    # --- Anyag tételek (hozzáadás + törlés egy sorban) ---
    frame_anyag = ttk.LabelFrame(inner_frame, text="Anyag tételek")
    frame_anyag.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
    frame_anyag.columnconfigure(0, weight=1)

    tree_anyag = ttk.Treeview(frame_anyag, columns=columns, show="headings", height=8)
    for col in columns:
        tree_anyag.heading(col, text=col)
        tree_anyag.column(col, width=100)
    tree_anyag.grid(row=0, column=0, sticky="nsew")
    tree_anyag_scroll = ttk.Scrollbar(frame_anyag, orient="vertical", command=tree_anyag.yview)
    tree_anyag.configure(yscrollcommand=tree_anyag_scroll.set)
    tree_anyag_scroll.grid(row=0, column=1, sticky="ns")

    # GOMBOK EGY SORBAN
    anyag_btn_frame = ttk.Frame(frame_anyag)
    anyag_btn_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(4, 0))
    anyag_btn_frame.columnconfigure((0, 1), weight=1)

    ttk.Button(
        anyag_btn_frame, text="📦 Hozzáadás",
        command=lambda: open_item_selector(
            win, db_handler, lambda tetel: hozzaadott_tetel(tetel, adat['tetel_lista'])
        )
    ).grid(row=0, column=0, sticky="ew", padx=4)
    ttk.Button(
        anyag_btn_frame, text="🗑️ Törlés",
        command=lambda: delete_selected_anyag()
    ).grid(row=0, column=1, sticky="ew", padx=4)

    # --- Kivitelezési munkák (hozzáadás + törlés egy sorban) ---
    frame_kiv = ttk.LabelFrame(inner_frame, text="Kivitelezési munkák")
    frame_kiv.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
    frame_kiv.columnconfigure(0, weight=1)

    tree_kiv = ttk.Treeview(frame_kiv, columns=columns, show="headings", height=8)
    for col in columns:
        tree_kiv.heading(col, text=col)
        tree_kiv.column(col, width=100)
    tree_kiv.grid(row=0, column=0, sticky="nsew")
    tree_kiv_scroll = ttk.Scrollbar(frame_kiv, orient="vertical", command=tree_kiv.yview)
    tree_kiv.configure(yscrollcommand=tree_kiv_scroll.set)
    tree_kiv_scroll.grid(row=0, column=1, sticky="ns")

    # GOMBOK EGY SORBAN
    kiv_btn_frame = ttk.Frame(frame_kiv)
    kiv_btn_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(4, 0))
    kiv_btn_frame.columnconfigure((0, 1), weight=1)

    ttk.Button(
        kiv_btn_frame, text="🔧 Hozzáadás",
        command=lambda: open_kivitelezesi_selector(
            win, lambda tetel: hozzaadott_tetel(tetel, adat['kivitelezesi_tetelek'])
        )
    ).grid(row=0, column=0, sticky="ew", padx=4)
    ttk.Button(
        kiv_btn_frame, text="🗑️ Törlés",
        command=lambda: delete_selected_kiv()
    ).grid(row=0, column=1, sticky="ew", padx=4)

    osszeg_label = ttk.Label(inner_frame, text="Teljes összeg: 0 Ft", font=("Segoe UI", 10, "bold"))
    osszeg_label.grid(row=3, column=0, pady=5, sticky="w")

    btn_frame = ttk.Frame(inner_frame)
    btn_frame.grid(row=4, column=0, sticky="ew")
    btn_frame.columnconfigure((0, 1), weight=1)

    def delete_selected_anyag():
        selected = tree_anyag.selection()
        if selected:
            idx = tree_anyag.index(selected[0])
            if messagebox.askyesno("Törlés", "Biztosan törlöd a kiválasztott anyag tételt?"):
                del adat['tetel_lista'][idx]
                refresh_tree()
                
    def delete_selected_kiv():
        selected = tree_kiv.selection()
        if selected:
            idx = tree_kiv.index(selected[0])
            if messagebox.askyesno("Törlés", "Biztosan törlöd a kiválasztott kivitelezési tételt?"):
                del adat['kivitelezesi_tetelek'][idx]
                refresh_tree()

    ttk.Button(
        btn_frame, text="❌ Bezárás", command=win.destroy
    ).grid(row=0, column=2, sticky="ew", padx=5)

    def refresh_tree():
        tree_anyag.delete(*tree_anyag.get_children())
        tree_kiv.delete(*tree_kiv.get_children())
        total = 0

        for tetel in adat['tetel_lista']:
            osszeg = int(tetel.get("mennyiseg", 1)) * float(tetel.get("egysegar", 0))
            tree_anyag.insert("", tk.END, values=(
                tetel.get("nev", ""), tetel.get("egyseg", ""), tetel.get("egysegar", ""),
                tetel.get("mennyiseg", 1), osszeg, tetel.get("megjegyzes", "")
            ))
            total += osszeg

        for tetel in adat['kivitelezesi_tetelek']:
            osszeg = int(tetel.get("mennyiseg", 1)) * float(tetel.get("egysegar", 0))
            tree_kiv.insert("", tk.END, values=(
                tetel.get("nev", ""), tetel.get("egyseg", ""), tetel.get("egysegar", ""),
                tetel.get("mennyiseg", 1), osszeg, tetel.get("megjegyzes", "")
            ))
            total += osszeg

        osszeg_label.config(text=f"Teljes összeg: {total:,} Ft")
        update_total_callback()

    def hozzaadott_tetel(tetel, lista):
        def confirm():
            try:
                mennyiseg = int(mennyiseg_entry.get())
                lista.append({
                    "nev": tetel[0],
                    "egyseg": tetel[1],
                    "egysegar": tetel[2],
                    "mennyiseg": mennyiseg,
                    "megjegyzes": ""
                })
                refresh_tree()
                msg.destroy()
                messagebox.showinfo("Tétel hozzáadva", f"{tetel[0]} hozzáadva {mennyiseg} db.")
            except ValueError:
                messagebox.showerror("Hiba", "Érvénytelen mennyiség!")

        msg = tk.Toplevel(win)
        msg.title("Mennyiség megadása")
        ttk.Label(msg, text=f"Mennyiség a következőhöz: {tetel[0]}").pack(pady=5)
        mennyiseg_entry = ttk.Entry(msg)
        mennyiseg_entry.insert(0, "1")
        mennyiseg_entry.pack(pady=5)
        ok_btn = ttk.Button(msg, text="✅ OK", command=confirm)
        ok_btn.pack(pady=5)
        mennyiseg_entry.bind("<Return>", lambda e: confirm())
        mennyiseg_entry.focus()



    refresh_tree()
