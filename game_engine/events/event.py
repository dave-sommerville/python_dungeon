from abc import ABC, abstractmethod

class Event():
    param = -1
    def __init__(self, param):
        self.param = param

    @abstractmethod
    def get_options(self):
        pass
    
    @abstractmethod
    def resolve(self, action, dungeon):
        pass