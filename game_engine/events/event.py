from abc import ABC, abstractmethod

class Event():
    entity = None

    def __init__(self, entity):
        self.entity = entity

    @abstractmethod
    def get_options(self):
        pass
    
    @abstractmethod
    def resolve(self, action, dungeon):
        pass