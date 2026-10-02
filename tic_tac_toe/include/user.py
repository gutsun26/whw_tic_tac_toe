class User:
    def __init__(self, user_id=None, username="", password_hash=""):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
