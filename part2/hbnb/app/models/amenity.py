import uuid

class Amenity:
    def __init__(self, name, description=None):
        # Générer un UUID unique pour chaque nouvelle instance
        self.id = str(uuid.uuid4())  # ID sous forme de chaîne UUID
        self.name = name
        self.description = description

    def to_dict(self):
        """Retourner les informations de l'amenity sous forme de dictionnaire"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
