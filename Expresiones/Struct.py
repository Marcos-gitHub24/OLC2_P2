from Abstract.Objeto import TipoObjeto
from Abstract.NodoReporteArbol import NodoReporteArbol
from Expresiones.Identificador import Identificador
from TS.Generador import Generador
from TS.Tipo import TIPO
from Instrucciones.Return import Return
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break
from TS.Simbolo import Simbolo


class Struct(NodoAST):
    def __init__(self, nombre ,atributos, mutable,fila, columna):
        self.nombre = nombre
        self.atributos = atributos
        self.mutable = mutable
        self.diccionario = {}
        self.fila = fila
        self.columna = columna
    
    def interpretar(self, entorno):
        met = entorno.obtenerStruct(self.nombre)
        aux = Generador()
        generador = aux.obtenerGen()
        if met == None:
            contador = 0 
            lista_aux =  []      
            diccionario_aux = {}     
            bandera = False
            for i in self.atributos:
                lista_aux.append(i)
                if isinstance(i.tipo,list):
                    if i.tipo[0] == TIPO.STRUCT:
                        if i.tipo[1] == self.nombre:
                            diccionario_aux[i.nombre] = [i.tipo, contador]
                            bandera = True
                        else:
                            obtener_struct = entorno.obtenerStruct(i.tipo[1])
                            self.diccionario[i.nombre] = [i.tipo, contador, obtener_struct]
                    else:
                        self.diccionario[i.nombre] = [i.tipo, contador]
                else:
                    self.diccionario[i.nombre] = [i.tipo, contador]
                    diccionario_aux[i.nombre] = [i.tipo, contador]
                contador += 1
            if bandera:
                contador = 0
                for i in lista_aux:
                    if isinstance(i.tipo,list):
                        if i.tipo[0] == TIPO.STRUCT:
                            if i.tipo[1] == self.nombre:
                                self.diccionario[i.nombre] = [i.tipo,contador,diccionario_aux]
                            else:
                                obtener_struct = entorno.obtenerStruct(i.tipo[1])
                                self.diccionario[i.nombre] = [i.tipo, contador, obtener_struct]
                        else:
                            self.diccionario[i.nombre] = [i.tipo, contador]
                    else:
                        self.diccionario[i.nombre] = [i.tipo, contador]
                    contador += 1

            generador.TSglobal.guardarStruct(self.nombre, self.diccionario) 
            #simbolo = Simbolo(self.nombre, self.fila, self.columna, self)
            #table.setTabla(simbolo)
            
        else:
            generador.TSglobal.addExcepcion(Excepcion("Semantico", "Ya existe una función con ese nombre", self.fila, self.columna))
            return Excepcion("Semantico", "Ya existe una función con ese nombre", self.fila, self.columna)

    def getNodo(self):
        nodo = NodoReporteArbol("DECLARACION_STRUCT")
        nuevo = NodoReporteArbol("LISTA_ATRIBUTOS")
        if self.mutable:
            nodo.agregarHijoCadena("mutable")
        nodo.agregarHijoCadena("struct")
        nodo.agregarHijoCadena(self.nombre)
        unaVez = True
        for i in self.atributos:
            if unaVez:
                nuevo1 = NodoReporteArbol("ATRIBUTO")
                if i.tipo == TIPO.ENTERO:
                    nuevo1.agregarHijoCadena(i.nombre)
                    nuevo1.agregarHijoCadena("::")
                    nuevo1.agregarHijoCadena("Int64")
                elif i.tipo == TIPO.DECIMAL:
                    nuevo1.agregarHijoCadena(i.nombre)
                    nuevo1.agregarHijoCadena("::")
                    nuevo1.agregarHijoCadena("Float64")
                elif i.tipo == TIPO.CADENA:
                    nuevo1.agregarHijoCadena(i.nombre)
                    nuevo1.agregarHijoCadena("::")
                    nuevo1.agregarHijoCadena("String")
                elif i.tipo == TIPO.CHARACTER:
                    nuevo1.agregarHijoCadena(i.nombre)
                    nuevo1.agregarHijoCadena("::")
                    nuevo1.agregarHijoCadena("Char")
                elif i.tipo == TIPO.BOOLEANO:
                    nuevo1.agregarHijoCadena(i.nombre)
                    nuevo1.agregarHijoCadena("::")
                    nuevo1.agregarHijoCadena("Boolean")
                else:
                    nuevo1.agregarHijoCadena(i.nombre)
                nuevo1.agregarHijoCadena(";")
                nuevo.agregarHijoNodo(nuevo1)
                
            else:
                n = nuevo
                nuevo1 = NodoReporteArbol("ATRIBUTO")
                nuevo = NodoReporteArbol("LISTA_ATRIBUTO")
                nuevo.agregarHijoNodo(n)
                if i.tipo == TIPO.ENTERO:
                    nuevo1.agregarHijoCadena(i.nombre)
                    nuevo1.agregarHijoCadena("::")
                    nuevo1.agregarHijoCadena("Int64")
                elif i.tipo == TIPO.DECIMAL:
                    nuevo1.agregarHijoCadena(i.nombre)
                    nuevo1.agregarHijoCadena("::")
                    nuevo1.agregarHijoCadena("Float64")
                elif i.tipo == TIPO.CADENA:
                    nuevo1.agregarHijoCadena(i.nombre)
                    nuevo1.agregarHijoCadena("::")
                    nuevo1.agregarHijoCadena("String")
                elif i.tipo == TIPO.CHARACTER:
                    nuevo1.agregarHijoCadena(i.nombre)
                    nuevo1.agregarHijoCadena("::")
                    nuevo1.agregarHijoCadena("Char")
                elif i.tipo == TIPO.BOOLEANO:
                    nuevo1.agregarHijoCadena(i.nombre)
                    nuevo1.agregarHijoCadena("::")
                    nuevo1.agregarHijoCadena("Boolean")
                else:
                    nuevo1.agregarHijoCadena(i.nombre)
                nuevo1.agregarHijoCadena(";")
                nuevo.agregarHijoNodo(nuevo1)
            unaVez = False
        nodo.agregarHijoNodo(nuevo)
        nodo.agregarHijoCadena("end")
        nodo.agregarHijoCadena(";")
        return nodo
