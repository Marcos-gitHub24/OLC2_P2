from Expresiones.Struct import Struct
from Abstract.Objeto import TipoObjeto
from Abstract.NodoReporteArbol import NodoReporteArbol
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO
from Abstract.Expresion import Expresion
from Abstract.Return import Return
from TS.Generador import Generador

class Imprimirln(NodoAST):
    def __init__(self, expresion, fila, columna):
        super().__init__(TipoObjeto.CADENA, fila, columna)
        self.expresion = expresion
        self.cadena = ""
        

    def interpretar(self, entorno):
        self.cadena = ""
        for i in self.expresion:
            print(i)
            val = i.interpretar(entorno)
            aux = Generador()
            generador = aux.obtenerGen()
            if val.tipo == TIPO.ENTERO:
                generador.agregarPrint("d", val.valor)
            elif val.tipo == TIPO.DECIMAL:
                generador.agregarPrint("f", val.valor)
                
            elif val.tipo == TIPO.BOOLEANO:
                tempLbl = generador.agregarLabel()     

                generador.colocarLbl(val.truelbl)
                generador.printTrue()
                
                generador.agregarGoto(tempLbl)
                
                generador.colocarLbl(val.falselbl)
                generador.printFalse()

                generador.colocarLbl(tempLbl)

            elif val.tipo == TIPO.CADENA or val.tipo ==TIPO.CHARACTER:
                generador.fPrintString()
                temporal = generador.agregarTemporal()
                generador.agregarExpresion(temporal, 'P', entorno.size, '+')
                generador.agregarExpresion(temporal, temporal, '1', '+')
                generador.guardar_stack(temporal, val.valor)
                generador.newEnv(entorno.size)
                generador.callFun('printString')
                tmp = generador.agregarTemporal()
                generador.obtener_stack(tmp, 'P')
                generador.retEnv(entorno.size)
            elif val.tipo == TIPO.ARREGLO:
                #heap = generador.agregarTemporal()
                #generador.obtener_stack(heap,val.valor)
                print('------------------------A IMPRIMIR EL ARRGELO VOY PADRE----------------------')
                print(val)
                print(val.arreglo)
                generador.agregarPrint('c','91')
                generador.agregarPrint('c','32')
                imprimirVector(generador,val.arreglo,val.valor,entorno)
                generador.agregarPrint('c','32')
                generador.agregarPrint('c','93');
        generador.agregarPrint('c','10')

    def getNodo(self):
        nodo = NodoReporteArbol("IMPRIMIR")
        nuevo = NodoReporteArbol("EXPRESIONES")
        unaVez = True
        for i in self.expresion:
            if unaVez:
                nuevo1 = NodoReporteArbol("EXPRESION")
                nuevo1.agregarHijoNodo(i.getNodo())
                nuevo.agregarHijoNodo(nuevo1)
            else:
                n = nuevo
                nuevo1 = NodoReporteArbol("EXPRESION")
                nuevo = NodoReporteArbol("EXPRESIONES")
                nuevo.agregarHijoNodo(n)
                nuevo.agregarHijoCadena(",")
                nuevo1.agregarHijoNodo(i.getNodo())
                nuevo.agregarHijoNodo(nuevo1)
            unaVez = False
        nodo.agregarHijoCadena("print")
        nodo.agregarHijoCadena("(")
        nodo.agregarHijoNodo(nuevo)
        nodo.agregarHijoCadena(")")
        nodo.agregarHijoCadena(";")
        return nodo

def obtenerVector(tree, table, vector):
        lista = []
        for i in vector:
            valor = i.interpretar(tree, table)
            if isinstance(valor.valor, list):
               lista.append(obtenerVector(tree, table, valor.valor))
            else:
                lista.append(valor.valor)
        
        return lista
def imprimirVector(generador,arreglo,heap,entorno):
    #generador.agregarPrint('c','91');
    coma = 0
    tamano = generador.agregarTemporal()
    generador.obtener_heap(tamano,heap)
    generador.agregarExpresion(heap,heap,'1','+')
    contador = generador.agregarTemporal()
    generador.agregarExpresion(contador,'0','','');
    recorre_lbl = generador.agregarLabel()
    salida_lbl = generador.agregarLabel()
    generador.colocarLbl(recorre_lbl)
    generador.agregarIf(contador,tamano,'==',salida_lbl)
    
    for i in arreglo:
        if isinstance(i,list):
            nuevo = i
            #generador.agregarExpresion(heap,heap,'1','+')
            aux = generador.agregarTemporal()
            generador.agregarExpresion(aux,heap,'','')
            generador.obtener_heap(heap,heap)
            
            #generador.agregarPrint('c','44');
            generador.agregarPrint('c','91')
            imprimirVector(generador,nuevo,heap,entorno)
            generador.agregarPrint('c','93')
            #generador.agregarIf(contador,tamano,'==',salida_lbl)
           
            generador.agregarPrint('c','32');
            #generador.agregarPrint('c','44');
            #generador.agregarPrint('c','44');
            generador.agregarExpresion(heap,aux,'','')
            generador.agregarExpresion(heap,heap,'1','+')
            generador.agregarExpresion(contador,contador,'1','+')
        else:
            generador.agregarExpresion(contador,contador,'1','+')
            imprime = generador.agregarTemporal()
            generador.obtener_heap(imprime,heap)
            if i == TIPO.ENTERO:
                generador.agregarPrint('d',imprime);
                generador.agregarIf(contador,tamano,'==',salida_lbl)
                generador.agregarPrint('c','44');
               
            elif i == TIPO.DECIMAL:
                generador.agregarPrint('f',imprime);
                generador.agregarIf(contador,tamano,'==',salida_lbl)
                generador.agregarPrint('c','44');
            elif i == TIPO.CADENA:
                generador.fPrintString()
                temporal = generador.agregarTemporal()
                generador.agregarExpresion(temporal, 'P', entorno.size, '+')
                generador.agregarExpresion(temporal, temporal, '1', '+')
                generador.guardar_stack(temporal, imprime)
                generador.newEnv(entorno.size)
                generador.callFun('printString')
                tmp = generador.agregarTemporal()
                generador.obtener_stack(tmp, 'P')
                generador.retEnv(entorno.size)
                generador.agregarIf(contador,tamano,'==',salida_lbl)
                generador.agregarPrint('c','44');
            generador.agregarExpresion(heap,heap,'1','+')
        coma += 1
    
    #generador.agregarExpresion(heap,heap,'1','+')
    generador.agregarGoto(recorre_lbl)
    generador.colocarLbl(salida_lbl)
    #generador.agregarPrint('c','93');
    
def obtenerStruct(struct):
    cadena = struct.nombre + "( "
    for clave in struct.diccionario:
        if isinstance(struct.diccionario[clave], Struct) == False:
            if struct.diccionario[clave].valor == None:
                cadena += 'nothing, '
            else:
                cadena += str(struct.diccionario[clave].valor) + ", "
        else:
            cadena += obtenerStruct(struct.diccionario[clave]) + ", "
    cadena = cadena[0:-2]
    cadena += ")"
    return cadena
            

