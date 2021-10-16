from Expresiones.atributo import atributo
from Abstract.Objeto import TipoObjeto
from Abstract.NodoReporteArbol import NodoReporteArbol
from TS.Tipo import TIPO
from Instrucciones.Return import Return
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break
from TS.Simbolo import Simbolo
from Expresiones.Identificador import Identificador

class AccesoStruct(NodoAST):
    def __init__(self, nombre , atributos, fila, columna):
        self.nombre = nombre
        self.atributos = atributos
        self.fila = fila
        self.columna = columna
    def interpretar(self, tree, table):
        obtenerStruct = Identificador(self.nombre, self.fila, self.columna)
        estructura = obtenerStruct.interpretar(tree, table)
        if len(self.atributos) == 1:
            for clave in estructura.diccionario:
                if clave == self.atributos[0]:
                    return estructura.diccionario[clave]
        else:
            iterador = 0
            encontro = False
            diccionario = estructura.diccionario
            clave = ""
            while iterador < len(self.atributos):
                for clave in diccionario:
                    if clave == self.atributos[iterador] and iterador != len(self.atributos)-1:
                        atrib = diccionario[clave]
                        diccionario = atrib.diccionario
                        encontro = True
                        break
                    if iterador == len(self.atributos)-1:
                        if clave == self.atributos[iterador]:
                            encontro = True
                            break
                if encontro:
                    encontro =  False
                else:
                    tree.addExcepcion(Excepcion("Semantico", "No existe un atributo con ese nombre", self.fila, self.columna))
                    return Excepcion("Semantico", "No existe un atributo con ese nombre", self.fila, self.columna)
                iterador+=1
            return diccionario[clave]

        

    def getNodo(self):
        nodo = NodoReporteArbol("ACCESO_STRUCT")
        nodo.agregarHijoCadena(self.nombre)
        nodo.agregarHijoCadena(".")
        nuevo = NodoReporteArbol("EXPRESIONES")
        unaVez = True
        for i in self.atributos:
            if unaVez:
                nuevo1 = NodoReporteArbol("EXPRESION")
                nuevo1.agregarHijoCadena(i)
                nuevo.agregarHijoNodo(nuevo1)
            else:
                n = nuevo
                nuevo1 = NodoReporteArbol("EXPRESION")
                nuevo = NodoReporteArbol("EXPRESIONES")
                nuevo.agregarHijoNodo(n)
                nuevo.agregarHijoCadena(".")
                nuevo1.agregarHijoCadena(i)
                nuevo.agregarHijoNodo(nuevo1)
            unaVez = False
        nodo.agregarHijoNodo(nuevo)
        return nodo