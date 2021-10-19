from Abstract.NodoReporteArbol import NodoReporteArbol
from Abstract.NodoAST import NodoAST
from TS.Generador import Generador
from TS.Tipo import TIPO

class Break(NodoAST):
    def __init__(self, fila, columna):
        super().__init__(TIPO.BREAK, fila, columna)
        

    def interpretar(self, entorno):
        if entorno.lbl_break == None:
            return
        aux = Generador()
        generador = aux.obtenerGen()
        generador.agregarGoto(entorno.lbl_break)

    def getNodo(self):
        nodo = NodoReporteArbol("BREAK")
        nodo.agregarHijoCadena("break")
        nodo.agregarHijoCadena(";")
        return nodo