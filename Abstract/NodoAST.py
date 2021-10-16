from abc import ABC, abstractmethod
from TS.Entorno import Entorno

class NodoAST(ABC):
    def __init__(self, tipo, fila, columna):
        self.tipo = tipo
        self.fila = fila
        self.columna = columna
        super().__init__()

    @abstractmethod
    def interpretar(self, entorno):
        pass

    @abstractmethod
    def getNodo(self):
        pass
