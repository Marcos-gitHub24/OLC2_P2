from TS.Symbol import *

class Entorno:
    
    def __init__(self, prev):
        self.prev = prev
        self.lbl_break = ''
        self.lbl_return = ''
        self.lbl_continue = ''
        self.lbl_return = ''
        self.dentro = None
        # NUEVO
        self.size = 0
        if(prev != None):
            self.size = self.prev.size
            self.lbl_return = self.prev.lbl_return
            self.lbl_break = self.prev.lbl_break
            self.lbl_continue = self.prev.lbl_continue
        
        self.variables = {}
        self.arreglos = {}
        self.functions = {}
        self.structs = {}
    
    def guardarVariable(self, identificacion, tipo, inHeap, struct, arreglo):
        if identificacion in self.variables.keys():
            print("Variable ya existe")
            # agregar error a una tabla
        else:
            simbolo = Symbol(identificacion, tipo, self.size, self.prev == None, inHeap, struct, arreglo)
            self.size += 1
            self.variables[identificacion] = simbolo
        return self.variables[identificacion]

    def guardarFuncion(self, idFunc, function):
        if idFunc in self.functions.keys():
            print("Función repetida")
        else:
            self.functions[idFunc] = function
    
    def guardarStruct(self, idStruct, attr):
        if idStruct in self.structs.keys():
            print("Struct repetido")
        else:
            self.structs[idStruct] = attr

    def obtenerVariable(self, idVar):
        env = self
        while env != None:
            if idVar in env.variables.keys():
                return env.variables[idVar]
            env = env.prev
        return None
    
    def obtenerFuncion(self, idFunc):
        env = self
        while env != None:
            if idFunc in env.functions.keys():
                return env.functions[idFunc]
            env = env.prev
        return None
        
    def obtenerStruct(self, idStruct):
        env = self
        while env != None:
            if idStruct in env.structs.keys():
                return env.structs[idStruct]
            end = end.prev
        return None

    def obtenerGlobal(self):
        env = self
        while env.prev != None:
            env = env.prev
        return env