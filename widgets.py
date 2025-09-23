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

        self.top_frame = tk.Frame(self.frame, bg=self.bg_color)
        self.top_frame.pack(fill="x")

        self.canvas = tk.Canvas(self.frame, bg=self.bg_color, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.bg_color)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event):
            # Windows e Mac
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        # Linux (algumas distros usam Button-4 e Button-5)
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)  
        self.canvas.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))

        self.create_widgets()

    def create_widgets(self):

        close_button = tk.Button(
            self.top_frame,
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
            self.top_frame,
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
            self.top_frame,
            text=f"Sticker-app: Adicione seus lembretes",
            bg=self.bg_color,
            fg=self.fg_color,
            font=("Arial", 12),
            justify="left",
        )

        self.label_title.pack(padx=10, pady=(30, 10))

        input_frame = tk.Frame(self.top_frame, bg=self.bg_color)
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

        self.labels_frame = tk.Frame(self.scrollable_frame, bg=self.bg_color)
        self.labels_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.inner_frame.bind("<Button-1>", lambda e: self.entry.focus_set())
        self.labels_frame.bind("<Button-1>", lambda e: self.entry.focus_set())
        self.entry.bind("<Button-1>", lambda e: self.entry.focus_set())

        self.label_title.bind("<Button-1>", self.start_move)
        self.label_title.bind("<B1-Motion>", self.do_move)

    def toggle_done(self, label, text):
        # checa se já está riscado
        current_font = label.cget("font")
        if "overstrike" in current_font:
            label.config(font=("Arial", 12))
        else:
            label.config(font=("Arial", 12, "overstrike"))

        # regrava o arquivo inteiro com estados atualizados
        file_manager = FileManager()
        file_manager.create_folder("stickers")

        with open(f"stickers/{self.sticker_title}.txt", "w") as f:
            for lbl, original_text in self.labels:
                is_done = "overstrike" in lbl.cget("font")
                status = "1" if is_done else "0"
                f.write(f"{status}|{original_text}\n")

    def add_label(self, text, done=False):
        item_frame = tk.Frame(self.labels_frame, bg=self.bg_color)
        item_frame.pack(anchor="center", pady=2, fill="x")

        font_style = ("Arial", 12, "overstrike") if done else ("Arial", 12)

        content_frame = tk.Frame(item_frame, bg=self.bg_color)
        content_frame.pack(anchor="center", fill="x", padx=100)

        label = tk.Label(
            content_frame, 
            text=text, 
            font=font_style, 
            bg=self.bg_color, 
            fg=self.fg_color, 
            wraplength=400, 
            justify="left",
            anchor="w"
        )
        label.grid(row=0, column=0, sticky="w")

        toggle_button = tk.Button(
            content_frame,
            text="✔",
            command=lambda: self.toggle_done(label, text),
            bg=self.button_bg,
            fg=self.button_fg,
            relief="flat",
            width=3
        )
        toggle_button.grid(row=0, column=1, sticky="e", padx=5)
        
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=0)
        
        self.labels.append((label, text))
        
    def initial_widgets(self, items):
       for done, text in items:
        self.add_label(text, done)

    def save_text(self):
        text = self.entry.get().strip()
        if not text:
            messagebox.showwarning("Aviso", "Digite algum texto antes de salvar.")
            return

        file_manager = FileManager()

        file_manager.create_folder("stickers")
        file_manager.write_file("stickers", self.sticker_title, text + "\n")
        self.add_label(text, done=False)

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
