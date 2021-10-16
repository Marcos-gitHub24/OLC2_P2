from Abstract.Objeto import TipoObjeto
from Abstract.NodoReporteArbol import NodoReporteArbol
from TS.Tipo import TIPO
from Instrucciones.Return import Return
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break
from TS.Simbolo import Simbolo


class Funcion(NodoAST):
    def __init__(self, nombre, metodo, fila, columna):
        self.nombre = nombre
        self.metodo = metodo
        self.fila = fila
        self.columna = columna
    
    def interpretar(self, tree, table):
        nuevaTabla = TablaSimbolos(table) 
        met = table.getTabla(self.nombre)
        if met == None:
            simbolo = Simbolo(self.nombre, self.fila, self.columna, self.metodo)
            table.setTabla(simbolo)
        else:
            tree.addExcepcion(Excepcion("Semantico", "Ya existe una función con ese nombre", self.fila, self.columna))
            return Excepcion("Semantico", "Ya existe una función con ese nombre", self.fila, self.columna)

    def getNodo(self):
        nodo = NodoReporteArbol("FUNCION")
        parametros = NodoReporteArbol("PARAMETROS")
        nodo.agregarHijoCadena("function")
        nodo.agregarHijoCadena(self.nombre)
        nodo.agregarHijoCadena("(")
        para = True
        if self.metodo.parametros != None:
            for i in self.metodo.parametros:
                if para:
                    nuevo1 = NodoReporteArbol("PARAMETRO")
                    nuevo1.agregarHijoCadena(i)
                    parametros.agregarHijoNodo(nuevo1)
                else:
                    n = parametros
                    nuevo1 = NodoReporteArbol("PARAMETRO")
                    parametros = NodoReporteArbol("PARAMETROS")
                    parametros.agregarHijoNodo(n)
                    parametros.agregarHijoCadena(",")
                    nuevo1.agregarHijoCadena(i)
                    parametros.agregarHijoNodo(nuevo1)
                para = False
            nodo.agregarHijoNodo(parametros)
        nodo.agregarHijoCadena(")")
        instrucciones = NodoReporteArbol("INSTRUCCIONES")
        instrucciones = NodoReporteArbol("INSTRUCCIONES")
        unaVez = True
        for instr in self.metodo.instrucciones:
            if unaVez:
                nuevo1 = NodoReporteArbol("INSTRUCCION")
                nuevo1.agregarHijoNodo(instr.getNodo())
                #nuevo1.agregarHijoCadena(";")
                instrucciones.agregarHijoNodo(nuevo1)
            else:
                n = instrucciones
                nuevo1 = NodoReporteArbol("INSTRUCCION")
                instrucciones = NodoReporteArbol("INSTRUCCIONES")
                instrucciones.agregarHijoNodo(n)
                nuevo1.agregarHijoNodo(instr.getNodo())
                #nuevo1.agregarHijoCadena(";")
                instrucciones.agregarHijoNodo(nuevo1)
            unaVez = False
        nodo.agregarHijoNodo(instrucciones)
        nodo.agregarHijoCadena("end")
        nodo.agregarHijoCadena(";")
        return nodo