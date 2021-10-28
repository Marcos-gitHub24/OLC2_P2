from Abstract.Objeto import TipoObjeto
from Abstract.NodoReporteArbol import NodoReporteArbol
from TS.Tipo import TIPO
from Instrucciones.Return import Return
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break
from TS.Simbolo import Simbolo
from TS.Entorno import Entorno
from TS.Generador import Generador

class Return_Function(NodoAST):
    def __init__(self, expresion,  fila, columna):
        self.expresion = expresion
        self.fila = fila
        self.columna = columna
    
    def interpretar(self, entorno):
        if entorno.lbl_return == '':
            return
        aux = Generador()
        generador = aux.obtenerGen()

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