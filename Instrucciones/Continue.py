from Abstract.NodoReporteArbol import NodoReporteArbol
from Abstract.NodoAST import NodoAST
from TS.Tipo import TIPO

class Continue(NodoAST):
    def __init__(self, fila, columna):
        super().__init__(TIPO.CONTINUE, fila, columna)

    def interpretar(self, tree, table):
        return self

    def getNodo(self):
        nodo = NodoReporteArbol("CONTINUE")
        nodo.agregarHijoCadena("continue")
        nodo.agregarHijoCadena(";")
        return nodo