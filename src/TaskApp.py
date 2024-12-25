import pyautogui
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageDraw
import pystray
import threading
import os
import sys
import json
from CustomDialog import CustomDialog
from AutoCADTask import AutoCADTask
from config import ICON_PATH, COLORS_PATH
from TaskManager import TaskManager

# Load colors from colors.json
with open(COLORS_PATH, "r") as file:
    colors = json.load(file)


class TaskApp:
    def __init__(self, root):
        self.task_manager = AutoCADTask()
        self.root = root
        self.root.title("AutoTool")

        # Set background color and transparency
        self.root.configure(bg=colors['bg_color'])
        self.root.wm_attributes('-alpha', 0.9)
        self.root.attributes("-topmost", True)
        
        # Adjust the width of the window
        self.root.geometry("320x600")

        # Set custom icon for the window
        if os.path.exists(ICON_PATH):
            self.root.iconbitmap(ICON_PATH)

        # Ensure menus are always on top
        self.root.option_add('*Menu.tearOff', 0)
        self.root.option_add('*Menu.topmost', 1)

        self.task_list = tk.Listbox(root, width=50, height=15, bg=colors['listbox_bg_color'], fg=colors['text_color'])
        self.task_list.pack(pady=10)

        self.add_delete_frame = tk.Frame(root, bg=colors['bg_color'])
        self.add_delete_frame.pack(pady=5)

        self.move_up_button = tk.Button(self.add_delete_frame, text="↑", command=self.move_task_up, bg=colors['button_color'], fg=colors['text_color'])
        self.move_up_button.pack(side=tk.LEFT, padx=5)

        self.move_down_button = tk.Button(self.add_delete_frame, text="↓", command=self.move_task_down, bg=colors['button_color'], fg=colors['text_color'])
        self.move_down_button.pack(side=tk.LEFT, padx=5)

        self.add_menu_button = tk.Menubutton(self.add_delete_frame, text="Añadir", relief=tk.RAISED, bg=colors['button_color'], fg=colors['text_color'])
        self.add_menu = tk.Menu(self.add_menu_button, tearoff=0, bg=colors['menu_bg_color'], fg=colors['text_color'])
        self.add_menu_button.config(menu=self.add_menu)

        self.add_menu.add_command(label="Añadir Texto", command=self.add_text_task)
        self.add_menu.add_command(label="Añadir Tecla", command=self.add_key_task)
        self.add_menu.add_command(label="Añadir Combo", command=self.add_combo_task)
        self.add_menu.add_command(label="Añadir Click", command=self.add_click_task)
        self.add_menu.add_command(label="Añadir Click Derecho", command=self.add_right_click_task)
        self.add_menu.add_command(label="Añadir Click Scroll", command=self.add_scroll_click_task)
        self.add_menu.add_command(label="Añadir Scroll Arriba", command=self.add_scroll_up_task)
        self.add_menu.add_command(label="Añadir Scroll Abajo", command=self.add_scroll_down_task)
        self.add_menu.add_command(label="Añadir Mantener Click", command=self.add_hold_click_task)
        self.add_menu.add_command(label="Añadir Espera", command=self.add_wait_task)
        self.add_menu.add_command(label="Añadir Texto Incremental", command=self.add_incremental_text_task)
        self.add_menu.add_command(label="Añadir Texto Incremental Especial", command=self.add_special_incremental_text_task)

        self.add_menu_button.pack(side=tk.LEFT, padx=5)

        self.edit_button = tk.Menubutton(self.add_delete_frame, text="Editar Tarea", relief=tk.RAISED, bg=colors['button_color'], fg=colors['text_color'])
        self.edit_menu = tk.Menu(self.edit_button, tearoff=0, bg=colors['menu_bg_color'], fg=colors['text_color'])
        self.edit_button.config(menu=self.edit_menu)

        self.edit_menu.add_command(label="Borrar Tarea", command=self.delete_task)
        self.edit_menu.add_command(label="Ejecución Única", command=self.toggle_single_execution)
        self.edit_menu.add_command(label="Cambiar Repeticiones", command=self.change_task_repeat)

        self.edit_button.pack(side=tk.LEFT, padx=5)

        self.repeat_delay_frame = tk.Frame(root, bg=colors['bg_color'])
        self.repeat_delay_frame.pack(pady=5)

        self.repeat_button = tk.Button(self.repeat_delay_frame, text="Repetir", command=self.set_repeat, bg=colors['button_color'], fg=colors['text_color'])
        self.repeat_button.pack(side=tk.LEFT, padx=5)

        self.delay_button = tk.Button(self.repeat_delay_frame, text="Delay", command=self.set_delay, bg=colors['button_color'], fg=colors['text_color'])
        self.delay_button.pack(side=tk.LEFT, padx=5)

        self.execute_stop_frame = tk.Frame(root, bg=colors['bg_color'])
        self.execute_stop_frame.pack(pady=5)

        self.execute_button = tk.Button(self.execute_stop_frame, text="Ejecutar", command=self.execute_tasks, bg=colors['button_color'], fg=colors['text_color'])
        self.execute_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = tk.Button(self.execute_stop_frame, text="Pausar", command=self.pause_execution, bg=colors['button_color'], fg=colors['text_color'])
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(self.execute_stop_frame, text="Detener", command=self.stop_execution, bg=colors['button_color'], fg=colors['text_color'])
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.cursor_label = tk.Label(root, text="Posición del cursor: X=0, Y=0", bg=colors['bg_color'], fg=colors['text_color'])
        self.cursor_label.pack(pady=5)

        self.file_menu_button = tk.Menubutton(root, text="Archivo", relief=tk.RAISED, bg=colors['button_color'], fg=colors['text_color'])
        self.file_menu = tk.Menu(self.file_menu_button, tearoff=0, bg=colors['menu_bg_color'], fg=colors['text_color'])
        self.file_menu_button.config(menu=self.file_menu)

        self.file_menu.add_command(label="Guardar Tareas", command=self.save_tasks)
        self.file_menu.add_command(label="Cargar Tareas", command=self.load_tasks)
        self.file_menu.add_command(label="Exportar Script", command=self.export_script)

        self.file_menu_button.pack(pady=5)

        self.update_cursor_position()

        # Setup tray icon
        self.setup_tray_icon()

        # Secondary window for pause and stop buttons
        self.secondary_window = None

        self.task_manager_ui = TaskManager(self.task_manager, self.task_list)

    def show_secondary_window(self):
        if self.secondary_window is None:
            self.secondary_window = tk.Toplevel(self.root)
            self.secondary_window.title("Control")
            self.secondary_window.geometry(f"320x80+{self.root.winfo_x() + 10}+{self.root.winfo_y() + self.execute_stop_frame.winfo_y() + 10}")
            self.secondary_window.configure(bg=colors['bg_color'])
            self.secondary_window.attributes("-topmost", True)
            self.secondary_window.overrideredirect(True)  # Remove title bar
            if os.path.exists(ICON_PATH):
                self.secondary_window.iconbitmap(ICON_PATH)

            button_frame = tk.Frame(self.secondary_window, bg=colors['bg_color'])
            button_frame.pack(expand=True, padx=10, pady=10)

            execute_button = tk.Button(button_frame, text="Ejecutar", command=self.execute_tasks, bg=colors['button_color'], fg=colors['text_color'])
            execute_button.pack(side=tk.LEFT, padx=5)

            self.secondary_pause_button = tk.Button(button_frame, text="Pausar", command=self.pause_execution, bg=colors['button_color'], fg=colors['text_color'])
            self.secondary_pause_button.pack(side=tk.LEFT, padx=5)

            stop_button = tk.Button(button_frame, text="Detener", command=self.stop_execution, bg=colors['button_color'], fg=colors['text_color'])
            stop_button.pack(side=tk.LEFT, padx=5)

    def hide_secondary_window(self):
        if self.secondary_window is not None:
            self.secondary_window.destroy()
            self.secondary_window = None

    def execute_tasks(self):
        self.root.withdraw()
        self.show_secondary_window()
        self.task_manager.execute_tasks()

    def pause_execution(self):
        if self.task_manager.paused:
            self.task_manager.resume_execution()
            self.pause_button.config(text="Pausar")
            if self.secondary_pause_button:
                self.secondary_pause_button.config(text="Pausar")
        else:
            self.task_manager.pause_execution()
            self.pause_button.config(text="Reanudar")
            if self.secondary_pause_button:
                self.secondary_pause_button.config(text="Reanudar")

    def stop_execution(self):
        def stop_task():
            if self.task_manager.running:
                self.task_manager.stop_execution()
            self.task_manager.reset_counters()
            self.pause_button.config(text="Pausar")
            if self.secondary_pause_button:
                self.secondary_pause_button.config(text="Pausar")
            self.root.deiconify()
            self.hide_secondary_window()

        threading.Thread(target=stop_task).start()

    def show_custom_dialog(self, title, prompt):
        """Muestra un diálogo personalizado que siempre está por encima"""
        dialog = CustomDialog(self.root, title=title, prompt=prompt)
        return dialog.result

    def ask_integer_dialog(self, title, prompt):
        dialog = CustomDialog(self.root, title=title, prompt=prompt)
        result = dialog.result
        if result is not None:
            try:
                return int(result)
            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese un número válido")
        return None

    def add_text_task(self):
        self.task_manager_ui.add_text_task()

    def add_key_task(self):
        self.task_manager_ui.add_key_task()

    def add_combo_task(self):
        self.task_manager_ui.add_combo_task()

    def add_click_task(self):
        self.task_manager_ui.add_click_task()

    def add_right_click_task(self):
        self.task_manager_ui.add_right_click_task()

    def add_scroll_click_task(self):
        self.task_manager_ui.add_scroll_click_task()

    def add_scroll_up_task(self):
        self.task_manager_ui.add_scroll_up_task()

    def add_scroll_down_task(self):
        self.task_manager_ui.add_scroll_down_task()

    def add_wait_task(self):
        self.task_manager_ui.add_wait_task()

    def add_incremental_text_task(self):
        self.task_manager_ui.add_incremental_text_task()

    def add_special_incremental_text_task(self):
        self.task_manager_ui.add_special_incremental_text_task()

    def add_hold_click_task(self):
        self.task_manager_ui.add_hold_click_task()

    def delete_task(self):
        self.task_manager_ui.delete_task()

    def move_task_up(self):
        self.task_manager_ui.move_task_up()

    def move_task_down(self):
        self.task_manager_ui.move_task_down()

    def update_task_list(self):
        self.task_manager_ui.update_task_list()

    def toggle_single_execution(self):
        try:
            selected = self.task_list.curselection()[0]
            self.task_manager.toggle_single_execution(selected)
            self.update_task_list()
        except IndexError:
            messagebox.showerror("Error", "Seleccione una tarea para cambiar su modo de ejecución.", parent=self.root)

    def set_repeat(self):
        dialog = CustomDialog(self.root, title="Repetir", prompt="¿Cuántas veces desea que se ejecute la serie de instrucciones?")
        count = dialog.result
        if count is not None:
            try:
                count = int(count)
                self.task_manager.set_repeat_count(count)
            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese un número válido")

    def set_delay(self):
        dialog = CustomDialog(self.root, title="Delay", prompt="Ingrese el delay entre tareas (segundos):")
        delay = dialog.result
        if delay is not None:
            try:
                delay = float(delay)
                self.task_manager.set_delay_between_tasks(delay)
            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese un número válido")

    def update_cursor_position(self):
        x, y = pyautogui.position()
        self.cursor_label.config(text=f"Posición del cursor: X={x}, Y={y}")
        self.root.after(100, self.update_cursor_position)

    def save_tasks(self):
        try:
            with open("tasks.txt", "w") as file:
                for task in self.task_manager.tasks:
                    file.write(f"{task}\n")
            messagebox.showinfo("Guardado", "Tareas guardadas exitosamente.", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar tareas: {str(e)}", parent=self.root)

    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as file:
                self.task_manager.tasks.clear()
                self.task_list.delete(0, tk.END)
                for line in file:
                    action, value, repeat, single_execution = eval(line.strip())
                    self.task_manager.tasks.append((action, value, repeat, single_execution))
                    self.task_list.insert(tk.END, f"{action}: {value} x{repeat}")
            messagebox.showinfo("Cargado", "Tareas cargadas exitosamente.", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar tareas: {str(e)}", parent=self.root)

    def export_script(self):
        try:
            filename = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py")])
            if filename:
                with open(filename, "w") as file:
                    file.write("import pyautogui\nimport time\n")
                    for task in self.task_manager.tasks:
                        action, value, repeat, single_execution = task
                        if action == "text":
                            file.write(f"pyautogui.typewrite('{value}')\n")
                        elif action == "key":
                            file.write(f"pyautogui.press('{value}')\n")
                        elif action == "combo":
                            keys = ', '.join([f'\"{k}\"' for k in value])
                            file.write(f"pyautogui.hotkey({keys})\n")
                        elif action == "click":
                            x, y = value
                            file.write(f"pyautogui.click({x}, {y})\n")
                        elif action == "wait":
                            file.write(f"time.sleep({value})\n")
                messagebox.showinfo("Exportado", "Script exportado exitosamente.", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar script: {str(e)}", parent=self.root)

    def create_default_icon(self):
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), color='black')
        dc = ImageDraw.Draw(image)
        margin = 4
        dc.ellipse([margin, margin, width - margin, height - margin], fill='white')
        return image

    def get_resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def quit_window(self, icon, item):
        icon.stop()
        self.root.quit()
        os._exit(0)

    def setup_tray_icon(self):
        try:
            icon_path = self.get_resource_path("config/brand-amigo.ico")
            if os.path.exists(icon_path):
                image = Image.open(icon_path)
            else:
                image = self.create_default_icon()

            menu = pystray.Menu(
                pystray.MenuItem("Salir", self.quit_window)
            )
            self.icon = pystray.Icon("AutoTool", image, "AutoTool", menu)
            tray_thread = threading.Thread(target=self.icon.run)
            tray_thread.daemon = True
            tray_thread.start()
        except Exception as e:
            print(f"Error al configurar el icono: {e}")

    def change_task_repeat(self):
        try:
            selected = self.task_list.curselection()[0]
            new_repeat = self.ask_integer_dialog("Cambiar Repeticiones", "Ingrese cuántas veces se repetirá esta tarea:")
            if new_repeat is not None:
                self.task_manager.change_task_repeat(selected, new_repeat)
                self.update_task_list()
        except IndexError:
            messagebox.showerror("Error", "Seleccione una tarea para cambiar sus repeticiones.", parent=self.root)
