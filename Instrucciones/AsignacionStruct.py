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



class AsignacionStruct(NodoAST):
    def __init__(self, identificador, struct, atributos, fila, columna):
        self.identificador = identificador
        self.atributos = atributos
        self.struct = struct
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        if self.identificador != None:
            obtenerStruct = Identificador(self.struct, self.fila, self.columna)
            estructura = obtenerStruct.interpretar(tree, table)
            nueva_estructura = Struct(estructura.nombre, estructura.atributos, estructura.mutable, estructura.fila, estructura.columna)
            for i in estructura.diccionario:
                nueva_estructura.diccionario[i] = ""
            nueva_estructura.mutable = estructura.mutable
            print(estructura.mutable)
            if len(self.atributos) == len(estructura.atributos):
                iterador = 0
                for clave in nueva_estructura.diccionario:
                    if isinstance(self.atributos[iterador], Excepcion):
                        tree.addExcepcion(self.atributos[iterador])
                        return self.atributos[iterador]
                    asignar = self.atributos[iterador].interpretar(tree, table)
                    if nueva_estructura.atributos[iterador].tipo != None:
                        if nueva_estructura.atributos[iterador].tipo == asignar.tipo:
                            nueva_estructura.diccionario[clave] = self.atributos[iterador].interpretar(tree, table)
                        else:
                            tree.addExcepcion(Excepcion("Semantico", "Valor no conincide con el tipo", self.fila, self.columna))
                            return Excepcion("Semantico", "Valor no conincide con el tipo", self.fila, self.columna)
                    else:
                        nueva_estructura.diccionario[clave] = self.atributos[iterador].interpretar(tree, table)
                    iterador += 1
                asignar = Asignacion(self.identificador, nueva_estructura, None, self.fila, self.columna)
                asignar.interpretar(tree, table)
            else:
                tree.addExcepcion(Excepcion("Semantico", "Numero de parametros no coincide", self.fila, self.columna))
                return Excepcion("Semantico", "Numero de parametros no coincide", self.fila, self.columna)
        else:
            obtenerStruct = Identificador(self.struct, self.fila, self.columna)
            estructura = obtenerStruct.interpretar(tree, table)
            nueva_estructura = Struct(estructura.nombre, estructura.atributos, estructura.mutable, estructura.fila, estructura.columna)
            for i in estructura.diccionario:
                nueva_estructura.diccionario[i] = ""
            nueva_estructura.mutable = estructura.mutable
            print(estructura.mutable)
            if len(self.atributos) == len(estructura.atributos):
                iterador = 0
                for clave in nueva_estructura.diccionario:
                    if isinstance(self.atributos[iterador], Excepcion):
                        tree.addExcepcion(self.atributos[iterador])
                        return self.atributos[iterador]
                    asignar = self.atributos[iterador].interpretar(tree, table)
                    if nueva_estructura.atributos[iterador].tipo != None:
                        if nueva_estructura.atributos[iterador].tipo == asignar.tipo:
                            nueva_estructura.diccionario[clave] = self.atributos[iterador].interpretar(tree, table)
                        else:
                            tree.addExcepcion(Excepcion("Semantico", "Valor no conincide con el tipo", self.fila, self.columna))
                            return Excepcion("Semantico", "Valor no conincide con el tipo", self.fila, self.columna)
                    else:
                        nueva_estructura.diccionario[clave] = self.atributos[iterador].interpretar(tree, table)
                    iterador += 1
                return nueva_estructura
            else:
                tree.addExcepcion(Excepcion("Semantico", "Numero de parametros no coincide", self.fila, self.columna))
                return Excepcion("Semantico", "Numero de parametros no coincide", self.fila, self.columna)
        
        return None

    def getNodo(self):
        nodo = NodoReporteArbol("ASIGNACION_STRUCT")
        nodo.agregarHijo(str(self.identificador))
        nodo.agregarHijoNodo(self.expresion.getNodo())
        return nodo