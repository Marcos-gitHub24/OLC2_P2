from Abstract.NodoReporteArbol import NodoReporteArbol
from Abstract.Return import Return
from TS.Excepcion import Excepcion
from Abstract.NodoAST import NodoAST
from TS.Generador import Generador
from TS.Tipo import TIPO


class Identificador(NodoAST):
    def __init__(self, identificador, fila, columna):
        self.identificador = identificador
        self.fila = fila
        self.columna = columna
        self.truelbl = None
        self.falselbl = None

    def interpretar(self, entorno):
        aux = Generador()
        generador = aux.obtenerGen()
        variable = entorno.obtenerVariable(self.identificador)
        print('-------iddididi')
        print(variable.tipo)
        if variable == None:
            print('No hay variable')
            return
        
        temporal = generador.agregarTemporal()
        posicion = variable.pos
        if not variable.isGlobal:
            posicion = generador.agregarTemporal()
            generador.agregarExpresion(posicion,'P',variable.pos,'+')
        generador.obtener_stack(temporal,posicion)

        if variable.tipo != TIPO.BOOLEANO:
            return Return(temporal, variable.tipo, True)
        if self.truelbl == None:
            self.truelbl = generador.agregarLabel()
        if self.falselbl == None:
            self.falselbl = generador.agregarLabel()
        
        generador.agregarIf(temporal, '1', '==', self.truelbl)
        generador.agregarGoto(self.falselbl)
        resultado = Return(None, TIPO.BOOLEANO, False)
        resultado.truelbl = self.truelbl
        resultado.falselbl = self.falselbl
        return resultado


    def getNodo(self):
        nodo = NodoReporteArbol("IDENTIFICADOR")
        nodo.agregarHijo(str(self.identificador))
        return nodo