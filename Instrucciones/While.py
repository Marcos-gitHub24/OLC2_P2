from Instrucciones.Continue import Continue
from Abstract.Objeto import TipoObjeto
from Abstract.NodoReporteArbol import NodoReporteArbol
from Instrucciones.If import If
from Instrucciones.Return import Return
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.Generador import Generador
from TS.Tipo import TIPO
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break
from TS.Entorno import Entorno

class While(NodoAST):
    def __init__(self, condicion, instrucciones, fila, columna):
        super().__init__(TIPO.BOOLEANO, fila, columna)
        self.condicion = condicion
        self.instrucciones = instrucciones

    def interpretar(self, entorno):
        aux = Generador()
        generador = aux.obtenerGen()
        lbl_while = generador.agregarLabel()
        generador.colocarLbl(lbl_while)
        condicion = self.condicion.interpretar(entorno)
        nuevo_entorno = Entorno(entorno)

        nuevo_entorno.lbl_break = condicion.falselbl
        nuevo_entorno.lbl_continue = lbl_while
        
        generador.colocarLbl(condicion.truelbl)
        for i in self.instrucciones:
            i.interpretar(nuevo_entorno)
        generador.agregarGoto(lbl_while)
        print('---lblwhile----')
        print(condicion.falselbl)
        generador.colocarLbl(condicion.falselbl)
       

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