from Abstract.Objeto import TipoObjeto
from Abstract.NodoReporteArbol import NodoReporteArbol
from TS.Tipo import TIPO
from Instrucciones.Return import Return
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break
from TS.Simbolo import Simbolo
from TS.Entorno import Entorno
from TS.Generador import Generador

class Funcion(NodoAST):
    def __init__(self, nombre, metodo, fila, columna):
        super().__init__(TIPO.ENTERO, fila, columna)
        self.nombre = nombre
        self.metodo = metodo
        self.fila = fila
        self.columna = columna
    
    def interpretar(self, entorno):
        if isinstance(self.metodo.tipo,list):
            print('+++++FIJATE QUE SU TIPO ES UNA LISTA++++++++++++++')
            print(self.metodo.tipo)
            self.metodo.arreglo_tipo = self.metodo.tipo
            self.tipo = TIPO.ARREGLO
        else:
            self.tipo = self.metodo.tipo
        entorno.guardarFuncion(self.nombre, self)
        aux = Generador()
        generador = aux.obtenerGen()
        print('******************metodoTipo*********************')
        print(self.tipo)
        print('*************************************************')
        nuevo_entorno = Entorno(entorno)
        nuevo_entorno.dentro = '1'
        lbl_return = generador.agregarLabel()
        nuevo_entorno.lbl_return = lbl_return
        nuevo_entorno.size = 1
        
        tipo = TIPO.ENTERO
        for i in self.metodo.getParametros():
            arreglo = None
            if isinstance(i.tipo,list):
                print("[[[[[[[[[[[[[[[[[[[[[[[ARREGLO]]]]]]]]]]]]]]]]]]]]]]]")
                print(i.tipo)
                tipo = TIPO.ARREGLO
                arreglo = i.tipo  #aca esta el arreglo de tipo
            else:
                tipo = i.tipo
            nuevo_entorno.guardarVariable(i.nombre,tipo, (tipo == TIPO.CADENA or tipo == TIPO.STRUCT or tipo == TIPO.ARREGLO), tipo == TIPO.STRUCT, arreglo)
        
        generador.addBeginFunc(self.nombre)

        
        for i in self.metodo.getInstrucciones():
            i.interpretar(nuevo_entorno)
       
            #print('ERROR')
        #generador.agregarGoto(lbl_return)
        generador.colocarLbl(lbl_return)
        generador.addEndFunc()

            #tree.addExcepcion(Excepcion("Semantico", "Ya existe una función con ese nombre", self.fila, self.columna))
            #return Excepcion("Semantico", "Ya existe una función con ese nombre", self.fila, self.columna)

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