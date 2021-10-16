from Expresiones.Struct import Struct
from Objeto.Primitivo import Primitivo
from os import times
from re import T
from Abstract.Objeto import TipoObjeto
from Abstract.NodoReporteArbol import NodoReporteArbol
from TS.Excepcion import Excepcion
from Abstract.NodoAST import NodoAST
from TS.Simbolo import Simbolo
from TS.Tipo import TIPO



class Asignacion(NodoAST):
    def __init__(self, identificador, expresion, tipo, fila, columna):
        self.identificador = identificador
        self.expresion = expresion
        self.tipo = tipo
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        result = None
        if self.tipo == None:
            if self.expresion != None and isinstance(self.expresion, Struct) == False:
                value = self.expresion.interpretar(tree, table)
                if isinstance(value, Struct) == False:
                    if value.tipo==TIPO.ERROR:
                        tree.addExcepcion(value)
                        return value
                    simbolo = Simbolo(self.identificador, self.fila, self.columna, value)
                    result = table.actualizarTabla(simbolo)     # Si no se encuentra el simbolo, lo agrega 
                else:
                    simbolo = Simbolo(self.identificador, self.fila, self.columna, value)
                    result = table.actualizarTabla(simbolo)
            elif self.expresion != None and isinstance(self.expresion, Struct) == True:
                simbolo = Simbolo(self.identificador, self.fila, self.columna, self.expresion)
                result = table.actualizarTabla(simbolo)
            else:
                obtener = table.getTabla(self.identificador)
                if obtener == None:
                    simbolo = Simbolo(self.identificador, self.fila, self.columna, Primitivo(TIPO.NULO, self.fila, self.columna, None))
                    result = table.actualizarTabla(simbolo)                     
        else:
            if self.expresion != None and isinstance(self.expresion, Struct) == False:
                value = self.expresion.interpretar(tree, table)
                if value.tipo==TIPO.ERROR:
                    tree.addExcepcion(value)
                    return value;
                if value.tipo == self.tipo:
                    simbolo = Simbolo(self.identificador, self.fila, self.columna, value)
                    result = table.actualizarTabla(simbolo)
                else:
                    tree.updateConsola("No son del mismo tipo") 
                    tree.addExcepcion(Excepcion(TIPO.ERROR, f"Semantico, No son del mismo tipo", self.fila, self.columna))
                    return None
            elif self.expresion != None and isinstance(self.expresion, Struct):
                simbolo = Simbolo(self.identificador, self.fila, self.columna, self.expresion)
                result = table.actualizarTabla(simbolo)
                
            else:
                 obtener = table.getTabla(self.identificador)
                 if obtener == None:
                    simbolo = Simbolo(self.identificador, self.fila, self.columna, Primitivo(TIPO.NULO, self.fila, self.columna, None))
                    result = table.actualizarTabla(simbolo)          
           
        if isinstance(result,Excepcion): 
            tree.addExcepcion(result)
            return result
        
        return None

    def getNodo(self):
        if self.tipo == None and self.expresion != None:
            nodo = NodoReporteArbol("DECLARACION")
            instruccion = NodoReporteArbol("DECLARACION")
            #nodo.agregarHijoNodo(instruccion)
            nodo.agregarHijo(str(self.identificador))
            nodo.agregarHijoCadena("=")
            expresion = NodoReporteArbol("EXPRESION")
            nodo.agregarHijoNodo(expresion)
            nodo.agregarHijoCadena(";")
            expresion.agregarHijoNodo(self.expresion.getNodo())
            return nodo
        elif self.expresion == None:
            nodo = NodoReporteArbol("DECLARACION")
            instruccion = NodoReporteArbol("DECLARACION")
            #nodo.agregarHijoNodo(instruccion)
            nodo.agregarHijo(str(self.identificador))
            nodo.agregarHijoCadena(";")
            return nodo
        else:
            nodo = NodoReporteArbol("DECLARACION")
            instruccion = NodoReporteArbol("DECLARACION")
            #nodo.agregarHijoNodo(instruccion)
            nodo.agregarHijo(str(self.identificador))
            nodo.agregarHijoCadena("=")
            expresion = NodoReporteArbol("EXPRESION")
            nodo.agregarHijoNodo(expresion)
            expresion.agregarHijoNodo(self.expresion.getNodo())
            if self.tipo == TIPO.ENTERO:
                nodo.agregarHijoCadena(":")
                nodo.agregarHijoCadena(":")
                nodo.agregarHijoCadena("Int64")
                nodo.agregarHijoCadena(";")
            elif self.tipo == TIPO.DECIMAL:
                nodo.agregarHijoCadena(":")
                nodo.agregarHijoCadena(":")
                nodo.agregarHijoCadena("Float64")
                nodo.agregarHijoCadena(";")
            elif self.tipo == TIPO.CADENA:
                nodo.agregarHijoCadena(":")
                nodo.agregarHijoCadena(":")
                nodo.agregarHijoCadena("String")
                nodo.agregarHijoCadena(";")
            elif self.tipo == TIPO.CHARACTER:
                nodo.agregarHijoCadena(":")
                nodo.agregarHijoCadena(":")
                nodo.agregarHijoCadena("Char")
                nodo.agregarHijoCadena(";")
            elif self.tipo == TIPO.BOOLEANO:
                nodo.agregarHijoCadena(":")
                nodo.agregarHijoCadena(":")
                nodo.agregarHijoCadena("Boolean")
                nodo.agregarHijoCadena(";")
            return nodo
            