
from Instrucciones.AsignacionStruct import AsignacionStruct
from Abstract.Return import Return
from Abstract.NodoReporteArbol import NodoReporteArbol
from TS.Entorno import Entorno
from TS.Simbolo import Simbolo
from Instrucciones.Funcion import Funcion
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break
from Expresiones.Struct import Struct
from TS.Generador import Generador
from TS.Tipo import TIPO

class Llamada(NodoAST):
    def __init__(self, nombre, parametros, fila, columna):
        self.nombre = nombre
        self.parametros = parametros
        self.fila = fila
        self.columna = columna
    
    def interpretar(self, entorno):
        met = entorno.obtenerFuncion(self.nombre)
        if met != None:
            valores_parametros = []
            aux = Generador()
            generador = aux.obtenerGen()
            tamano = entorno.size
            temporal_recupero_guardo = None  # esta variable es para cuando en una llamada se tiene como parametro otra llamada
            for i in self.parametros:
                bandera = False
                if entorno.dentro != None and isinstance(i, Llamada):
                    bandera = True
                    generador.addComment('GUARDO') 
                                              
                    temporal_recupero_guardo = generador.temporales[len(generador.temporales)-1]  # aca guardo el ultimo temporal
                    guardo = generador.agregarTemporal() 
                    generador.agregarExpresion(guardo,'P',entorno.size,'+')
                    generador.guardar_stack(guardo,temporal_recupero_guardo)
                    entorno.size = entorno.size + 1
                    

                valores_parametros.append(i.interpretar(entorno))

                if bandera:  #para recuperar el resultado despues de haber interpretado la llamada
                    generador.addComment('RECUPERO')
                    recupero = generador.agregarTemporal()
                    entorno.size = entorno.size -1
                    generador.agregarExpresion(recupero,'P',entorno.size,'+')   
                    generador.obtener_stack(temporal_recupero_guardo,recupero) # aca recupero el temporal que se guardo

            temporal = generador.agregarTemporal()

            generador.agregarExpresion(temporal,'P',tamano+1,'+')
            auxiliar = 0

            for i in valores_parametros:
                auxiliar += 1
                generador.guardar_stack(temporal,i.valor)
                if auxiliar != len(valores_parametros):
                    generador.agregarExpresion(temporal,temporal,'1','+')

            generador.newEnv(tamano)
            generador.callFun(self.nombre)
            generador.obtener_stack(temporal,'P')
            generador.retEnv(tamano)
            tipo_return = TIPO.ENTERO
            es_arreglo = False
            arreglo_return = None
            print('=========METO.TIPO ===============')
            print(met.tipo)
            print(met.metodo.arreglo_tipo)
            if met.tipo== TIPO.ARREGLO:
                print('=========entro aacacac===============')
                tipo_return = TIPO.ARREGLO
                arreglo_return = met.metodo.arreglo_tipo
            else:
                arreglo_return = None
                tipo_return = met.tipo
            print(met.tipo)
            print('=========ARREGLO===============')
            print(arreglo_return)
            if met.tipo == TIPO.BOOLEANO:
                lbltrue = generador.agregarLabel()
                lblfalse = generador.agregarLabel()
                generador.agregarIf(temporal,'1','==',lbltrue)
                generador.agregarGoto(lblfalse)
                retornar = Return(temporal, tipo_return, True)
                retornar.arreglo = met.metodo.arreglo_tipo
                retornar.truelbl = lbltrue
                retornar.falselbl = lblfalse
                return retornar
            else:
                
                retornar = Return(temporal, tipo_return, True)
                retornar.arreglo = arreglo_return
                print('=========ARREGLO DEL RETORNO===============')
                print(tipo_return)
                print(arreglo_return)
                return retornar
        else:
            print("para structs")

            
        #else:
        #    return Excepcion("Semantico", f"Error al llamar a {self.nombre}", self.fila, self.columna)

                    
    def getNodo(self):
        nodo = NodoReporteArbol("LLAMADA")
        nodo.agregarHijo(str(self.nombre))
        nodo.agregarHijoCadena("(")
        para = True
        if self.parametros != None:
            parametros = NodoReporteArbol("PARAMETROS")
            for i in self.parametros:
                if para:
                    nuevo1 = NodoReporteArbol("PARAMETRO")
                    nuevo1.agregarHijoNodo(i.getNodo())
                    parametros.agregarHijoNodo(nuevo1)
                else:
                    n = parametros
                    nuevo1 = NodoReporteArbol("PARAMETRO")
                    parametros = NodoReporteArbol("PARAMETROS")
                    parametros.agregarHijoNodo(n)
                    parametros.agregarHijoCadena(",")
                    nuevo1.agregarHijoNodo(i.getNodo())
                    parametros.agregarHijoNodo(nuevo1)
                para = False
            nodo.agregarHijoNodo(parametros)
        nodo.agregarHijoCadena(")")
        nodo.agregarHijoCadena(";")
        return nodo