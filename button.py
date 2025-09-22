import os

import tkinter as tk
from tkinter import messagebox

class Button:
    def __init__(self, screen, text):
        self.screen = screen
        self.root_window = self.screen.root_window
        self.text = text
        self.button = None
        self.sticker_title = None

    def confirm(self, entry, popup):
        name = entry.get().strip()
        if name:
            self.screen.add_sticker(name)
            popup.destroy()
            self.sticker_title = name
        else:
            messagebox.showwarning("Aviso", "Por favor, insira um nome para o sticker")

    def disable_close(self):
        messagebox.showinfo("Atenção", "Você deve inserir o nome do primeiro sticker")

    def add_sticker_command(self, color, first_time=False):
        popup = tk.Toplevel(self.root_window)
        popup.title("Novo sticker")
        popup.geometry("250x120")
        popup.configure(bg=color.background_color)
        popup.transient(self.root_window)
        popup.grab_set()

        label = tk.Label(
            popup,
            text="Nome do novo sticker",
            bg=color.background_color,
            fg=color.text_color
        )
        label.pack(pady=(15, 5))

        entry = tk.Entry(popup, font=("Arial", 12))
        entry.pack(padx=10, fill="x")
        entry.focus_set()

        btn_add = tk.Button(
            popup,
            text="Adicionar",
            command=lambda: self.confirm(entry, popup),
            bg="#2196f3",
            fg="white",
            font=("Arial", 11, "bold")
        )
        btn_add.pack(pady=10)

        popup.bind("<Return>", lambda e: self.confirm(entry, popup))

        if first_time:
            popup.protocol("WM_DELETE_WINDOW", self.disable_close)

    def configure_add_sticker(self, color):
        self.button = tk.Button(
            self.root_window,
            text=self.text,
            command=lambda: self.add_sticker_command(color),
            bg="#00bcd4",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="raised",
            padx=12,
            pady=6,
            cursor="hand2"
        )
        self.button.place(relx=1.0, rely=1.0, anchor="se", x=-15, y=-15)
        refresh_button = tk.Button(
            self.root_window,
            text = "recarregar",
            command = self.screen.refresh_stickers,
            bg = "#37c049",
            fg = "white",
            font = ("Arial", 12, "bold"),
            relief="raised",
            padx=12,
            pady=6,
            cursor="hand2"
        )
        refresh_button.place(relx=1.0, rely=1.0, anchor="se", x=-125, y=-15)