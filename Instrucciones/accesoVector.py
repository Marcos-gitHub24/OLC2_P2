from Expresiones.Aritmetica import Aritmetica
import re
from Objeto.Primitivo import Primitivo
from os import times
from re import T
from Abstract.Objeto import TipoObjeto
from Abstract.NodoReporteArbol import NodoReporteArbol
from TS.Excepcion import Excepcion
from Abstract.NodoAST import NodoAST
from TS.Simbolo import Simbolo
from TS.Tipo import TIPO



class Acceso(NodoAST):
    def __init__(self, identificador, lista, fila, columna):
        self.identificador = identificador
        self.lista = lista
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        lista = []
        for i in self.lista:
            result = i.interpretar(tree, table)
            if(result.tipo == TIPO.CADENA):
                tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede tener un indice cadena",self.fila,self.columna))
                return  Excepcion(TIPO.ERROR, f"No puede tener un indice cadena",self.fila,self.columna)
            if(result.tipo == TIPO.CHARACTER):
                tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede tener un indice char",self.fila,self.columna))
                return  Excepcion(TIPO.ERROR, f"No puede tener un indice char",self.fila,self.columna)
            if(result.tipo == TIPO.BOOLEANO):
                tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede tener un indice booleano",self.fila,self.columna))
                return  Excepcion(TIPO.ERROR, f"No puede tener un indice booleano",self.fila,self.columna)
            if(result.tipo == TIPO.DECIMAL):
                tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede tener un indice decimal",self.fila,self.columna))
                return  Excepcion(TIPO.ERROR, f"No puede adadsadadasdasd un indice decimal",self.fila,self.columna)
            lista.append(result.valor)

        simbolo = table.getTabla(self.identificador)
        
        if simbolo == None:
            tree.addExcepcion(Excepcion("Semantico", "Variable " + self.identificador + " no encontrada.", self.fila, self.columna))
            return Excepcion("Semantico", "Variable " + self.identificador + " no encontrada.", self.fila, self.columna)
        tmp = simbolo.getValor()
        varibale = tmp.interpretar(tree, table)
        if varibale.tipo == TIPO.ARREGLO:
            una_dimension = True
            for i in varibale.valor:
                verificar = i.interpretar(tree, table)
                if isinstance(verificar.valor, list):
                    una_dimension = False
            
            if una_dimension == True:
                if lista[0] <= len(varibale.valor):
                    ver = varibale.valor[lista[0]-1].interpretar(tree, table)
                    return ver
                else:
                    tree.addExcepcion(Excepcion("Semantico", "ERROR EN UNA DIMENSION", self.fila, self.columna))
                    return Excepcion("Semantico", "ERROR EN UNA DIMENSION", self.fila, self.columna)

            else:
                for i in lista:
                    if i <= len(varibale.valor) and i>0:
                        ver = varibale.valor[i-1].interpretar(tree, table)
                        if isinstance(ver.valor, list):
                            varibale = ver;
                        else:
                            if i == lista[len(lista)-1]:
                                return ver
                            else:
                                tree.addExcepcion(Excepcion("Semantico", "Indice incorrecto para acceder al vector", self.fila, self.columna))
                                return Excepcion("Semantico", "Indice incorrecto para acceder al vector", self.fila, self.columna)
                    else:
                        tree.addExcepcion(Excepcion("Semantico", "Indice incorrecto para acceder al vector", self.fila, self.columna))
                        return Excepcion("Semantico", "Indice incorrecto para acceder al vector", self.fila, self.columna)
                return ver

    def getNodo(self):
        nodo = NodoReporteArbol("LISTA_VECTOR")
        nodo.agregarHijo(self.identificador)
        nodo.agregarHijoCadena("[")
        unaVez = True
        for i in self.lista:
            if unaVez:
                nuevo1 = NodoReporteArbol("EXPRESION")
                nuevo1.agregarHijoNodo(i.getNodo())
                nodo.agregarHijoNodo(nuevo1)
            else:
                n = nodo
                nuevo1 = NodoReporteArbol("EXPRESION")
                nodo = NodoReporteArbol("LISTA_VECTOR")
                nodo.agregarHijoNodo(n)
                nodo.agregarHijoCadena(",")
                nuevo1.agregarHijoNodo(i.getNodo())
                nodo.agregarHijoNodo(nuevo1)
            unaVez = False
        nodo.agregarHijoCadena("]")
        return nodo

   

