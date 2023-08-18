import tkinter as tk
from tkinter import messagebox
import os
from triviaDataBase import SQLiteTriviaDb
from triviaDataBase import FirebaseTriviaDb
from gen_db import new_questions_db

class QuestionGenerator:
    def __init__(self, controller):
        self.controller = controller
        self.window = tk.Tk()
        self.window.title("Question Generator")
        self.window.geometry("800x800")  # Set window size
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)

        self.question_entry = None
        self.answer_entries = []
        self.correct_answer_var = None
        self.difficulty_var = None
        self.trivia_db = FirebaseTriviaDb()

        self.create_widgets()

    def create_widgets(self):
        # Create the question label and entry
        question_label = tk.Label(self.window, text="Question:")
        question_label.pack()
        self.question_entry = tk.Entry(self.window, width=50)
        self.question_entry.pack()

        # Create the answer labels and entries
        for i in range(4):
            answer_label = tk.Label(self.window, text=f"Answer {i+1}:")
            answer_label.pack()
            answer_entry = tk.Entry(self.window, width=50)
            answer_entry.pack()
            self.answer_entries.append(answer_entry)

        # Create the correct answer label and radio buttons
        correct_answer_label = tk.Label(self.window, text="Correct Answer:")
        correct_answer_label.pack()
        self.correct_answer_var = tk.IntVar()
        for i in range(4):
            radio_button = tk.Radiobutton(
                self.window,
                text=f"Answer {i+1}",
                variable=self.correct_answer_var,
                value=i)
            radio_button.pack()

        # Create the difficulty label and radio buttons
        difficulty_label = tk.Label(self.window, text="Difficulty:")
        difficulty_label.pack()
        self.difficulty_var = tk.StringVar()
        difficulties = ["Easy", "Medium", "Hard"]
        for difficulty in difficulties:
            radio_button = tk.Radiobutton(
                self.window,
                text=difficulty,
                variable=self.difficulty_var,
                value=difficulty)
            radio_button.pack()

        # Create the submit button
        submit_button = tk.Button(
            self.window,
            text="Submit",
            command=self.add_question)
        submit_button.pack(pady=10)

        # Create the red button to erase database and generate new questions
        red_button = tk.Button(
            self.window,
            text="Erase Database and Generate New Questions",
            bg="red",
            command=self.ask_confirmation)
        red_button.pack(pady=20)

        # Create the close button
        close_button = tk.Button(
            self.window,
            text="Close",
            command=self.close_window)
        close_button.pack()

    def ask_confirmation(self):
        response = messagebox.askyesno(
            "Confirmation", "Are you sure you want to erase the database?")
        if response:
            self.erase_database_and_generate_questions()

    def erase_database_and_generate_questions(self):
        self.trivia_db.erase_database_and_generate_questions()

    def add_question(self):
        question = self.question_entry.get()
        answers = [entry.get() for entry in self.answer_entries]
        correct_answer = self.correct_answer_var.get()
        difficulty = self.difficulty_var.get()

        if not question or any(
                answer == "" for answer in answers) or correct_answer == -1 or difficulty == "":
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Insert the question into the database
        if self.trivia_db.insert_question(
            question, answers, correct_answer, difficulty):
            # Clear the input fields
            self.question_entry.delete(0, tk.END)
            for entry in self.answer_entries:
                entry.delete(0, tk.END)
            self.correct_answer_var.set(0)
            self.difficulty_var.set("Easy")

            messagebox.showinfo("Success", "Question added successfully.")
        else:
            messagebox.showerror(
                "Error", "Failed to add question to the database.")

    def show_window(self):
        self.window.mainloop()

    def close_window(self):
        self.window.destroy()
        self.controller.module_selector("login")

if __name__ == "__main__":
    class MainController:
        def __init__(self):
            pass

        def module_selector(self, module):
            if module == "menu":
                print("Switching to menu module...")
                # Perform actions for the menu module
            elif module == "trivia":
                print("Switching to trivia module...")
                # Perform actions for the trivia module
            else:
                print("Invalid module.")

    controller = MainController()
    QuestionGenerator(controller).show_window()

