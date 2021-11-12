import re
from Expresiones.atributo import atributo
from Abstract.Objeto import TipoObjeto
from Abstract.NodoReporteArbol import NodoReporteArbol
from TS.Tipo import TIPO
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break
from TS.Simbolo import Simbolo
from Abstract.Return import Return
from TS.Generador import Generador
    
from Expresiones.Identificador import Identificador


class ModificaStruct(NodoAST):
    def __init__(self, identificador, atributo, expresion, fila, columna):
        self.identificador = identificador
        self.atributo = atributo
        self.expresion = expresion
        self.fila = fila
        self.columna = columna

    def interpretar(self, entorno):
        nuevo_valor = self.expresion.interpretar(entorno)
        aux = Generador()
        generador = aux.obtenerGen()
        obtenerStruct = Identificador(self.identificador, self.fila, self.columna)
        variable = obtenerStruct.interpretar(entorno)
        tipo = ''
        contador = 1
        
        if len(self.atributo) == 1:
            for i in self.atributo:
                if i in variable.struct.keys():
                    print(variable.struct[i])
                    tipo = variable.struct[i][0]
                    referencia = generador.agregarTemporal()
                    dic = variable.struct
                    if isinstance(variable.struct[i][0],list):  
                            tipo = TIPO.ARREGLO
                   
                    generador.agregarExpresion(referencia,variable.valor,dic[i][1],'+') #aca tengo que sumar la posicion donde esta el atributo en heap
                    generador.guardar_heap(referencia, nuevo_valor.valor)
                else:
                    generador.TSglobal.addExcepcion(Excepcion("Semantico", "No existe un atributo con ese nombre", self.fila, self.columna))
                    return Excepcion("Semantico", "No existe un atributo con ese nombre", self.fila, self.columna)
    
        else:
            diccionario = variable.struct
            anterior = diccionario
            valor = variable.valor
            pivote = generador.agregarTemporal()
            generador.agregarExpresion(pivote,valor,'','')
            for i in self.atributo:
                if contador == len(self.atributo):
                    
                    referencia = generador.agregarTemporal()

                    generador.agregarExpresion(referencia,pivote,'','') # agregado
                    generador.agregarExpresion(referencia,referencia,diccionario[i][1],'+') #aca tengo que sumar la posicion donde esta el atributo en heap
                    generador.guardar_heap(referencia, nuevo_valor.valor)


                else:
                    if i in diccionario.keys():
                        anterior = diccionario
                        diccionario = diccionario[i][2]
                        contador+=1
                        generador.agregarExpresion(pivote,pivote,anterior[i][1],'+')
                        generador.obtener_heap(pivote,pivote)
                    else:
                        generador.TSglobal.addExcepcion(Excepcion("Semantico", "No existe un atributo con ese nombre", self.fila, self.columna))
                        return Excepcion("Semantico", "No existe un atributo con ese nombre", self.fila, self.columna)
        


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