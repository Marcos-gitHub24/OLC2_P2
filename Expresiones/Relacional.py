from Abstract.Return import Return
from Expresiones.Struct import Struct
from Instrucciones.Llamada import Llamada
from Objeto.Primitivo import Primitivo
from Abstract.Objeto import TipoObjeto
from Abstract.NodoReporteArbol import NodoReporteArbol
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.Generador import Generador
from TS.Tipo import TIPO, OperadorRelacional


class Relacional(NodoAST):
    def __init__(self, operador, OperacionIzq, OperacionDer, fila, columna):
        self.operador = operador
        self.OperacionIzq = OperacionIzq
        self.OperacionDer = OperacionDer
        self.fila = fila
        self.columna = columna
        self.truelbl = None
        self.falselbl = None

    def interpretar(self, entorno):
        aux = Generador()
        generador = aux.obtenerGen()
        res_left = self.OperacionIzq.interpretar(entorno)
        res_right = None
        bandera_llamada = False
        temporal_recupero_guardo = None
        if isinstance(self.OperacionDer, Llamada) and entorno.dentro != None:
            temporal_recupero_guardo = res_left.valor
            guardo = generador.agregarTemporal() 
            generador.agregarExpresion(guardo,'P',entorno.size,'+')
            generador.guardar_stack(guardo,temporal_recupero_guardo)
            entorno.size = entorno.size + 1
            bandera_llamada = True
        
        resultado = Return('', TIPO.BOOLEANO, False)
        bandera = False
        if not isinstance(res_left, Struct) and not isinstance(res_right, Struct):
            
            '''if(res_left.tipo == TipoObjeto.ERROR):
                return res_left
            if(res_right.tipo == TipoObjeto.ERROR):
                return res_right'''
            operador = ''
            if self.operador == OperadorRelacional.MAYORIGUAL:
                operador = '>='
            if self.operador == OperadorRelacional.MAYORQUE:
                operador = '>'
            if self.operador == OperadorRelacional.MENORIGUAL:
                operador = '<='
            if self.operador == OperadorRelacional.MENORQUE:
                operador = '<'
            if self.operador == OperadorRelacional.IGUALIGUAL:
                operador = '=='
            if self.operador == OperadorRelacional.DIFERENTE:
                operador = '!='
            if res_left.tipo != TIPO.BOOLEANO:
                res_right = self.OperacionDer.interpretar(entorno)
                if bandera_llamada:
                    recupero = generador.agregarTemporal()
                    entorno.size = entorno.size -1
                    generador.agregarExpresion(recupero,'P',entorno.size,'+')
                    generador.obtener_stack(temporal_recupero_guardo,recupero)
                  
                if(res_left.tipo == TIPO.ENTERO and res_right.tipo == TIPO.ENTERO):
                    bandera = True
                    # return Primitivo(TIPO.BOOLEANO, self.fila, self.columna, int(res_left.getValue()) >= int(res_right.getValue()))
                elif(res_left.tipo == TIPO.ENTERO and res_right.tipo == TIPO.DECIMAL):
                    bandera = True
                    # return Primitivo(TIPO.BOOLEANO, self.fila, self.columna, int(res_left.getValue()) >= float(res_right.getValue()))
                elif(res_left.tipo == TIPO.DECIMAL and res_right.tipo == TIPO.ENTERO):
                    bandera = True
                    # return Primitivo(TIPO.BOOLEANO, self.fila, self.columna, float(res_left.getValue()) >= int(res_right.getValue()))
                elif(res_left.tipo == TIPO.DECIMAL and res_right.tipo == TIPO.DECIMAL):
                    bandera = True
                    # return Primitivo(TIPO.BOOLEANO, self.fila, self.columna, float(res_left.getValue()) >= float(res_right.getValue()))
                elif(res_left.tipo == TIPO.CADENA and res_right.tipo == TIPO.CADENA):
                    if operador == '==' or operador == '!=':
                        generador.funCompararStrings()
                        if self.truelbl == None:
                            self.truelbl = generador.agregarLabel()
                        if self.falselbl == None:
                            self.falselbl = generador.agregarLabel()
                        
                        primera = generador.agregarTemporal()
                        generador.agregarExpresion(primera,'P',entorno.size,'+')
                        generador.agregarExpresion(primera,primera,'1','+')
                        generador.guardar_stack(primera,res_left.valor)

                        segunda = generador.agregarTemporal()
                        generador.agregarExpresion(segunda,'P',entorno.size,'+')
                        generador.agregarExpresion(segunda,segunda,'2','+')
                        generador.guardar_stack(segunda,res_right.valor)

                        generador.agregarExpresion('P','P',entorno.size,'+')
                        generador.callFun('compararStrings')
                        result = generador.agregarTemporal()
                        generador.obtener_stack(result, 'P')
                        generador.agregarExpresion('P','P',entorno.size,'-')
                        if operador == '==':
                            generador.agregarIf(result, '1', '==', self.truelbl)
                            generador.agregarGoto(self.falselbl)
                        else:
                            generador.agregarIf(result, '1', '==', self.falselbl)
                            generador.agregarGoto(self.truelbl)
                        resultado.truelbl = self.truelbl
                        resultado.falselbl = self.falselbl
                        return resultado
                    
                    # return Primitivo(TIPO.BOOLEANO, self.fila, self.columna, str(res_left.getValue()) >= str(str(res_right.getValue())))
                elif(res_left.tipo == TIPO.NULO or res_right.tipo == TIPO.NULO):
                    bandera = True
                    # return Primitivo(TIPO.BOOLEANO, self.fila, self.columna, bool(res_left.getValue()) >= bool(res_right.getValue()))
                if bandera:
                    if self.truelbl == None:
                        self.truelbl = generador.agregarLabel()
                    if self.falselbl == None:
                        self.falselbl = generador.agregarLabel()
                    generador.agregarIf(res_left.valor, res_right.valor, operador, self.truelbl)
                    generador.agregarGoto(self.falselbl)
                    resultado.truelbl = self.truelbl
                    resultado.falselbl = self.falselbl
                    return resultado
                else:
                    #tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede realizarse la comparacion con esos operadores",self.fila,self.columna))
                    return Excepcion(TIPO.ERROR, f"No puede realizarse la comparacion con esos operadores", self.fila, self.columna)
            else:
                                
                goto_derecho = generador.agregarLabel()
                temp_izquierdo = generador.agregarTemporal()

                generador.colocarLbl(res_left.truelbl)
                generador.agregarExpresion(temp_izquierdo, '1', '', '')
                generador.agregarGoto(goto_derecho)

                generador.colocarLbl(res_left.falselbl)
                generador.agregarExpresion(temp_izquierdo, '0', '', '')
                generador.colocarLbl(goto_derecho)

                res_right = self.OperacionDer.interpretar(entorno)
                if bandera_llamada:
                    recupero = generador.agregarTemporal()
                    entorno.size = entorno.size -1
                    generador.agregarExpresion(recupero,'P',entorno.size,'+')
                    generador.obtener_stack(temporal_recupero_guardo,recupero)

                if res_right.tipo != TIPO.BOOLEANO:
                    return                          # retorno error 

                gotoEnd = generador.agregarLabel()
                temp_derecho = generador.agregarTemporal()

                generador.colocarLbl(res_right.truelbl)
                generador.agregarExpresion(temp_derecho, '1', '', '')
                generador.agregarGoto(gotoEnd)

                generador.colocarLbl(res_right.falselbl)
                generador.agregarExpresion(temp_derecho, '0', '', '')
                generador.colocarLbl(gotoEnd)

                if self.truelbl == None:
                        self.truelbl = generador.agregarLabel()
                if self.falselbl == None:
                        self.falselbl = generador.agregarLabel()
                generador.agregarIf(temp_izquierdo, temp_derecho, operador, self.truelbl)
                generador.agregarGoto(self.falselbl)
                resultado.truelbl = self.truelbl
                resultado.falselbl = self.falselbl
                return resultado
            

            #return Excepcion(TIPO.ERROR, f"Operador desconocido: {self.operador}", self.fila, self.columna)

    def getNodo(self):
        nodo = NodoReporteArbol("RELACIONAL")
        izquierdo = NodoReporteArbol("EXPRESION")
        nodo.agregarHijoNodo(izquierdo)
        derecho = NodoReporteArbol("EXPRESION")
        if self.operador == OperadorRelacional.IGUALIGUAL:
            nodo.agregarHijoCadena("==")
        elif self.operador == OperadorRelacional.DIFERENTE:
            nodo.agregarHijoCadena("!=")
        elif self.operador == OperadorRelacional.MAYORIGUAL:
            nodo.agregarHijoCadena(">=")
        elif self.operador == OperadorRelacional.MAYORQUE:
            nodo.agregarHijoCadena(">")
        elif self.operador == OperadorRelacional.MENORIGUAL:
            nodo.agregarHijoCadena("<=")
        elif self.operador == OperadorRelacional.MENORQUE:
            nodo.agregarHijoCadena("<")
        izquierdo.agregarHijoNodo(self.OperacionIzq.getNodo())
        nodo.agregarHijoNodo(derecho)
        derecho.agregarHijoNodo(self.OperacionDer.getNodo())

        return nodo

    def obtenerVal(self, tipo, val):
        if tipo == TIPO.ENTERO:
            return int(val)
        elif tipo == TIPO.DECIMAL:
            return float(val)
        elif tipo == TIPO.BOOLEANO:
            return bool(val)
        return str(val)

