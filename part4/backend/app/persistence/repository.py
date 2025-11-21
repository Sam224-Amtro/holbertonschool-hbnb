from abc import ABC, abstractmethod
from app.extensions import db

class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass

class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        return db.session.query(self.model).get(obj_id)

    def get_all(self):
        return db.session.query(self.model).all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()
            return obj
        return None

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        return db.session.query(self.model).filter(getattr(self.model, attr_name) == attr_value).all()

#class InMemoryRepository:
#    def __init__(self):
#        self.data = {}
#
#    def add(self, item):
#        if not hasattr(item, 'id'):
#            raise ValueError("Item must have an 'id' attribute")
#        print(f"Adding item with ID: {item.id}")  # Debug
#        self.data[item.id] = item
#
#    def get(self, item_id):
#        print(f"Looking for item with ID: {item_id}")  # Debug
#        return self.data.get(item_id)
#
#    def get_by_attribute(self, attr, value):
#        for item in self.data.values():
#            if getattr(item, attr) == value:
#                return item
#        return None
#
#    def update(self, item):
#        if item.id in self.data:
#            print(f"Updating item with ID: {item.id}")  # Debug
#            self.data[item.id] = item
#            return True
#        print(f"Item with ID {item.id} not found")  # Debug
#        return False
#
#    def get_all(self):
#        print(f"Current data in repository: {self.data}")  # Debug
#        return list(self.data.values())
#    
