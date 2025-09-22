import os

from tkinter import messagebox

class FileManager:
    def create_folder(self, name):
        os.makedirs(name, exist_ok=True)
    
    def write_file(self, folder_name, file_name, text):
        with open(f"{folder_name}/{file_name}.txt", "a") as file:
            file.write(text)

    def get_files(self, folder_name):
        files = []
        for file in os.listdir(folder_name):
            if file.endswith(".txt"):
                files.append(file)
        return files

    def check_folder_exists(self):
        data = os.listdir(".")
        return "stickers" in data
    
    def check_files_exists(self):
        data = os.listdir("stickers")
        return len(data) > 0

    def read_file(self, folder_name, file_name):
        with open(f"{folder_name}/{file_name}", "r") as file:
            return file.readlines()
        
    def delete_file(self, name, popup):
        if not name.strip():
            messagebox.showwarning("Aviso", "Nenhum nome informado para apagar.")
            return

        file_path = os.path.join("stickers", f"{name}.txt")  # ajuste para o formato/pasta real
        if os.path.exists(file_path):
            os.remove(file_path)
            messagebox.showinfo("Sucesso", f"Sticker '{name}' foi apagado.")
            popup.destroy()
        else:
            messagebox.showwarning("Aviso", f"O sticker '{name}' não existe.")
