import tkinter as tk
from gui.main_menu import open_main_menu

def main():
    root = tk.Tk()
    root.title("Árajánlat Készítő")
    root.geometry("400x300")
    open_main_menu(root)
    root.mainloop()

if __name__ == "__main__":
    main()
