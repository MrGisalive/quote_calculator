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
