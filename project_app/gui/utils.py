def center_window(win, width=None, height=None, y_offset=100):
    win.update_idletasks()  # Frissít, hogy pontos méret legyen

    w = width or win.winfo_width()
    h = height or win.winfo_height()

    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()

    x = int((screen_w - w) / 2)
    y = int((screen_h - h) / 2) - y_offset
    if y < 0:
        y = 0  # Ne menjen fel a képernyő teteje fölé
    win.geometry(f"{w}x{h}+{x}+{y}")

def open_folder_in_explorer(folder_path, parent=None):
    import sys, os, subprocess
    from tkinter import messagebox
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    try:
        if sys.platform.startswith('win'):
            os.startfile(folder_path)
        elif sys.platform.startswith('darwin'):
            subprocess.Popen(['open', folder_path])
        else:
            subprocess.Popen(['xdg-open', folder_path])
    except Exception as e:
        messagebox.showerror("Hiba", f"Nem sikerült megnyitni a mappát:\n{e}", parent=parent)
