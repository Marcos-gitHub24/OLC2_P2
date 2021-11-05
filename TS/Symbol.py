from Abstract.Return import *

class Symbol:
    def __init__(self, identificador, tipo, posicion, es_global, en_heap, struct, arreglo):
        self.id = identificador
        self.tipo = tipo
        self.pos = posicion
        self.isGlobal = es_global
        self.inHeap = en_heap
        self.value = None
        self.struct = struct
        self.arreglo = arreglo