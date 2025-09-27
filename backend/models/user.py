class User:
    def __init__(self, name, email, password, user_id = 0):
        self.id = user_id
        self.name = name
        self.email = email
        self.password = password