from TS.Simbolo import Simbolo
from Expresiones.Identificador import Identificador
from io import open_code
from os import truncate
from Objeto.Primitivo import Primitivo
from Abstract.Objeto import TipoObjeto
from enum import Enum
from Abstract.NodoReporteArbol import NodoReporteArbol
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO, OperadorAritmetico
from math import log, log10, sin, cos, tan, sqrt, trunc

class Nativa(NodoAST):
    
    def __init__(self, operador, base, valor, fila, columna):
        super().__init__(TIPO.ENTERO, fila, columna)
        self.operador = operador
        self.base = base
        self.valor = valor

    def interpretar(self, tree, table):
        res_base = None
        res_valor = None
        if(self.valor == ""):
            if isinstance(self.base, str):
                 res_base = self.base
            else:
                res_base = self.base.interpretar(tree,table)
                if(res_base.tipo == TIPO.ERROR):
                    tree.addExcepcion(res_base)
                    return res_base;
        elif isinstance(self.base, str):
             res_base = self.base
             res_valor = self.valor.interpretar(tree,table)
             if(res_valor.tipo == TIPO.ERROR):
                tree.addExcepcion(res_valor)
                return res_valor;
        else:
            res_base = self.base.interpretar(tree,table)
            if(res_base.tipo == TIPO.ERROR):
                tree.addExcepcion(res_base)
                return res_base;
            res_valor = self.valor.interpretar(tree,table)
            if(res_valor.tipo == TIPO.ERROR):
                tree.addExcepcion(res_valor)
                return res_valor;

        if (self.operador == OperadorAritmetico.BASE10):
            valor = log10(res_base.getValue())
            return Primitivo(TIPO.DECIMAL, self.fila, self.columna, valor)

        if (self.operador == OperadorAritmetico.BASE):
            return Primitivo(TIPO.DECIMAL, self.fila, self.columna, log(float(res_base.getValue()),float(res_valor.getValue())))

        if (self.operador == OperadorAritmetico.SENO):
            return Primitivo(TIPO.DECIMAL, self.fila, self.columna, sin(float(res_base.getValue())))

        if (self.operador == OperadorAritmetico.COSENO):
            return Primitivo(TIPO.DECIMAL, self.fila, self.columna, cos(float(res_base.getValue())))

        if (self.operador == OperadorAritmetico.TANGENTE):
            return Primitivo(TIPO.DECIMAL, self.fila, self.columna, tan(float(res_base.getValue())))

        if (self.operador == OperadorAritmetico.RAIZ):
            if(float(str(res_base.getValue())) > 0):
                return Primitivo(TIPO.DECIMAL, self.fila, self.columna, sqrt(float(res_base.getValue())))

        if (self.operador == OperadorAritmetico.LOWER):
            return Primitivo(TIPO.CADENA, self.fila, self.columna, str.lower(str(res_base.getValue())))
        
        if (self.operador == OperadorAritmetico.UPPER):
            return Primitivo(TIPO.CADENA, self.fila, self.columna, str.upper(str(res_base.getValue())))

        if (self.operador == OperadorAritmetico.PARSE):
            if res_valor.tipo == TIPO.CADENA:
                if res_base == "Float64":
                    return Primitivo(TIPO.DECIMAL, self.fila, self.columna, float(res_valor.getValue()))
                elif res_base == "Int64":
                    return Primitivo(TIPO.ENTERO, self.fila, self.columna, int(res_valor.getValue()))
                else:
                    tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede parsearse con ese tipo",self.fila,self.columna))
                    return Excepcion(TIPO.ERROR, f"No puede parsearse con ese tipo",self.fila,self.columna);
            else:
                tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede parsearse con ese tipo",self.fila,self.columna))
                return Excepcion(TIPO.ERROR, f"No puede parsearse con ese tipo",self.fila,self.columna);

        if (self.operador == OperadorAritmetico.TRUNC):
            if res_valor.tipo == TIPO.DECIMAL:
                if res_base == "Int64":
                    return Primitivo(TIPO.ENTERO, self.fila, self.columna, trunc(res_valor.getValue()))
                elif res_base == "":
                    return Primitivo(TIPO.DECIMAL, self.fila, self.columna, trunc(res_valor.getValue()))
                else:
                    tree.addExcepcion(Excepcion(TIPO.ERROR, f"No trunquear ese tipo",self.fila,self.columna))
                    return Excepcion(TIPO.ERROR, f"No trunquear ese tipo",self.fila,self.columna);
            else:
                tree.addExcepcion(Excepcion(TIPO.ERROR, f"No trunquear ese tipo",self.fila,self.columna))
                return Excepcion(TIPO.ERROR, f"No trunquear ese tipo",self.fila,self.columna);

        if (self.operador == OperadorAritmetico.FLOAT):
            if res_base.tipo == TIPO.ENTERO:
                return Primitivo(TIPO.DECIMAL, self.fila, self.columna, float(res_base.getValue()))
            else:
                tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede realizar float a ese tipo",self.fila,self.columna))
                return Excepcion(TIPO.ERROR, f"No puede realizar float a ese tipo",self.fila,self.columna);

        if (self.operador == OperadorAritmetico.STRING):
            if isinstance(res_base.getValue(), list):
                lista = []
                for i in res_base.getValue():
                    a = i.interpretar(tree, table)
                    lista.append(a.valor)
                return Primitivo(TIPO.CADENA, self.fila, self.columna, str(lista))        
            return Primitivo(TIPO.CADENA, self.fila, self.columna, str(res_base.getValue()))
        
        if (self.operador == OperadorAritmetico.TYPEOF):
            if res_base.tipo == TIPO.ENTERO:
                return Primitivo(TIPO.CADENA, self.fila, self.columna, "Int64")
            elif res_base.tipo == TIPO.DECIMAL:
                return Primitivo(TIPO.CADENA, self.fila, self.columna, "Float64")
            elif res_base.tipo == TIPO.CHARACTER:
                return Primitivo(TIPO.CADENA, self.fila, self.columna, "Char")
            elif res_base.tipo == TIPO.BOOLEANO:
                return Primitivo(TIPO.CADENA, self.fila, self.columna, "Bool")
            elif res_base.tipo == TIPO.CADENA:
                return Primitivo(TIPO.CADENA, self.fila, self.columna, "String")
            else:
                tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede realizar typeof con esa expresion",self.fila,self.columna))
                return Excepcion(TIPO.ERROR, f"No puede realizar typeof con esa expresion",self.fila,self.columna);

        if self.operador == OperadorAritmetico.PUSH:
            if isinstance(res_base, str):
                arreglo = Identificador(res_base, self.fila, self.columna)
                arreglo = arreglo.interpretar(tree, table)
                if arreglo.tipo == TIPO.ARREGLO:
                    arreglo.valor.append(res_valor)
                    simbolo = Simbolo(res_base, self.fila, self.columna, Primitivo(TIPO.ARREGLO, self.fila, self.columna, arreglo.valor))
                    table.actualizarTabla(simbolo)
                else:     
                    tree.addExcepcion(Excepcion(TIPO.ERROR, f"Solo se puede realizar el push en arreglos",self.fila,self.columna))
                    return Excepcion(TIPO.ERROR, f"Solo se puede realizar el push en arreglos",self.fila,self.columna);
            elif isinstance(res_base, Primitivo):
                     if res_base.tipo == TIPO.ARREGLO:
                        res_base.valor.append(res_valor)
                     else:     
                        tree.addExcepcion(Excepcion(TIPO.ERROR, f"Solo se puede realizar el length en arreglos",self.fila,self.columna))
                        return Excepcion(TIPO.ERROR, f"Solo se puede realizar el length en arreglos",self.fila,self.columna);
            else:   
                tree.addExcepcion(Excepcion(TIPO.ERROR, f"Solo se puede realizar el length en arreglos",self.fila,self.columna))
                return Excepcion(TIPO.ERROR, f"Solo se puede realizar el length en arreglos",self.fila,self.columna);
    
        if self.operador == OperadorAritmetico.POP:
            arreglo = Identificador(res_base, self.fila, self.columna)
            arreglo = arreglo.interpretar(tree, table)
            if arreglo.tipo == TIPO.ARREGLO:
                valor = arreglo.valor.pop(len(arreglo.valor)-1)
                simbolo = Simbolo(res_base, self.fila, self.columna, Primitivo(TIPO.ARREGLO, self.fila, self.columna, arreglo.valor))
                table.actualizarTabla(simbolo)
                valor = valor.interpretar(tree, table)
                return Primitivo(valor.tipo, self.fila, self.columna, valor.valor)
            else:
                tree.addExcepcion(Excepcion(TIPO.ERROR, f"Solo se puede realizar el pop en arreglos",self.fila,self.columna))     
                return Excepcion(TIPO.ERROR, f"Solo se puede realizar el pop en arreglos",self.fila,self.columna);
        
        if self.operador == OperadorAritmetico.LENGTH:
                if isinstance(res_base, str):
                    arreglo = Identificador(res_base, self.fila, self.columna)
                    arreglo = arreglo.interpretar(tree, table)
                    if arreglo.tipo == TIPO.ARREGLO:
                        valor = len(arreglo.valor)
                        return Primitivo(TIPO.ENTERO, self.fila, self.columna, valor)
                    else:  
                        tree.addExcepcion(Excepcion(TIPO.ERROR, f"Solo se puede realizar el length en arreglos",self.fila,self.columna))   
                        return Excepcion(TIPO.ERROR, f"Solo se puede realizar el length en arreglos",self.fila,self.columna);
                elif isinstance(res_base, Primitivo):
                     if res_base.tipo == TIPO.ARREGLO:
                        valor = len(res_base.valor)
                        return Primitivo(TIPO.ENTERO, self.fila, self.columna, valor)
                     else:     
                        tree.addExcepcion(Excepcion(TIPO.ERROR, f"Solo se puede realizar el length en arreglos",self.fila,self.columna))
                        return Excepcion(TIPO.ERROR, f"Solo se puede realizar el length en arreglos",self.fila,self.columna);
                else:
                    tree.addExcepcion(Excepcion(TIPO.ERROR, f"Solo se puede realizar el length en arreglos",self.fila,self.columna))     
                    return Excepcion(TIPO.ERROR, f"Solo se puede realizar el length en arreglos",self.fila,self.columna);


    def getNodo(self):
        if self.operador == OperadorAritmetico.BASE10:
            nodo = NodoReporteArbol("LOGARITMO10")
            nodo.agregarHijoCadena("log10")
            nodo.agregarHijoCadena("(")
            expresion = NodoReporteArbol("EXPRESION")
            expresion.agregarHijoNodo(self.base.getNodo())
            nodo.agregarHijoNodo(expresion)
            nodo.agregarHijoCadena(")")
            return nodo
        elif self.operador == OperadorAritmetico.BASE:
            expresion = NodoReporteArbol("LOGARITMO")
            izquierdo = NodoReporteArbol("EXPRESION")
            derecho = NodoReporteArbol("EXPRESION")
            expresion.agregarHijoCadena("log")
            expresion.agregarHijoCadena("(")
            expresion.agregarHijoNodo(izquierdo)
            izquierdo.agregarHijoNodo(self.base.getNodo())
            expresion.agregarHijoCadena(",")
            expresion.agregarHijoNodo(derecho)
            derecho.agregarHijoNodo(self.valor.getNodo())
            expresion.agregarHijoCadena(")")
            return expresion
        elif self.operador == OperadorAritmetico.SENO:
            nodo = NodoReporteArbol("SENO")
            nodo.agregarHijoCadena("sin")
            nodo.agregarHijoCadena("(")
            expresion = NodoReporteArbol("EXPRESION")
            expresion.agregarHijoNodo(self.base.getNodo())
            nodo.agregarHijoNodo(expresion)
            nodo.agregarHijoCadena(")")
            return nodo
        elif self.operador == OperadorAritmetico.COSENO:
            nodo = NodoReporteArbol("COSENO")
            nodo.agregarHijoCadena("cos")
            nodo.agregarHijoCadena("(")
            expresion = NodoReporteArbol("EXPRESION")
            expresion.agregarHijoNodo(self.base.getNodo())
            nodo.agregarHijoNodo(expresion)
            nodo.agregarHijoCadena(")")
            return nodo
        elif self.operador == OperadorAritmetico.TANGENTE:
            nodo = NodoReporteArbol("TANGENTE")
            nodo.agregarHijoCadena("tan")
            nodo.agregarHijoCadena("(")
            expresion = NodoReporteArbol("EXPRESION")
            expresion.agregarHijoNodo(self.base.getNodo())
            nodo.agregarHijoNodo(expresion)
            nodo.agregarHijoCadena(")")
            return nodo
        elif self.operador == OperadorAritmetico.RAIZ:
            nodo = NodoReporteArbol("RAIZ")
            nodo.agregarHijoCadena("sqrt")
            nodo.agregarHijoCadena("(")
            expresion = NodoReporteArbol("EXPRESION")
            expresion.agregarHijoNodo(self.base.getNodo())
            nodo.agregarHijoNodo(expresion)
            nodo.agregarHijoCadena(")")
            return nodo
        elif self.operador == OperadorAritmetico.LOWER:
            nodo = NodoReporteArbol("LOWER")
            nodo.agregarHijoCadena("lowercase")
            nodo.agregarHijoCadena("(")
            expresion = NodoReporteArbol("EXPRESION")
            expresion.agregarHijoNodo(self.base.getNodo())
            nodo.agregarHijoNodo(expresion)
            nodo.agregarHijoCadena(")")
            return nodo
        elif self.operador == OperadorAritmetico.UPPER:
            nodo = NodoReporteArbol("UPPER")
            nodo.agregarHijoCadena("uppercase")
            nodo.agregarHijoCadena("(")
            expresion = NodoReporteArbol("EXPRESION")
            expresion.agregarHijoNodo(self.base.getNodo())
            nodo.agregarHijoNodo(expresion)
            nodo.agregarHijoCadena(")")
            return nodo
        elif self.operador == OperadorAritmetico.PARSE:
            if self.base == "Float64":
                nodo = NodoReporteArbol("PARSE")
                nodo.agregarHijoCadena("parse")
                nodo.agregarHijoCadena("(")
                nodo.agregarHijoCadena("Float64")
                nodo.agregarHijoCadena(",")
                expresion = NodoReporteArbol("EXPRESION")
                expresion.agregarHijoNodo(self.valor.getNodo())
                nodo.agregarHijoNodo(expresion)
                nodo.agregarHijoCadena(")")
                return nodo
            elif self.base == "Int64":
                nodo = NodoReporteArbol("PARSE")
                nodo.agregarHijoCadena("parse")
                nodo.agregarHijoCadena("(")
                nodo.agregarHijoCadena("Int64")
                nodo.agregarHijoCadena(",")
                expresion = NodoReporteArbol("EXPRESION")
                expresion.agregarHijoNodo(self.valor.getNodo())
                nodo.agregarHijoNodo(expresion)
                nodo.agregarHijoCadena(")")
                return nodo
        elif self.operador == OperadorAritmetico.TRUNC:
            nodo = NodoReporteArbol("TRUNC")
            nodo.agregarHijoCadena("trunc")
            nodo.agregarHijoCadena("(")
            if self.base != None:
                nodo.agregarHijoCadena("Int64")
                nodo.agregarHijoCadena(",")
            expresion = NodoReporteArbol("EXPRESION")
            expresion.agregarHijoNodo(self.valor.getNodo())
            nodo.agregarHijoNodo(expresion)
            nodo.agregarHijoCadena(")")
            return nodo
        elif self.operador == OperadorAritmetico.FLOAT:
            nodo = NodoReporteArbol("FLOAT")
            nodo.agregarHijoCadena("float")
            nodo.agregarHijoCadena("(")
            expresion = NodoReporteArbol("EXPRESION")
            expresion.agregarHijoNodo(self.base.getNodo())
            nodo.agregarHijoNodo(expresion)
            nodo.agregarHijoCadena(")")
            return nodo
        elif self.operador == OperadorAritmetico.STRING:
            nodo = NodoReporteArbol("STRING")
            nodo.agregarHijoCadena("String")
            nodo.agregarHijoCadena("(")
            expresion = NodoReporteArbol("EXPRESION")
            expresion.agregarHijoNodo(self.base.getNodo())
            nodo.agregarHijoNodo(expresion)
            nodo.agregarHijoCadena(")")
            return nodo
        elif self.operador == OperadorAritmetico.TYPEOF:
            nodo = NodoReporteArbol("TYPEOF")
            nodo.agregarHijoCadena("typeof")
            nodo.agregarHijoCadena("(")
            expresion = NodoReporteArbol("EXPRESION")
            expresion.agregarHijoNodo(self.base.getNodo())
            nodo.agregarHijoNodo(expresion)
            nodo.agregarHijoCadena(")")
            return nodo
        elif self.operador == OperadorAritmetico.PUSH:
            if isinstance(self.base, str):
                instruccion = NodoReporteArbol("INSTRUCCION")
                nodo = NodoReporteArbol("PUSH")
                instruccion.agregarHijoNodo(nodo)
                nodo.agregarHijoCadena("push")
                nodo.agregarHijoCadena("!")
                nodo.agregarHijoCadena("(")
                expresion = NodoReporteArbol("IDENTIFICADOR")
                expresion.agregarHijoCadena(self.base)
                nodo.agregarHijoNodo(expresion)
                nodo.agregarHijoCadena(",")
                derecho = NodoReporteArbol("EXPRESION")
                derecho.agregarHijoNodo(self.valor.getNodo())
                nodo.agregarHijoNodo(derecho)
                nodo.agregarHijoCadena(")")
                return instruccion
            else:
                instruccion = NodoReporteArbol("INSTRUCCION")
                nodo = NodoReporteArbol("PUSH")
                instruccion.agregarHijoNodo(nodo)
                nodo.agregarHijoCadena("push")
                nodo.agregarHijoCadena("!")
                nodo.agregarHijoCadena("(")
                expresion = NodoReporteArbol("EXPRESION")
                expresion.agregarHijoNodo(self.base.getNodo())
                nodo.agregarHijoNodo(expresion)
                nodo.agregarHijoCadena(",")
                derecho = NodoReporteArbol("EXPRESION")
                derecho.agregarHijoNodo(self.valor.getNodo())
                nodo.agregarHijoNodo(derecho)
                nodo.agregarHijoCadena(")")
                return instruccion
        elif self.operador == OperadorAritmetico.POP:
            nodo = NodoReporteArbol("POP")
            nodo.agregarHijoCadena("pop")
            nodo.agregarHijoCadena("!")
            nodo.agregarHijoCadena("(")
            expresion = NodoReporteArbol("EXPRESION")
            expresion.agregarHijoCadena(self.base)
            nodo.agregarHijoNodo(expresion)
            nodo.agregarHijoCadena(")")
            return nodo
        elif self.operador == OperadorAritmetico.LENGTH:
            if isinstance(self.base, str):
                nodo = NodoReporteArbol("LENGTH")
                nodo.agregarHijoCadena("length")
                nodo.agregarHijoCadena("(")
                expresion = NodoReporteArbol("IDENTIFICADOR")
                expresion.agregarHijoCadena(self.base)
                nodo.agregarHijoNodo(expresion)
                nodo.agregarHijoCadena(")")
                return nodo
            else:
                nodo = NodoReporteArbol("LENGTH")
                nodo.agregarHijoCadena("length")
                nodo.agregarHijoCadena("(")
                expresion = NodoReporteArbol("EXPRESION")
                expresion.agregarHijoNodo(self.base.getNodo())
                nodo.agregarHijoNodo(expresion)
                nodo.agregarHijoCadena(")")
                return nodo

        
       