def valid_username(username):
    username = username.strip()
    return 3 <= len(username) <= 30


def valid_password(password):
    return len(password) >= 4
