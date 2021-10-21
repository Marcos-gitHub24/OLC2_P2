from TS.Generador import Generador
from Abstract.Return import Return
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

    def interpretar(self, entorno):
        lista = []
        aux = Generador()
        generador = aux.obtenerGen()
        nuevo_valor = self.nuevo.interpretar(entorno)
        for i in self.lista:
            result = i.interpretar(entorno)
            if(result.tipo == TIPO.CADENA):
                #tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede tener un indice cadena",self.fila,self.columna))
                return  Excepcion(TIPO.ERROR, f"No puede tener un indice cadena",self.fila,self.columna)
            if(result.tipo == TIPO.CHARACTER):
                #tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede tener un indice char",self.fila,self.columna))
                return  Excepcion(TIPO.ERROR, f"No puede tener un indice char",self.fila,self.columna)
            if(result.tipo == TIPO.BOOLEANO):
                #tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede tener un indice booleano",self.fila,self.columna))
                return  Excepcion(TIPO.ERROR, f"No puede tener un indice booleano",self.fila,self.columna)
            if(result.tipo == TIPO.DECIMAL):
                #tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede tener un indice decimal",self.fila,self.columna))
                return  Excepcion(TIPO.ERROR, f"No puede adadsadadasdasd un indice decimal",self.fila,self.columna)
            lista.append(result.valor)
        variable = entorno.obtenerVariable(self.identificador)
        print("-----variable---")
        print(variable.arreglo)
        pivote = generador.agregarTemporal()
        apunta_heap = generador.agregarTemporal()
        generador.obtener_stack(pivote,variable.pos)
        tamano = generador.agregarTemporal()
        indice = generador.agregarTemporal()
        extra = generador.agregarLabel()
        #resultado.falselbl = extra
        for i in lista:
            salida = generador.agregarLabel()
            error = generador.agregarLabel()
            
            generador.obtener_heap(tamano,pivote)
            generador.agregarExpresion(indice,i,'','')

            generador.agregarIf(indice,tamano,'>',error)
            generador.agregarExpresion(apunta_heap,pivote,indice,'+')
            generador.obtener_heap(pivote,apunta_heap)
            
            generador.agregarGoto(salida)
            generador.colocarLbl(error)
            generador.agregarPrint('c','101')
            generador.agregarPrint('c','114')
            generador.agregarPrint('c','114')
            generador.agregarPrint('c','111')
            generador.agregarPrint('c','114')
            generador.agregarGoto(extra)
            generador.colocarLbl(salida)
        generador.guardar_heap(apunta_heap,nuevo_valor.valor)
        generador.colocarLbl(extra)
        #return Return(pivote,TIPO.ENTERO,True)
        
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