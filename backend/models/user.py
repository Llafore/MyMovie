class User:
    def __init__(self, clerk_id, name, email, password, user_id = 0):
        self.clerk_id = clerk_id
        self.name = name
        self.email = email
        self.password = password