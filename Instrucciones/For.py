from TS.Simbolo import Simbolo
from Objeto.Primitivo import Primitivo
from Expresiones.Identificador import Identificador
from typing import final
from Instrucciones.Asignacion import Asignacion
from Instrucciones.Continue import Continue
import re
from Abstract.Objeto import TipoObjeto
from Abstract.NodoReporteArbol import NodoReporteArbol
from Instrucciones.Return import Return
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break

class For(NodoAST):
    def __init__(self, id, inicio, final,instrucciones, fila, columna):
        super().__init__(TIPO.BOOLEANO, fila, columna)
        self.id = id
        self.inicio = inicio
        self.final = final
        self.instrucciones = instrucciones

    def interpretar(self, tree, table):
        nueva_tabla = TablaSimbolos(table)
        nueva_tabla.setEntorno("For")
        tree.agregarTabla(nueva_tabla)
        valor_inicio = self.inicio.interpretar(tree, nueva_tabla)
        if(valor_inicio.tipo == TIPO.ERROR):
            tree.addExcepcion(valor_inicio)
            return valor_inicio;
        valor_final = self.final.interpretar(tree, nueva_tabla)
        if(valor_final.tipo == TIPO.ERROR):
            tree.addExcepcion(valor_final)
            return valor_final;

        if(valor_inicio.tipo == TIPO.CADENA):
            tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede realizar un for con una cadena",self.fila,self.columna))
            return  Excepcion(TIPO.ERROR, f"No puede realizar un for con una cadena",self.fila,self.columna)
        if(valor_inicio.tipo == TIPO.CHARACTER):
            tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede realizar un for con un caracter",self.fila,self.columna))
            return  Excepcion(TIPO.ERROR, f"No puede realizar un for con un caracter",self.fila,self.columna)
        if(valor_final.tipo == TIPO.CADENA):
            tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede realizar un for con una cadena",self.fila,self.columna))
            return  Excepcion(TIPO.ERROR, f"No puede realizar un for con una cadena",self.fila,self.columna)
        if(valor_final.tipo == TIPO.CHARACTER):
            tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede realizar un for con una cadena",self.fila,self.columna))
            return  Excepcion(TIPO.ERROR, f"No puede realizar un for con un caracter",self.fila,self.columna)

        asignar = Asignacion(self.id, valor_inicio, None, self.fila, self.columna)
        asignar.interpretar(tree, nueva_tabla)
        iterador = valor_inicio.valor
        condicion = True
        while iterador <= valor_final.valor:
            tabla_for = TablaSimbolos(nueva_tabla)
            tabla_for.setEntorno("For")
            tree.agregarTabla(tabla_for)
            for i in self.instrucciones:
                if isinstance(i, Excepcion):
                    tree.updateConsola(i.toString())
                    tree.addExcepcion(i)
                    continue
                result = i.interpretar(tree, tabla_for)
                if isinstance(result, Excepcion):
                    tree.updateConsola(result.toString())
                    tree.addExcepcion(result.toString())
                    continue
                if isinstance(result, Break):
                    condicion = False
                    break
                if isinstance(result, Continue):
                    break
                if isinstance(result, Return):
                    return result
            if condicion == False:
                condicion = True
                break
            iterador += 1
            simbolo = Simbolo(self.id, self.fila, self.columna, Primitivo(TIPO.ENTERO, self.fila, self.columna, iterador))
            tabla_for.actualizarTabla(simbolo)

    def getNodo(self):
        nodo = NodoReporteArbol("FOR")
        nodo.agregarHijoCadena("for")
        nodo.agregarHijoCadena(self.id)
        nodo.agregarHijoCadena("in")
        nodo.agregarHijoNodo(self.inicio.getNodo())
        nodo.agregarHijoCadena(":")
        nodo.agregarHijoNodo(self.final.getNodo())
        instrucciones = NodoReporteArbol("INSTRUCCIONES")
        unaVez = True
        for instr in self.instrucciones:
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