from re import A
from Abstract.Return import Return
from Expresiones.Struct import Struct
from Instrucciones.Asignacion import Asignacion
from Expresiones.Identificador import Identificador
from Objeto.Primitivo import Primitivo
from Abstract.Objeto import TipoObjeto
from Abstract.NodoReporteArbol import NodoReporteArbol
from TS.Excepcion import Excepcion
from Abstract.NodoAST import NodoAST
from TS.Generador import Generador
from TS.Simbolo import Simbolo
from TS.Tipo import TIPO



class AsignacionStruct(NodoAST):
    def __init__(self, struct, atributos, fila, columna):
        #self.identificador = identificador
        self.atributos = atributos
        self.struct = struct
        self.fila = fila
        self.columna = columna

    def interpretar(self, entorno):
        aux =  Generador()
        generador = aux.obtenerGen()
        estructura = entorno.obtenerStruct(self.struct)
        
        if estructura != None:
            atrs = []
            for i in self.atributos:
                atrs.append(i.interpretar(entorno))
            contador = 0
            
            guardar_heap = generador.agregarTemporal()
            generador.agregarExpresion(guardar_heap,'H','','')
            retorno = Return(guardar_heap, TIPO.STRUCT, True)
            tipo = ''
            for i in estructura:
                tipo = estructura[i][0]
                if isinstance(tipo,list):
                    if tipo[0] != TIPO.STRUCT:
                        tipo = TIPO.ARREGLO
                        retorno.arreglo = atrs[contador].arreglo
                    else:
                        tipo = TIPO.STRUCT
                        retorno.struct = atrs[contador].struct
                if atrs[contador].tipo == tipo:        
                    generador.guardar_heap('H',atrs[contador].valor)
                    generador.agregarExpresion('H','H','1','+')
                else:
                    if atrs[contador].tipo == TIPO.NULO:
                        generador.guardar_heap('H',atrs[contador].valor)
                        generador.agregarExpresion('H','H','1','+')
                    else:
                        # aca erro de tipos
                        generador.TSglobal.addExcepcion(Excepcion(TIPO.ERROR, f"No coincide el tipo",self.fila,self.columna))
                        return  Excepcion(TIPO.ERROR, f"Semantico, No coincide el tipo",self.fila,self.columna)
                    
                contador +=1
            retorno.struct = estructura
            return retorno
        else:
            generador.TSglobal.addExcepcion(Excepcion("Semantico", "Numero de parametros no coincide", self.fila, self.columna))
            return Excepcion("Semantico", "Numero de parametros no coincide", self.fila, self.columna)
            

    def getNodo(self):
        nodo = NodoReporteArbol("ASIGNACION_STRUCT")
        nodo.agregarHijo(str(self.identificador))
        nodo.agregarHijoNodo(self.expresion.getNodo())
        return nodo