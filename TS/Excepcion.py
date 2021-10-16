import time
from Abstract.Objeto import Objeto, TipoObjeto
from TS.Tipo import TIPO


class Excepcion(Objeto):
    def __init__(self, tipo, descripcion, fila, columna):
        self.tipoError = tipo
        self.descripcion = descripcion
        self.fila = fila
        self.columna = columna
        self.tipo=TIPO.ERROR
        self.fecha = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    def toString(self):
        return str(self.tipoError) + " - " + str(self.descripcion) + " [" + str(self.fila) + "," + str(self.columna) + "]"

    def getValue(self):
        return "";

    