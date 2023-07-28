import sqlite3

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
		# Insert example questions for each difficulty level
	insert_question("What is the capital of France?",
		            ["Paris", "London", "Berlin", "Madrid"],
		            0,
		            "Easy")
	insert_question("Who painted the Mona Lisa?",
		            ["Vincent van Gogh", "Leonardo da Vinci", "Pablo Picasso", "Claude Monet"],
		            1,
		            "Easy")
	insert_question("What is the symbol for hydrogen?",
		            ["H", "He", "O", "C"],
		            0,
		            "Easy")
	insert_question("What is the largest planet in our solar system?",
		            ["Earth", "Saturn", "Jupiter", "Mars"],
		            2,
		            "Easy")
	insert_question("What is the square root of 16?",
		            ["2", "4", "6", "8"],
		            1,
		            "Easy")

	insert_question("Which country hosted the 2016 Summer Olympics?",
		            ["United States", "China", "Brazil", "Australia"],
		            2,
		            "Medium")
	insert_question("Who wrote the novel 'To Kill a Mockingbird'?",
		            ["Harper Lee", "J.D. Salinger", "George Orwell", "Mark Twain"],
		            0,
		            "Medium")
	insert_question("What is the chemical formula for water?",
		            ["H2O", "CO2", "NaCl", "C6H12O6"],
		            0,
		            "Medium")
	insert_question("Which scientist developed the theory of general relativity?",
		            ["Isaac Newton", "Albert Einstein", "Niels Bohr", "Marie Curie"],
		            1,
		            "Medium")
	insert_question("What is the tallest mountain in Africa?",
		            ["Mount Everest", "Mount Kilimanjaro", "Mount McKinley", "Mount Fuji"],
		            1,
		            "Medium")

	insert_question("In which year was the World Wide Web invented?",
		            ["1989", "1995", "2001", "1975"],
		            0,
		            "Hard")
	insert_question("Who discovered penicillin?",
		            ["Alexander Fleming", "Marie Curie", "Thomas Edison", "Louis Pasteur"],
		            0,
		            "Hard")
	insert_question("What is the unit of measurement for electric current?",
		            ["Volt", "Ohm", "Watt", "Ampere"],
		            3,
		            "Hard")
	insert_question("Which element has the atomic number 79?",
		            ["Iron", "Copper", "Gold", "Silver"],
		            2,
		            "Hard")
	insert_question("Who painted the 'Sistine Chapel Ceiling'?",
		            ["Michelangelo", "Leonardo da Vinci", "Raphael", "Donatello"],
		            0,
		            "Hard")


# Create the question table in the database if it doesn't exist
create_question_table()


