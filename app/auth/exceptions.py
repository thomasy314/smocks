

class UserAlreadyExists(Exception):

    def __init__(self, username: str):
        super().__init__(f'username already exists: {username}')