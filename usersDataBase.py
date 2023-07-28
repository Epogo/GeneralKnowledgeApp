import sqlite3
from abc import ABC, abstractmethod


class UsersDb(ABC):
    @abstractmethod
    def create_user_table(self):
        pass

    @abstractmethod
    def create_user(self, username: str, password: str) -> bool:
        pass

    @abstractmethod
    def get_user(self, username: str) -> dict:
        pass

    @abstractmethod
    def is_admin(self, username: str) -> bool:
        pass

    @abstractmethod
    def update_best_score(self, username: str, score: int) -> bool:
        pass

    @abstractmethod
    def get_best_score(self, username: str) -> int:
        pass
        
    @abstractmethod   
    def close(self) -> bool:
    	pass


class SQLiteUsersDb(UsersDb):
    def __init__(self):
        self.conn = sqlite3.connect("users.db")
        self.cursor = self.conn.cursor()

    def create_user_table(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, best_score INTEGER, is_admin INTEGER)"
        )
        # Check if the admin user already exists
        self.cursor.execute("SELECT * FROM users WHERE username=?", ("admin",))
        admin_user = self.cursor.fetchone()

        if not admin_user:
            # Add the admin user to the database
            self.cursor.execute("INSERT INTO users VALUES (?, ?, 0, 1)",
                           ("admin", "go1234"))
        self.conn.commit()

    def create_user(self, username: str, password: str) -> bool:
        # Implementation to create a new user in the database
        self.cursor.execute(
            "INSERT INTO users (username, password, best_score, is_admin) VALUES (?, ?, 0, 0)",
            (username, password)
        )
        self.conn.commit()
        return True

    def get_user(self, username: str) -> dict:
        # Implementation to get a user's data from the database
        self.cursor.execute(
            "SELECT * FROM users WHERE username=?", (username,)
        )
        user = self.cursor.fetchone()
        if user:
            return {
                "username": user[0],
                "password": user[1],
                "best_score": user[2],
                "is_admin": user[3]
            }
        else:
            return None

    def is_admin(self, username: str) -> bool:
        # Implementation to check if a user is an admin
        user = self.get_user(username)
        return user['is_admin'] if user else False

    def update_best_score(self, username: str, score: int) -> bool:
        # Implementation to update a user's best score in the database
        self.cursor.execute(
            "UPDATE users SET best_score=? WHERE username=?",
            (score, username)
        )
        self.conn.commit()
        return True

    def get_best_score(self, username: str) -> int:
        # Implementation to retrieve the best score for a user from the
        # database
        user = self.get_user(username)
        return user['best_score'] if user else 0

    def close(self):
        self.conn.close()
