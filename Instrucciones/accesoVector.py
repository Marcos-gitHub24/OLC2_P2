from Abstract.Return import Return
from TS.Generador import Generador
from Expresiones.Aritmetica import Aritmetica
from Objeto.Primitivo import Primitivo
from Abstract.Objeto import TipoObjeto
from Abstract.NodoReporteArbol import NodoReporteArbol
from TS.Excepcion import Excepcion
from Abstract.NodoAST import NodoAST
from TS.Simbolo import Simbolo
from TS.Tipo import TIPO



class Acceso(NodoAST):
    def __init__(self, identificador, lista, fila, columna):
        self.identificador = identificador
        self.lista = lista
        self.fila = fila
        self.columna = columna

    def interpretar(self, entorno):
        lista = []
        aux = Generador()
        generador = aux.obtenerGen()
        for i in self.lista:
            result = i.interpretar(entorno)
            if(result.tipo == TIPO.CADENA):
                #tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede tener un indice cadena",self.fila,self.columna))
                return  Excepcion(TIPO.ERROR, f"No puede tener un indice cadena",self.fila,self.columna)
            if(result.tipo == TIPO.CHARACTER):
                #tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede tener un indice char",self.fila,self.columna))
                return  Excepcion(TIPO.ERROR, f"No puede tener un indice char",self.fila,self.columna)
            if(result.tipo == TIPO.BOOLEANO):
                #tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede tener un indice booleano",self.fila,self.columna))
                return  Excepcion(TIPO.ERROR, f"No puede tener un indice booleano",self.fila,self.columna)
            if(result.tipo == TIPO.DECIMAL):
                #tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede tener un indice decimal",self.fila,self.columna))
                return  Excepcion(TIPO.ERROR, f"No puede adadsadadasdasd un indice decimal",self.fila,self.columna)
            lista.append(result.valor)
        variable = entorno.obtenerVariable(self.identificador)
        print("-----variable---")
        print(variable.arreglo)
        pivote = generador.agregarTemporal()
        apunta_heap = generador.agregarTemporal()
        generador.obtener_stack(pivote,variable.pos)
        tamano = generador.agregarTemporal()
        indice = generador.agregarTemporal()
        #extra = generador.agregarLabel()
        arreglo_tipo = variable.arreglo
        contador = 1
        tipo_retorno = TIPO.ENTERO
        for i in arreglo_tipo:
            if isinstance(i,list) == True and contador != len(lista):
                arreglo_tipo = variable.arreglo[int(lista[contador-1])-1]
            elif isinstance(i,list) == True and contador == len(lista):
                print(contador)
                if int(lista[contador-1]) >= len(arreglo_tipo):
                    continue
                arreglo_tipo = variable.arreglo[int(lista[contador-1])-1]
                break
            elif isinstance(i,list)== False and contador == len(lista):
                if int(lista[contador-1]) >= len(arreglo_tipo):
                    tipo_retorno = arreglo_tipo[len(arreglo_tipo)-1]
                else:
                    tipo_retorno = arreglo_tipo[int(lista[contador-1])-1]
                break
            elif isinstance(i,list) and contador == len(lista):
                tipo_retorno = TIPO.ARREGLO                 # tengo que arreglar cuando el indice sea mayor al tamaño
            contador += 1

        resultado = Return(pivote,tipo_retorno,True)
        extra = generador.agregarLabel()
        
        #resultado.falselbl = extra
        for i in lista:
            
            salida = generador.agregarLabel()
            error = generador.agregarLabel()
            generador.obtener_heap(tamano,pivote)
            generador.agregarExpresion(indice,i,'','')

            generador.agregarIf(indice,tamano,'>',error)
            generador.agregarExpresion(apunta_heap,pivote,indice,'+')
            generador.obtener_heap(pivote,apunta_heap)
            
            generador.agregarGoto(salida)
            generador.colocarLbl(error)
            generador.agregarPrint('c','101')
            generador.agregarPrint('c','114')
            generador.agregarPrint('c','114')
            generador.agregarPrint('c','111')
            generador.agregarPrint('c','114')
            generador.agregarExpresion(pivote,'0','','')
            generador.agregarGoto(extra)
            generador.colocarLbl(salida)
        generador.colocarLbl(extra)
        #return Return(pivote,TIPO.ENTERO,True)
        return resultado
        
    def getNodo(self):
        nodo = NodoReporteArbol("LISTA_VECTOR")
        nodo.agregarHijo(self.identificador)
        nodo.agregarHijoCadena("[")
        unaVez = True
        for i in self.lista:
            if unaVez:
                nuevo1 = NodoReporteArbol("EXPRESION")
                nuevo1.agregarHijoNodo(i.getNodo())
                nodo.agregarHijoNodo(nuevo1)
            else:
                n = nodo
                nuevo1 = NodoReporteArbol("EXPRESION")
                nodo = NodoReporteArbol("LISTA_VECTOR")
                nodo.agregarHijoNodo(n)
                nodo.agregarHijoCadena(",")
                nuevo1.agregarHijoNodo(i.getNodo())
                nodo.agregarHijoNodo(nuevo1)
            unaVez = False
        nodo.agregarHijoCadena("]")
        return nodo

   
