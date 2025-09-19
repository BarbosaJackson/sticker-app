import tkinter as tk                     # importa o módulo tkinter com o alias "tk" (widgets básicos)
from tkinter import ttk, messagebox      # importa ttk (widgets temáticos) e messagebox (diálogos de mensagem)

from color import Color
from button import Button

class Screen:
    def __init__(self, color, root_window):
        self.color = color
        self.root_window = root_window
        self.first_sticker_created = False
        self.notebook_container = self.configure_notebook_container(root_window)
        self.notebook = self.configure_notebook()
        self.stickers = []
        self.resize_handle = self.configure_resize_handle()
    
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
    
    def focus_after_load():                                           # função que foca o primeiro Entry após o carregamento
        self.stickers[0].entry.focus_set()                            # foca no entry do primeiro sticker (assume que exista pelo índice 0)
    
    def configure_resize_handle(self):
        resize_handle = tk.Frame(self.root_window, bg=self.color.resize_color, cursor="bottom_right_corner", width=15, height=15)  # pequeno frame no canto para redimensionar manualmente
        resize_handle.pack(side="right", anchor="se", padx=3, pady=3) # empacota o handle no canto inferior direito
        resize_handle.bind("<Button-1>", self.start_resize)               # bind para iniciar redimensionamento (ao clicar)
        resize_handle.bind("<B1-Motion>", self.do_resize)                 # bind para fazer o redimensionamento enquanto arrasta
        return resize_handle
    
    def add_sticker(self, name):
        new_sticker = None
        self.notebook.add(new_sticker.frame, text=name)
        self.notebook.select(new_sticker.frame)
        self.stickers.append(new_sticker)
        self.root_window.after(100, lambda: new_sticker.entry.focus_set())

    def start_screen(self):
        self.root_window.mainloop()


color = Color("#2e2e2e", "#f0f0f0", "#ff5555", "#ffffff", "#666666")
screen = Screen(color, tk.Tk())
screen.configure_root_window("Stickers App", 500, 400, 300, 300)
button = Button(screen, "Adicionar")
button.configure_add_sticker(color)
screen.start_screen()

#if len(stickers) > 0:                                        # se já houver stickers na lista
#    root.after(100, focus_after_load)                        # agenda foco inicial (não será executado porque stickers está vazio)
