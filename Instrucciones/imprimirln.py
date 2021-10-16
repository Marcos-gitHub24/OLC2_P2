from Expresiones.Struct import Struct
from Abstract.Objeto import TipoObjeto
from Abstract.NodoReporteArbol import NodoReporteArbol
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO

class Imprimirln(NodoAST):
    def __init__(self, expresion, fila, columna):
        super().__init__(TipoObjeto.CADENA, fila, columna)
        self.expresion = expresion
        self.cadena = ""
        """self.expresion = expresion
        self.fila = fila
        self.columna = columna"""

    def interpretar(self, tree, table):
        self.cadena = ""
        for i in self.expresion:
            value = i.interpretar(tree, table)
            if isinstance(value, Excepcion) :
                    return value
            elif isinstance(value, Struct):
                self.cadena += str(obtenerStruct(value))
                
            elif  isinstance(value.valor, list):
                self.cadena += str(obtenerVector(tree, table, value.valor))
            else:
                if value.valor == None:
                    self.cadena += 'nothing'    
                else:
                    self.cadena += str(value.valor)
        tree.updateConsolaln(self.cadena) #TODO: Actualizar singleton en su campo consola
        return None

    def getNodo(self):
        nodo = NodoReporteArbol("IMPRIMIRLN")
        nuevo = NodoReporteArbol("EXPRESIONES")
        unaVez = True
        for i in self.expresion:
            if unaVez:
                nuevo1 = NodoReporteArbol("EXPRESION")
                nuevo1.agregarHijoNodo(i.getNodo())
                nuevo.agregarHijoNodo(nuevo1)
            else:
                n = nuevo
                nuevo1 = NodoReporteArbol("EXPRESION")
                nuevo = NodoReporteArbol("EXPRESIONES")
                nuevo.agregarHijoNodo(n)
                nuevo.agregarHijoCadena(",")
                nuevo1.agregarHijoNodo(i.getNodo())
                nuevo.agregarHijoNodo(nuevo1)
            unaVez = False
        nodo.agregarHijoCadena("println")
        nodo.agregarHijoCadena("(")
        nodo.agregarHijoNodo(nuevo)
        nodo.agregarHijoCadena(")")
        nodo.agregarHijoCadena(";")
        return nodo

def obtenerVector(tree, table, vector):
        lista = []
        for i in vector:
            valor = i.interpretar(tree, table)
            if isinstance(valor.valor, list):
               lista.append(obtenerVector(tree, table, valor.valor))
            else:
                lista.append(valor.valor)
        
        return lista

def obtenerStruct(struct):
    cadena = struct.nombre + "( "
    for clave in struct.diccionario:
        if isinstance(struct.diccionario[clave], Struct) == False:
            if struct.diccionario[clave].valor == None:
                cadena += 'nothing, '
            else:
                cadena += str(struct.diccionario[clave].valor) + ", "
        else:
            cadena += obtenerStruct(struct.diccionario[clave]) + ", "
    cadena = cadena[0:-2]
    cadena += ")"
    return cadena