from Expresiones.Struct import Struct
from Abstract.NodoReporteArbol import NodoReporteArbol
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.Generador import Generador
from TS.Tipo import TIPO



class Asignacion(NodoAST):
    def __init__(self, identificador, expresion, tipo, fila, columna):
        self.identificador = identificador
        self.expresion = expresion
        self.tipo = tipo
        self.fila = fila
        self.columna = columna

    def interpretar(self, entorno):
        if self.identificador == None:
            return
        generador = Generador()
        generador = generador.obtenerGen()
        #es_struct = False
        esta_heap = False
        if self.tipo == None:
            if self.expresion != None and isinstance(self.expresion, Struct) == False:
                valor = self.expresion.interpretar(entorno)
                if isinstance(valor, Struct) == False:
                    if valor.tipo == TIPO.ERROR:
                        generador.TSglobal.addExcepcion(valor)
                        return valor
                         
                variable = entorno.obtenerVariable(self.identificador)
                if variable == None:
                    if valor.tipo == TIPO.CADENA:
                        esta_heap = True
                    if valor.tipo == TIPO.STRUCT:
                        #es_struct = True
                        esta_heap = True
                    if valor.tipo == TIPO.ARREGLO:
                        esta_heap = True
                    variable = entorno.guardarVariable(self.identificador,valor.tipo,esta_heap,valor.struct, valor.arreglo, self.fila, self.columna)
                    variable.tipo = valor.tipo
            else: # si es struct 
                valor = self.expresion
                variable = entorno.obtenerVariable(self.identificador)
                if variable == None:
                    if valor.tipo == TIPO.CADENA:
                        esta_heap = True
                    if valor.tipo == TIPO.STRUCT:
                        #es_struct = True
                        esta_heap = True
                    if valor.tipo == TIPO.ARREGLO:
                        esta_heap = True
                    variable = entorno.guardarVariable(self.identificador,valor.tipo,esta_heap,valor.struct,valor.arreglo, self.fila, self.columna)
                    variable.tipo = valor.tipo
            posicion = variable.pos
            variable.tipo = valor.tipo
            if not variable.isGlobal:
                posicion = generador.agregarTemporal()
                generador.agregarExpresion(posicion,'P',variable.pos,'+')
            if valor.tipo == TIPO.BOOLEANO:
                lbl = generador.agregarLabel()
                generador.colocarLbl(valor.truelbl)
                generador.guardar_stack(posicion, '1')
                generador.agregarGoto(lbl)
                generador.colocarLbl(valor.falselbl)
                generador.guardar_stack(posicion, '0')
                generador.colocarLbl(lbl)
            else:
                generador.guardar_stack(posicion, valor.valor)
                
        else:
            if self.expresion != None and isinstance(self.expresion, Struct) == False:
                valor = self.expresion.interpretar(entorno)
                if valor.tipo == TIPO.ERROR:
                    generador.TSglobal.addExcepcion(valor)
                    return valor
                if valor.tipo == self.tipo:
                    variable = entorno.obtenerVariable(self.identificador)
                    if variable == None:
                        if valor.tipo == TIPO.CADENA:
                            esta_heap = True
                        if valor.tipo == TIPO.STRUCT:
                            #es_struct = True
                            esta_heap = True
                        if valor.tipo == TIPO.ARREGLO:
                            esta_heap = True
                        variable = entorno.guardarVariable(self.identificador,valor.tipo,esta_heap,valor.struct, valor.arreglo, self.fila, self.columna)
                else:
                    print('No son del mismo tipo')
                    generador.TSglobal.addExcepcion(Excepcion(TIPO.ERROR, f"Semantico, No son del mismo tipo", self.fila, self.columna))
                    return None
            elif self.expresion !=None and isinstance(self.expresion,Struct):
                valor = self.expresion
                variable = entorno.obtenerVariable(self.identificador)
                if variable == None:
                    if valor.tipo == TIPO.CADENA:
                        esta_heap = True
                    if valor.tipo == TIPO.STRUCT:
                        #es_struct = True
                        esta_heap = True
                    if valor.tipo == TIPO.ARREGLO:
                        esta_heap = True
                    variable = entorno.guardarVariable(self.identificador,valor.tipo,esta_heap,valor.struct,valor.arreglo, self.fila, self.columnas)
            variable.tipo = valor.tipo
            posicion = variable.pos
            if not variable.isGlobal:
                posicion = generador.agregarTemporal()
                generador.agregarExpresion(posicion,'P',variable.pos,'+')
            if valor.tipo == TIPO.BOOLEANO:
                lbl = generador.agregarLabel()
                generador.colocarLbl(valor.truelbl)
                generador.guardar_stack(posicion, '1')
                generador.agregarGoto(lbl)
                generador.colocarLbl(valor.falselbl)
                generador.guardar_stack(posicion, '0')
                generador.colocarLbl(lbl)
            else:
                generador.guardar_stack(posicion, valor.valor)
                


        
        

    def getNodo(self):
        if self.tipo == None and self.expresion != None:
            nodo = NodoReporteArbol("DECLARACION")
            instruccion = NodoReporteArbol("DECLARACION")
            #nodo.agregarHijoNodo(instruccion)
            nodo.agregarHijo(str(self.identificador))
            nodo.agregarHijoCadena("=")
            expresion = NodoReporteArbol("EXPRESION")
            nodo.agregarHijoNodo(expresion)
            nodo.agregarHijoCadena(";")
            expresion.agregarHijoNodo(self.expresion.getNodo())
            return nodo
        elif self.expresion == None:
            nodo = NodoReporteArbol("DECLARACION")
            instruccion = NodoReporteArbol("DECLARACION")
            #nodo.agregarHijoNodo(instruccion)
            nodo.agregarHijo(str(self.identificador))
            nodo.agregarHijoCadena(";")
            return nodo
        else:
            nodo = NodoReporteArbol("DECLARACION")
            instruccion = NodoReporteArbol("DECLARACION")
            #nodo.agregarHijoNodo(instruccion)
            nodo.agregarHijo(str(self.identificador))
            nodo.agregarHijoCadena("=")
            expresion = NodoReporteArbol("EXPRESION")
            nodo.agregarHijoNodo(expresion)
            expresion.agregarHijoNodo(self.expresion.getNodo())
            if self.tipo == TIPO.ENTERO:
                nodo.agregarHijoCadena(":")
                nodo.agregarHijoCadena(":")
                nodo.agregarHijoCadena("Int64")
                nodo.agregarHijoCadena(";")
            elif self.tipo == TIPO.DECIMAL:
                nodo.agregarHijoCadena(":")
                nodo.agregarHijoCadena(":")
                nodo.agregarHijoCadena("Float64")
                nodo.agregarHijoCadena(";")
            elif self.tipo == TIPO.CADENA:
                nodo.agregarHijoCadena(":")
                nodo.agregarHijoCadena(":")
                nodo.agregarHijoCadena("String")
                nodo.agregarHijoCadena(";")
            elif self.tipo == TIPO.CHARACTER:
                nodo.agregarHijoCadena(":")
                nodo.agregarHijoCadena(":")
                nodo.agregarHijoCadena("Char")
                nodo.agregarHijoCadena(";")
            elif self.tipo == TIPO.BOOLEANO:
                nodo.agregarHijoCadena(":")
                nodo.agregarHijoCadena(":")
                nodo.agregarHijoCadena("Boolean")
                nodo.agregarHijoCadena(";")
            return nodo