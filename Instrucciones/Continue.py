from Abstract.NodoReporteArbol import NodoReporteArbol
from Abstract.NodoAST import NodoAST
from TS.Generador import Generador
from TS.Tipo import TIPO

class Continue(NodoAST):
    def __init__(self, fila, columna):
        super().__init__(TIPO.CONTINUE, fila, columna)

    def interpretar(self, entorno):
        if entorno.lbl_continue == None:
            return
        aux = Generador()
        generador = aux.obtenerGen()
        generador.agregarGoto(entorno.lbl_continue)
        print('--continue--')
        print(entorno.lbl_continue)
        return self

    def getNodo(self):
        nodo = NodoReporteArbol("CONTINUE")
        nodo.agregarHijoCadena("continue")
        nodo.agregarHijoCadena(";")
        return nodo