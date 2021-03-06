from re import template
from Instrucciones.Imprimir import obtenerVector
from TS.Generador import Generador
from TS.Entorno import Entorno
from TS.Simbolo import Simbolo
from Objeto.Primitivo import Primitivo
from Expresiones.Identificador import Identificador
from Instrucciones.Asignacion import Asignacion
from Instrucciones.Continue import Continue
from Abstract.NodoReporteArbol import NodoReporteArbol
from Instrucciones.Return import Return
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break

class ForCadena(NodoAST):
    def __init__(self, id, inicio,instrucciones, fila, columna):
        super().__init__(TIPO.CADENA, fila, columna)
        self.id = id
        self.inicio = inicio
        self.instrucciones = instrucciones

    def interpretar(self, entorno):
        nuevo_entorno = Entorno(entorno)
        nuevo_entorno.setEntorno("For")
        valor_inicio = self.inicio.interpretar(nuevo_entorno)
        aux = Generador()
        generador = aux.obtenerGen()
        generador.TSglobal.agregarTabla(nuevo_entorno)
        if(valor_inicio.tipo == TIPO.ERROR):
            generador.TSglobal.addExcepcion(valor_inicio)
            return valor_inicio;

        if valor_inicio.tipo == TIPO.CADENA:     
            if(valor_inicio.tipo == TIPO.ENTERO):
                generador.TSglobal.addExcepcion(Excepcion(TIPO.ERROR, f"No puede realizar este for con un entero",self.fila,self.columna))
                return  Excepcion(TIPO.ERROR, f"No puede realizar este for con un entero",self.fila,self.columna)
            if(valor_inicio.tipo == TIPO.DECIMAL):
                generador.TSglobal.addExcepcion(Excepcion(TIPO.ERROR, f"No puede realizar un for con un caracter",self.fila,self.columna))
                return  Excepcion(TIPO.ERROR, f"No puede realizar un for con un caracter",self.fila,self.columna)
            if(valor_inicio.tipo == TIPO.BOOLEANO):
                generador.TSglobal.addExcepcion(Excepcion(TIPO.ERROR, f"No puede realizar un for con un boolean",self.fila,self.columna))
                return  Excepcion(TIPO.ERROR, f"No puede realizar un for con un caracter",self.fila,self.columna)
            
            
            #asignar = Asignacion(self.id, self.inicio, None, self.fila, self.columna)
            #asignar.interpretar(nuevo_entorno)
            
            
            #temp_final = generador.agregarTemporal()
            #generador.agregarExpresion(temp_final,valor_final.valor,'','')
            
            # el primitivo me devuelve un temporal con la posicion en el heap
            #guardar = Identificador(self.id, self.fila, self.columna)
            #guardar_interpretar = guardar.interpretar(nuevo_entorno)
            
            simbolo = nuevo_entorno.guardarVariable(self.id, valor_inicio.tipo, False, False,None, self.fila, self.columna)
            heap = generador.agregarTemporal()
            #temp_inicio = guardar_interpretar.valor
            temp_inicio = valor_inicio.valor

            tmp = generador.agregarTemporal()
            generador.agregarExpresion(tmp,'P',simbolo.pos,'+')
            generador.guardar_stack(tmp,valor_inicio.valor)

            variable = nuevo_entorno.obtenerVariable(self.id)

            generador.agregarExpresion(tmp,'P',variable.pos,'+')
            generador.obtener_stack(heap,tmp)
            

            lbl_for = generador.agregarLabel()
            generador.colocarLbl(lbl_for)

            generador.obtener_heap(temp_inicio,heap)

            lbl_instrucciones = generador.agregarLabel()
            lbl_salida = generador.agregarLabel()
            lbl_incremento = generador.agregarLabel()
            generador.agregarIf(temp_inicio,'-1','!=',lbl_instrucciones)
            generador.agregarGoto(lbl_salida)
            
            nuevo_entorno.lbl_break = lbl_salida
            nuevo_entorno.lbl_continue = lbl_incremento
            
            generador.colocarLbl(lbl_instrucciones)
            generador.agregarExpresion(tmp,'P',variable.pos,'+')
            generador.guardar_stack(tmp,'H')
            generador.guardar_heap('H',temp_inicio)
            generador.agregarExpresion('H','H','1','+')
            generador.guardar_heap('H','-1')
            generador.agregarExpresion('H','H','1','+')
            for i in self.instrucciones:
                i.interpretar(nuevo_entorno)
            
            generador.agregarGoto(lbl_incremento)
            generador.colocarLbl(lbl_incremento)
            generador.agregarExpresion(heap,heap,'1','+')
            
            generador.obtener_heap(temp_inicio, heap)
            generador.agregarExpresion(tmp,'P',variable.pos,'+')
            generador.guardar_stack(tmp,heap)
            generador.agregarGoto(lbl_for)
            generador.colocarLbl(lbl_salida)



        else:
            if(valor_inicio.tipo == TIPO.ENTERO):
                generador.TSglobal.addExcepcion(Excepcion(TIPO.ERROR, f"No puede realizar este for con un entero",self.fila,self.columna))
                return  Excepcion(TIPO.ERROR, f"No puede realizar este for con un entero",self.fila,self.columna)
            if(valor_inicio.tipo == TIPO.DECIMAL):
                generador.TSglobal.addExcepcion(Excepcion(TIPO.ERROR, f"No puede realizar un for con un decimal",self.fila,self.columna))
                return  Excepcion(TIPO.ERROR, f"No puede realizar un for con un caracter",self.fila,self.columna)
            if(valor_inicio.tipo == TIPO.BOOLEANO):
                generador.TSglobal.addExcepcion(Excepcion(TIPO.ERROR, f"No puede realizar un for con un boolean",self.fila,self.columna))
                return  Excepcion(TIPO.ERROR, f"No puede realizar un for con un boolean",self.fila,self.columna)
            if(valor_inicio.tipo == TIPO.CHARACTER):
                generador.TSglobal.addExcepcion(Excepcion(TIPO.ERROR, f"No puede realizar un for con un caracter",self.fila,self.columna))
                return  Excepcion(TIPO.ERROR, f"No puede realizar un for con un caracter",self.fila,self.columna)

            aux = Generador()
            generador = aux.obtenerGen()
            #asignar = Asignacion(self.id, self.inicio, None, self.fila, self.columna)
            #asignar.interpretar(nuevo_entorno)
            
            
            #temp_final = generador.agregarTemporal()
            #generador.agregarExpresion(temp_final,valor_final.valor,'','')
            
            # el primitivo me devuelve un temporal con la posicion en el heap
            #guardar = Identificador(self.id, self.fila, self.columna)
            #guardar_interpretar = guardar.interpretar(nuevo_entorno)
            tipo_retorno = TIPO.ENTERO
            arreglo_enviar = valor_inicio.arreglo 
            if isinstance(valor_inicio.arreglo[0],list):
                tipo_retorno = TIPO.ARREGLO
                arreglo_enviar = valor_inicio.arreglo[0]
            else:
                tipo_retorno = valor_inicio.arreglo[0]
            generador.addComment('aca empieza el FOR EN ARREGLO')
            simbolo = nuevo_entorno.guardarVariable(self.id, tipo_retorno, False, False,arreglo_enviar, self.fila, self.columna)
            heap = generador.agregarTemporal()
            #temp_inicio = guardar_interpretar.valor
            temp_inicio = generador.agregarTemporal()
            generador.agregarExpresion(temp_inicio,'0','','')

            tmp = generador.agregarTemporal()
            generador.agregarExpresion(tmp,'P',simbolo.pos,'+')
            generador.guardar_stack(tmp,valor_inicio.valor)

            variable = nuevo_entorno.obtenerVariable(self.id)
            valor_final = generador.agregarTemporal()

            generador.agregarExpresion(tmp,'P',variable.pos,'+')
            generador.obtener_stack(heap,tmp)

            

            lbl_for = generador.agregarLabel()
            generador.obtener_heap(valor_final,heap) # aca obtengo el tama??o del vector
            generador.agregarExpresion(heap,heap,'1','+') # posicion 1 del arreglo
            #generador.guardar_stack(simbolo.pos,heap)

            valor_heap = generador.agregarTemporal()
            generador.obtener_heap(valor_heap,heap)
            generador.agregarExpresion(tmp,'P',variable.pos,'+')
            generador.guardar_stack(tmp,valor_heap)
            

            
            generador.colocarLbl(lbl_for)


            
            lbl_instrucciones = generador.agregarLabel()
            lbl_salida = generador.agregarLabel()
            lbl_incremento = generador.agregarLabel()
            
            generador.agregarIf(temp_inicio,valor_final,'<',lbl_instrucciones)
            generador.agregarGoto(lbl_salida)
            
            nuevo_entorno.lbl_break = lbl_salida
            nuevo_entorno.lbl_continue = lbl_incremento

            '''valor_heap = generador.agregarTemporal()
            generador.obtener_heap(valor_heap,heap)
            generador.guardar_stack(variable.pos,valor_heap)
            generador.agregarExpresion(heap,heap,'1','+')'''

            generador.colocarLbl(lbl_instrucciones)
            
            for i in self.instrucciones:
                i.interpretar(nuevo_entorno)
            
            generador.agregarGoto(lbl_incremento)
            generador.colocarLbl(lbl_incremento)
            generador.agregarExpresion(temp_inicio,temp_inicio,'1','+')
            generador.agregarExpresion(heap,heap,'1','+')
            generador.obtener_heap(valor_heap,heap)
            obtengo = generador.agregarTemporal()
            generador.agregarExpresion(obtengo,'P',variable.pos,'+')
            generador.guardar_stack(obtengo,valor_heap)
            #generador.guardar_stack(variable.pos,heap)
            generador.agregarGoto(lbl_for)
            generador.colocarLbl(lbl_salida)



    def getNodo(self):
        
            nodo = NodoReporteArbol("FOR")
            nodo.agregarHijoCadena("for")
            nodo.agregarHijoCadena(self.id)
            nodo.agregarHijoCadena("in")
            nodo.agregarHijoNodo(self.inicio.getNodo())
            instrucciones = NodoReporteArbol("INSTRUCCIONES")
            unaVez = True
            for instr in self.instrucciones:
                if unaVez:
                    nuevo1 = NodoReporteArbol("INSTRUCCION")
                    nuevo1.agregarHijoNodo(instr.getNodo())
                    #nuevo1.agregarHijoCadena(";")
                    instrucciones.agregarHijoNodo(nuevo1)
                else:
                    n = instrucciones
                    nuevo1 = NodoReporteArbol("INSTRUCCION")
                    instrucciones = NodoReporteArbol("INSTRUCCIONES")
                    instrucciones.agregarHijoNodo(n)
                    nuevo1.agregarHijoNodo(instr.getNodo())
                    #nuevo1.agregarHijoCadena(";")
                    instrucciones.agregarHijoNodo(nuevo1)
                unaVez = False
            nodo.agregarHijoNodo(instrucciones)
            nodo.agregarHijoCadena("end")
            nodo.agregarHijoCadena(";")
            return nodo
    