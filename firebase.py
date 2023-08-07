import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase app (replace with your credentials)
cred = credentials.Certificate("knowledgequiz.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Reference to a document
doc_ref = db.collection('users').document('89UrOwR0tMdCSkQ5AQuU')

# Get the document snapshot
doc_snapshot = doc_ref.get()

# Check if the document exists
if doc_snapshot.exists:
    # Get the fields as a dictionary
    document_data = doc_snapshot.to_dict()
    
    # Print the fields
    for field, value in document_data.items():
        print(f"{field}: {value}")
else:
    print("Document does not exist")

