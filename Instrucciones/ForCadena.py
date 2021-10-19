from re import template
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
        valor_inicio = self.inicio.interpretar(nuevo_entorno)
        print(valor_inicio)
        if(valor_inicio.tipo == TIPO.ERROR):
            #tree.addExcepcion(valor_inicio)
            return valor_inicio;

        if valor_inicio.tipo == TIPO.CADENA:     
            if(valor_inicio.tipo == TIPO.ENTERO):
                #tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede realizar este for con un entero",self.fila,self.columna))
                return  Excepcion(TIPO.ERROR, f"No puede realizar este for con un entero",self.fila,self.columna)
            if(valor_inicio.tipo == TIPO.DECIMAL):
                #tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede realizar un for con un caracter",self.fila,self.columna))
                return  Excepcion(TIPO.ERROR, f"No puede realizar un for con un caracter",self.fila,self.columna)
            if(valor_inicio.tipo == TIPO.BOOLEANO):
                #tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede realizar un for con un boolean",self.fila,self.columna))
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
            
            simbolo = nuevo_entorno.guardarVariable(self.id, valor_inicio.tipo, True, False)
            heap = generador.agregarTemporal()
            #temp_inicio = guardar_interpretar.valor
            temp_inicio = valor_inicio.valor
            generador.guardar_stack(simbolo.pos,valor_inicio.valor)
            variable = nuevo_entorno.obtenerVariable(self.id)

            generador.obtener_stack(heap,variable.pos)
            

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
            generador.guardar_stack(variable.pos,'H')
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
            generador.guardar_stack(variable.pos,heap)
            generador.agregarGoto(lbl_for)
            generador.colocarLbl(lbl_salida)



        else:
            if(valor_inicio.tipo == TIPO.ENTERO):
                #tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede realizar este for con un entero",self.fila,self.columna))
                return  Excepcion(TIPO.ERROR, f"No puede realizar este for con un entero",self.fila,self.columna)
            if(valor_inicio.tipo == TIPO.DECIMAL):
                #tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede realizar un for con un decimal",self.fila,self.columna))
                return  Excepcion(TIPO.ERROR, f"No puede realizar un for con un caracter",self.fila,self.columna)
            if(valor_inicio.tipo == TIPO.BOOLEANO):
                #tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede realizar un for con un boolean",self.fila,self.columna))
                return  Excepcion(TIPO.ERROR, f"No puede realizar un for con un boolean",self.fila,self.columna)
            if(valor_inicio.tipo == TIPO.CHARACTER):
                #tree.addExcepcion(Excepcion(TIPO.ERROR, f"No puede realizar un for con un caracter",self.fila,self.columna))
                return  Excepcion(TIPO.ERROR, f"No puede realizar un for con un caracter",self.fila,self.columna)

            '''valor_final = len(valor_inicio.valor)
            primer_valor = valor_inicio.valor[0].interpretar(tree,table)
            asignar = Asignacion(self.id, Primitivo(primer_valor.tipo, self.fila, self.columna, primer_valor.valor), None, self.fila, self.columna)
            asignar.interpretar(tree, nueva_tabla)
            iterador = 0
            condicion = True
            while iterador < valor_final:
                tabla_for = TablaSimbolos(nueva_tabla)
                tabla_for.setEntorno("For")
                tree.agregarTabla(tabla_for)
                for i in self.instrucciones:
                    if isinstance(i, Excepcion):
                        tree.updateConsola(i.toString())
                        tree.addExcepcion(i)
                        continue
                    result = i.interpretar(tree, tabla_for)
                    if isinstance(result, Excepcion):
                        tree.updateConsola(result.toString())
                        tree.addExcepcion(result)
                        continue
                    if isinstance(result, Break):
                        condicion = False
                        break
                    if isinstance(result, Continue):
                        break
                    if isinstance(result, Return):
                        return result
                if condicion == False:
                    condicion = True
                    break
                iterador += 1
                if iterador != valor_final:
                    inter = valor_inicio.valor[iterador].interpretar(tree, table)
                    simbolo = Simbolo(self.id, self.fila, self.columna, Primitivo(inter.tipo, self.fila, self.columna, inter.valor))
                    tabla_for.actualizarTabla(simbolo)'''

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
    