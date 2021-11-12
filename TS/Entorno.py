from TS.Symbol import *
from TS.Tipo import TIPO
from Instrucciones.Metodo import Metodo
class Entorno:
    
    def __init__(self, prev):
        self.prev = prev

        self.variables = {}
        self.funciones = {}
        self.structs = {}
        self.excepciones = []
        self.tablas = []
        self.lbl_break = ''
        self.lbl_return = ''
        self.lbl_continue = ''
        self.lbl_return = ''
        self.dentro = None
        self.size = 0

        self.dot = ""
        self.tabla = ""
        self.grafoError = ""
        self.contador = 0
        self.c = 0
        self.entorno = ""
        
        if(prev != None):
            self.size = self.prev.size
            self.lbl_return = self.prev.lbl_return
            self.lbl_break = self.prev.lbl_break
            self.lbl_continue = self.prev.lbl_continue
        

    def setExcepciones(self, excepciones):
        self.excepciones = excepciones
    
    def addExcepcion(self, excepcion):
        self.excepciones.append(excepcion)

    def getExcepciones(self):
        return self.excepciones

    def guardarVariable(self, identificacion, tipo, inHeap, struct, arreglo, fila, columna):
        if identificacion in self.variables.keys():
            # agregar un error 
            return None
        else:
            simbolo = Symbol(identificacion, tipo, self.size, self.prev == None, inHeap, struct, arreglo, fila, columna)
            self.size += 1
            self.variables[identificacion] = simbolo
        return self.variables[identificacion]

    def guardarFuncion(self, identificacion, funcion):
        if identificacion in self.funciones.keys():
            # agregar un error de que no existe la funcion
            return None
        else:
            self.funciones[identificacion] = funcion
    
    def guardarStruct(self, identificacion, atributo):
        if identificacion in self.structs.keys():
            # agregar un error de que no existe la estructura
            return None
        else:
            self.structs[identificacion] = atributo

    def obtenerVariable(self, identificacion):
        entorno = self
        while entorno != None:
            if identificacion in entorno.variables.keys():
                return entorno.variables[identificacion]
            entorno = entorno.prev
        return None
    
    def obtenerFuncion(self, identificacion):
        entorno = self
        while entorno != None:
            if identificacion in entorno.funciones.keys():
                return entorno.funciones[identificacion]
            entorno = entorno.prev
        return None
        
    def obtenerStruct(self, identificacion):
        entorno = self
        while entorno != None:
            if identificacion in entorno.structs.keys():
                return entorno.structs[identificacion]
            entorno = entorno.prev
        return None

    def obtenerGlobal(self):
        entorno = self
        while entorno.prev != None:
            entorno = entorno.prev
        return entorno


    def setEntorno(self, nombre):
        self.entorno = nombre

    def agregarTabla(self, tabla):
        self.tablas.append(tabla)

    def getTablas(self):
        return self.tablas

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
        self.tabla += "<TR><TD>Tipo</TD><TD>Identificador</TD><TD>Entorno</TD><TD>Stack</TD><TD>Heap</TD><TD>Fila</TD><TD>Columna</TD></TR>\n"
        self.c = 1
        self.recorrerTablas(arbol)
        self.tabla += "</TABLE>>];\n}"
        return self.tabla

    def recorrerTablas(self, arbol):
        print("aca empiezo a hacer la tabla")
        print(arbol.getTablas())
        listaTablas = []
        tipo = ""
        for i in arbol.getTablas():
            print(i.variables)
            for llave, valor in i.variables.items():
                heap = 'No'
                posicion = valor.pos
                print(valor.tipo)
                if valor.tipo == TIPO.STRUCT:
                    tipo = "Struct"
                elif valor.tipo == TIPO.ENTERO:
                    tipo = "Int64"
                elif valor.tipo == TIPO.DECIMAL:
                    tipo = "Float64"
                elif valor.tipo == TIPO.CADENA:
                    tipo = "String"
                elif valor.tipo == TIPO.CHARACTER:
                    tipo = "Char"
                elif valor.tipo == TIPO.BOOLEANO:
                    tipo = "Boolean"
                elif valor.tipo == TIPO.FUNCION:
                    tipo = "Function"
                elif valor.tipo == TIPO.STRUCT:
                    tipo = "Struct"
                elif valor.tipo == TIPO.ARREGLO:
                    tipo = "Arreglo"
                if valor.inHeap:
                    heap = 'Si'
                if i.entorno == "":
                    listaTablas.append("<TR><TD>"+tipo+"</TD><TD>"+llave+"</TD><TD>"+"Global"+"</TD><TD>"+str(posicion)+"</TD><TD>"+heap+"</TD><TD>"+str(valor.fila)+"</TD><TD>"+str(valor.columna)+"</TD></TR>\n")
                else:
                    listaTablas.append("<TR><TD>"+tipo+"</TD><TD>"+llave+"</TD><TD>"+i.entorno+"</TD><TD>"+str(posicion)+"</TD><TD>"+heap+"</TD><TD>"+str(valor.fila)+"</TD><TD>"+str(valor.columna)+"</TD></TR>\n")
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
        for i in self.getExcepciones():
            self.grafoError += "<TR><TD>"+str(contador)+"</TD><TD>"+i.descripcion+"</TD><TD>"+str(i.fecha)+"</TD><TD>"+str(i.fila)+"</TD><TD>"+str(i.columna)+"</TD></TR>\n"
            contador += 1