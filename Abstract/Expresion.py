from abc import ABC, abstractmethod

class Expresion(ABC):
    def __init__(self, line, column):
        self.line = line
        self.column = column
        self.trueLbl = ''
        self.falseLbl = ''
    
    @abstractmethod
    def compile(self, environment):
        pass