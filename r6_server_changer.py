import os
import tkinter as tk
from tkinter import messagebox
import json
from pathlib import Path

class ServerManager:
    def __init__(self):
        self.servers = {
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
        
    def find_gamesettings_files(self):
        paths = [
            Path.home() / "Documents" / "My Games" / "Rainbow Six - Siege",
            Path.home() / "OneDrive" / "Documents" / "My Games" / "Rainbow Six - Siege"
        ]
        
        files = []
        for path in paths:
            if path.exists():
                for folder in path.iterdir():
                    if folder.name != "Benchmark" and folder.is_dir():
                        file_path = folder / "GameSettings.ini"
                        if file_path.exists():
                            files.append(file_path)
        return files
    
    def read_current_server(self, file_path):
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    if line.startswith("DataCenterHint="):
                        return line.strip().split("=")[1]
        except Exception:
            pass
        return "default"
    
    def write_new_server(self, file_path, new_server):
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
            
            updated = False
            for i, line in enumerate(lines):
                if line.startswith("DataCenterHint="):
                    lines[i] = f"DataCenterHint={new_server}\n"
                    updated = True
                    break
            
            if not updated:
                lines.append(f"DataCenterHint={new_server}\n")
                
            with open(file_path, 'w') as file:
                file.writelines(lines)
            return True
        except Exception:
            return False
            
    def change_server(self, server, callback=None):
        files = self.find_gamesettings_files()
        if not files:
            messagebox.showerror("Error", "No GameSettings.ini files found.")
            return False
        
        success_count = 0
        for file_path in files:
            if self.write_new_server(file_path, server):
                success_count += 1
        
        if success_count > 0:
            messagebox.showinfo("Success", 
                               f"Server changed to {self.servers[server]} for {success_count} account(s).\n"
                               f"Please restart the game.")
            if callback:
                callback(server)
            return True
        else:
            messagebox.showerror("Error", "Failed to change server. Check file permissions.")
            return False


class ThemeManager:
    def __init__(self):
        self.themes = {
            "dark": {
                "bg": "#1e1e1e",
                "fg": "#ffffff",
                "button_bg": "#3a3a3a",
                "button_fg": "#ffffff",
                "button_active_bg": "#4a4a4a",
                "highlight_bg": "#007acc",
                "secondary_bg": "#252526",
                "border": "#333333",
                "success": "#4caf50",
                "error": "#f44336"
            },
            "light": {
                "bg": "#f5f5f5",
                "fg": "#212121",
                "button_bg": "#e0e0e0",
                "button_fg": "#212121",
                "button_active_bg": "#d0d0d0",
                "highlight_bg": "#0078d7",
                "secondary_bg": "#ffffff",
                "border": "#cccccc",
                "success": "#4caf50",
                "error": "#f44336"
            }
        }
        self.current_theme = "dark"
        
        # Try to load saved theme preference
        self.config_path = Path.home() / ".r6serverchanger"
        self.config_file = self.config_path / "config.json"
        self.load_config()
    
    def load_config(self):
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.current_theme = config.get("theme", "dark")
            except Exception:
                pass
    
    def save_config(self):
        try:
            self.config_path.mkdir(exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump({"theme": self.current_theme}, f)
        except Exception:
            pass
    
    def get_theme(self):
        return self.themes[self.current_theme]
    
    def toggle_theme(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self.save_config()
        return self.get_theme()


class AnimatedButton(tk.Canvas):
    def __init__(self, parent, text, command=None, width=120, height=40, **kwargs):
        self.theme = kwargs.pop('theme', {})
        super().__init__(parent, width=width, height=height, 
                         highlightthickness=0, **kwargs)
        self.command = command
        self.text = text
        self.width = width
        self.height = height
        
        # Animation state
        self.hover = False
        self.clicked = False
        
        # Configure
        self.bg = self.theme.get('button_bg', '#3a3a3a')
        self.fg = self.theme.get('button_fg', '#ffffff')
        self.active_bg = self.theme.get('button_active_bg', '#4a4a4a')
        self.highlight = self.theme.get('highlight_bg', '#007acc')
        
        # Create button
        self.create_rectangle(0, 0, width, height, fill=self.bg, outline="")
        self.text_id = self.create_text(width//2, height//2, text=text, fill=self.fg, font=("Segoe UI", 10))
        
        # Bind events
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        self.bind("<ButtonRelease-1>", self.on_release)
    
    def on_enter(self, event):
        self.hover = True
        self.animate()
    
    def on_leave(self, event):
        self.hover = False
        self.clicked = False
        self.animate()
    
    def on_click(self, event):
        self.clicked = True
        self.animate()
    
    def on_release(self, event):
        if self.clicked and self.hover and self.command:
            self.command()
        self.clicked = False
        self.animate()
    
    def animate(self):
        if self.clicked:
            fill = self.highlight
            self.config(cursor="hand2")
        elif self.hover:
            fill = self.active_bg
            self.config(cursor="hand2")
        else:
            fill = self.bg
            self.config(cursor="")
        
        self.itemconfig(1, fill=fill)
    
    def update_theme(self, theme):
        self.bg = theme.get('button_bg', '#3a3a3a')
        self.fg = theme.get('button_fg', '#ffffff')
        self.active_bg = theme.get('button_active_bg', '#4a4a4a')
        self.highlight = theme.get('highlight_bg', '#007acc')
        self.itemconfig(self.text_id, fill=self.fg)
        self.animate()


class ServerChangerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Initialize managers
        self.server_manager = ServerManager()
        self.theme_manager = ThemeManager()
        
        # Configure window
        self.title("R6 Siege Server Changer")
        self.geometry("650x520")
        self.minsize(400, 400)
        
        # Set icon (if available)
        try:
            self.iconbitmap("r6_icon.ico")
        except:
            pass
        
        # Create main frame
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create UI elements
        self.create_widgets()
        
        # Apply initial theme
        self.apply_theme(self.theme_manager.get_theme())
        
        # Bind resize event
        self.bind("<Configure>", self.on_resize)
    
    def create_widgets(self):
        # Title frame
        self.title_frame = tk.Frame(self.main_frame)
        self.title_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        self.title_label = tk.Label(self.title_frame, text="R6 SIEGE SERVER CHANGER", 
                                    font=("Segoe UI", 18, "bold"))
        self.title_label.pack(side=tk.LEFT, padx=10)
        
        self.theme_button = AnimatedButton(self.title_frame, text="🌓 Toggle Theme", 
                                          command=self.toggle_theme, width=120, height=30,
                                          theme=self.theme_manager.get_theme())
        self.theme_button.pack(side=tk.RIGHT, padx=10)
        
        # Status frame
        self.status_frame = tk.Frame(self.main_frame)
        self.status_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.status_label = tk.Label(self.status_frame, text="Current Status:", 
                                    font=("Segoe UI", 10))
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        self.current_server_label = tk.Label(self.status_frame, text="Checking...", 
                                           font=("Segoe UI", 10, "bold"))
        self.current_server_label.pack(side=tk.LEFT, padx=5)
        
        # Separator
        self.separator = tk.Frame(self.main_frame, height=2)
        self.separator.pack(fill=tk.X, padx=30, pady=10)
        
        # Server buttons frame
        self.server_frame = tk.Frame(self.main_frame)
        self.server_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create 3 columns for server buttons
        for i in range(3):
            self.server_frame.columnconfigure(i, weight=1)
        
        # Create buttons for each server
        self.server_buttons = {}
        row, col = 0, 0
        max_cols = 3
        
        for code, name in self.server_manager.servers.items():
            button = AnimatedButton(self.server_frame, text=name, 
                                   command=lambda s=code: self.server_manager.change_server(s, self.update_status),
                                   width=180, height=40, theme=self.theme_manager.get_theme())
            button.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
            self.server_buttons[code] = button
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # Footer with instructions
        self.footer_frame = tk.Frame(self.main_frame)
        self.footer_frame.pack(fill=tk.X, padx=20, pady=20)
        
        self.instructions = tk.Label(self.footer_frame, 
                                    text="Click a server to change. Make sure the game is closed before changing servers.",
                                    font=("Segoe UI", 9), wraplength=600, justify=tk.CENTER)
        self.instructions.pack(fill=tk.X, padx=10)
        
        # Init status
        self.after(100, self.update_status)
    
    def update_status(self, selected_server=None):
        files = self.server_manager.find_gamesettings_files()
        
        if not files:
            self.current_server_label.config(text="No game installation found")
            return
        
        if selected_server:
            server_name = self.server_manager.servers.get(selected_server, "Unknown")
            self.current_server_label.config(text=f"{server_name}")
            return
            
        # Read current server from first file
        current = self.server_manager.read_current_server(files[0])
        server_name = self.server_manager.servers.get(current, "Unknown")
        self.current_server_label.config(text=f"{server_name}")
    
    def toggle_theme(self):
        theme = self.theme_manager.toggle_theme()
        self.apply_theme(theme)
    
    def apply_theme(self, theme):
        # Main background
        self.configure(bg=theme["bg"])
        self.main_frame.configure(bg=theme["bg"])
        
        # Title
        self.title_frame.configure(bg=theme["bg"])
        self.title_label.configure(bg=theme["bg"], fg=theme["fg"])
        
        # Status
        self.status_frame.configure(bg=theme["bg"])
        self.status_label.configure(bg=theme["bg"], fg=theme["fg"])
        self.current_server_label.configure(bg=theme["bg"], fg=theme["highlight_bg"])
        
        # Separator
        self.separator.configure(bg=theme["border"])
        
        # Server buttons frame
        self.server_frame.configure(bg=theme["bg"])
        
        # Update buttons
        for button in self.server_buttons.values():
            button.update_theme(theme)
        
        # Theme button
        self.theme_button.update_theme(theme)
        
        # Footer
        self.footer_frame.configure(bg=theme["bg"])
        self.instructions.configure(bg=theme["bg"], fg=theme["fg"])
    
    def on_resize(self, event=None):
        # This ensures the UI adjusts when resized
        width = self.winfo_width()
        
        # Adjust fonts based on window size
        title_size = max(14, min(18, width // 30))
        self.title_label.configure(font=("Segoe UI", title_size, "bold"))
        
        # Adjust wraplength
        self.instructions.configure(wraplength=width - 60)


if __name__ == "__main__":
    app = ServerChangerApp()
    app.mainloop()