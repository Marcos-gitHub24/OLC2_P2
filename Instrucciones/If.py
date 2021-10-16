import re
from Instrucciones.Continue import Continue
from Abstract.Objeto import TipoObjeto
from Abstract.NodoReporteArbol import NodoReporteArbol
from Instrucciones.Return import Return
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break


class If(NodoAST):
    def __init__(self, condicion, instruccionesIf, instruccionesElse, fila, columna):
        super().__init__(TIPO.BOOLEANO, fila, columna)
        self.condicion = condicion
        self.instruccionesIf = instruccionesIf
        self.instruccionesElse = instruccionesElse

    def interpretar(self, tree, table):
        condicion = self.condicion.interpretar(tree, table)
        if isinstance(condicion, Excepcion):
            return condicion
        if condicion.tipo == TIPO.BOOLEANO:
            # Si la condicion del if es verdadera
            
            if bool(condicion.valor) == True and self.instruccionesIf != None:
                nuevo = TablaSimbolos(table)
                nuevo.setEntorno("If")
                tree.agregarTabla(nuevo)
                for i in self.instruccionesIf:
                    if isinstance(i, Excepcion):
                        tree.updateConsola(i.toString())
                        tree.addExcepcion(i)
                        continue
                    if isinstance(i, Return):
                        return i
                    result = i.interpretar(tree, nuevo)
                    if isinstance(result, Excepcion):
                        tree.getExcepciones().append(result)
                        tree.updateConsola(result.toString())
                        tree.addExcepcion(result)
                        continue
                    if isinstance(result, Break):
                        condicion = False
                        return result
                    if isinstance(result, Continue):
                        return result
                    if isinstance(result, Return):
                        return result

            elif bool(condicion.valor) == False:
                if self.instruccionesElse != None:
                    nuevaTabla = TablaSimbolos(table)
                    nuevaTabla.setEntorno("If")
                    tree.agregarTabla(nuevaTabla)
                    if isinstance(self.instruccionesElse, If):
                        result = self.instruccionesElse.interpretar(tree, nuevaTabla)
                        if isinstance(result, Excepcion):
                            tree.getExcepciones().append(result)
                            tree.updateConsola(result.toString())
                            tree.addExcepcion(result)

                        if isinstance(result, Break):
                            condicion = False
                            return result
                        if isinstance(result, Continue):
                            return result
                        if isinstance(result, Return):
                            return result
                    else:
                        for i in self.instruccionesElse:
                            if isinstance(i, Return):
                                return i
                            if isinstance(i, Excepcion):
                                tree.updateConsola(i.toString())
                                tree.addExcepcion(i)
                                continue
                            result = i.interpretar(tree, nuevaTabla)
                            if isinstance(result, Excepcion):
                                tree.getExcepciones().append(result)
                                tree.updateConsola(result.toString())
                                tree.addExcepcion(result)
                                continue
                            if isinstance(result, Break):
                                condicion = False
                                return result
                            if isinstance(result, Continue):
                                return None
                            if isinstance(result, Return):
                                return result

        else:
            return Excepcion("Semantico", "Tipo de dato no booleano en IF.", self.fila, self.columna)

    def getNodo(self):
        nodo = NodoReporteArbol("IF")
        nodo.agregarHijoCadena("if")
        nodo.agregarHijoNodo(self.condicion.getNodo())
        instruccionesif = NodoReporteArbol("INSTRUCCIONES")
        unaVez = True
        for instr in self.instruccionesIf:
            if unaVez:
                nuevo1 = NodoReporteArbol("INSTRUCCION")
                nuevo1.agregarHijoNodo(instr.getNodo())
                #nuevo1.agregarHijoCadena(";")
                instruccionesif.agregarHijoNodo(nuevo1)
            else:
                n = instruccionesif
                nuevo1 = NodoReporteArbol("INSTRUCCION")
                instruccionesif = NodoReporteArbol("INSTRUCCIONES")
                instruccionesif.agregarHijoNodo(n)
                nuevo1.agregarHijoNodo(instr.getNodo())
                #nuevo1.agregarHijoCadena(";")
                instruccionesif.agregarHijoNodo(nuevo1)
            unaVez = False
        nodo.agregarHijoNodo(instruccionesif)
        if self.instruccionesElse != None:
            if isinstance(self.instruccionesElse, If):
               nodo.agregarHijoNodo(self.instruccionesElse.getNodo())
            else:
                nodo2 = NodoReporteArbol("ELSE")
                nodo2.agregarHijoCadena("else")
                instruccioneselse = NodoReporteArbol("INSTRUCCIONES")
                unaVez1 = True
                for instr in self.instruccionesElse:
                    if unaVez1:
                        nuevo1 = NodoReporteArbol("INSTRUCCION")
                        nuevo1.agregarHijoNodo(instr.getNodo())
                        #nuevo1.agregarHijoCadena(";")
                        instruccioneselse.agregarHijoNodo(nuevo1)
                    else:
                        n = instruccioneselse
                        nuevo1 = NodoReporteArbol("INSTRUCCION")
                        instruccioneselse = NodoReporteArbol("INSTRUCCIONES")
                        instruccioneselse.agregarHijoNodo(n)
                        nuevo1.agregarHijoNodo(instr.getNodo())
                        #nuevo1.agregarHijoCadena(";")
                        instruccioneselse.agregarHijoNodo(nuevo1)
                    unaVez1 = False
                nodo2.agregarHijoNodo(instruccioneselse)
                nodo.agregarHijoNodo(nodo2)
        nodo.agregarHijoCadena("end")
        nodo.agregarHijoCadena(";")
        return nodo
