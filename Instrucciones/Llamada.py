
from Instrucciones.AsignacionStruct import AsignacionStruct
from Instrucciones.Return import Return
from Abstract.NodoReporteArbol import NodoReporteArbol
from TS.Simbolo import Simbolo
from Instrucciones.Funcion import Funcion
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break
from Expresiones.Struct import Struct


class Llamada(NodoAST):
    def __init__(self, nombre, parametros, fila, columna):
        self.nombre = nombre
        self.parametros = parametros
        self.fila = fila
        self.columna = columna
    
    def interpretar(self, tree, table):
        met = table.getTabla(self.nombre)
        if met != None:
            if isinstance(met.getValor(), Struct) == False:
                tabla_nueva = TablaSimbolos(table)
                tabla_nueva.setEntorno("Funcion")
                tree.agregarTabla(tabla_nueva)
                if self.parametros == None:
                    inst = met.getValor()
                    instrucciones  = inst.getInstrucciones()
                    for i in instrucciones:
                        if isinstance(i, Excepcion):
                            tree.updateConsola(i.toString())
                            tree.addExcepcion(i)
                            continue
                        resultado = i.interpretar(tree, tabla_nueva)
                        if isinstance(resultado, Excepcion):
                            tree.updateConsola(resultado.toString())
                            tree.addExcepcion(resultado)
                            continue
                        if isinstance(resultado,Return):
                            return resultado
                else:
                    inst = met.getValor()
                    instrucciones  = inst.getInstrucciones()
                    parametros = inst.getParametros()
                    if len(parametros) == len(self.parametros):
                        index = 0
                        for i in inst.getParametros():
                            result = self.parametros[index].interpretar(tree, table)
                            simbolo = Simbolo(str(i),self.fila, self.columna, result)
                            tabla_nueva.setTabla(simbolo)
                            index += 1

                        for m in instrucciones:
                            if isinstance(m, Excepcion):
                                tree.updateConsola(m.toString())
                                tree.addExcepcion(m)
                                continue
                            if isinstance(m, Return):
                                if m.expresion != None:
                                    devolver = m.expresion.interpretar(tree, tabla_nueva)
                                    return devolver
                                else:
                                    return None
                            resultado = m.interpretar(tree, tabla_nueva)
                            if isinstance(resultado, Return):
                                if resultado.expresion != None:
                                    devolver = resultado.expresion.interpretar(tree, tabla_nueva)
                                    return devolver
                                else:
                                    return None
            else:
                struct = AsignacionStruct(None, self.nombre, self.parametros, self.fila, self.columna)
                return struct.interpretar(tree, table)
        else:
            return Excepcion("Semantico", f"Error al llamar a {self.nombre}", self.fila, self.columna)

                    
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