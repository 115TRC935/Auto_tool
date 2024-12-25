import tkinter as tk
from tkinter import messagebox
import json
from CustomDialog import CustomDialog
from config import COLORS_PATH

# Load colors from colors.json
with open(COLORS_PATH, "r") as file:
    colors = json.load(file)

class TaskManager:
    def __init__(self, task_manager, task_list):
        self.task_manager = task_manager
        self.task_list = task_list

    def add_text_task(self):
        dialog = CustomDialog(self.task_list.master, title="Texto", prompt="Ingrese el texto:")
        text = dialog.result
        if text:
            self.task_manager.add_text_input(text)
            self.task_list.insert(tk.END, f"Texto: {text} x1")

    def add_key_task(self):
        dialog = CustomDialog(self.task_list.master, title="Tecla", prompt="Ingrese la tecla:")
        key = dialog.result
        if key:
            self.task_manager.add_key_press(key)
            self.task_list.insert(tk.END, f"Tecla: {key} x1")

    def add_combo_task(self):
        dialog = CustomDialog(self.task_list.master, title="Combinación", prompt="Ingrese teclas separadas por comas:")
        keys = dialog.result
        if keys:
            keys = keys.split(',')
            self.task_manager.add_key_combo(*keys)
            self.task_list.insert(tk.END, f"Combo: {keys} x1")

    def add_click_task(self):
        dialog_x = CustomDialog(self.task_list.master, title="Click", prompt="Ingrese posición X:")
        x = dialog_x.result
        if x is not None:
            try:
                x = int(x)
                dialog_y = CustomDialog(self.task_list.master, title="Click", prompt="Ingrese posición Y:")
                y = dialog_y.result
                if y is not None:
                    y = int(y)
                    self.task_manager.add_click(x, y)
                    self.task_list.insert(tk.END, f"Click: ({x}, {y}) x1")
            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese números válidos")

    def add_right_click_task(self):
        dialog_x = CustomDialog(self.task_list.master, title="Click Derecho", prompt="Ingrese posición X:")
        x = dialog_x.result
        if x is not None:
            try:
                x = int(x)
                dialog_y = CustomDialog(self.task_list.master, title="Click Derecho", prompt="Ingrese posición Y:")
                y = dialog_y.result
                if y is not None:
                    y = int(y)
                    self.task_manager.add_right_click(x, y)
                    self.task_list.insert(tk.END, f"Click Derecho: ({x}, {y}) x1")
            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese números válidos")

    def add_scroll_click_task(self):
        dialog_x = CustomDialog(self.task_list.master, title="Click Scroll", prompt="Ingrese posición X:")
        x = dialog_x.result
        if x is not None:
            try:
                x = int(x)
                dialog_y = CustomDialog(self.task_list.master, title="Click Scroll", prompt="Ingrese posición Y:")
                y = dialog_y.result
                if y is not None:
                    y = int(y)
                    self.task_manager.add_scroll_click(x, y)
                    self.task_list.insert(tk.END, f"Click Scroll: ({x}, {y}) x1")
            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese números válidos")

    def add_scroll_up_task(self):
        clicks = self.ask_integer_dialog("Scroll Arriba", "Ingrese el número de clicks:")
        if clicks is not None:
            try:
                clicks = int(clicks)
                self.task_manager.add_scroll_up(clicks)
                self.task_list.insert(tk.END, f"Scroll Arriba: {clicks} clicks x1")
            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese un número válido")

    def add_scroll_down_task(self):
        clicks = self.ask_integer_dialog("Scroll Abajo", "Ingrese el número de clicks:")
        if clicks is not None:
            try:
                clicks = int(clicks)
                self.task_manager.add_scroll_down(clicks)
                self.task_list.insert(tk.END, f"Scroll Abajo: {clicks} clicks x1")
            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese un número válido")

    def add_wait_task(self):
        dialog = CustomDialog(self.task_list.master, title="Espera", prompt="Ingrese segundos:")
        seconds = dialog.result
        if seconds is not None:
            try:
                seconds = float(seconds)
                self.task_manager.add_wait(seconds)
                self.task_list.insert(tk.END, f"Espera: {seconds}s x1")
            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese un número válido")

    def add_incremental_text_task(self):
        dialog = CustomDialog(self.task_list.master, title="Texto Incremental", prompt="Ingrese el valor inicial:")
        start_value = dialog.result
        if start_value is not None:
            try:
                start_value = int(start_value)
                self.task_manager.add_incremental_text(start_value)
                self.task_list.insert(tk.END, f"Texto Incremental: {start_value} x1")
            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese un número válido")

    def add_special_incremental_text_task(self):
        dialog = CustomDialog(self.task_list.master, title="Texto Incremental Especial", prompt="Ingrese el valor inicial:")
        start_value = dialog.result
        if start_value is not None:
            try:
                start_value = int(start_value)
                self.task_manager.add_special_incremental_text(start_value)
                self.task_list.insert(tk.END, f"Texto Incremental Especial: {start_value} x1")
            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese un número válido")

    def add_hold_click_task(self):
        dialog_x = CustomDialog(self.task_list.master, title="Mantener Click", prompt="Ingrese posición X:")
        x = dialog_x.result
        if x is not None:
            try:
                x = int(x)
                dialog_y = CustomDialog(self.task_list.master, title="Mantener Click", prompt="Ingrese posición Y:")
                y = dialog_y.result
                if y is not None:
                    y = int(y)
                    dialog_duration = CustomDialog(self.task_list.master, title="Mantener Click", prompt="Ingrese duración (segundos):")
                    duration = dialog_duration.result
                    if duration is not None:
                        try:
                            duration = float(duration)
                            self.task_manager.add_hold_click(x, y, duration)
                            self.task_list.insert(tk.END, f"Mantener Click: ({x}, {y}) por {duration}s x1")
                        except ValueError:
                            messagebox.showerror("Error", "Por favor ingrese una duración válida")
            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese números válidos")

    def delete_task(self):
        try:
            selected = self.task_list.curselection()[0]
            self.task_manager.delete_task(selected)
            self.task_list.delete(selected)
        except IndexError:
            messagebox.showerror("Error", "Seleccione una tarea para borrar.", parent=self.task_list.master)

    def move_task_up(self):
        try:
            selected = self.task_list.curselection()[0]
            self.task_manager.move_task_up(selected)
            self.update_task_list()
        except IndexError:
            messagebox.showerror("Error", "Seleccione una tarea para mover.", parent=self.task_list.master)

    def move_task_down(self):
        try:
            selected = self.task_list.curselection()[0]
            self.task_manager.move_task_down(selected)
            self.update_task_list()
        except IndexError:
            messagebox.showerror("Error", "Seleccione una tarea para mover.", parent=self.task_list.master)

    def update_task_list(self):
        self.task_list.delete(0, tk.END)
        for task in self.task_manager.tasks:
            action, value, repeat, single_execution = task
            display_text = f"{action}: {value} x{repeat}"
            if single_execution:
                display_text += " (single)"
            self.task_list.insert(tk.END, display_text)

    def ask_integer_dialog(self, title, prompt):
        dialog = CustomDialog(self.task_list.master, title=title, prompt=prompt)
        result = dialog.result
        if result is not None:
            try:
                return int(result)
            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese un número válido")
        return None
