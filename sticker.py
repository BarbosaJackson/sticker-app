import tkinter as tk
from tkinter import ttk, messagebox

class EntryToLabelsSticker:
    def __init__(self, notebook, bg_color, fg_color, button_bg, button_fg):
        self.notebook = notebook
        self.frame = ttk.Frame(notebook)
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.button_bg = button_bg
        self.button_fg = button_fg
        self.labels = []

        self.create_widgets()

    def create_widgets(self):
        self.inner_frame = tk.Frame(self.frame, bg=self.bg_color)
        self.inner_frame.pack(expand=True, fill='both')

        self.close_button = tk.Button(
            self.inner_frame,
            text="✖",
            command=self.close_tab,
            bg=self.button_bg,
            fg=self.button_fg,
            relief="flat",
            activebackground="#ff4444",
            font=("TkDefaultFont", 10, "bold"),
            padx=5,
            pady=2,
        )
        self.close_button.place(relx=1, rely=0, anchor="ne", x=-5, y=5)

        self.label_title = tk.Label(
            self.inner_frame,
            text="Sticker: Entry + salvar para labels",
            bg=self.bg_color,
            fg=self.fg_color,
            font=("TkDefaultFont", 12),
            justify="left",
        )
        self.label_title.pack(padx=10, pady=(30, 10))

        input_frame = tk.Frame(self.inner_frame, bg=self.bg_color)
        input_frame.pack(padx=10, pady=5, fill="x")

        self.entry = tk.Entry(input_frame, font=("TkDefaultFont", 12))
        self.entry.pack(side="left", fill="x", expand=True)

        save_button = tk.Button(
            input_frame,
            text="Salvar",
            command=self.save_text,
            bg="#4caf50",
            fg="white",
            font=("TkDefaultFont", 11, "bold"),
            relief="flat",
            padx=10,
            pady=5,
        )
        save_button.pack(side="left", padx=(10, 0))

        self.labels_frame = tk.Frame(self.inner_frame, bg=self.bg_color)
        self.labels_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Ao clicar em qualquer lugar, traz foco pro Entry
        self.inner_frame.bind("<Button-1>", lambda e: self.entry.focus_set())
        self.labels_frame.bind("<Button-1>", lambda e: self.entry.focus_set())
        self.entry.bind("<Button-1>", lambda e: self.entry.focus_set())

        # Bind para arrastar janela
        self.label_title.bind("<Button-1>", self.start_move)
        self.label_title.bind("<B1-Motion>", self.do_move)

    def save_text(self):
        texto = self.entry.get().strip()
        if not texto:
            messagebox.showwarning("Aviso", "Digite algum texto antes de salvar.")
            return

        label = tk.Label(self.labels_frame, text=texto, font=("TkDefaultFont", 12), bg=self.bg_color, fg=self.fg_color, wraplength=450, justify="left")
        label.pack(anchor="w", pady=2)
        self.labels.append(label)

        self.entry.delete(0, tk.END)
        self.entry.focus_set()

    def close_tab(self):
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
        x = root.winfo_x() + dx
        y = root.winfo_y() + dy
        root.geometry(f"+{x}+{y}")
        root._drag_x = event.x_root
        root._drag_y = event.y_root

# Funções para redimensionamento da janela
def start_resize(event):
    root._resize_x = event.x
    root._resize_y = event.y
    root._orig_width = root.winfo_width()
    root._orig_height = root.winfo_height()

def do_resize(event):
    dx = event.x - root._resize_x
    dy = event.y - root._resize_y
    new_width = max(300, root._orig_width + dx)
    new_height = max(200, root._orig_height + dy)
    root.geometry(f"{new_width}x{new_height}")

# Variável global para controlar se é a primeira criação
first_sticker_created = False

def open_add_popup(first_time=False):
    popup = tk.Toplevel(root)
    popup.title("Novo Sticker")
    popup.geometry("250x120")
    popup.configure(bg=bg_color)
    popup.transient(root)
    popup.grab_set()

    label = tk.Label(popup, text="Nome do novo sticker:", bg=bg_color, fg=fg_color)
    label.pack(pady=(15, 5))

    entry = tk.Entry(popup, font=("TkDefaultFont", 12))
    entry.pack(padx=10, fill="x")
    entry.focus_set()

    def confirmar():
        global first_sticker_created
        nome = entry.get().strip()
        if nome:
            add_sticker(nome)
            popup.destroy()
            first_sticker_created = True
            print("criou o sticker  ")
        else:
            messagebox.showwarning("Aviso", "Por favor, insira um nome válido.")

    btn = tk.Button(popup, text="Adicionar", command=confirmar, bg="#2196f3", fg="white", font=("TkDefaultFont", 11, "bold"))
    btn.pack(pady=10)
    popup.bind("<Return>", lambda e: confirmar())

    # Se for na inicialização, bloqueia fechamento até adicionar o sticker
    if first_time:
        def disable_close():
            messagebox.showinfo("Atenção", "Você deve inserir o nome do primeiro sticker para continuar.")
        popup.protocol("WM_DELETE_WINDOW", disable_close)


# --- Configuração da janela principal ---
bg_color = "#2e2e2e"
fg_color = "#f0f0f0"
button_bg = "#ff5555"
button_fg = "#ffffff"
resize_color = "#666666"

root = tk.Tk()
root.title("Stickers em Abas com Entry + Labels")
root.wm_attributes("-topmost", True)
root.geometry("500x400+300+300")

# Container que segura o notebook e o botão "+"
notebook_container = tk.Frame(root, bg=bg_color)
notebook_container.pack(side="top", fill="x", padx=5, pady=5)

# Notebook (aba)
notebook = ttk.Notebook(notebook_container)
notebook.pack(side="left", fill="x", expand=True)

# Lista para armazenar os stickers
stickers = []

def add_sticker(name):
    new_sticker = EntryToLabelsSticker(notebook, bg_color, fg_color, button_bg, button_fg)
    notebook.add(new_sticker.frame, text=name)
    notebook.select(new_sticker.frame)
    stickers.append(new_sticker)
    root.after(100, lambda: new_sticker.entry.focus_set())

# Adiciona o primeiro sticker
# add_sticker("Sticker 1")

# Foco no primeiro campo após carregar
def focus_after_load():
    stickers[0].entry.focus_set()

if len(stickers) > 0:
    root.after(100, focus_after_load)

# Resize handle
resize_handle = tk.Frame(root, bg=resize_color, cursor="bottom_right_corner", width=15, height=15)
resize_handle.pack(side="right", anchor="se", padx=3, pady=3)
resize_handle.bind("<Button-1>", start_resize)
resize_handle.bind("<B1-Motion>", do_resize)

btn_add_corner = tk.Button(
    root,
    text="Adicionar Sticker",
    command=open_add_popup,
    bg="#00bcd4",
    fg="white",
    font=("TkDefaultFont", 12, "bold"),
    relief="raised",
    padx=12,
    pady=6,
    cursor="hand2"
)
btn_add_corner.place(relx=1.0, rely=1.0, anchor="se", x=-15, y=-15)

open_add_popup(first_time=True)
root.mainloop()
