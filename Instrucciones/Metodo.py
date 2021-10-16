class Metodo:
    def __init__(self, instrucciones, parametros):
        self.instrucciones = instrucciones
        self.parametros = parametros

    def getInstrucciones(self):
        return self.instrucciones
    
    def getParametros(self):
        return self.parametros