from Expresiones.Struct import Struct
from Instrucciones.Asignacion import Asignacion
from Expresiones.Identificador import Identificador
from Objeto.Primitivo import Primitivo
from os import times
from re import T
from Abstract.Objeto import TipoObjeto
from Abstract.NodoReporteArbol import NodoReporteArbol
from TS.Excepcion import Excepcion
from Abstract.NodoAST import NodoAST
from TS.Simbolo import Simbolo
from TS.Tipo import TIPO



class ModificaStruct(NodoAST):
    def __init__(self, identificador, atributo, expresion, fila, columna):
        self.identificador = identificador
        self.atributo = atributo
        self.expresion = expresion
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        obtenerStruct = Identificador(self.identificador, self.fila, self.columna)
        estructura = obtenerStruct.interpretar(tree, table)
        if isinstance(self.expresion, Excepcion):
            return self.expresion
        valor = self.expresion.interpretar(tree, table)
        if isinstance(valor, Struct) == False:
            if valor.tipo==TIPO.ERROR:
                tree.addExcepcion(valor)
                return valor
            if estructura.mutable == True:
                iterador = 0
                for nombre in estructura.diccionario:
                    if nombre == self.atributo:
                        if estructura.atributos[iterador].tipo != None:
                            if estructura.atributos[iterador].tipo == valor.tipo:
                                estructura.diccionario[nombre] = valor
                                simbolo = Simbolo(self.identificador, self.fila, self.columna, estructura)
                                table.actualizarTabla(simbolo)
                                return;
                            else:
                                tree.addExcepcion(Excepcion("Semantico", "Nuevo valor no es del mismo tipo", self.fila, self.columna))
                                return Excepcion("Semantico", "Nuevo valor no es del mismo tipo", self.fila, self.columna)

                        else:
                            estructura.diccionario[nombre] = valor
                            simbolo = Simbolo(self.identificador, self.fila, self.columna, estructura)
                            table.actualizarTabla(simbolo)
                            return;
                    iterador +=1
                tree.addExcepcion(Excepcion("Semantico", "No hay un atributo con ese nombre", self.fila, self.columna))
                return Excepcion("Semantico", "No hay un atributo con ese nombre", self.fila, self.columna)
            else:
                tree.addExcepcion(Excepcion("Semantico", "El estruct es inmutable", self.fila, self.columna))
                return Excepcion("Semantico", "El estruct es inmutable", self.fila, self.columna)
        else:
            if estructura.mutable == True:
                iterador = 0
                for nombre in estructura.diccionario:
                    if nombre == self.atributo:
                        estructura.diccionario[nombre] = valor
                        simbolo = Simbolo(self.identificador, self.fila, self.columna, estructura)
                        table.actualizarTabla(simbolo)
                        return;
                    iterador +=1
                tree.addExcepcion(Excepcion("Semantico", "No hay un atributo con ese nombre", self.fila, self.columna))
                return Excepcion("Semantico", "No hay un atributo con ese nombre", self.fila, self.columna)
            else:
                tree.addExcepcion(Excepcion("Semantico", "El estruct es inmutable", self.fila, self.columna))
                return Excepcion("Semantico", "El estruct es inmutable", self.fila, self.columna)

    def getNodo(self):
        nodo = NodoReporteArbol("MODIFICAR_STRUCT")
        nodo.agregarHijoCadena(self.identificador)
        nodo.agregarHijoCadena(".")
        nodo.agregarHijoCadena(self.atributo)
        nodo.agregarHijoCadena("=")
        expresion = NodoReporteArbol("EXPRESION")
        expresion.agregarHijoNodo(self.expresion.getNodo())
        nodo.agregarHijoNodo(expresion)
        nodo.agregarHijoCadena(";")
        return nodo