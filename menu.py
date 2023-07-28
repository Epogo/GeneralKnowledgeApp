import tkinter as tk
from tkinter import ttk
import sys


class MenuWindow:
    def __init__(self, username, controller):
        self.window = tk.Tk()
        self.window.title("Menu")
        self.window.geometry("300x200")
        self.username = username
        self.controller = controller
        self.best_score = controller.get_best_score(username)

        # Create a label to display the username and best score
        username_label = tk.Label(
            self.window,
            text=f"Welcome, {username}!\nBest Score: {self.best_score}")
        username_label.pack(pady=10)

        # Create a frame to hold the buttons
        button_frame = ttk.Frame(self.window)
        button_frame.pack(pady=10)

        # Create a custom style for the buttons
        style = ttk.Style()
        style.configure(
            "MenuButton.TButton",
            foreground="white",
            background="#4CAF50",
            font=("Arial", 12, "bold"))  # Specify font as keyword argument

        # Create buttons for trivia game levels
        easy_button = ttk.Button(
            button_frame,
            text="Easy",
            style="MenuButton.TButton",
            command=lambda: self.start_game("Easy"))
        easy_button.pack(side="left", padx=5)

        medium_button = ttk.Button(
            button_frame,
            text="Medium",
            style="MenuButton.TButton",
            command=lambda: self.start_game("Medium"))
        medium_button.pack(side="left", padx=5)

        hard_button = ttk.Button(
            button_frame,
            text="Hard",
            style="MenuButton.TButton",
            command=lambda: self.start_game("Hard"))
        hard_button.pack(side="left", padx=5)

        self.window.protocol("WM_DELETE_WINDOW", self.close_menu)

    def start_game(self, level):
        self.window.destroy()  # Destroy the menu window
        self.controller.set_level(level)
        self.controller.module_selector("trivia")

    def close_menu(self):
        self.window.destroy()  # Destroy the menu window
        sys.exit()


def open_menu(username, best_score, controller):
    menu_window = MenuWindow(username, controller)
    menu_window.window.mainloop()

