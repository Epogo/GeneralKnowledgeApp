import sqlite3
import firebase_admin
from firebase_admin import credentials, firestore
import random
import os
from tkinter import messagebox
from abc import ABC, abstractmethod
from firebaseFactory import firebase_factory
from firebaseDbCreator import generateNewFb# Import the module where new_questions_db function is defined

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

    @abstractmethod
    def get_last_question_id(self):
        pass

    @abstractmethod
    def erase_database_and_generate_questions(self):
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
            last_id = self.get_last_question_id() + 1
            self.cursor.execute(
                "INSERT INTO questions (id, question, answer1, answer2, answer3, answer4, correct_answer, difficulty) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (last_id, question, answers[0], answers[1],
                 answers[2], answers[3], correct_answer, difficulty)
            )
            self.conn.commit()
            return True
        except sqlite3.Error:
            return False

    def load_questions(self, difficulty, num_questions=5):
        chosen_questions = set()
        questions = []

        while len(questions) < num_questions:
            self.cursor.execute(
                "SELECT id, question, answer1, answer2, answer3, answer4, correct_answer FROM questions WHERE difficulty=? ORDER BY RANDOM() LIMIT 1",
                (difficulty,)
            )
            question_data = self.cursor.fetchone()

            question_id = question_data[0]
            if question_id not in chosen_questions:
                chosen_questions.add(question_id)

                question = {
                    "question": question_data[1],
                    "answers": [
                        question_data[2],
                        question_data[3],
                        question_data[4],
                        question_data[5],
                    ],
                    "correct_answer": question_data[6],
                }
                questions.append(question)

        return questions

    def get_last_question_id(self):
        conn = sqlite3.connect("trivia.db")
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(id) FROM questions")
        last_id = cursor.fetchone()[0]
        conn.close()
        return last_id if last_id is not None else 0
    
    def erase_database_and_generate_questions(self):
        self.close()
        # Delete the trivia.db file if it exists
        if os.path.exists("trivia.db"):
            os.remove("trivia.db")
            messagebox.showinfo("Success", "Trivia database erased.")

        # Generate new questions using new_questions_db function
        new_questions_db()
        messagebox.showinfo("Success", "New questions generated.")
        self.conn = sqlite3.connect("trivia.db")
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()

class FirebaseTriviaDb(TriviaDb):
    def __init__(self):
        self.db = firebase_factory.get_firestore_client()

    def create_trivia_table(self):
        # Firebase Firestore does not require explicit table creation
        pass

    def insert_question(self, question, answers, correct_answer, difficulty):
        try:
            last_id = self.get_last_question_id() + 1
            question_ref = self.db.collection(
                'questions').document(str(last_id))
            question_ref.set({
            	"id": last_id,
                "question": question,
                "answer1": answers[0],
                "answer2": answers[1],
                "answer3": answers[2],
                "answer4": answers[3],
                "correct_answer": correct_answer,
                "difficulty": difficulty
            })
            return True
        except Exception as e:
            return False

    def load_questions(self, difficulty, num_questions=5):
        questions_ref = self.db.collection('questions').where(
            'difficulty', '==', difficulty).stream()
        all_questions = [q.to_dict() for q in questions_ref]

        chosen_questions = random.sample(all_questions, num_questions)
        questions = []

        for question_data in chosen_questions:
            question = {
                "question": question_data["question"],
                "answers": [
                    question_data["answer1"],
                    question_data["answer2"],
                    question_data["answer3"],
                    question_data["answer4"],
                ],
                "correct_answer": question_data["correct_answer"],
            }
            questions.append(question)

        return questions

    def get_last_question_id(self):
        questions_ref = self.db.collection('questions').stream()
        question_ids = [int(q.id) for q in questions_ref]
        return max(question_ids) if question_ids else 0

    def erase_database_and_generate_questions(self):
        collection_ref = self.db.collection('questions')
        docs = collection_ref.stream()

        for doc in docs:
            doc.reference.delete()
        
        generateNewFb()
        messagebox.showinfo("Success", "New questions generated.")

    def close(self):
        # Firebase Admin SDK does not require explicit close
        pass
