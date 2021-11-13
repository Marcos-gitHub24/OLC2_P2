from Abstract.Return import Return
from Expresiones.Identificador import Identificador
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
                generador.TSglobal.addExcepcion(Excepcion(TIPO.ERROR, f"No puede tener un indice cadena",self.fila,self.columna))
                return  Excepcion(TIPO.ERROR, f"No puede tener un indice cadena",self.fila,self.columna)
            if(result.tipo == TIPO.CHARACTER):
                generador.TSglobal.addExcepcion(Excepcion(TIPO.ERROR, f"No puede tener un indice char",self.fila,self.columna))
                return  Excepcion(TIPO.ERROR, f"No puede tener un indice char",self.fila,self.columna)
            if(result.tipo == TIPO.BOOLEANO):
                generador.TSglobal.addExcepcion(Excepcion(TIPO.ERROR, f"No puede tener un indice booleano",self.fila,self.columna))
                return  Excepcion(TIPO.ERROR, f"No puede tener un indice booleano",self.fila,self.columna)
            if(result.tipo == TIPO.DECIMAL):
                generador.TSglobal.addExcepcion(Excepcion(TIPO.ERROR, f"No puede tener un indice decimal",self.fila,self.columna))
                return  Excepcion(TIPO.ERROR, f"No puede tener un indice decimal",self.fila,self.columna)
            lista.append(result.valor)
        
        arrego_guardado = Identificador(self.identificador, self.fila, self.columna)
        arreglo_usar = arrego_guardado.interpretar(entorno)
        temp_inicio = arreglo_usar.valor
        variable = entorno.obtenerVariable(self.identificador)
        generador.addComment('ACA ACCEDO AL VECTOR')
        #print(variable.arreglo)
        pivote = generador.agregarTemporal()
        pivote = temp_inicio
        apunta_heap = generador.agregarTemporal()
        #obtengo = generador.agregarTemporal()
        #generador.agregarExpresion(obtengo,'P',variable.pos,'+')
        #generador.obtener_stack(pivote,temp_inicio)
        tamano = generador.agregarTemporal()
        indice = generador.agregarTemporal()
        #extra = generador.agregarLabel()
        arreglo_tipo = variable.arreglo
        contador = 1
        tipo_retorno = TIPO.ENTERO
        
        #print(obtengoTipo(variable.arreglo,len(variable.arreglo),len(variable.arreglo)))
        bandera = False

        if len(lista)==1:
            if isinstance(variable.arreglo[0],list):
                tipo_retorno = TIPO.ARREGLO
                arreglo_tipo = variable.arreglo[0]
            else:
                tipo_retorno = variable.arreglo[0]
        else:
            for i in variable.arreglo:                  # me sirve para ver que tipo regresar
                nivel = len(lista)-1
                if isinstance(i,list):
                    contador = 0
                    arreglo = i
                    while contador < nivel:
                        if isinstance(arreglo[0],list):
                            arreglo = arreglo[0]
                            nivel = nivel - 1
                        if nivel<len(lista):
                            if isinstance(arreglo[0],list):
                                nivel = nivel - 1
                                tipo_retorno = TIPO.ARREGLO
                                arreglo_tipo = arreglo[0]
                                bandera = True
                                break
                            else:
                                nivel = nivel - 1
                                tipo_retorno = arreglo[0]
                                bandera = True
                                break
                        contador = contador + 1
                if bandera:
                    break
        '''if len(lista)==1:
            if isinstance(variable.arreglo[0],list):
                tipo_retorno = TIPO.ARREGLO
            else:
                tipo_retorno = variable.arreglo[0]
        else:
            try:
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

                
            except:
                if isinstance(variable.arreglo[0],list):
                    tipo_retorno = TIPO.ARREGLO
                else:
                    tipo_retorno = variable.arreglo[0]'''
        resultado = Return(pivote,tipo_retorno,True)
        resultado.arreglo = arreglo_tipo
        extra = generador.agregarLabel()
        #resultado.falselbl = extra
        for i in lista:
            
            salida = generador.agregarLabel()
            error = generador.agregarLabel()
            generador.obtener_heap(tamano,pivote)
            generador.agregarExpresion(indice,i,'','')

            generador.agregarIf(indice,tamano,'>',error)
            generador.agregarIf(indice,'1','<',error)
            generador.agregarExpresion(apunta_heap,pivote,indice,'+')
            generador.obtener_heap(pivote,apunta_heap)
            
            generador.agregarGoto(salida)
            generador.colocarLbl(error)
            generador.agregarPrint('c','66')
            generador.agregarPrint('c','111')
            generador.agregarPrint('c','117')
            generador.agregarPrint('c','110')
            generador.agregarPrint('c','100')

            generador.agregarPrint('c','115')
            generador.agregarPrint('c','69')
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
def obtengoTipo(arreglo,contador,nivel):
    tipo = ''
    for i in arreglo:
        if isinstance(i,list):
            contador = contador - 1
            tipo = obtengoTipo(i,contador,nivel)
    if contador == 1:
        return tipo

   
