import hashlib

class Customer:
    def __init__(self, id, name, email, password, hashed=True):
        self.id = id
        self.name = name
        self.email = email
        self.password = password if hashed else self.hash_password(password)

    def hash_password(self, plain):
        return hashlib.sha256(plain.encode()).hexdigest()

    def check_password(self, attempt):
        return self.hash_password(attempt) == self.password

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password
        }
