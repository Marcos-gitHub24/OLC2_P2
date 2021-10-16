from math import e
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



class Modifica(NodoAST):
    def __init__(self, identificador, lista, nuevo,fila, columna):
        self.identificador = identificador
        self.lista = lista
        self.fila = fila
        self.nuevo = nuevo
        self.columna = columna

    def interpretar(self, tree, table):
        lista = []
        nueva_lista  = []
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
                return  Excepcion(TIPO.ERROR, f"No puede tener un indice decimal",self.fila,self.columna)
            lista.append(result.valor)

        simbolo = table.getTabla(self.identificador)
        nuevo_valor = self.nuevo.interpretar(tree, table)
        if isinstance(nuevo_valor,Excepcion): return nuevo_valor
        if simbolo == None:
            tree.addExcepcion(Excepcion("Semantico", "Variable " + self.identificador + " no encontrada.", self.fila, self.columna))
            return Excepcion("Semantico", "Variable " + self.identificador + " no encontrada.", self.fila, self.columna)
        tmp = simbolo.getValor()
        varibale = tmp.interpretar(tree, table)
        if isinstance(varibale.valor, list) == False:
            tree.addExcepcion(Excepcion("Semantico", "No esta accediendo a un arreglo", self.fila, self.columna))
            return Excepcion("Semantico", "No esta accediendo a un arreglo", self.fila, self.columna)
        original = varibale
        primitivo_original = varibale
        vector_anterior = []
        if varibale.tipo == TIPO.ARREGLO:
            una_dimension = True
            for i in varibale.valor:
                verificar = i.interpretar(tree, table)
                if isinstance(verificar.valor, list):
                    una_dimension = False
            
            if una_dimension == True:
                if lista[0] <= len(varibale.valor) and lista[0] >0:
                    varibale.valor[lista[0]-1] = nuevo_valor
                    primitivo_original =  varibale
                    simbolo.setValor(primitivo_original)
                    table.actualizarTabla(simbolo)
                else:
                    tree.addExcepcion(Excepcion("Semantico", "ERROR EN UNA DIMENSION", self.fila, self.columna))
                    return Excepcion("Semantico", "ERROR EN UNA DIMENSION", self.fila, self.columna)

            else:
                for i in lista:
                    if i <= len(varibale.valor) and i>0:
                        ver = varibale.valor[i-1].interpretar(tree, table)
                        vector_anterior = varibale.valor
                        if isinstance(ver.valor, list):
                            varibale = ver;
                        else:
                            if i == lista[len(lista)-1]:
                                nueva_lista = obtenerVector(tree, table, original, ver.valor, nuevo_valor.valor, vector_anterior)
                            else:
                                tree.addExcepcion(Excepcion("Semantico", "Indice incorrecto para acceder al vector", self.fila, self.columna))
                                return Excepcion("Semantico", "Indice incorrecto para acceder al vector", self.fila, self.columna)
                    else:
                        tree.addExcepcion(Excepcion("Semantico", "Indice incorrecto para acceder al vector", self.fila, self.columna))
                        return Excepcion("Semantico", "Indice incorrecto para acceder al vector", self.fila, self.columna)
                primitivo_original = nueva_lista
                simbolo.setValor(primitivo_original)
                table.actualizarTabla(simbolo)
        
    def getNodo(self):
        nodo = NodoReporteArbol("MODIFICA_VECTOR")
        nodo1 = NodoReporteArbol("ACCESO_VECTOR")
        nodo.agregarHijo(self.identificador)
        nodo.agregarHijoNodo(nodo1)
        unaVez = True
        for i in self.lista:
            if unaVez:
                nuevo1 = NodoReporteArbol("EXPRESION")
                nuevo1.agregarHijoCadena("[")
                nuevo1.agregarHijoNodo(i.getNodo())
                nuevo1.agregarHijoCadena("]")
                nodo1.agregarHijoNodo(nuevo1)
            else:
                n = nodo1
                nuevo1 = NodoReporteArbol("EXPRESION")
                nodo1 = NodoReporteArbol("ACCESO_VECTOR")
                nodo1.agregarHijoNodo(n)
                nuevo1.agregarHijoCadena("[")
                nuevo1.agregarHijoNodo(i.getNodo())
                nuevo1.agregarHijoCadena("]")
                nodo1.agregarHijoNodo(nuevo1)
            unaVez = False
        nodo.agregarHijoCadena("=")
        expresion = NodoReporteArbol("EXPRESION")
        expresion.agregarHijoNodo(self.nuevo.getNodo())
        nodo.agregarHijoNodo(expresion)
        nodo.agregarHijoCadena(";")
        return nodo

def obtenerVector(tree, table, vector, buscar, nuevo, anterior):
        lista = []
        encontro = True
        vec = vector.interpretar(tree, table)
        for i in vec.valor:
            valor = i.interpretar(tree, table)
            if isinstance(valor.valor, list):
               lista.append(obtenerVector(tree, table, valor, buscar, nuevo, anterior))
            else:
                if valor.valor == buscar and anterior == vec.valor and encontro:
                    valor.valor = nuevo
                    lista.append(valor)
                    encontro = False
                else:
                    lista.append(valor)
        return Primitivo(TIPO.ARREGLO, 0, 0, lista)