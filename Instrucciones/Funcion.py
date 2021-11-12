from enum import EnumMeta
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
        if self.metodo.tipo != None:
            bandera = True
            if isinstance(self.metodo.tipo,list):
                if self.metodo.tipo[0] != TIPO.STRUCT:
                    print(self.metodo.tipo)
                    self.metodo.arreglo_tipo = self.metodo.tipo
                    self.tipo = TIPO.ARREGLO
                else:
                    self.tipo = TIPO.STRUCT
                    self.metodo.struct = entorno.obtenerStruct(self.metodo.tipo[1])
                    bandera = False

            else:
                if bandera:
                    self.tipo = self.metodo.tipo
            entorno.guardarFuncion(self.nombre, self)
            aux = Generador()
            generador = aux.obtenerGen()
            nuevo_entorno = Entorno(entorno)
            nuevo_entorno.setEntorno(self.nombre)
            generador.TSglobal.agregarTabla(nuevo_entorno)
            nuevo_entorno.dentro = '1'
            lbl_return = generador.agregarLabel()
            nuevo_entorno.lbl_return = lbl_return
            nuevo_entorno.size = 1
            
            tipo = TIPO.ENTERO
            if self.metodo.getParametros() != None:
                for i in self.metodo.getParametros():
                    arreglo = None
                    bandera = True
                    nombre_struct = ''
                    if isinstance(i.tipo,list):
                        if i.tipo[0] != TIPO.STRUCT:
                            tipo = TIPO.ARREGLO
                            arreglo = i.tipo  #aca esta el arreglo de tipo
                            
                        else:
                            tipo = i.tipo[0]
                            nombre_struct = i.tipo[1]
                            bandera = False
                    else:
                        if bandera:
                            tipo = i.tipo
                    struct = nuevo_entorno.obtenerStruct(nombre_struct)
                    nuevo_entorno.guardarVariable(i.nombre,tipo, (tipo == TIPO.CADENA or tipo == TIPO.STRUCT or tipo == TIPO.ARREGLO), struct, arreglo, self.fila, self.columna)
                
            generador.addBeginFunc(self.nombre)

            
            for i in self.metodo.getInstrucciones():
                i.interpretar(nuevo_entorno)
        
                #print('ERROR')
            generador.agregarGoto(lbl_return)
            generador.colocarLbl(lbl_return)
            generador.addEndFunc()

                #tree.addExcepcion(Excepcion("Semantico", "Ya existe una función con ese nombre", self.fila, self.columna))
                #return Excepcion("Semantico", "Ya existe una función con ese nombre", self.fila, self.columna)
        else:
            entorno.guardarFuncion(self.nombre, self)
            aux = Generador()
            generador = aux.obtenerGen()
            nuevo_entorno = Entorno(entorno)
            nuevo_entorno.setEntorno(self.nombre)
            generador.TSglobal.agregarTabla(nuevo_entorno)
            nuevo_entorno.dentro = '1'
            nuevo_entorno.size = 1
            if self.metodo.getParametros() != None:
                tipo = TIPO.ENTERO
                
                for i in self.metodo.getParametros():
                    arreglo = None
                    bandera = True
                    nombre_struct = ''
                    if isinstance(i.tipo,list):
                        if i.tipo[0] != TIPO.STRUCT:
                            tipo = TIPO.ARREGLO
                            arreglo = i.tipo  #aca esta el arreglo de tipo
                        else:
                            tipo = i.tipo[0]
                            nombre_struct = i.tipo[1]
                            bandera = False
                    else:
                        if bandera:
                            tipo = i.tipo
                    struct = nuevo_entorno.obtenerStruct(nombre_struct)
                    nuevo_entorno.guardarVariable(i.nombre,tipo, (tipo == TIPO.CADENA or tipo == TIPO.STRUCT or tipo == TIPO.ARREGLO), struct, arreglo, self.fila, self.columna)
                
            generador.addBeginFunc(self.nombre)

            
            for i in self.metodo.getInstrucciones():
                i.interpretar(nuevo_entorno)
        
                #print('ERROR')
            #generador.agregarGoto(nuevo_entorno.lbl_return)
            generador.addEndFunc()

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