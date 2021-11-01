from re import S
from .Entorno import Entorno

class Generador:
    generador = None
    def __init__(self):
        # Contadores
        self.countTemp = 0
        self.countLabel = 0
        # Code
        self.codigo = ''
        self.funciones = ''
        self.nativas = ''
        self.es_funcion = False
        self.es_nativa = False
        # Lista de Temporales
        self.temporales = []
        # Lista de Nativas
        self.printString = False
        self.potencia = False
        self.concat = False
        self.potenciaString = False
        self.compStrings = False
        self.parseInt = False
        self.parseFloat = False
        self.toUpper = False
        self.toLower = False
        self.trunc = False
        self.mod = False

    def cleanAll(self):
        # Contadores
        self.countTemp = 0
        self.countLabel = 0
        # Code
        self.codigo = ''
        self.funciones = ''
        self.nativas = ''
        self.es_funcion = False
        self.es_nativa = False
        # Lista de Temporales
        self.temporales = []
        # Lista de Nativas
        self.printString = False
        Generador.generador = Generador()
    
    #############
    # CODE
    #############
    def getHeader(self):
        if self.mod:
            ret = '/*----HEADER----*/\npackage main;\n\nimport (\n\t"fmt"\n\t"math"\n)\n\n'
            self.mod = False
        else:
            ret = '/*----HEADER----*/\npackage main;\n\nimport (\n\t"fmt"\n)\n\n'
        if len(self.temporales) > 0:
            ret += 'var '
            for temp in range(len(self.temporales)):
                ret += self.temporales[temp]
                if temp != (len(self.temporales) - 1):
                    ret += ", "
            ret += " float64;\n"
        ret += "var P, H float64;\nvar stack [10000]float64;\nvar heap [10000]float64;\n\n"
        return ret

    def getCode(self):
        return f'{self.getHeader()}{self.nativas}\n{self.funciones}\nfunc main(){{\n        P = 0;\n        H = 0;\n{self.codigo}\n}}'

    def agregarCodigo(self, codigo):
        if(self.es_nativa):
            if(self.nativas == ''):
                self.nativas = self.nativas + '/*-----NATIVES-----*/\n'
            self.nativas = self.nativas + codigo
        elif(self.es_funcion):
            if(self.funciones == ''):
                self.funciones = self.funciones + '/*-----FUNCS-----*/\n'
            self.funciones = self.funciones + '\t' +  codigo
        else:
            self.codigo = self.codigo + '\t' +  codigo

    def addComment(self, comment):
        self.agregarCodigo(f'/* {comment} */\n')
    
    def obtenerGen(self):
        if Generador.generador == None:
            Generador.generador = Generador()
        return Generador.generador

    def addSpace(self):
        self.agregarCodigo("\n")

    def agregarTemporal(self):
        temp = f't{self.countTemp}'
        self.countTemp += 1             
        self.temporales.append(temp)
        return temp

    def agregarLabel(self):
        label = f'L{self.countLabel}'
        self.countLabel += 1
        return label

    def colocarLbl(self, label):
        self.agregarCodigo(f'{label}:\n')

    def agregarGoto(self, label):
        self.agregarCodigo(f'goto {label};\n')
    
    def agregarIf(self, left, right, op, label):
        self.agregarCodigo(f'if {left} {op} {right} {{goto {label};}}\n')

    def agregarExpresion(self, result, left, right, op):
        self.agregarCodigo(f'{result}={left}{op}{right};\n')
    
    def addBeginFunc(self, id):
        if(not self.es_nativa):
            self.es_funcion = True
        self.agregarCodigo(f'func {id}(){{\n')
    
    def addEndFunc(self):
        self.agregarCodigo('\n}\n');
        if(not self.es_nativa):
            self.es_funcion = False

    def guardar_stack(self, pos, value):
        self.agregarCodigo(f'stack[int({pos})]={value};\n')
    
    def obtener_stack(self, place, pos):
        self.agregarCodigo(f'{place}=stack[int({pos})];\n')

    
    def newEnv(self, size):
        self.agregarCodigo(f'P=P+{size};\n')

    def callFun(self, id):
        self.agregarCodigo(f'{id}();\n')

    def retEnv(self, size):
        self.agregarCodigo(f'P=P-{size};\n')

    def guardar_heap(self, pos, value):
        self.agregarCodigo(f'heap[int({pos})]={value};\n')

    def obtener_heap(self, place, pos):
        self.agregarCodigo(f'{place}=heap[int({pos})];\n')

    def sumar_heap(self):
        self.agregarCodigo('H=H+1;\n')

    def modulo(self,temporal,pos1,pos2):
        self.agregarCodigo(f'{temporal}=math.Mod({pos1},{pos2});\n')



    # INSTRUCCIONES
    def agregarPrint(self, type, value):
        if type == 'd':
            self.agregarCodigo(f'fmt.Printf("%{type}", int({value}));\n')
        elif type == 'f':
            self.agregarCodigo(f'fmt.Printf("%{type}", {value});\n')
        elif type == 'c':
            self.agregarCodigo(f'fmt.Printf("%{type}", int({value}));\n')
    
    def printTrue(self):
        self.agregarPrint("c", 116)
        self.agregarPrint("c", 114)
        self.agregarPrint("c", 117)
        self.agregarPrint("c", 101)

    def printFalse(self):
        self.agregarPrint("c", 102)
        self.agregarPrint("c", 97)
        self.agregarPrint("c", 108)
        self.agregarPrint("c", 115)
        self.agregarPrint("c", 101)
    
    def fPrintString(self):
        if(self.printString):
            return
        self.printString = True
        self.es_nativa = True

        self.addBeginFunc('printString')
        # Label para salir de la funcion
        returnLbl = self.agregarLabel()
        # Label para la comparacion para buscar fin de cadena
        compareLbl = self.agregarLabel()

        # Temporal puntero a Stack
        tempP = self.agregarTemporal()

        # Temporal puntero a Heap
        tempH = self.agregarTemporal()

        self.agregarExpresion(tempP, 'P', '1', '+')

        self.obtener_stack(tempH, tempP)

        # Temporal para comparar
        tempC = self.agregarTemporal()

        self.colocarLbl(compareLbl)

        self.obtener_heap(tempC, tempH)

        self.agregarIf(tempC, '-1', '==', returnLbl)

        self.agregarPrint('c', tempC)

        self.agregarExpresion(tempH, tempH, '1', '+')

        self.agregarGoto(compareLbl)

        self.colocarLbl(returnLbl)
        self.addEndFunc()
        self.es_nativa = False

    def funcPotencia(self):
        if (self.potencia):
            return
        self.potencia = True
        self.es_nativa = True
        self.addBeginFunc('potencia')
        lblCero = self.agregarLabel() #label para cuando el exponente es 0
        lblWhile = self.agregarLabel() #label para el ciclo
        lblSalida = self.agregarLabel() #label para la salida
        posicion_base = self.agregarTemporal() 
        self.agregarExpresion(posicion_base,'P','1','+') #Indice base
        base = self.agregarTemporal()
        self.obtener_stack(base, posicion_base) # aca ya tengo la base

        posicion_exponente = self.agregarTemporal() #indice exponente
        self.agregarExpresion(posicion_exponente,'P','2','+')
        exponente = self.agregarTemporal()
        self.obtener_stack(exponente, posicion_exponente) #aca ya tengo al exponente
        
        contador = self.agregarTemporal()
        self.agregarExpresion(contador,'1','','') #inicio el contador
        self.agregarIf(exponente,'0','==',lblCero) #if si el exponente es 0
        self.agregarGoto(lblWhile) #lbl del while
        self.colocarLbl(lblCero)
        self.agregarExpresion(base,'1','','') #se devuelve un cero
        self.agregarExpresion(contador,contador,'1','+')#inicio contador
        self.agregarGoto(lblSalida)
        self.colocarLbl(lblWhile) #empieza el while
        self.agregarIf(contador, exponente, '==', lblSalida)
        self.agregarExpresion(base,base,base,'*')
        self.agregarExpresion(contador,contador,'1','+')
        self.agregarGoto(lblWhile)

        self.colocarLbl(lblSalida)
        self.guardar_stack('P',base)
        self.addEndFunc()
        self.es_nativa = False
    
    def funConcat(self):
        if (self.concat):
            return
        self.concat = True
        self.es_nativa = True
        self.addBeginFunc('concatenar')
        lbl_salida = self.agregarLabel()
        inicio_nueva = self.agregarTemporal() 
        self.agregarExpresion(inicio_nueva, 'H','','') #Guardo la posicion inidial de la nueva cadena a formar
        posicion_primera = self.agregarTemporal()
        self.agregarExpresion(posicion_primera,'P','1','+') #Obtengo la posicion inicial de la cadena 1
        primer_apuntador = self.agregarTemporal() 
        self.obtener_stack(primer_apuntador,posicion_primera) #se obtiene la referencia al heap de la primera cadena

        primer_while = self.agregarLabel()
        lbl_siguiente = self.agregarLabel() #cuando termina de recorrer la primera cadena
        self.colocarLbl(primer_while)
        primera_cadena = self.agregarTemporal() #temporal para el manejo del heap de la primera cadena
        self.obtener_heap(primera_cadena,primer_apuntador)

        self.agregarIf(primera_cadena,'-1','==',lbl_siguiente)
        self.guardar_heap('H',primera_cadena)
        self.agregarExpresion('H','H','1','+') 
        self.agregarExpresion(primer_apuntador,primer_apuntador,'1','+') #moviendo la referencia al heap
        self.agregarGoto(primer_while)

        self.colocarLbl(lbl_siguiente)
        posicion_segunda = self.agregarTemporal()
        self.agregarExpresion(posicion_segunda,'P','2','+') #Obtengo la posicion inicial de la cadena 2
        segundo_apuntador = self.agregarTemporal()
        self.obtener_stack(segundo_apuntador,posicion_segunda) #se obtiene la referencia al heap de la segunda cadena

        segundo_while = self.agregarLabel()
        self.colocarLbl(segundo_while)
        segunda_cadena = self.agregarTemporal()
        self.obtener_heap(segunda_cadena,segundo_apuntador)
        
        self.agregarIf(segunda_cadena,'-1','==',lbl_salida)
        self.guardar_heap('H',segunda_cadena)
        self.agregarExpresion('H','H','1','+')
        self.agregarExpresion(segundo_apuntador,segundo_apuntador,'1','+')
        self.agregarGoto(segundo_while)
        self.colocarLbl(lbl_salida)
        self.guardar_heap('H','-1')
        self.agregarExpresion('H','H','1','+')
        self.guardar_stack('P',inicio_nueva)
        self.addEndFunc()
        self.es_nativa = False
    
    def funcPotenciaString(self):
        if (self.potenciaString):
            return
        self.potenciaString = True
        self.es_nativa = True
        self.addBeginFunc('potenciaString')
        
        apuntador_palabra = self.agregarTemporal() 
        self.agregarExpresion(apuntador_palabra,'P','1','+')
        palabra = self.agregarTemporal()
        self.obtener_stack(palabra,apuntador_palabra) #palabra base

        apuntador_exponente = self.agregarTemporal()
        self.agregarExpresion(apuntador_exponente,'P','2','+')
        exponente = self.agregarTemporal()
        self.obtener_stack(exponente,apuntador_exponente)  #exponente 

        contador = self.agregarTemporal() #contador para el evaluar cuantas veces se hace el ciclo
        self.agregarExpresion(contador,'0','','')

        inicio_nueva = self.agregarTemporal() #se guarda la posicion donde estara la nueva palabra
        self.agregarExpresion(inicio_nueva,'H','','')

        pivote = self.agregarTemporal()
        self.agregarExpresion(pivote,palabra,'','') #pivote para moverse en el heap 

        lbl_while1 = self.agregarLabel()
        lbl_while2 = self.agregarLabel() #Labels para los whiles y la salida
        lbl_salida = self.agregarLabel()

        self.colocarLbl(lbl_while1)
        self.agregarIf(exponente,contador,'==',lbl_salida) #if para saber si ya se hizo la potencia la cantidad necesaria
        self.agregarExpresion(contador,contador,'1','+')
        self.agregarExpresion(pivote,palabra,'','')
        self.colocarLbl(lbl_while2)
        pivote_nueva = self.agregarTemporal()
        self.obtener_heap(pivote_nueva,pivote)
        self.agregarExpresion(pivote,pivote,'1','+')

        self.agregarIf(pivote_nueva,'-1','==',lbl_while1)
        self.guardar_heap('H',pivote_nueva)
        self.agregarExpresion('H','H','1','+')
        self.agregarGoto(lbl_while2)

        self.colocarLbl(lbl_salida)
        self.guardar_heap('H','-1')
        self.agregarExpresion('H','H','1','+')
        self.guardar_stack('P',inicio_nueva)

        self.addEndFunc()
        self.es_nativa = False

    def funCompararStrings(self):
        if (self.compStrings):
            return
        self.compStrings = True
        self.es_nativa = True
        self.addBeginFunc('compararStrings')

        primer_apuntador = self.agregarTemporal()
        self.agregarExpresion(primer_apuntador,'P','1','+')
        primer_pivote = self.agregarTemporal() #referencia de la primera palabra en el heap
        self.obtener_stack(primer_pivote,primer_apuntador) #pivote primera palabra
        
        segundo_apuntador = self.agregarTemporal()
        self.agregarExpresion(segundo_apuntador,'P','2','+')
        segundo_pivote = self.agregarTemporal() #referencia de la segunda palabra en el heap
        self.obtener_stack(segundo_pivote,segundo_apuntador) #pivote segunda palabra

        lbl_while = self.agregarLabel()
        lbl_true = self.agregarLabel()
        lbl_false = self.agregarLabel() #generamos los labels necesarios
        lbl_salida = self.agregarLabel()

        self.colocarLbl(lbl_while)
        primera_palabra = self.agregarTemporal()
        segunda_palabra = self.agregarTemporal()
        
        self.obtener_heap(primera_palabra,primer_pivote)
        self.obtener_heap(segunda_palabra,segundo_pivote)
        
        self.agregarIf(primera_palabra,segunda_palabra,'!=',lbl_false)
        self.agregarIf(segunda_palabra,'-1','!=',lbl_true)

        self.agregarExpresion(primer_pivote,primer_pivote,'1','+')
        self.agregarExpresion(segundo_pivote,segundo_pivote,'1','+')

        self.agregarGoto(lbl_while)
        self.colocarLbl(lbl_true)
        self.guardar_stack('P','1')
        self.agregarGoto(lbl_salida)
        self.colocarLbl(lbl_false)
        self.guardar_stack('P','0')
        self.colocarLbl(lbl_salida)

        self.addEndFunc()
        self.es_nativa = False

    def funParseInt(self):
        if (self.parseInt):
            return
        self.parseInt = True
        self.es_nativa = True
        self.addBeginFunc('parseInt')

        resultado = self.agregarTemporal()
        self.agregarExpresion(resultado,'0','','')
        referencia = self.agregarTemporal()
        self.agregarExpresion(referencia,'P','1','+')
        heap = self.agregarTemporal()
        self.obtener_stack(heap,referencia)

        lbl_while = self.agregarLabel()
        salida = self.agregarLabel()
        
        self.colocarLbl(lbl_while)
        letra = self.agregarTemporal()
        self.obtener_heap(letra,heap)
        self.agregarIf(letra,'-1','==',salida)
        self.agregarExpresion(resultado,resultado,'10','*')
        resta = self.agregarTemporal()
        self.agregarExpresion(resta,letra,'48','-')
        self.agregarExpresion(resultado,resultado,resta,'+')
        self.agregarExpresion(heap,heap,'1','+')
        self.agregarGoto(lbl_while)

        self.colocarLbl(salida)
        self.guardar_stack('P',resultado)

        self.addEndFunc()
        self.es_nativa = False

    def funParseFloat(self):
        if (self.parseFloat):
            return
        self.parseFloat = True
        self.es_nativa = True
        self.addBeginFunc('parseFloat')

        resultado = self.agregarTemporal()
        decimales = self.agregarTemporal()
        division_decimal = self.agregarTemporal()
        contador_decimal = self.agregarTemporal()
        #multiplica = self.agregarTemporal()
        divide = self.agregarTemporal()
        referencia = self.agregarTemporal()
        heap = self.agregarTemporal()

        primer_while = self.agregarLabel()
        segundo_while = self.agregarLabel()
        salida = self.agregarLabel()

        self.agregarExpresion(resultado,'0','','')
        self.agregarExpresion(decimales,'0','','')
        self.agregarExpresion(division_decimal,'0','','')
        self.agregarExpresion(contador_decimal,'0','','')
        #self.agregarExpresion(multiplica,'0','','')
        self.agregarExpresion(divide,'1','','')
        self.agregarExpresion(referencia,'P','1','+')
        self.obtener_stack(heap,referencia)

        self.colocarLbl(primer_while)
        valor_heap = self.agregarTemporal()
        self.obtener_heap(valor_heap,heap)
        self.agregarIf(valor_heap,'-1','==',salida)
        self.agregarIf(valor_heap,'46','==',segundo_while)

        self.agregarExpresion(resultado,resultado,'10','*')
        resta = self.agregarTemporal()
        self.agregarExpresion(resta,valor_heap,'48','-')
        self.agregarExpresion(resultado,resultado,resta,'+')
        self.agregarExpresion(heap,heap,'1','+')
        self.agregarGoto(primer_while)

        self.colocarLbl(segundo_while)
        self.agregarExpresion(heap,heap,'1','+')
        self.obtener_heap(valor_heap,heap)
        self.agregarIf(valor_heap,'-1','==',salida)
        resta_dos = self.agregarTemporal()
        self.agregarExpresion(resta_dos,valor_heap,'48','-')
        self.agregarExpresion(divide,divide,'10','*')
        self.agregarExpresion(division_decimal,resta_dos,divide,'/')
        self.agregarExpresion(decimales,decimales,division_decimal,'+')
        self.agregarExpresion(contador_decimal,contador_decimal,'1','+')
        self.agregarGoto(segundo_while)

        self.colocarLbl(salida)
        self.agregarExpresion(resultado,resultado,decimales,'+')
        self.guardar_stack('P',resultado)

        self.addEndFunc()
        self.es_nativa = False

    def funToUpper(self):
        if (self.toUpper):
            return
        self.toUpper = True
        self.es_nativa = True
        self.addBeginFunc('toUpper')

        referencia = self.agregarTemporal()
        self.agregarExpresion(referencia,'P','1','+')
        heap = self.agregarTemporal()
        self.obtener_stack(heap,referencia)

        lbl_while = self.agregarLabel()
        lbl_incremento = self.agregarLabel()
        salida = self.agregarLabel()

        self.colocarLbl(lbl_while)
        valor_heap = self.agregarTemporal()
        self.obtener_heap(valor_heap,heap)
        self.agregarIf(valor_heap,'-1','==',salida)
        self.agregarIf(valor_heap,'96','<=',lbl_incremento)
        self.agregarIf(valor_heap,'123','>=',lbl_incremento)
        letra = self.agregarTemporal()
        self.agregarExpresion(letra,valor_heap,'32','-')
        self.guardar_heap(heap,letra)
        self.colocarLbl(lbl_incremento)
        self.agregarExpresion(heap,heap,'1','+')
        self.agregarGoto(lbl_while)
        self.colocarLbl(salida)

        self.addEndFunc()
        self.es_nativa = False

    def funToLower(self):
        if (self.toLower):
            return
        self.toLower = True
        self.es_nativa = True
        self.addBeginFunc('toLower')

        referencia = self.agregarTemporal()
        self.agregarExpresion(referencia,'P','1','+')
        heap = self.agregarTemporal()
        self.obtener_stack(heap,referencia)

        lbl_while = self.agregarLabel()
        lbl_incremento = self.agregarLabel()
        salida = self.agregarLabel()

        self.colocarLbl(lbl_while)
        valor_heap = self.agregarTemporal()
        self.obtener_heap(valor_heap,heap)
        self.agregarIf(valor_heap,'-1','==',salida)
        self.agregarIf(valor_heap,'64','<=',lbl_incremento)
        self.agregarIf(valor_heap,'91','>=',lbl_incremento)
        letra = self.agregarTemporal()
        self.agregarExpresion(letra,valor_heap,'32','+')
        self.guardar_heap(heap,letra)
        self.colocarLbl(lbl_incremento)
        self.agregarExpresion(heap,heap,'1','+')
        self.agregarGoto(lbl_while)
        self.colocarLbl(salida)

        self.addEndFunc()
        self.es_nativa = False

    def funcTrunc(self):
        if (self.trunc):
            return
        self.trunc = True
        self.es_nativa = True
        self.addBeginFunc('trunc')

        referencia = self.agregarTemporal()
        self.agregarExpresion(referencia,'P','1','+')
        stack = self.agregarTemporal()
        self.obtener_stack(stack,referencia)

        negativo = self.agregarLabel()
        salida = self.agregarLabel()

        self.agregarIf(stack,'0','<',negativo)
        modulo = self.agregarTemporal()
        self.modulo(modulo,stack,'1')
        #self.agregarExpresion(stack,stack,modulo,'-')
        self.agregarGoto(salida)

        self.colocarLbl(negativo)
        self.modulo(modulo,stack,'-1')
        #self.agregarExpresion(stack,stack,modulo,'-')
        self.colocarLbl(salida)
        self.agregarExpresion(stack,stack,modulo,'-')
        self.guardar_stack('P',stack)

        self.addEndFunc()
        self.es_nativa = False