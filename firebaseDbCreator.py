import firebase_admin
from firebase_admin import credentials, firestore
from firebaseFactory import firebase_factory
import json

def generateNewFb():
	# Get firebase instance.
	db = firebase_factory.get_firestore_client()

	# Read questions from the JSON file
	with open("questions.json", "r") as json_file:
		questions = json.load(json_file)

	# Create the questions collection if it doesn't exist
	questions_ref = db.collection('questions')
	if not questions_ref.get():
		last_id = 0
	else:
		last_id_doc = questions_ref.order_by('id', direction=firestore.Query.DESCENDING).limit(1).stream()
		last_id = 0 if not last_id_doc else int(next(last_id_doc).to_dict()["id"])

	for q in questions:
		last_id += 1
		question_ref = questions_ref.document(str(last_id))
		question_ref.set({
		    "id": last_id,
		    "question": q["question"],
		    "answer1": q["answers"][0],
		    "answer2": q["answers"][1],
		    "answer3": q["answers"][2],
		    "answer4": q["answers"][3],
		    "correct_answer": q["correct_answer"],
		    "difficulty": q["difficulty"]
		})

	print("Questions collection created successfully.")

if __name__ == "__main__":
	generateNewFb()

