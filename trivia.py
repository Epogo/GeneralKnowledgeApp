import tkinter as tk
import random
from triviaDataBase import SQLiteTriviaDb
from triviaDataBase import FirebaseTriviaDb
from usersDataBase import SQLiteUsersDb
from usersDataBase import FireBaseUsersDb
from main import MainController


class TriviaGame:
    def __init__(self, level, username, controller):
        self.questions = []
        self.current_question_index = 0
        self.score = 0
        self.window = None
        self.question_label = None
        self.answer_buttons = []
        self.timer_label = None
        self.timer_id = None
        self.level = level
        self.username = username
        self.score_window = None
        self.controller = controller
        self.trivia_db = FirebaseTriviaDb()
        self.users_db = FireBaseUsersDb()
        
    def __del__(self):
    	self.trivia_db.close()
    	self.users_db.close()

    def start_game(self):
        self.trivia_db.create_trivia_table()
        self.questions = self.trivia_db.load_questions(self.level)
        self.controller.set_num_of_questions(len(self.questions))
        self.window = tk.Tk()
        self.window.title("Trivia Game")
        self.window.geometry("500x400")

        self.question_label = tk.Label(self.window, text="")
        self.question_label.pack(pady=10)

        for i in range(4):
            button = tk.Button(
                self.window,
                text="",
                width=30,
                command=lambda i=i: self.check_answer(i),
            )
            self.answer_buttons.append(button)
            button.pack(pady=5)
            button.bind("<Enter>", self.on_button_enter)
            button.bind("<Leave>", self.on_button_leave)

        self.timer_label = tk.Label(self.window, text="")
        self.timer_label.pack(pady=10)

        self.next_question()

        self.window.mainloop()

    def next_question(self):
        if self.current_question_index < self.controller.get_num_of_questions():
            question = self.questions[self.current_question_index]

            answers = question["answers"]

            self.question_label.config(text=question["question"])
            for i, button in enumerate(self.answer_buttons):
                button.config(
                    text=answers[i],
                    highlightbackground="lightgray",
                    state=tk.NORMAL)

            self.start_timer()
        else:
            if self.window is not None:
                self.window.destroy()  # Destroy the menu window
            self.controller.set_score(self.score)
            self.controller.module_selector("end_of_game")

    def start_timer(self):
        self.timer_label.config(text="Time left: 10")
        self.timer_countdown(10)

    def timer_countdown(self, seconds):
        if seconds > 0:
            self.timer_label.config(text=f"Time left: {seconds}")
            self.timer_id = self.window.after(
                1000, self.timer_countdown, seconds - 1
            )
        else:
            self.check_answer(-1)

    def check_answer(self, index):
        if self.timer_id is not None:
            self.window.after_cancel(self.timer_id)

        question = self.questions[self.current_question_index]
        correct_answer_index = question["correct_answer"]

        if index == correct_answer_index:
            self.score += 1
            if index != -1:
                self.answer_buttons[index].config(highlightbackground="green")
        else:
            if index != -1:
                self.answer_buttons[index].config(highlightbackground="red")
            self.answer_buttons[correct_answer_index].config(
                highlightbackground="green")

        self.window.after(1500, self.clear_answers)

    def clear_answers(self):
        for button in self.answer_buttons:
            button.config(highlightbackground="lightgray", state=tk.DISABLED)
        self.current_question_index += 1
        self.window.after(1500, self.next_question)

    def end_game(self):
        self.questions = self.trivia_db.load_questions(self.level)
        num_of_questions = self.controller.get_num_of_questions()
        self.score = self.controller.get_score()

        total_score = int((self.score / num_of_questions) * 100)

        best_score = self.users_db.get_best_score(self.username)

        if total_score > best_score:
            self.users_db.update_best_score(self.username, total_score)

        self.trivia_db.close()
        self.users_db.close()

        score_window = tk.Tk()
        score_window.title("Trivia Game - Score")
        score_window.geometry("300x200")
        self.window = score_window

        score_label = tk.Label(score_window, text=f"Your Score: {total_score}")
        score_label.pack(pady=20)

        restart_button = tk.Button(
            score_window,
            text="Restart",
            command=self.restart_game)
        restart_button.pack(pady=10)

        close_button = tk.Button(
            score_window,
            text="Close",
            command=self.close_game)
        close_button.pack(pady=10)
        self.score_window = score_window

    def restart_game(self):
        if self.score_window is not None:
            self.score_window.destroy()
        self.controller.set_username(self.username)
        self.controller.module_selector("menu")

    def close_game(self):
        if self.timer_id is not None:
            self.window.after_cancel(self.timer_id)
        del self.controller
        self.window.destroy()

    def on_button_enter(self, event):
        event.widget.config(bg="lightblue")

    def on_button_leave(self, event):
        event.widget.config(bg="white")

