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

class AccesoStruct(NodoAST):
    def __init__(self, nombre , atributos, fila, columna):
        self.nombre = nombre
        self.atributos = atributos
        self.fila = fila
        self.columna = columna
    def interpretar(self, entorno):
        aux = Generador()
        generador = aux.obtenerGen()
        obtenerStruct = Identificador(self.nombre, self.fila, self.columna)
        variable = obtenerStruct.interpretar(entorno)
        tipo = ''
        contador = 1
        if len(self.atributos) == 1:
            for i in self.atributos:
                if i in variable.struct.keys():
                    tipo = variable.struct[i][0]
                    if isinstance(variable.struct[i][0],list):
                        tipo = TIPO.ARREGLO
                        

                    referencia = generador.agregarTemporal()
                    regreso = generador.agregarTemporal() # el temporal que regresa el valor o referencia en el heap
                    generador.agregarExpresion(referencia,variable.valor,variable.struct[i][1],'+') #aca tengo que sumar la posicion donde esta el atributo en heap
                    generador.obtener_heap(regreso,referencia)
                    retorno = Return(regreso,tipo,True)
                    retorno.arreglo = variable.struct[i][0]
                    retorno.struct = variable.struct
                    return retorno

                else:
                    generador.TSglobal.addExcepcion(Excepcion("Semantico", "No existe un atributo con ese nombre", self.fila, self.columna))
                    return Excepcion("Semantico", "No existe un atributo con ese nombre", self.fila, self.columna)
        else:
            diccionario = variable.struct
            anterior = diccionario
            valor = variable.valor
            pivote = generador.agregarTemporal()
            generador.agregarExpresion(pivote,valor,'','')
            
            for i in self.atributos:
                if contador == len(self.atributos):
                    referencia = generador.agregarTemporal()
                    regreso = generador.agregarTemporal() # el temporal que regresa el valor o referencia en el heap
                    tipo = diccionario[i][0]
                    retorno = Return(regreso,tipo,True)
                    
                    if isinstance(diccionario[i][0],list):
                        tipo = TIPO.ARREGLO
                        retorno.arreglo = diccionario[i][0]   
                        
                        print(retorno.arreglo)        
                    #generador.obtener_heap(referencia,pivote)
                    generador.agregarExpresion(referencia,pivote,'','') # agregado
                    generador.agregarExpresion(referencia,referencia,diccionario[i][1],'+') #aca tengo que sumar la posicion donde esta el atributo en heap
                    generador.obtener_heap(regreso,referencia)

                    retorno.struct = variable.struct
                    retorno.tipo = tipo
                    return retorno

                else:
                    if i in diccionario.keys():
                        anterior = diccionario
                        diccionario = diccionario[i][2]
                        contador+=1
                        generador.agregarExpresion(pivote,pivote,anterior[i][1],'+')
                        generador.obtener_heap(pivote,pivote)
                        #generador.obtener_heap()
                    else:
                        generador.TSglobal.addExcepcion(Excepcion("Semantico", "No existe un atributo con ese nombre", self.fila, self.columna))
                        return Excepcion("Semantico", "No existe un atributo con ese nombre", self.fila, self.columna)
        

                
                    


                    


        

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