from Abstract.NodoReporteArbol import NodoReporteArbol
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO
from TS.TablaSimbolos import TablaSimbolos
from TS.Generador import Generador

class Return(NodoAST):
    def __init__(self, expresion, fila, columna):
        super().__init__(TIPO.RETURN, fila, columna)
        self.expresion = expresion

    def interpretar(self, entorno):
        if entorno.lbl_return == '':
            return
        aux = Generador()
        generador = aux.obtenerGen()
        print(self.expresion)
        if self.expresion != None:
            
            valor = self.expresion.interpretar(entorno)
            if valor.tipo == TIPO.BOOLEANO:
                temporal = generador.agregarLabel()
                generador.colocarLbl(valor.truelbl)
                generador.guardar_stack('P','1')
                generador.agregarGoto(temporal)

                generador.colocarLbl(valor.falselbl)
                generador.guardar_stack('P','0')
                generador.colocarLbl(temporal)
            else:
                generador.guardar_stack('P',valor.valor)
        
        generador.agregarGoto(entorno.lbl_return)


    def getNodo(self):
        nodo = NodoReporteArbol("RETURN")
        if self.expresion != None:
            nodo.agregarHijoCadena("return")
            nodo.agregarHijoNodo(self.expresion.getNodo())
            nodo.agregarHijoCadena(";")
        else:
            nodo.agregarHijoCadena("return")
            nodo.agregarHijoCadena(";")
        return nodo