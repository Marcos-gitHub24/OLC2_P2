from TS.Simbolo import Simbolo
from Objeto.Primitivo import Primitivo
from Expresiones.Identificador import Identificador
from typing import final
from Instrucciones.Asignacion import Asignacion
from Instrucciones.Continue import Continue
from Abstract.NodoReporteArbol import NodoReporteArbol
from Instrucciones.Return import Return
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break

class ForArreglo(NodoAST):
    def __init__(self, id, arreglo, inicio, final, instrucciones, fila, columna):
        super().__init__(TIPO.CADENA, fila, columna)
        self.id = id
        self.arreglo = arreglo
        self.inicio = inicio
        self.final = final
        self.instrucciones = instrucciones

    def interpretar(self, tree, table):
        nueva_tabla = TablaSimbolos(table)
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
        if(valor_final.tipo == TIPO.BOOLEANO):
            tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede realizar un for con un boolean",self.fila,self.columna))
            return  Excepcion(TIPO.ERROR, f"No puede realizar un for con un boolean",self.fila,self.columna)
        if(valor_final.tipo == TIPO.CHARACTER):
            tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede realizar un for con un caracter",self.fila,self.columna))
            return  Excepcion(TIPO.ERROR, f"No puede realizar un for con un caracter",self.fila,self.columna)

        asignar = Asignacion(self.id, valor_inicio, None, self.fila, self.columna)
        asignar.interpretar(tree, nueva_tabla)
        iterador = valor_inicio.valor
        condicion = True
        arreglo = Identificador(self.arreglo, self.fila, self.columna)
        arreglo = arreglo.interpretar(tree, table)
        if valor_inicio.valor < 1:
            tree.addExcepcion(Excepcion("Semantico", "Primer indice menor a 1", self.fila, self.columna))
            return Excepcion("Semantico", "Primer indice menor a 1", self.fila, self.columna)
        if valor_inicio.valor > len(arreglo.valor):
            tree.addExcepcion(Excepcion("Semantico", "Segundo indice mayor al tamaño del arreglo", self.fila, self.columna))
            return Excepcion("Semantico", "Segundo indice mayor al tamaño del arreglo", self.fila, self.columna)

        primer_valor = arreglo.valor[iterador-1].interpretar(tree,table)
        asignar = Asignacion(self.id, Primitivo(primer_valor.tipo, self.fila, self.columna, primer_valor.valor), None, self.fila, self.columna)
        asignar.interpretar(tree, nueva_tabla)
        iterador = iterador -1;
        while iterador < valor_final.valor:
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
                    tree.addExcepcion(result)
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
            if iterador != valor_final.valor:
                inter = arreglo.valor[iterador].interpretar(tree, table)
                simbolo = Simbolo(self.id, self.fila, self.columna, Primitivo(inter.tipo, self.fila, self.columna, inter.valor))
                tabla_for.actualizarTabla(simbolo)

    def getNodo(self):
        nodo = NodoReporteArbol("FOR")
        nodo.agregarHijoCadena("for")
        nodo.agregarHijoCadena(self.id)
        nodo.agregarHijoCadena("in")
        nodo.agregarHijoCadena(self.arreglo)
        nodo.agregarHijoCadena("[")
        nodo.agregarHijoNodo(self.inicio.getNodo())
        nodo.agregarHijoCadena(":")
        nodo.agregarHijoNodo(self.final.getNodo())
        nodo.agregarHijoCadena("]")
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