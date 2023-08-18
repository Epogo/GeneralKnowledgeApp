import firebase_admin
from firebase_admin import credentials

class FirebaseFactory:
    _initialized = False  # Class-level flag to track initialization
    _instance = None  # Singleton instance

    def __new__(cls):
        if not cls._initialized:
            cred = credentials.Certificate("knowledgequiz.json")
            firebase_admin.initialize_app(cred)
            cls._initialized = True
        if cls._instance is None:
            cls._instance = super(FirebaseFactory, cls).__new__(cls)
        return cls._instance

    def get_firestore_client(self):
        return firebase_admin.firestore.client()

# Create an instance of FirebaseFactory
firebase_factory = FirebaseFactory()
