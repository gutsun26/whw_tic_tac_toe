import hashlib
from tic_tac_toe.src.database import Database


class UserManager:
    def __init__(self):
        self.db = Database()

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def register(self, username, password):
        username = username.strip()

        if not username or not password:
            return False, "Username and password are required."

        existing = self.db.fetch_one(
            "SELECT user_id FROM users WHERE username = %s",
            (username,)
        )

        if existing:
            return False, "Username already exists."

        password_hash = self.hash_password(password)

        user_id = self.db.execute(
            """INSERT INTO users (username, password_hash)
               VALUES (%s, %s)""",
            (username, password_hash)
        )

        self.db.execute(
            """INSERT INTO player_statistics
               (user_id, games_played, wins, losses, draws, score)
               VALUES (%s, 0, 0, 0, 0, 0)""",
            (user_id,)
        )

        return True, "Registration successful."

    def login(self, username, password):
        password_hash = self.hash_password(password)

        return self.db.fetch_one(
            """SELECT user_id, username
               FROM users
               WHERE username = %s AND password_hash = %s""",
            (username.strip(), password_hash)
        )

    def get_all_users(self):
        return self.db.fetch_all(
            "SELECT user_id, username FROM users ORDER BY username"
        )
