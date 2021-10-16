from Objeto.Primitivo import Primitivo
from Abstract.Objeto import TipoObjeto
from enum import Enum
from Abstract.NodoReporteArbol import NodoReporteArbol
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO, OperadorAritmetico
from Abstract.Expresion import Expresion
from Abstract.Return import Return
from TS.Generador import Generador
class Aritmetica(NodoAST):
    
    def __init__(self, operador, OperacionIzq, OperacionDer, operandoU,fila, columna):
        super().__init__(TIPO.ENTERO, fila, columna)
        self.operador = operador
        self.OperacionIzq = OperacionIzq
        self.OperacionDer = OperacionDer
        self.operandoU = operandoU


    def interpretar(self, entorno):
        res_left = None
        res_right = None
        res_unario = None
        aux = Generador()
        generador = aux.obtenerGen()
        if self.operandoU == "":
            res_left = self.OperacionIzq.interpretar(entorno)
            res_right = self.OperacionDer.interpretar(entorno)
            if(res_left.tipo == TIPO.ERROR):
                #tree.addExcepcion(res_left)
                return res_left;
            if(res_right.tipo == TIPO.ERROR):
                #tree.addExcepcion(res_right)
                return res_right;
        else:
            res_unario = self.operandoU.interpretar(entorno)
            if(res_unario.tipo == TIPO.ERROR):
                #tree.addExcepcion(res_unario)
                return res_unario;  
        temporal = generador.agregarTemporal()
        operador = ""
        if (self.operador==OperadorAritmetico.MAS):
            operador = '+'
            if(res_left.tipo == TIPO.ENTERO and res_right.tipo == TIPO.ENTERO):
                generador.agregarExpresion(temporal, res_left.valor, res_right.valor, operador)
                #return Primitivo(TIPO.ENTERO, self.fila, self.columna, int(res_left.getValue()) + int(res_right.getValue()));
                return Return(temporal, TIPO.ENTERO, True)
            elif(res_left.tipo == TIPO.ENTERO and res_right.tipo == TIPO.DECIMAL):
                generador.agregarExpresion(temporal, res_left.valor, res_right.valor, operador)
                #return Primitivo(TIPO.DECIMAL, self.fila, self.columna, int(res_left.getValue()) + float(res_right.getValue()));
                return Return(temporal, TIPO.DECIMAL, True)

            elif(res_left.tipo == TIPO.DECIMAL and res_right.tipo == TIPO.ENTERO):
                generador.agregarExpresion(temporal, res_left.valor, res_right.valor, operador)
                #return Primitivo(TIPO.DECIMAL, self.fila, self.columna, float(res_left.getValue()) + int(res_right.getValue()));
                return Return(temporal, TIPO.DECIMAL, True)

            elif(res_left.tipo == TIPO.DECIMAL and res_right.tipo == TIPO.DECIMAL):
                generador.agregarExpresion(temporal, res_left.valor, res_right.valor, operador)
                #return Primitivo(TIPO.DECIMAL, self.fila, self.columna, float(res_left.getValue()) + float(res_right.getValue()));
                return Return(temporal, TIPO.DECIMAL, True)
            else:
                #tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede realizarse la suma con esos operadores",self.fila,self.columna))
                return Excepcion(TIPO.ERROR, f"No puede realizarse la suma con esos operadores",self.fila,self.columna)
        
        if (self.operador==OperadorAritmetico.MENOS):
            operador = '-'
            if(res_left.tipo == TIPO.ENTERO and res_right.tipo == TIPO.ENTERO):
                generador.agregarExpresion(temporal, res_left.valor, res_right.valor, operador)
                #return Primitivo(TIPO.ENTERO, self.fila, self.columna, int(res_left.getValue()) - int(res_right.getValue()));
                return Return(temporal, TIPO.ENTERO, True)

            elif(res_left.tipo == TIPO.ENTERO and res_right.tipo == TIPO.DECIMAL):
                generador.agregarExpresion(temporal, res_left.valor, res_right.valor, operador)
                #return Primitivo(TIPO.DECIMAL, self.fila, self.columna, int(res_left.getValue()) - float(res_right.getValue()));
                return Return(temporal, TIPO.DECIMAL, True)

            elif(res_left.tipo == TIPO.DECIMAL and res_right.tipo == TIPO.ENTERO):
                generador.agregarExpresion(temporal, res_left.valor, res_right.valor, operador)
                #return Primitivo(TIPO.DECIMAL, self.fila, self.columna, float(res_left.getValue()) - int(res_right.getValue()));
                return Return(temporal, TIPO.DECIMAL, True)

            elif(res_left.tipo == TIPO.DECIMAL and res_right.tipo == TIPO.DECIMAL):
                generador.agregarExpresion(temporal, res_left.valor, res_right.valor, operador)
                #return Primitivo(TIPO.DECIMAL, self.fila, self.columna, float(res_left.getValue()) - float(res_right.getValue()));
                return Return(temporal, TIPO.DECIMAL, True)
        
            else:
                #tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede realizarse la resta con esos operadores",self.fila,self.columna))
                return Excepcion(TIPO.ERROR, f"No puede realizarse la resta con esos operadores",self.fila,self.columna)

        if (self.operador==OperadorAritmetico.POR):
            operador = '*'
            if(res_left.tipo == TIPO.ENTERO and res_right.tipo == TIPO.ENTERO):
                generador.agregarExpresion(temporal, res_left.valor, res_right.valor, operador)
                #return Primitivo(TIPO.ENTERO, self.fila, self.columna, int(res_left.getValue()) * int(res_right.getValue()));
                return Return(temporal, TIPO.ENTERO, True)

            elif(res_left.tipo == TIPO.ENTERO and res_right.tipo == TIPO.DECIMAL):
                generador.agregarExpresion(temporal, res_left.valor, res_right.valor, operador)
                #return Primitivo(TIPO.DECIMAL, self.fila, self.columna, int(res_left.getValue()) * float(res_right.getValue()));
                return Return(temporal, TIPO.DECIMAL, True)

            elif(res_left.tipo == TIPO.DECIMAL and res_right.tipo == TIPO.ENTERO):
                generador.agregarExpresion(temporal, res_left.valor, res_right.valor, operador)
                #return Primitivo(TIPO.DECIMAL, self.fila, self.columna, float(res_left.getValue()) * int(res_right.getValue()));
                return Return(temporal, TIPO.DECIMAL, True)

            elif(res_left.tipo == TIPO.DECIMAL and res_right.tipo == TIPO.DECIMAL):
                generador.agregarExpresion(temporal, res_left.valor, res_right.valor, operador)
                #return Primitivo(TIPO.DECIMAL, self.fila, self.columna, float(res_left.getValue()) * float(res_right.getValue()));
                return Return(temporal, TIPO.DECIMAL, True)
            
            elif(res_left.tipo == TIPO.CADENA and res_right.tipo == TIPO.CADENA):
                #generador.agregarExpresion(temporal, res_left.valor, res_right.valor, operador)
                #return Primitivo(TIPO.CADENA, self.fila, self.columna, str(res_left.getValue()) + str(res_right.getValue()));
                #return Return(temporal, TIPO.CADENA, True)
                generador.funConcat()
                base = generador.agregarTemporal()
                generador.agregarExpresion(base,'P',entorno.size,'+')
                generador.agregarExpresion(base,base,'1','+')
                generador.setStack(base,res_left.valor)

                exponente = generador.agregarTemporal()
                generador.agregarExpresion(exponente,'P',entorno.size,'+')
                generador.agregarExpresion(exponente,exponente,'2','+')
                generador.setStack(exponente,res_right.valor)
                generador.agregarExpresion('P','P',entorno.size,'+')
                generador.callFun('concatenar')

                resultado = generador.agregarTemporal()
                generador.getStack(resultado, 'P')
                generador.agregarExpresion('P','P',entorno.size,'-')
                return Return(resultado,TIPO.CADENA, True)

            else:
                #tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede realizarse la multiplicacion con esos operadores",self.fila,self.columna))
                return Excepcion(TIPO.ERROR, f"No puede realizarse la multiplicacion con esos operadores",self.fila,self.columna)
        

        if (self.operador==OperadorAritmetico.DIV):
            operador = '/'
            if(res_left.tipo == TIPO.ENTERO and res_right.tipo == TIPO.ENTERO):
                generador.agregarExpresion(temporal, res_left.valor, res_right.valor, operador)
                #return Primitivo(TIPO.DECIMAL, self.fila, self.columna, int(res_left.getValue()) / int(res_right.getValue()));
                return Return(temporal, TIPO.ENTERO, True)

            elif(res_left.tipo == TIPO.ENTERO and res_right.tipo == TIPO.DECIMAL):
                generador.agregarExpresion(temporal, res_left.valor, res_right.valor, operador)
                #return Primitivo(TIPO.DECIMAL, self.fila, self.columna, int(res_left.getValue()) / float(res_right.getValue()));
                return Return(temporal, TIPO.DECIMAL, True)

            elif(res_left.tipo == TIPO.DECIMAL and res_right.tipo == TIPO.ENTERO):
                generador.agregarExpresion(temporal, res_left.valor, res_right.valor, operador)
                #return Primitivo(TIPO.DECIMAL, self.fila, self.columna, float(res_left.getValue()) / int(res_right.getValue()));
                return Return(temporal, TIPO.DECIMAL, True)

            elif(res_left.tipo == TIPO.DECIMAL and res_right.tipo == TIPO.DECIMAL):
                generador.agregarExpresion(temporal, res_left.valor, res_right.valor, operador)
                #return Primitivo(TIPO.DECIMAL, self.fila, self.columna, float(res_left.getValue()) / float(res_right.getValue()));
                return Return(temporal, TIPO.DECIMAL, True)
        
            else:
                #tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede realizarse la division con esos operadores",self.fila,self.columna))
                return Excepcion(TIPO.ERROR, f"No puede realizarse la division con esos operadores",self.fila,self.columna)
        

        if(self.operador==OperadorAritmetico.POTENCIA):
            bandera = False
            if(res_left.tipo == TIPO.CADENA and res_right.tipo == TIPO.ENTERO):
                bandera = True
                #return Primitivo(TIPO.CADENA, self.fila, self.columna, str(res_left.getValue()) * int(res_right.getValue()));
            
            elif(res_left.tipo == TIPO.ENTERO and res_right.tipo == TIPO.ENTERO):
                bandera = True
                #return Primitivo(TIPO.ENTERO, self.fila, self.columna, int(res_left.getValue()) ** int(res_right.getValue()));

            elif(res_left.tipo == TIPO.ENTERO and res_right.tipo == TIPO.DECIMAL):
                return Primitivo(TIPO.DECIMAL, self.fila, self.columna, int(res_left.getValue()) ** float(res_right.getValue()));

            elif(res_left.tipo == TIPO.DECIMAL and res_right.tipo == TIPO.ENTERO):
                bandera = True
                #return Primitivo(TIPO.DECIMAL, self.fila, self.columna, float(res_left.getValue()) ** int(res_right.getValue()));

            elif(res_left.tipo == TIPO.DECIMAL and res_right.tipo == TIPO.DECIMAL):
                return Primitivo(TIPO.DECIMAL, self.fila, self.columna, float(res_left.getValue()) ** float(res_right.getValue()));

            if bandera:
                generador.funcPotencia()
                base = generador.agregarTemporal()
                generador.agregarExpresion(base,'P',entorno.size,'+')
                generador.agregarExpresion(base,base,'1','+')
                generador.setStack(base,res_left.valor)

                exponente = generador.agregarTemporal()
                generador.agregarExpresion(exponente,'P',entorno.size,'+')
                generador.agregarExpresion(exponente,exponente,'2','+')
                generador.setStack(exponente,res_right.valor)
                generador.agregarExpresion('P','P',entorno.size,'+')
                generador.callFun('potencia')
                resultado = generador.agregarTemporal()
                generador.getStack(resultado, 'P')
                generador.agregarExpresion('P','P',entorno.size,'-')
                return Return(resultado,TIPO.DECIMAL, True)


            else:
                #tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede realizarse la potencia con esos operadores",self.fila,self.columna))
                return Excepcion(TIPO.ERROR, f"No puede realizarse la potencia con esos operadores",self.fila,self.columna)
        

        if (self.operador==OperadorAritmetico.MODULO):
            operador = '%'
            if(res_left.tipo == TIPO.ENTERO and res_right.tipo == TIPO.ENTERO):
                generador.agregarExpresion(temporal, res_left.valor, res_right.valor, operador)
                #return Primitivo(TIPO.DECIMAL, self.fila, self.columna, int(res_left.getValue()) % int(res_right.getValue()));
                return Return(temporal, TIPO.ENTERO, True)


            elif(res_left.tipo == TIPO.ENTERO and res_right.tipo == TIPO.DECIMAL):
                generador.agregarExpresion(temporal, res_left.valor, res_right.valor, operador)
                #return Primitivo(TIPO.DECIMAL, self.fila, self.columna, int(res_left.getValue()) % float(res_right.getValue()));
                return Return(temporal, TIPO.DECIMAL, True)

            elif(res_left.tipo == TIPO.DECIMAL and res_right.tipo == TIPO.ENTERO):
                generador.agregarExpresion(temporal, res_left.valor, res_right.valor, operador)
                #return Primitivo(TIPO.DECIMAL, self.fila, self.columna, float(res_left.getValue()) % int(res_right.getValue()));
                return Return(temporal, TIPO.DECIMAL, True)

            elif(res_left.tipo == TIPO.DECIMAL and res_right.tipo == TIPO.DECIMAL):
                generador.agregarExpresion(temporal, res_left.valor, res_right.valor, operador)
                #return Primitivo(TIPO.DECIMAL, self.fila, self.columna, float(res_left.getValue()) % float(res_right.getValue()));
                return Return(temporal, TIPO.DECIMAL, True)
            else:
                #tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede realizarse el modulo con esos operadores",self.fila,self.columna))
                return Excepcion(TIPO.ERROR, f"No puede realizarse el modulo con esos operadores",self.fila,self.columna)
        
        
        if (self.operador==OperadorAritmetico.MENOSUNARIO):
            operador = '-'
            if (res_unario.tipo == TIPO.ENTERO):
                generador.agregarExpresion(temporal, '', res_unario.valor, operador)
                #return Primitivo(TIPO.ENTERO, self.fila, self.columna, int(res_unario.getValue()) * -1)
                return Return(temporal, TIPO.ENTERO, True)
            elif (res_unario.tipo == TIPO.DECIMAL):
                generador.agregarExpresion(temporal, '', res_unario.valor, operador)
                #return Primitivo(TIPO.DECIMAL, self.fila, self.columna, float(res_unario.getValue()) * -1)
                return Return(temporal, TIPO.DECIMAL, True)
            else:
                #tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede realizarse la negacion con esos operadores",self.fila,self.columna))
                return Excepcion(TIPO.ERROR, f"No puede realizarse la negacion con esos operadores",self.fila,self.columna)
        #tree.addExcepcion(Excepcion(TIPO.ERROR, f"Operador desconocido: {self.operador}",self.fila,self.columna))
        return Excepcion(TIPO.ERROR, f"Operador desconocido: {self.operador}",self.fila,self.columna);


    def getNodo(self):
        nodo = NodoReporteArbol("ARITMETICA")
        if self.operandoU == "":
            izquierdo = NodoReporteArbol("EXPRESION")
            nodo.agregarHijoNodo(izquierdo)
            derecho = NodoReporteArbol("EXPRESION")
            
            if self.operador == OperadorAritmetico.MAS:
                nodo.agregarHijoCadena("+")
            elif self.operador == OperadorAritmetico.MENOS:
                nodo.agregarHijoCadena("-")
            elif self.operador == OperadorAritmetico.POR:
                nodo.agregarHijoCadena("*")
            elif self.operador == OperadorAritmetico.DIV:
                nodo.agregarHijoCadena("/")
            elif self.operador == OperadorAritmetico.POTENCIA:
                nodo.agregarHijoCadena("^")
            elif self.operador == OperadorAritmetico.MODULO:
                nodo.agregarHijoCadena("%")
            izquierdo.agregarHijoNodo(self.OperacionIzq.getNodo())
            nodo.agregarHijoNodo(derecho)
            derecho.agregarHijoNodo(self.OperacionDer.getNodo())
        else:
            nodo.agregarHijo("-")
            izquierdo = NodoReporteArbol("EXPRESION")
            nodo.agregarHijoNodo(izquierdo)
            izquierdo.agregarHijoNodo(self.operandoU.getNodo())
        
        return nodo