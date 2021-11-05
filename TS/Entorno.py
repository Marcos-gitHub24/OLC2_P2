from TS.Symbol import *

class Entorno:
    
    def __init__(self, prev):
        self.prev = prev

        self.variables = {}
        self.funciones = {}
        self.structs = {}

        self.lbl_break = ''
        self.lbl_return = ''
        self.lbl_continue = ''
        self.lbl_return = ''
        self.dentro = None
        self.size = 0
        
        if(prev != None):
            self.size = self.prev.size
            self.lbl_return = self.prev.lbl_return
            self.lbl_break = self.prev.lbl_break
            self.lbl_continue = self.prev.lbl_continue
        
        
    
    def guardarVariable(self, identificacion, tipo, inHeap, struct, arreglo):
        if identificacion in self.variables.keys():
            # agregar un error 
            return None
        else:
            simbolo = Symbol(identificacion, tipo, self.size, self.prev == None, inHeap, struct, arreglo)
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