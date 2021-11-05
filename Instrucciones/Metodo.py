class Metodo:
    def __init__(self, instrucciones, parametros, tipo):
        self.instrucciones = instrucciones
        self.parametros = parametros
        self.tipo = tipo
        self.arreglo_tipo = None
        self.struct = None

    def getInstrucciones(self):
        return self.instrucciones
    
    def getParametros(self):
        return self.parametros

    def getTipo(self):
        return self.tipo