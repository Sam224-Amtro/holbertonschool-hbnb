from abc import ABC, abstractmethod


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


class InMemoryRepository:
    def __init__(self):
        self.data = {}

    def add(self, item):
        self.data[item.id] = item

    def get(self, item_id):
        return self.data.get(item_id)

    def get_by_attribute(self, attr, value):
        for item in self.data.values():
            if getattr(item, attr) == value:
                return item
        return None

    def update(self, item):
        if item.id in self.data:
            self.data[item.id] = item
            return True
        return False

    def get_all(self):
        # Return all items stored in the repository
        return list(self.data.values())  # Use values() to get all items
