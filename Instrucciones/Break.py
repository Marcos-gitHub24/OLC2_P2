from Abstract.NodoReporteArbol import NodoReporteArbol
from Abstract.NodoAST import NodoAST
from TS.Tipo import TIPO

class Break(NodoAST):
    def __init__(self, fila, columna):
        super().__init__(TIPO.BREAK, fila, columna)
        

    def interpretar(self, tree, table):
        return self

    def getNodo(self):
        nodo = NodoReporteArbol("BREAK")
        nodo.agregarHijoCadena("break")
        nodo.agregarHijoCadena(";")
        return nodo