from Abstract.NodoReporteArbol import NodoReporteArbol
from Instrucciones.Metodo import Metodo
from Expresiones.Struct import Struct
from TS.Tipo import TIPO


class Arbol:
    def __init__(self, instrucciones ):
        self.instrucciones = instrucciones
        self.funciones = []
        self.excepciones = []
        self.consola = ""
        self.TSglobal = None
        self.dot = ""
        self.tabla = ""
        self.grafoError = ""
        self.tablas = []
        self.contador = 0
        self.c = 0

    def getInstrucciones(self):
        return self.instrucciones

    def setInstrucciones(self, instrucciones):
        self.instrucciones = instrucciones

    def getExcepciones(self):
        return self.excepciones

    def setExcepciones(self, excepciones):
        self.excepciones = excepciones
    
    def addExcepcion(self, excepcion):
        self.excepciones.append(excepcion)

    def getExcepciones(self):
        return self.excepciones

    def getConsola(self):
        return self.consola
    
    def setConsola(self, consola):
        self.consola = consola

    def updateConsola(self,cadena):
        self.consola += str(cadena)
    
    def updateConsolaln(self,cadena):
        self.consola += str(cadena) + '\n'

    def getTSGlobal(self):
        return self.TSglobal
    
    def setTSglobal(self, TSglobal):
        self.TSglobal = TSglobal

    def getFunciones(self):
        return self.funciones

    def getFuncion(self, nombre):
        for funcion in self.funciones:
            if funcion.nombre == nombre:
                return funcion
        return None
    
    def addFuncion(self, funcion):
        self.funciones.append(funcion)

    def agregarTabla(self, tabla):
        self.tablas.append(tabla)
    def getTablas(self):
        return self.tablas

    def empiezoArbol(self):
        raiz = NodoReporteArbol("RAIZ")
        unavez = True
        instrucciones = NodoReporteArbol("INSTRUCCIONES")
        for i in self.getInstrucciones():
            if unavez:
                instr = NodoReporteArbol("INSTRUCCION")
                instr.agregarHijoNodo(i.getNodo())
                instrucciones.agregarHijoNodo(instr)
            else:
                tmp = instrucciones
                instr = NodoReporteArbol("INSTRUCCION")
                instrucciones = NodoReporteArbol("INSTRUCCIONES")
                instrucciones.agregarHijoNodo(tmp)
                instr.agregarHijoNodo(i.getNodo())
                instrucciones.agregarHijoNodo(instr)
            unavez = False
        raiz.agregarHijoNodo(instrucciones)
        cadena = self.getDot(raiz)
        return cadena

    def getDot(self, raiz): ## DEVUELVE EL STRING DE LA GRAFICA EN GRAPHVIZ
        self.dot = ""
        self.dot += "digraph {\n"
        self.dot += "n0[label=\"" + raiz.getValor().replace("\"", "\\\"") + "\"];\n"
        self.contador = 1
        self.recorrerAST("n0", raiz)
        self.dot += "}"
        return self.dot
     
    def recorrerAST(self, idPadre, nodoPadre):
        for hijo in nodoPadre.getHijos():
            nombreHijo = "n" + str(self.contador)
            self.dot += nombreHijo + "[label=\"" + hijo.getValor().replace("\"", "\\\"") + "\"];\n"
            self.dot += idPadre + "->" + nombreHijo + ";\n"
            self.contador += 1
            self.recorrerAST(nombreHijo, hijo)

    def crearTabla(self, arbol):
        self.tabla = ""
        self.tabla += "digraph G \n {\n Nodo[shape=none,margin=0, style=rounded, fontsize=10, label=<\n"
        self.tabla += "<TABLE border=\"1\"  CELLSPACING=\"0\" CELLPADDING=\"4\">"
        self.tabla += "<TR><TD>Tipo</TD><TD>Identificador</TD><TD>Entorno</TD><TD>Fila</TD><TD>Columna</TD></TR>\n"
        self.c = 1
        self.recorrerTablas(arbol)
        self.tabla += "</TABLE>>];\n}"
        return self.tabla

    def recorrerTablas(self, arbol):
        listaTablas = []
        tipo = ""
        for i in arbol.getTablas():
            for llave, valor in i.tabla.items():
                if isinstance(valor.valor, Struct):
                    tipo = "Struct"
                elif isinstance(valor.valor, Metodo):
                    tipo = "Function"
                elif valor.valor.tipo == TIPO.ENTERO:
                    tipo = "Int64"
                elif valor.valor.tipo == TIPO.DECIMAL:
                    tipo = "Float64"
                elif valor.valor.tipo == TIPO.CADENA:
                    tipo = "String"
                elif valor.valor.tipo == TIPO.CHARACTER:
                    tipo = "Char"
                elif valor.valor.tipo == TIPO.BOOLEANO:
                    tipo = "Boolean"
                elif valor.valor.tipo == TIPO.FUNCION:
                    tipo = "Function"
                elif valor.valor.tipo == TIPO.STRUCT:
                    tipo = "Struct"
                elif valor.valor.tipo == TIPO.ARREGLO:
                    tipo = "Arreglo"
                if i.entorno == "":
                    listaTablas.append("<TR><TD>"+tipo+"</TD><TD>"+llave+"</TD><TD>"+"Global"+"</TD><TD>"+str(valor.fila)+"</TD><TD>"+str(valor.columna)+"</TD></TR>\n")
                else:
                    listaTablas.append("<TR><TD>"+tipo+"</TD><TD>"+llave+"</TD><TD>"+i.entorno+"</TD><TD>"+str(valor.fila)+"</TD><TD>"+str(valor.columna)+"</TD></TR>\n")
        nueva = set(listaTablas)
        for i in nueva:
            self.tabla += str(i)   
    
    def tablaError(self, arbol):
        self.grafoError = ""
        self.grafoError += "digraph G \n {\n Nodo[shape=none,margin=0, style=rounded, fontsize=10, label=<\n"
        self.grafoError += "<TABLE border=\"1\"  CELLSPACING=\"0\" CELLPADDING=\"4\">"
        self.grafoError += "<TR><TD>No</TD><TD>Descripcion</TD><TD>Fecha y Hora</TD><TD>Fila</TD><TD>Columna</TD></TR>\n"
        self.c = 1
        self.recorrerErrores(arbol)
        self.grafoError += "</TABLE>>];\n}"
        return self.grafoError

    def recorrerErrores(self, arbol):
        contador = 1
        for i in arbol.getExcepciones():
            self.grafoError += "<TR><TD>"+str(contador)+"</TD><TD>"+i.descripcion+"</TD><TD>"+str(i.fecha)+"</TD><TD>"+str(i.fila)+"</TD><TD>"+str(i.columna)+"</TD></TR>\n"
            contador += 1



                



