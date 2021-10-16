from Expresiones.Struct import Struct
from Instrucciones.Asignacion import Asignacion
from Instrucciones.AsignacionStruct import AsignacionStruct
from Instrucciones.Llamada import Llamada
from Instrucciones.Metodo import Metodo
from Instrucciones.Return import Return
from Abstract.NodoReporteArbol import NodoReporteArbol
from TS.Simbolo import Simbolo
from Instrucciones.Funcion import Funcion
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.TablaSimbolos import TablaSimbolos

class LlamadaIntermedia(NodoAST):
    def __init__(self, identificador, structFuncion ,parametros, fila, columna):
        self.identificador = identificador
        self.structFuncion = structFuncion
        self.parametros = parametros
        self.fila = fila
        self.columna = columna
    
    def interpretar(self, tree, table):
        objeto = table.getTabla(self.structFuncion)
        if self.identificador != None:
            if objeto != None:
                if isinstance(objeto.getValor(), Metodo):
                    llamar = Llamada(self.structFuncion, self.parametros, self.fila, self.columna)
                    asignar = Asignacion(self.identificador, llamar.interpretar(tree, table), None, self.fila, self.columna)
                    asignar.interpretar(tree, table)
                else:
                    struct =  AsignacionStruct(self.identificador, self.structFuncion, self.parametros, self.fila, self.columna) 
                    struct.interpretar(tree, table)
            else:
                return Excepcion("Semantico", "No existe un metodo/struct con ese nombre", self.fila, self.columna)
        else:
            if objeto != None:
                if isinstance(objeto.getValor(), Metodo):
                    llamar = Llamada(self.structFuncion, self.parametros, self.fila, self.columna)
                    return llamar.interpretar(tree, table)
                else:
                    estructura = objeto.getValor()
                    iterador = 0
                    for clave in objeto.getValor().diccionario:
                         estructura[clave] = self.parametros[iterador]
                         iterador +=1

                    return estructura
            else:
                return Excepcion("Semantico", "No existe un metodo/struct con ese nombre", self.fila, self.columna)

        
    def getNodo(self):
        nodo = NodoReporteArbol("LLAMADA A FUNCION")
        nodo.agregarHijo(str(self.nombre))
        parametros = NodoReporteArbol("PARAMETROS")
        for param in self.parametros:
            parametros.agregarHijoNodo(param.getNodo())
        nodo.agregarHijoNodo(parametros)
        return nodo