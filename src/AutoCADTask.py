import pyautogui
import time
from tkinter import messagebox
import threading

class AutoCADTask:
    def __init__(self):
        self.tasks = []
        self.repeat_count = 1
        self.running = False
        self.paused = False
        self.delay_between_tasks = 0
        self.execution_thread = None
        self.special_incremental_text_value = 100
        self.special_incremental_text_base = 100

    def add_text_input(self, text, repeat=1):
        self.tasks.append(("text", text, repeat, False))

    def add_key_press(self, key, repeat=1):
        self.tasks.append(("key", key, repeat, False))

    def add_key_combo(self, *keys, repeat=1):
        self.tasks.append(("combo", keys, repeat, False))

    def add_click(self, x, y, repeat=1):
        self.tasks.append(("click", (x, y), repeat, False))

    def add_right_click(self, x, y, repeat=1):
        self.tasks.append(("right_click", (x, y), repeat, False))

    def add_scroll_click(self, x, y, repeat=1):
        self.tasks.append(("scroll_click", (x, y), repeat, False))

    def add_scroll_up(self, clicks, repeat=1):
        self.tasks.append(("scroll_up", clicks, repeat, False))

    def add_scroll_down(self, clicks, repeat=1):
        self.tasks.append(("scroll_down", clicks, repeat, False))

    def add_hold_click(self, x, y, duration, repeat=1):
        self.tasks.append(("hold_click", (x, y, duration), repeat, False))

    def add_wait(self, seconds, repeat=1):
        self.tasks.append(("wait", seconds, repeat, False))

    def add_incremental_text(self, start_value, repeat=1):
        self.tasks.append(("incremental_text", start_value, repeat, False))

    def add_special_incremental_text(self, start_value, repeat=1):
        self.tasks.append(("special_incremental_text", start_value, repeat, False))

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]

    def move_task_up(self, index):
        if 0 < index < len(self.tasks):
            self.tasks[index], self.tasks[index - 1] = self.tasks[index - 1], self.tasks[index]

    def move_task_down(self, index):
        if 0 <= index < len(self.tasks) - 1:
            self.tasks[index], self.tasks[index + 1] = self.tasks[index + 1], self.tasks[index]

    def set_repeat_count(self, count):
        self.repeat_count = count

    def set_delay_between_tasks(self, delay):
        self.delay_between_tasks = delay

    def stop_execution(self):
        self.running = False
        if self.execution_thread is not None:
            self.execution_thread.join()

    def pause_execution(self):
        self.paused = True

    def resume_execution(self):
        self.paused = False

    def execute_tasks(self):
        self.running = True
        self.execution_thread = threading.Thread(target=self._execute_tasks)
        self.execution_thread.start()

    def _execute_tasks(self):
        try:
            for i in range(self.repeat_count):
                self.special_incremental_text_value = self.special_incremental_text_base
                for task in self.tasks:
                    action, value, repeat, single_execution = task
                    if single_execution and i > 0:
                        continue
                    for _ in range(repeat):
                        while self.paused:
                            time.sleep(0.1)
                        if not self.running:
                            return
                        if action == "text":
                            pyautogui.typewrite(value)
                        elif action == "key":
                            pyautogui.press(value)
                        elif action == "combo":
                            pyautogui.hotkey(*value)
                        elif action == "click":
                            x, y = value
                            pyautogui.click(x, y)
                        elif action == "right_click":
                            x, y = value
                            pyautogui.click(x, y, button='right')
                        elif action == "scroll_click":
                            x, y = value
                            pyautogui.click(x, y, button='middle')
                        elif action == "scroll_up":
                            pyautogui.scroll(value)
                        elif action == "scroll_down":
                            pyautogui.scroll(-value)
                        elif action == "hold_click":
                            x, y, duration = value
                            pyautogui.mouseDown(x, y)
                            time.sleep(duration)
                            pyautogui.mouseUp(x, y)
                        elif action == "wait":
                            for _ in range(int(value * 10)):  # Check every 0.1 seconds
                                if not self.running:
                                    return
                                while self.paused:
                                    time.sleep(0.1)
                                time.sleep(0.1)
                            continue  # Skip the final delay and move to the next task
                        elif action == "incremental_text":
                            pyautogui.typewrite(str(value + i))
                        elif action == "special_incremental_text":
                            pyautogui.typewrite(str(self.special_incremental_text_value))
                            self.special_incremental_text_value += 1

                        for _ in range(int(self.delay_between_tasks * 10)):  # Check every 0.1 seconds
                            if not self.running:
                                return
                            while self.paused:
                                time.sleep(0.1)
                            time.sleep(0.1)
                self.special_incremental_text_base += 100
        except Exception as e:
            messagebox.showerror("Error", f"Error durante la ejecución: {str(e)}")

    def toggle_single_execution(self, index):
        if 0 <= index < len(self.tasks):
            action, value, repeat, single_execution = self.tasks[index]
            self.tasks[index] = (action, value, repeat, not single_execution)

    def change_task_repeat(self, index, new_repeat):
        if 0 <= index < len(self.tasks):
            action, value, _, single_execution = self.tasks[index]
            self.tasks[index] = (action, value, new_repeat, single_execution)

    def reset_counters(self):
        self.special_incremental_text_value = 100
        self.special_incremental_text_base = 100

