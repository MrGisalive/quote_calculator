import tkinter as tk
from tkinter import ttk, messagebox
from .item_selector import open_item_selector
from .kivitelezesi_selector import open_kivitelezesi_selector
from gui.utils import center_window

def open_helyseg_window(parent, adat, db_handler, update_total_callback):
    """
    Egy helyiséghez tartozó részletező ablak. Anyag és kivitelezési tételek kezelése.
    """
    win = tk.Toplevel(parent)
    win.title(adat['nev'])
    win.geometry("850x600")
    center_window(win, 850, 600)

    # ---- Vissza gomb TOPBAR ----
    style = ttk.Style(win)
    style.configure('Vissza.TButton', font=('Arial', 13, 'bold'))
    topbar = ttk.Frame(win)
    topbar.pack(side="top", fill="x", padx=0, pady=(0, 8))

    def on_vissza():
        win.destroy()
    btn_vissza = ttk.Button(topbar, text="⬅️ Vissza", command=on_vissza, style='Vissza.TButton')
    btn_vissza.pack(side="left", padx=12, pady=8)

    # ---- Canvas, belső tartalom gördülővel ----
    win.columnconfigure(0, weight=1)
    win.rowconfigure(0, weight=1)
    canvas = tk.Canvas(win)
    canvas.pack(fill="both", expand=True, side="top")
    scrollbar = ttk.Scrollbar(win, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.place(relx=1.0, rely=0, relheight=1.0, anchor="ne")

    # Belső tartalom
    inner_frame = ttk.Frame(canvas, padding=10)
    inner_frame.columnconfigure(0, weight=1)
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")
    inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    ttk.Label(inner_frame, text=f"Helyiség: {adat['nev']}", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, sticky="w", pady=10)

    columns = ("Tétel", "Egység", "Ár", "Mennyiség", "Összesen", "Megjegyzés")

    # --- Anyag tételek panel ---
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

    # Anyag gombok egy sorban
    anyag_btn_frame = ttk.Frame(frame_anyag)
    anyag_btn_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(4, 0))
    anyag_btn_frame.columnconfigure((0, 1), weight=1)
    ttk.Button(
        anyag_btn_frame, text="📦 Hozzáadás",
        command=lambda: open_item_selector(
            win, db_handler, lambda tetelek: hozzaadott_tetel(tetelek, adat['tetel_lista'])
        )
    ).grid(row=0, column=0, sticky="ew", padx=4)
    ttk.Button(
        anyag_btn_frame, text="🗑️ Törlés",
        command=lambda: delete_selected_anyag()
    ).grid(row=0, column=1, sticky="ew", padx=4)

    # --- Kivitelezési munkák panel ---
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

    # Kivitelezési gombok egy sorban
    kiv_btn_frame = ttk.Frame(frame_kiv)
    kiv_btn_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(4, 0))
    kiv_btn_frame.columnconfigure((0, 1), weight=1)
    ttk.Button(
        kiv_btn_frame, text="🔧 Hozzáadás",
        command=lambda: open_kivitelezesi_selector(
            win, lambda tetelek: hozzaadott_tetel(tetelek, adat['kivitelezesi_tetelek'])
        )
    ).grid(row=0, column=0, sticky="ew", padx=4)
    ttk.Button(
        kiv_btn_frame, text="🗑️ Törlés",
        command=lambda: delete_selected_kiv()
    ).grid(row=0, column=1, sticky="ew", padx=4)

    # Összeg és lezáró gomb
    osszeg_label = ttk.Label(inner_frame, text="Teljes összeg: 0 Ft", font=("Segoe UI", 10, "bold"))
    osszeg_label.grid(row=3, column=0, pady=5, sticky="w")

    btn_frame = ttk.Frame(inner_frame)
    btn_frame.grid(row=4, column=0, sticky="ew")
    btn_frame.columnconfigure((0, 1), weight=1)
    ttk.Button(
        btn_frame, text="❌ Bezárás", command=win.destroy
    ).grid(row=0, column=2, sticky="ew", padx=5)

    # --- Belső függvények ---

    def delete_selected_anyag():
        """
        Kijelölt anyag tétel törlése megerősítéssel.
        """
        selected = tree_anyag.selection()
        if selected:
            idx = tree_anyag.index(selected[0])
            if messagebox.askyesno("Törlés", "Biztosan törlöd a kiválasztott anyag tételt?"):
                del adat['tetel_lista'][idx]
                refresh_tree()
                
    def delete_selected_kiv():
        """
        Kijelölt kivitelezési tétel törlése megerősítéssel.
        """
        selected = tree_kiv.selection()
        if selected:
            idx = tree_kiv.index(selected[0])
            if messagebox.askyesno("Törlés", "Biztosan törlöd a kiválasztott kivitelezési tételt?"):
                del adat['kivitelezesi_tetelek'][idx]
                refresh_tree()

    def refresh_tree():
        """
        Mindkét tábla és az összeg frissítése, a jelenlegi helyiség-adatok alapján.
        """
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

    def hozzaadott_tetel(tetelek, lista):
        """
        Listához több új tétel hozzáadása (akár anyag, akár kivitelezés).
        """
        try:
            for tetel in tetelek:
                lista.append({
                    "nev": tetel[0],
                    "egyseg": tetel[1],
                    "egysegar": tetel[2],
                    "mennyiseg": tetel[3],
                    "megjegyzes": ""
                })
            refresh_tree()
            messagebox.showinfo("Tétel(ek) hozzáadva", f"{len(tetelek)} tétel(ek) sikeresen hozzáadva.")
        except Exception as e:
            messagebox.showerror("Hiba", f"Hiba történt a tétel(ek) hozzáadásakor: {e}")

    # Mindig töltsük újra a táblákat indításkor!
    refresh_tree()
