import tkinter as tk
from tkinter import ttk, messagebox

from file_manager import FileManager

class Widgets:
    def __init__(self, notebook, bg_color, fg_color, button_bg, button_fg, add_sticker_button, sticker_title, screen):
        self.notebook = notebook
        self.frame = ttk.Frame(notebook)
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.button_bg = button_bg
        self.button_fg = button_fg
        self.labels = []
        self.add_sticker_button = add_sticker_button
        self.sticker_title = sticker_title
        self.inner_frame = tk.Frame(self.frame, bg=self.bg_color)
        self.inner_frame.pack(expand=True, fill='both')
        self.screen = screen

        self.create_widgets()

    def create_widgets(self):

        close_button = tk.Button(
            self.inner_frame,
            text = "✖",
            command = self.close_tab,
            bg = self.button_bg,
            fg = self.button_fg,
            relief = "flat",
            activebackground = "#ff4444",
            font = ("Arial", 10, "bold"),
            padx = 5,
            pady = 2,
        )
        close_button.place(
            relx = 1,
            rely = 0,
            anchor = "ne",
            x = -5,
            y = 5
        )

        file_manager = FileManager()

        delete_button = tk.Button(
            self.inner_frame,
            text="deletar",
            command=lambda: file_manager.delete_file(self.sticker_title, self.frame),
            bg = self.button_bg,
            fg = self.button_fg,
            relief = "flat",
            activeforeground="#ff4444",
            font = ("Arial", 12, "bold"),
            padx=5,
            pady=2
        )
        delete_button.place(
            relx=1,
            rely=0,
            anchor="ne",
            x=-40,
            y=5
        )

        self.label_title = tk.Label(
            self.inner_frame,
            text=f"Sticker-app: Adicione seus lembretes",
            bg=self.bg_color,
            fg=self.fg_color,
            font=("Arial", 12),
            justify="left",
        )

        self.label_title.pack(padx=10, pady=(30, 10))

        input_frame = tk.Frame(self.inner_frame, bg=self.bg_color)
        input_frame.pack(padx=10, pady=5, fill="x")

        self.entry = tk.Entry(input_frame, font=("Arial", 12))
        self.entry.pack(side="left", fill="x", expand=True)

        save_button = tk.Button(
            input_frame,
            text="Salvar",
            command=self.save_text,
            bg="#4caf50",
            fg="white",
            font=("Arial", 11, "bold"),
            relief="flat",
            padx=10,
            pady=5,
        )
        save_button.pack(side="left", padx=(10, 0))

        self.labels_frame = tk.Frame(self.inner_frame, bg=self.bg_color)
        self.labels_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.inner_frame.bind("<Button-1>", lambda e: self.entry.focus_set())
        self.labels_frame.bind("<Button-1>", lambda e: self.entry.focus_set())
        self.entry.bind("<Button-1>", lambda e: self.entry.focus_set())

        self.label_title.bind("<Button-1>", self.start_move)
        self.label_title.bind("<B1-Motion>", self.do_move)

    def initial_widgets(self, lines):
        for line in lines:
            text = line.strip()
            if text:
                label = tk.Label(self.labels_frame, text=text, font=("Arial", 12), bg=self.bg_color, fg=self.fg_color, wraplength=450, justify="left")
                label.pack(anchor="w", pady=2)
                self.labels.append(label)


    def save_text(self):
        text = self.entry.get().strip()
        if not text:
            messagebox.showwarning("Aviso", "Digite algum texto antes de salvar.")
            return

        file_manager = FileManager()

        file_manager.create_folder("stickers")
        file_manager.write_file("stickers", self.sticker_title, text + "\n")

        label = tk.Label(self.labels_frame, text=text, font=("Arial", 12), bg=self.bg_color, fg=self.fg_color, wraplength=450, justify="left")
        label.pack(anchor="w", pady=2)
        self.labels.append(label)

        self.entry.delete(0, tk.END)
        self.entry.focus_set()

    def close_tab(self):
        i = 0
        for sticker in self.screen.stickers:
            if sticker.frame == self.frame:
                break
            i += 1

        del self.screen.stickers[i]

        self.notebook.forget(self.frame)
        if not self.notebook.tabs():
            messagebox.showinfo("Aviso", "Nenhum sticker restante. Adicione um novo.")

    def start_move(self, event):
        root = self.frame.winfo_toplevel()
        root._drag_x = event.x_root
        root._drag_y = event.y_root

    def do_move(self, event):
        root = self.frame.winfo_toplevel()
        dx = event.x_root - root._drag_x
        dy = event.y_root - root._drag_y
        new_x = root.winfo_x() + dx
        new_y = root.winfo_y() + dy
        root.geometry(f"+{new_x}+{new_y}")
        root._drag_x = event.x_root
        root._drag_y = event.y_root
