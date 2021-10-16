class Return:
    def __init__(self, val, retType, isTemp, auxType = ""):
        self.valor = val
        self.tipo = retType
        self.auxType = auxType
        self.isTemp = isTemp
        self.truelbl = ''
        self.falselbl = ''