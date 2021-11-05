class Return:
    def __init__(self, val, retType, isTemp):
        self.valor = val
        self.tipo = retType
        self.isTemp = isTemp
        self.arreglo = None
        self.struct = None
        self.truelbl = None
        self.falselbl = None