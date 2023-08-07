import tkinter as tk
from tkinter import messagebox
from usersDataBase import SQLiteUsersDb
from usersDataBase import FireBaseUsersDb
from gen_question import QuestionGenerator
from main import MainController


def create_user_table():
    users_db = FireBaseUsersDb()
    users_db.create_user_table()


def sign_up():
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        status_label.config(
            text="Please enter a username and password.",
            fg="red")
        return

    user = users_db.get_user(username)

    if user:
        status_label.config(
            text="Username already exists. Please choose a different one.",
            fg="red")
    else:
        users_db.create_user(username, password)
        status_label.config(text="Sign up successful!", fg="green")
        # Clear the username and password fields
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)

    users_db.close()


def login():
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        status_label.config(
            text="Please enter a username and password.",
            fg="red")
        return

    user = users_db.get_user(username)

    if user and user['password'] == password:
        status_label.config(text="Login successful!", fg="green")
        best_score = users_db.get_best_score(username)
        is_admin = user['is_admin']
        # Clear the username and password fields
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)

        # Call the proceed function after a 2-second delay
        window.after(2000, lambda: proceed(username, best_score, is_admin))

    else:
        status_label.config(text="Invalid username or password.", fg="red")

    users_db.close()


def proceed(username, best_score, is_admin):
    window.destroy()  # Close the current window
    if not is_admin:
        controller = MainController(username, best_score)
        controller.module_selector("menu")
    else:
        controller = MainController()
        controller.module_selector("generator")


def launch_game():
    # Create the main window
    global window
    global users_db
    users_db = FireBaseUsersDb()
    window = tk.Tk()
    window.title("Login/Sign-up App")
    window.geometry("400x350")

    # Create the username label and entry
    username_label = tk.Label(window, text="Username:")
    username_label.pack()
    global username_entry
    username_entry = tk.Entry(window)
    username_entry.pack()

    # Create the password label and entry
    password_label = tk.Label(window, text="Password:")
    password_label.pack()
    global password_entry
    password_entry = tk.Entry(window, show="*")
    password_entry.pack()

    # Create the login button
    login_button = tk.Button(window, text="Login", command=login)
    login_button.pack(pady=10)

    # Create the sign-up button
    signup_button = tk.Button(window, text="Sign Up", command=sign_up)
    signup_button.pack(pady=5)

    # Create the status label
    global status_label
    status_label = tk.Label(window, text="")
    status_label.pack()

    # Create the user table in the database if it doesn't exist and add the
    # admin user
    create_user_table()

    # Create the stylish and beautiful text
    text_label = tk.Label(
        window,
        text="Created by Evgeni Pogoster",
        fg="blue",
        font=("Arial", 12, "bold"),
        pady=10
    )
    text_label.pack()

    # Start the main loop
    window.mainloop()


if __name__ == "__main__":
    launch_game()

