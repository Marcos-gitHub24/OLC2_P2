
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

            for i in self.parametros:
                bandera = False
                if entorno.dentro != None and isinstance(i, Llamada):
                    print("############SI ES LLAMADA ###########")
                    bandera = True
                    generador.guardarTemporales(generador.temporales[len(generador.temporales)-1],entorno.size,entorno)
                valores_parametros.append(i.interpretar(entorno))
                if bandera:
                    generador.recuperarTemporales(generador.temporales[len(generador.temporales)-1],entorno.size,entorno)

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
            arreglo_return = None
            print('---------TIPO-------------')
            if isinstance(met.tipo, list):
                print('=========entro aacacac===============')
                tipo_return = TIPO.ARREGLO
                arreglo_return = met.tipo
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
                retornar = Return(temporal, met.tipo, True)
                retornar.arreglo = met.metodo.arreglo_tipo
                retornar.truelbl = lbltrue
                retornar.falselbl = lblfalse
                return retornar
            else:
                retornar = Return(temporal, met.tipo, True)
                retornar.arreglo = met.metodo.arreglo_tipo
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