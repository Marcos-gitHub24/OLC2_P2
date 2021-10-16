from Abstract.Return import Return
from Objeto.Primitivo import Primitivo
from Abstract.Objeto import TipoObjeto
from Abstract.NodoReporteArbol import NodoReporteArbol
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.Generador import Generador
from TS.Tipo import TIPO, OperadorLogico, OperadorRelacional

class Logica(NodoAST):
    def __init__(self, operador, OperacionIzq, OperacionDer, operacionU, fila, columna):
        self.operador = operador
        self.OperacionIzq = OperacionIzq
        self.OperacionDer = OperacionDer
        self.operacionU = operacionU
        self.truelbl = None
        self.falselbl = None
        self.fila = fila
        self.columna = columna

    
    def interpretar(self, entorno):
        #if(self.operacionU == ""):
        aux = Generador()
        generador = aux.obtenerGen()
        if self.truelbl == None:
            self.truelbl = generador.agregarLabel()
        if self.falselbl == None:
            self.falselbl = generador.agregarLabel()
        label_final = ''
        resultado = Return('', TIPO.BOOLEANO, False)
            #if(self.OperacionIzq.tipo == TIPO.ERROR):
                #tree.addExcepcion(res_left)
                #return self.OperacionIzq.tipo;
            #if(self.OperacionDer.tipo == TIPO.ERROR):
                #tree.addExcepcion(res_right)
                #return self.OperacionDer;
        '''else:
            if(self.operacionU.tipo == TIPO.ERROR):
                #tree.addExcepcion(res_u)
                return self.operacionU;'''

        if (self.operador==OperadorLogico.OR):  # En el or se comparte la etiqueta verdadera, por eso le asingo los mismos valores
            self.OperacionIzq.truelbl = self.truelbl
            self.OperacionDer.truelbl = self.truelbl
            label_final = generador.agregarLabel()
            print('----')
            print(label_final)
            print('----')
            self.OperacionIzq.falselbl = label_final
            self.OperacionDer.falselbl = self.falselbl
            #return Primitivo(TIPO.BOOLEANO,self.fila, self.columna, bool(res_left.getValue()) or bool(res_right.getValue()));
        
        elif (self.operador==OperadorLogico.AND):  # En el and se comparte la etiqueta falsa, por eso le asingo los mismos valores
            label_final = generador.agregarLabel()
            self.OperacionIzq.truelbl = label_final
            self.OperacionDer.truelbl = self.truelbl
            self.OperacionDer.falselbl = self.falselbl
            self.OperacionIzq.falselbl = self.falselbl
            #return Primitivo(TIPO.BOOLEANO,self.fila, self.columna, bool(res_left.getValue()) and bool(res_right.getValue()));
            
        elif (self.operador==OperadorLogico.NOT):
            #label_final = generador.agregarLabel()
            self.operacionU.truelbl = self.falselbl
            self.operacionU.falselbl = self.truelbl
        if self.operacionU == '':
            res_left = self.OperacionIzq.interpretar(entorno)
            if res_left.tipo != TIPO.BOOLEANO:
                return
            generador.colocarLbl(label_final)
            res_right = self.OperacionDer.interpretar(entorno)
            if res_right.tipo != TIPO.BOOLEANO:
                return
            resultado.truelbl = self.truelbl
            resultado.falselbl = self.falselbl
            return resultado
        else:
            res_unario = self.operacionU.interpretar(entorno)
            if res_unario.tipo != TIPO.BOOLEANO:
                return
            resultado.truelbl = self.truelbl
            resultado.falselbl = self.falselbl
            return resultado
        
            #return Primitivo(TIPO.BOOLEANO,self.fila, self.columna, not bool(res_u.getValue()));
        #tree.addExcepcion(Excepcion(TIPO.ERROR, f"Operador desconocido: {self.operador}",self.fila,self.columna))
        return Excepcion(TIPO.ERROR, f"Operador desconocido: {self.operador}",self.fila,self.columna);

            
        

    def getNodo(self):
        nodo = NodoReporteArbol("LOGICA")
        if self.operacionU == "":
            izquierdo = NodoReporteArbol("EXPRESION")
            nodo.agregarHijoNodo(izquierdo)
            derecho = NodoReporteArbol("EXPRESION")
            if self.operador == OperadorLogico.AND:
                nodo.agregarHijoCadena("&&")
            elif self.operador == OperadorLogico.OR:
                nodo.agregarHijoCadena("||")
            izquierdo.agregarHijoNodo(self.OperacionIzq.getNodo())
            nodo.agregarHijoNodo(derecho)
            derecho.agregarHijoNodo(self.OperacionDer.getNodo())
        else:
            nodo.agregarHijoCadena("!")
            nodo.agregarHijoNodo(self.operacionU.getNodo())
        
        return nodo