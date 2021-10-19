from Expresiones.Struct import Struct
from Abstract.NodoReporteArbol import NodoReporteArbol
from Abstract.NodoAST import NodoAST
from Abstract.Objeto import Objeto, TipoObjeto
from TS.Generador import Generador
from TS.Tipo import TIPO
from Abstract.Return import Return
from abc import ABC, abstractmethod

class Primitivo(NodoAST):
    def __init__(self, tipo, fila, columna, valor):
        super().__init__(tipo, fila, columna)
        self.valor = valor
        self.truelbl = None
        self.falselbl = None

    def interpretar(self, entorno):
        aux = Generador()
        generador = aux.obtenerGen()
        if (self.tipo == TIPO.ENTERO or self.tipo == TIPO.DECIMAL):
            return Return(str(self.valor), self.tipo, False)
        elif self.tipo == TIPO.CADENA:
            temp = generador.agregarTemporal()
            generador.agregarExpresion(temp, 'H', '', '')
            for i in self.valor:
                generador.guardar_heap('H', ord(i))
                generador.sumar_heap()
            generador.guardar_heap('H', '-1')
            generador.sumar_heap()
            return Return(temp, TIPO.CADENA, True)
        elif self.tipo == TIPO.CHARACTER:
            temp = generador.agregarTemporal()
            generador.agregarExpresion(temp, 'H', '', '')
            for i in self.valor:
                generador.guardar_heap('H', ord(i))
                generador.sumar_heap()
            generador.guardar_heap('H', '-1')
            generador.sumar_heap()
            return Return(temp, TIPO.CHARACTER, True)
        elif self.tipo == TIPO.BOOLEANO:
            if self.truelbl == None:
                self.truelbl = generador.agregarLabel()
            if self.falselbl == None:
                self.falselbl = generador.agregarLabel()
            if self.valor:
                generador.agregarGoto(self.truelbl)
                generador.agregarGoto(self.falselbl)
            else:
                generador.agregarGoto(self.falselbl)
                generador.agregarGoto(self.truelbl)
            resultado = Return(self.valor, self.tipo, False)
            resultado.truelbl = self.truelbl
            resultado.falselbl = self.falselbl
            print('--primitivo--')
            print(resultado.truelbl)
            print(resultado.falselbl)
            print('--primitivo--')
            return resultado


    def getNodo(self):
        
        if isinstance(self.valor, list):
            nodo = NodoReporteArbol("PRIMITIVO")
            nodo.agregarHijoCadena("[")
            nuevo = NodoReporteArbol("LISTA_VECTOR")
            unaVez = True
            for i in self.valor:
                if unaVez:
                    nuevo1 = NodoReporteArbol("EXPRESION")
                    nuevo1.agregarHijoNodo(i.getNodo())
                    nuevo.agregarHijoNodo(nuevo1)
                else:
                    n = nuevo
                    nuevo1 = NodoReporteArbol("EXPRESION")
                    nuevo = NodoReporteArbol("LISTA_VECTOR")
                    nuevo.agregarHijoNodo(n)
                    nuevo.agregarHijoCadena(",")
                    nuevo1.agregarHijoNodo(i.getNodo())
                    nuevo.agregarHijoNodo(nuevo1)
                unaVez = False
            nodo.agregarHijoNodo(nuevo)
            nodo.agregarHijoCadena("]")
            return nodo
        nodo = NodoReporteArbol("PRIMITIVO")
        nodo.agregarHijo(self.valor)
        return nodo

    def getValue(self):
        return self.valor

    def toString(self):
        return str(self.valor)

'''
class Primitivo(Objeto):
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor=valor

    

    
'''

