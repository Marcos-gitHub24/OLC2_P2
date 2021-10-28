from TS.Entorno import Entorno
from TS.Generador import Generador
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

    def interpretar(self, entorno):
        nuevo_entorno = Entorno(entorno)
        valor_inicio = self.inicio.interpretar(entorno)
        if(valor_inicio.tipo == TIPO.ERROR):
            #tree.addExcepcion(valor_inicio)
            return 
        valor_final = self.final.interpretar(entorno)
        if(valor_final.tipo == TIPO.ERROR):
            #tree.addExcepcion(valor_final)
            return 

        if(valor_inicio.tipo == TIPO.CADENA):
            #tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede realizar un for con una cadena",self.fila,self.columna))
            return  Excepcion(TIPO.ERROR, f"No puede realizar un for con una cadena",self.fila,self.columna)
        if(valor_inicio.tipo == TIPO.CHARACTER):
            #tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede realizar un for con un caracter",self.fila,self.columna))
            return  Excepcion(TIPO.ERROR, f"No puede realizar un for con un caracter",self.fila,self.columna)
        if(valor_final.tipo == TIPO.CADENA):
            #tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede realizar un for con una cadena",self.fila,self.columna))
            return  Excepcion(TIPO.ERROR, f"No puede realizar un for con una cadena",self.fila,self.columna)
        if(valor_final.tipo == TIPO.CHARACTER):
            #tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede realizar un for con una cadena",self.fila,self.columna))
            return  Excepcion(TIPO.ERROR, f"No puede realizar un for con un caracter",self.fila,self.columna)

        asignar = Asignacion(self.id, self.inicio, None, self.fila, self.columna)
        asignar.interpretar(nuevo_entorno)
        
        aux = Generador()
        generador = aux.obtenerGen()
        generador.addComment('EMPIEZA EL FOR EN RANGO')
        temp_final = generador.agregarTemporal()
        generador.agregarExpresion(temp_final,valor_final.valor,'','')
        
        lbl_for = generador.agregarLabel()
        generador.colocarLbl(lbl_for)

        guardar = Identificador(self.id, self.fila, self.columna)
        guardar_interpretar = guardar.interpretar(nuevo_entorno)
        temp_inicio = guardar_interpretar.valor

        lbl_instrucciones = generador.agregarLabel()
        lbl_salida = generador.agregarLabel()
        lbl_incremento = generador.agregarLabel()

        generador.agregarIf(temp_inicio,temp_final,'<=',lbl_instrucciones)
        generador.agregarGoto(lbl_salida)
        
        nuevo_entorno.lbl_break = lbl_salida
        nuevo_entorno.lbl_continue = lbl_incremento

        generador.colocarLbl(lbl_instrucciones)

        for i in self.instrucciones:
            i.interpretar(nuevo_entorno)
        
        generador.agregarGoto(lbl_incremento)
        generador.colocarLbl(lbl_incremento)
        generador.agregarExpresion(temp_inicio,temp_inicio,'1','+')
        variable = nuevo_entorno.obtenerVariable(self.id)
        
        tmp = generador.agregarTemporal()
        generador.agregarExpresion(tmp,'P',variable.pos,'+')
        generador.guardar_stack(tmp,temp_inicio)

        generador.agregarGoto(lbl_for)
        generador.colocarLbl(lbl_salida)

        


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