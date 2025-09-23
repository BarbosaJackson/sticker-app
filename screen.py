import tkinter as tk
from tkinter import ttk

from color import Color
from button import Button
from widgets import Widgets
from file_manager import FileManager

class Screen:
    def __init__(self, color, root_window, file_control):
        self.file_control = file_control
        self.color = color
        self.root_window = root_window
        self.first_sticker_created = False
        self.notebook_container = self.configure_notebook_container(root_window)
        self.notebook = self.configure_notebook()
        self.stickers = []
        self.resize_handle = self.configure_resize_handle()
        self.add_sticker_button = self.configure_add_sticker_button()
        self.configure_load_stickers()
    
    def configure_root_window(self, title, width, height, pos_x, pos_y):
        self.root_window.title(title)
        self.root_window.wm_attributes("-topmost", True)
        self.root_window.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

    def configure_notebook_container(self, root_window):
        notebook_container = tk.Frame(root_window, bg=color.background_color) # frame que contém o notebook (ajuda layout)
        notebook_container.pack(side="top", fill="x", padx=5, pady=5)   # empacota o container no topo, preenchendo horizontalmente
        return notebook_container

    def configure_notebook(self):
        notebook = ttk.Notebook(self.notebook_container)                  # cria o widget Notebook (abas) com pai notebook_container
        notebook.pack(side="left", fill="x", expand=True)  
        return notebook

    def start_resize(self, event):
        self.root_window._resize_x = event.x
        self.root_window._resize_y = event.y
        self.root_window._orig_width = self.root_window.winfo_width()
        self.root_window._orig_height = self.root_window.winfo_height()

    def do_resize(self, event):
        dx = event.x - self.root_window._resize_x
        dy = event.y - self.root_window._resize_y
        new_width = max(300, self.root_window._orig_width + dx)
        new_height = max(300, self.root_window._orig_height + dy)
        self.root_window.geometry(f"{new_width}x{new_height}")
    
    def focus_after_load(self):
        if len(self.stickers) > 0:
            self.stickers[0].entry.focus_set()
    
    def configure_resize_handle(self):
        resize_handle = tk.Frame(
            self.root_window, 
            bg=self.color.resize_color, 
            cursor="bottom_right_corner", 
            width=15, 
            height=15
        )
        resize_handle.pack(side="right", anchor="se", padx=3, pady=3)
        resize_handle.bind("<Button-1>", self.start_resize)
        resize_handle.bind("<B1-Motion>", self.do_resize)
        return resize_handle

    def load_stickers_exists(self):
        files = self.file_control.get_files("stickers")
        for file in files:
            sticker_name = file[:-4]
            new_sticker = Widgets(
                self.notebook,
                self.color.background_color,
                self.color.text_color,
                self.color.button_background_color,
                self.color.button_text_color,
                self.add_sticker_button,
                sticker_name,
                self
            )
            new_sticker.initial_widgets(self.file_control.read_file("stickers", file))
            self.notebook.add(new_sticker.frame, text=sticker_name)
            self.notebook.select(new_sticker.frame)
            self.stickers.append(new_sticker)
            self.root_window.after(100, lambda: new_sticker.entry.focus_set())

    def configure_load_stickers(self):
        if self.file_control.check_folder_exists() and self.file_control.check_files_exists():
            self.load_stickers_exists()
        else:
            self.add_sticker_button.add_sticker_command(color)

    def configure_add_sticker_button(self):
        add_sticker_button = Button(self, "Adicionar")
        add_sticker_button.configure_add_sticker(color)
        return add_sticker_button

    def add_sticker(self, name):
        new_sticker = Widgets(
            self.notebook,
            self.color.background_color,
            self.color.text_color,
            self.color.button_background_color,
            self.color.button_text_color,
            self.add_sticker_button,
            name,
            self
        )
        self.notebook.add(new_sticker.frame, text=name)
        self.notebook.select(new_sticker.frame)
        self.stickers.append(new_sticker)
        self.root_window.after(100, lambda: new_sticker.entry.focus_set())

    def start_screen(self):
        self.focus_after_load()
        self.root_window.mainloop()

    def refresh_stickers(self):
        current_tabs = self.notebook.tabs()

        for sticker in self.stickers:
            if str(sticker.frame) in current_tabs:  # só remove se ainda existir
                self.notebook.forget(sticker.frame)
        self.stickers.clear()
        self.load_stickers_exists()


color = Color("#2e2e2e", "#f0f0f0", "#ff5555", "#ffffff", "#666666")
screen = Screen(color, tk.Tk(), FileManager())
screen.configure_root_window("Stickers App", 700, 500, 200, 150)
screen.start_screen()
