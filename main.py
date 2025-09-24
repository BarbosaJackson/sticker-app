import tkinter as tk

from color import Color
from file_manager import FileManager
from screen import Screen

def main():
    screen = Screen(
        Color("#2e2e2e", "#f0f0f0", "#ff5555", "#ffffff", "#666666"),
        tk.Tk(),
        FileManager()
    )
    screen.configure_root_window("Stickers App", 700, 500, 200, 150)
    screen.start_screen()

if __name__ == "__main__":
    main()