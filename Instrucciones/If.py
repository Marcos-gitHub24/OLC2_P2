import re
from Instrucciones.Continue import Continue
from Abstract.Objeto import TipoObjeto
from Abstract.NodoReporteArbol import NodoReporteArbol
from Instrucciones.Return import Return
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.Generador import Generador
from TS.Tipo import TIPO
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break


class If(NodoAST):
    def __init__(self, condicion, instruccionesIf, instruccionesElse, fila, columna):
        super().__init__(TIPO.BOOLEANO, fila, columna)
        self.condicion = condicion
        self.instruccionesIf = instruccionesIf
        self.instruccionesElse = instruccionesElse
        self.salir = None
        self.lbl_salida = None

    def interpretar(self,entorno):
        condicion = self.condicion.interpretar(entorno)
        if isinstance(condicion, Excepcion):
            return condicion
        if condicion.tipo == TIPO.BOOLEANO:
            bandera = True
            aux = Generador()
            generador = aux.obtenerGen()
            generador.colocarLbl(condicion.truelbl)
            if self.salir == None:
                self.salir = generador.agregarLabel()
            if self.lbl_salida == None:
                self.lbl_salida = True
            for i in self.instruccionesIf:
                i.interpretar(entorno)
            generador.agregarGoto(self.salir)
            print('--if--')
            print(self.salir)

            if isinstance(self.instruccionesElse, If):
                self.instruccionesElse.salir = self.salir
                self.instruccionesElse.lbl_salida = self.lbl_salida
                generador.colocarLbl(condicion.falselbl)
                self.instruccionesElse.interpretar(entorno)
                bandera = False
                return
            
            if bandera:
                #if self.instruccionesElse != None:
                    #salir = generador.agregarLabel()
                    #generador.agregarGoto(self.salir)
                generador.colocarLbl(condicion.falselbl)

                if self.instruccionesElse != None:
                    for i in self.instruccionesElse:
                        i.interpretar(entorno)
            
            generador.colocarLbl(self.salir)
            
          
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
