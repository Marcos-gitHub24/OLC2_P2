

from TS.Excepcion import Excepcion


class TablaSimbolos:
    def __init__(self, anterior = None):
        self.tabla = {} # Diccionario Vacio
        self.anterior = anterior
        self.entorno = ""

    def setTabla(self, simbolo):      # Agregar una variable
        if simbolo.id in self.tabla :
            return Excepcion("Semantico", "Variable " + simbolo.id + " ya existe", simbolo.fila, simbolo.columna)
        else:
            self.tabla[simbolo.id] = simbolo
            return None

    def getTabla(self, id):            # obtener una variable
        tablaActual = self
        while tablaActual != None:
            if id in tablaActual.tabla :
                return tablaActual.tabla[id]           # RETORNA SIMBOLO
            else:
                tablaActual = tablaActual.anterior
        return None

    def actualizarTabla(self, simbolo):
        tablaActual = self
        while tablaActual != None:
            if simbolo.id in tablaActual.tabla :
                tablaActual.tabla[simbolo.id].setValor(simbolo.getValor())
                return None             # simbolo actualizado
            else:
                tablaActual = tablaActual.anterior
        
        self.tabla[simbolo.id] = simbolo
        print(simbolo.id)
        return None # --> simbolo agregado
    

    def getAnterior(self):
        return self.anterior
        
    def setAnterior(self, tabla):
        self.anterior = tabla

    def setEntorno(self, nombre):
        self.entorno = nombre
    
    def getEntorno(self):
        return self.entorno
