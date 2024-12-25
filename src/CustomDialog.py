import tkinter as tk
from tkinter import simpledialog
import json
import os
import sys
from config import ICON_PATH, COLORS_PATH

# Load colors from colors.json
with open(COLORS_PATH, "r") as file:
    colors = json.load(file)

class CustomDialog(simpledialog.Dialog):
    def __init__(self, parent, title=None, prompt=None):
        self.prompt = prompt
        self.bg_color = colors['bg_color']  # Background color from colors.json
        self.button_color = colors['button_color']  # Button color from colors.json
        self.text_color = colors['text_color']  # Text color from colors.json
        super().__init__(parent, title)

    def body(self, master):
        self.attributes("-topmost", True)
        # Set custom icon for the dialog
        if os.path.exists(ICON_PATH):
            self.iconbitmap(ICON_PATH)
        # Configure dialog colors
        self.configure(bg=self.bg_color)
        master.configure(bg=self.bg_color)
        
        # Label with the prompt
        label = tk.Label(master, text=self.prompt, bg=self.bg_color, fg=self.text_color)
        label.grid(row=0, padx=10, pady=5)
        
        # Entry for input
        self.entry = tk.Entry(master, bg=colors['entry_bg_color'], fg=self.text_color, insertbackground=self.text_color)
        self.entry.grid(row=1, padx=10, pady=5)
        
        return self.entry

    def buttonbox(self):
        # Create a custom frame for the buttons
        box = tk.Frame(self, bg=self.bg_color)
        box.pack(fill='x', padx=5, pady=5)

        # OK button
        ok_button = tk.Button(box, text="OK", width=10, command=self.ok, 
                            bg=self.button_color, fg=self.text_color,
                            activebackground=self.button_color, activeforeground=self.text_color)
        ok_button.pack(side='left', padx=5, pady=5)
        
        # Cancel button
        cancel_button = tk.Button(box, text="Cancel", width=10, command=self.cancel,
                                bg=self.button_color, fg=self.text_color,
                                activebackground=self.button_color, activeforeground=self.text_color)
        cancel_button.pack(side='right', padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

    def apply(self):
        self.result = self.entry.get()

    def get_resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)