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

class While(NodoAST):
    def __init__(self, condicion, instrucciones, fila, columna):
        super().__init__(TIPO.BOOLEANO, fila, columna)
        self.condicion = condicion
        self.instrucciones = instrucciones

    def interpretar(self, tree, table):
        while True:
            condicion = self.condicion.interpretar(tree, table)
            if isinstance(condicion, Excepcion): 
                tree.addExcepcion(condicion)
                return condicion
            if condicion.tipo == TIPO.BOOLEANO:
                if bool(condicion.valor) == True:   # VERIFICA SI ES VERDADERA LA CONDICION
                    nuevaTabla = TablaSimbolos(table)       #NUEVO ENTORNO
                    nuevaTabla.setEntorno("While")
                    tree.agregarTabla(nuevaTabla)
                    if isinstance(self.instrucciones, Break): 
                            return None
                    for instruccion in self.instrucciones:
                        result = instruccion.interpretar(tree, nuevaTabla) #EJECUTA INSTRUCCION ADENTRO DEL IF
                        if isinstance(result, Excepcion) :
                            tree.getExcepciones().append(result)
                            tree.updateConsola(result.toString())
                            tree.addExcepcion(result)
                            continue
                        if isinstance(result, Break): 
                            return result
                        if isinstance(result, Return): return result
                        if isinstance(result, Continue):break

                else:
                    break
            else:
                tree.addExcepcion(Excepcion("Semantico", "Tipo de dato no booleano en la condicion.", self.fila, self.columna))
                return Excepcion("Semantico", "Tipo de dato no booleano en la condicion.", self.fila, self.columna)

    def getNodo(self):
        nodo = NodoReporteArbol("WHILE")
        nodo.agregarHijoCadena("while")
        nodo.agregarHijoNodo(self.condicion.getNodo())
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