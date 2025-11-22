import uuid

class User:
    def __init__(self, first_name, last_name, email):
        self.id = str(uuid.uuid4())  # Génère un UUID unique sous forme de chaîne
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def to_dict(self):
        """Convertit l'utilisateur en dictionnaire pour JSON"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }
