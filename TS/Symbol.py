from Abstract.Return import *

class Symbol:
    def __init__(self, symbolID, symbolType, position, globalVar, inHeap, struct):
        self.id = symbolID
        self.tipo = symbolType
        self.pos = position
        self.isGlobal = globalVar
        self.inHeap = inHeap
        self.value = None
        self.struct = struct