import sqlite3
import random
from abc import ABC, abstractmethod


class TriviaDb(ABC):
    @abstractmethod
    def create_trivia_table(self):
        pass

    @abstractmethod
    def insert_question(self, question, answers, correct_answer, difficulty):
        pass

    @abstractmethod
    def load_questions(self, difficulty):
        pass

    @abstractmethod   
    def close(self):
        pass


class SQLiteTriviaDb(TriviaDb):
    def __init__(self):
        self.conn = sqlite3.connect("trivia.db")
        self.cursor = self.conn.cursor()

    def create_trivia_table(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS questions (id INTEGER PRIMARY KEY, question TEXT, answer1 TEXT, answer2 TEXT, answer3 TEXT, answer4 TEXT, correct_answer INTEGER, difficulty TEXT)"
        )
        self.conn.commit()

    def insert_question(self, question, answers, correct_answer, difficulty):
        try:
            self.cursor.execute(
                "INSERT INTO questions (question, answer1, answer2, answer3, answer4, correct_answer, difficulty) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (question, answers[0], answers[1], answers[2], answers[3], correct_answer, difficulty)
            )
            self.conn.commit()
            return True
        except sqlite3.Error:
            return False

    def load_questions(self, difficulty):
        self.cursor.execute(
            "SELECT question, answer1, answer2, answer3, answer4, correct_answer FROM questions WHERE difficulty=?",
            (difficulty,)
        )
        questions_data = self.cursor.fetchall()

        # Shuffle the questions randomly
        random.shuffle(questions_data)

        # Return only the first 5 questions
        questions_data = questions_data[:5]

        questions = []
        for question_data in questions_data:
            question = {
                "question": question_data[0],
                "answers": [
                    question_data[1],
                    question_data[2],
                    question_data[3],
                    question_data[4],
                ],
                "correct_answer": question_data[5],
            }
            questions.append(question)

        return questions

    def close(self):
        self.conn.close()

