import tkinter as tk
from menu import open_menu
from gen_question import QuestionGenerator
from usersDataBase import SQLiteUsersDb
from usersDataBase import FireBaseUsersDb
import pygame
import threading

class MusicPlayer(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True

    def run(self):

        # Load and play the background music
        pygame.mixer.music.load("music.mp3")
        pygame.mixer.music.play(-1)  # -1 means play the music on loop

        while True:
            # Keep the thread alive to continue playing the music
            continue

class MainController:
    mixer_initialized = False  # Class-level variable to track mixer initialization

    def __init__(self, username=None, score=None, level=None):
        pygame.init()
        if not MainController.mixer_initialized:
            pygame.mixer.init()
            MainController.mixer_initialized = True
        self.username = username
        self.level = level
        self.score = score
        self.num_of_questions = 0
        self.best_score = 0
        self.users_db = FireBaseUsersDb()

    def start_music_thread(self):
        music_thread = MusicPlayer()
        music_thread.start()

    def __del__(self):
        # Stop the music and quit pygame when the controller is deleted
        if MainController.mixer_initialized:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            MainController.mixer_initialized = False
            pygame.quit()

    def start(self):
        from app import launch_game
        launch_game()

    def set_level(self, level):
        self.level = level

    def set_score(self, score):
        self.score = score

    def set_username(self, username):
        self.username = username

    def set_score(self, score):
        self.score = score

    def set_num_of_questions(self, num):
        self.num_of_questions = num

    def get_num_of_questions(self):
        return self.num_of_questions

    def get_score(self):
        return self.score

    def get_best_score(self, username):
        return self.users_db.get_best_score(username)

    def module_selector(self, module):
        from trivia import TriviaGame  # Import inside the method to avoid circular import
        if module == "login":
            main_controller = MainController()
            main_controller.start()
        elif module == "menu":
            open_menu(self.username, self.score, self)
        elif module == "generator":
            admin = QuestionGenerator(self)
            admin.show_window()
        elif module == "trivia":
            game = TriviaGame(self.level, self.username, self)
            game.start_game()
        elif module == "end_of_game":
            game = TriviaGame(self.level, self.username, self)
            game.end_game()


if __name__ == "__main__":
    main_controller = MainController()
    main_controller.start_music_thread()
    main_controller.start()

