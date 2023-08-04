import sqlite3
import json

def create_question_table():
    conn = sqlite3.connect("trivia.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS questions (id INTEGER PRIMARY KEY, question TEXT, answer1 TEXT, answer2 TEXT, answer3 TEXT, answer4 TEXT, correct_answer INTEGER, difficulty TEXT)")
    conn.commit()
    conn.close()

def insert_question(question, answers, correct_answer, difficulty):
    conn = sqlite3.connect("trivia.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO questions (question, answer1, answer2, answer3, answer4, correct_answer, difficulty) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (question, answers[0], answers[1], answers[2], answers[3], correct_answer, difficulty))
    conn.commit()
    conn.close()

def new_questions_db():
    create_question_table()
    
    with open("questions.json", "r") as json_file:
        questions = json.load(json_file)
        for q in questions:
            insert_question(q["question"], q["answers"], q["correct_answer"], q["difficulty"])


