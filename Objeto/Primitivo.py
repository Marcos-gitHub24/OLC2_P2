from Abstract.NodoReporteArbol import NodoReporteArbol
from Abstract.NodoAST import NodoAST
from TS.Generador import Generador
from TS.Tipo import TIPO
from Abstract.Return import Return


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
            guardo = generador.agregarTemporal()
            generador.agregarExpresion(guardo, 'H', '', '')
            for i in self.valor:
                generador.guardar_heap('H', ord(i))
                generador.sumar_heap()
            generador.guardar_heap('H', '-1')
            generador.sumar_heap()
            return Return(guardo, TIPO.CADENA, True)
        elif self.tipo == TIPO.CHARACTER:
            guardo = generador.agregarTemporal()
            generador.agregarExpresion(guardo, 'H', '', '')
            for i in self.valor:
                generador.guardar_heap('H', ord(i))
                generador.sumar_heap()
            generador.guardar_heap('H', '-1')
            generador.sumar_heap()
            return Return(guardo, TIPO.CHARACTER, True)
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
            return resultado
        elif self.tipo == TIPO.NULO:
            #guardo = generador.agregarTemporal()
            #generador.guardar_heap('H','-1')
            #generador.agregarExpresion(guardo,'H','','')
            #generador.agregarExpresion('H','H','1','+')
            return Return('-1', TIPO.NULO, False)
        elif self.tipo == TIPO.ARREGLO:
            guardo = generador.agregarTemporal()
            generador.agregarExpresion(guardo, 'H', '', '')
            pivote = generador.agregarTemporal()
            generador.agregarExpresion(pivote,guardo,'1','+')
            tamano = len(self.valor) + 1
            generador.agregarExpresion('H','H',str(tamano),'+')
            generador.guardar_heap(guardo,str(tamano-1))
            resultado = Return(guardo,TIPO.ARREGLO,True)
            for i in self.valor:
                intepretado = i.interpretar(entorno)
                generador.guardar_heap(pivote,intepretado.valor)
                generador.agregarExpresion(pivote,pivote,'1','+')
            #generador.guardar_heap('H', '-2')
            #generador.agregarExpresion('H','H','1','+')
            #generador.sumar_heap()
            arreglo = obtenerVector(entorno,self.valor)
            resultado.arreglo = arreglo
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

def obtenerVector(entorno, vector):
        lista = []
        for i in vector:
            #valor = i.interpretar(entorno)
            if not isinstance(i,Primitivo):
                lista.append(i.tipo)
            elif isinstance(i.valor,list):
               lista.append(obtenerVector(entorno,i.valor))
            else:
                lista.append(i.tipo)
        return lista
        
        

