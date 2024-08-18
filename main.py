import os
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.font import Font
import math

def find_gamesettings_files():
    base_path = os.path.expanduser("~\\Documents\\My Games\\Rainbow Six - Siege")
    gamesettings_files = []
    for folder in os.listdir(base_path):
        if folder != "Benchmark" and os.path.isdir(os.path.join(base_path, folder)):
            file_path = os.path.join(base_path, folder, "GameSettings.ini")
            if os.path.exists(file_path):
                gamesettings_files.append(file_path)
    return gamesettings_files

def read_current_server(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("DataCenterHint="):
                return line.strip().split("=")[1]
    return "default"

def write_new_server(file_path, new_server):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    for i, line in enumerate(lines):
        if line.startswith("DataCenterHint="):
            lines[i] = f"DataCenterHint={new_server}\n"
            break
    
    with open(file_path, 'w') as file:
        file.writelines(lines)

def change_server(server):
    gamesettings_files = find_gamesettings_files()
    if not gamesettings_files:
        messagebox.showerror("Error", "No GameSettings.ini files found.")
        return
    
    for file_path in gamesettings_files:
        write_new_server(file_path, server)
    
    messagebox.showinfo("Success", f"Server changed to {servers[server]} for all accounts. Please restart the game.")

class ResponsiveUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("R6 Siege Server Changer")
        self.geometry("600x500")
        self.configure(bg='#2c3e50')
        self.minsize(400, 300)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.create_widgets()
        self.bind("<Configure>", self.on_resize)

    def create_widgets(self):
        # Styles
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Arial', 10), background='#3498db', foreground='white')
        style.map('TButton', background=[('active', '#2980b9')])

        self.title_font = Font(family="Arial", size=16, weight="bold")
        self.label_font = Font(family="Arial", size=12)
        self.button_font = Font(family="Arial", size=10)

        self.title_label = tk.Label(self, text="R6 Siege Server Changer", font=self.title_font, bg='#2c3e50', fg='white')
        self.title_label.grid(row=0, column=0, pady=20, sticky="ew")

        self.button_frame = tk.Frame(self, bg='#2c3e50')
        self.button_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.buttons = []
        for server_code, server_name in servers.items():
            button = ttk.Button(self.button_frame, text=server_name, command=lambda s=server_code: change_server(s))
            self.buttons.append(button)

        self.instructions = tk.Label(self, text="Click a server to change.\nMake sure to close the game before changing.", 
                                     font=self.label_font, bg='#2c3e50', fg='white', justify=tk.CENTER, wraplength=400)
        self.instructions.grid(row=2, column=0, pady=20, sticky="ew")

    def on_resize(self, event):
        width = self.winfo_width()
        height = self.winfo_height()

        title_size = max(16, min(24, width // 25))
        label_size = max(10, min(14, width // 40))
        button_size = max(8, min(12, width // 50))

        self.title_font.configure(size=title_size)
        self.label_font.configure(size=label_size)
        self.button_font.configure(size=button_size)

        self.title_label.config(font=self.title_font)
        self.instructions.config(font=self.label_font, wraplength=width-40)

        button_width = width - 40
        button_height = 30
        num_buttons = len(self.buttons)

        num_columns = max(2, min(3, button_width // 150))
        num_rows = math.ceil(num_buttons / num_columns)

        for i in range(self.button_frame.grid_size()[0]):
            self.button_frame.grid_columnconfigure(i, weight=0)
        for i in range(self.button_frame.grid_size()[1]):
            self.button_frame.grid_rowconfigure(i, weight=0)

        for i in range(num_columns):
            self.button_frame.grid_columnconfigure(i, weight=1)
        for i in range(num_rows):
            self.button_frame.grid_rowconfigure(i, weight=1)

        for i, button in enumerate(self.buttons):
            row = i // num_columns
            col = i % num_columns
            button.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
            button.config(width=1)  # Reset width to allow proper scaling

# Server list dictionary
servers = {
    "default": "Auto (Default)",
    "playfab/australiaeast": "Australia East",
    "playfab/brazilsouth": "Brazil South",
    "playfab/centralus": "Central US",
    "playfab/eastasia": "East Asia",
    "playfab/eastus": "East US",
    "playfab/japaneast": "Japan East",
    "playfab/northeurope": "North Europe",
    "playfab/southafricanorth": "South Africa North",
    "playfab/southcentralus": "South Central US",
    "playfab/southeastasia": "Southeast Asia",
    "playfab/uaenorth": "UAE North",
    "playfab/westeurope": "West Europe",
    "playfab/westus": "West US"
}

if __name__ == "__main__":
    app = ResponsiveUI()
    app.mainloop()