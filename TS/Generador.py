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
        ret = '/*----HEADER----*/\npackage main;\n\nimport (\n\t"fmt"\n)\n\n'
        if len(self.temporales) > 0:
            ret += 'var '
            for temp in range(len(self.temporales)):
                ret += self.temporales[temp]
                if temp != (len(self.temporales) - 1):
                    ret += ", "
            ret += " float64\n"
        ret += "var P, H float64;\nvar stack [10000]float64;\nvar heap [10000]float64;\n\n"
        return ret

    def getCode(self):
        return f'{self.getHeader()}{self.nativas}\n{self.funciones}\nfunc main(){{\n        P = 0;\n        H = 0;\n{self.codigo}\n}}'

    def agregarCodigo(self, codigo):
        if(self.es_nativa):
            if(self.nativas == ''):
                self.nativas = self.nativas + '/*-----NATIVES-----*/\n'
            self.nativas = self.nativas + '\t' + codigo
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

    ########################
    # Manejo de Temporales
    ########################
    def agregarTemporal(self):
        temp = f't{self.countTemp}'
        self.countTemp += 1
        self.temporales.append(temp)
        return temp

    #####################
    # Manejo de Labels
    #####################
    def agregarLabel(self):
        label = f'L{self.countLabel}'
        self.countLabel += 1
        return label

    def colocarLbl(self, label):
        self.agregarCodigo(f'{label}:\n')

    ###################
    # GOTO
    ###################
    def agregarGoto(self, label):
        self.agregarCodigo(f'goto {label};\n')
    
    ###################
    # IF
    ###################
    def agregarIf(self, left, right, op, label):
        self.agregarCodigo(f'if {left} {op} {right} {{goto {label};}}\n')

    ###################
    # EXPRESIONES
    ###################
    def agregarExpresion(self, result, left, right, op):
        self.agregarCodigo(f'{result}={left}{op}{right};\n')
    
    ###################
    # FUNCS
    ###################
    def addBeginFunc(self, id):
        if(not self.es_nativa):
            self.es_funcion = True
        self.agregarCodigo(f'func {id}(){{\n')
    
    def addEndFunc(self):
        self.agregarCodigo('\n}\n');
        if(not self.es_nativa):
            self.es_funcion = False

    ###############
    # STACK
    ###############
    def setStack(self, pos, value):
        self.agregarCodigo(f'stack[int({pos})]={value};\n')
    
    def getStack(self, place, pos):
        self.agregarCodigo(f'{place}=stack[int({pos})];\n')

    #############
    # ENVS
    #############
    def newEnv(self, size):
        self.agregarCodigo(f'P=P+{size};\n')

    def callFun(self, id):
        self.agregarCodigo(f'{id}();\n')

    def retEnv(self, size):
        self.agregarCodigo(f'P=P-{size};\n')

    ###############
    # HEAP
    ###############
    def guardar_heap(self, pos, value):
        self.agregarCodigo(f'heap[int({pos})]={value};\n')

    def obtener_heap(self, place, pos):
        self.agregarCodigo(f'{place}=heap[int({pos})];\n')

    def sumar_heap(self):
        self.agregarCodigo('H=H+1;\n')

    # INSTRUCCIONES
    def agregarPrint(self, type, value):
        if type == 'd':
            self.agregarCodigo(f'fmt.Printf("%{type}", int({value}));\n')
        elif type == 'g':
            self.agregarCodigo(f'fmt.Printf("%{type}", float64({value}));\n')
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
    
    ##############
    # NATIVES
    ##############
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

        self.getStack(tempH, tempP)

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
        self.getStack(base, posicion_base) # aca ya tengo la base

        posicion_exponente = self.agregarTemporal() #indice exponente
        self.agregarExpresion(posicion_exponente,'P','2','+')
        exponente = self.agregarTemporal()
        self.getStack(exponente, posicion_exponente) #aca ya tengo al exponente
        
        contador = self.agregarTemporal()
        self.agregarExpresion(contador,'1','','') #inicio el contador
        self.agregarIf(exponente,'0','==',lblCero) #if si el exponente es 0
        self.agregarGoto(lblWhile) #lbl del while
        self.colocarLbl(lblCero)
        self.agregarExpresion(base,'0','','') #se devuelve un cero
        self.agregarExpresion(contador,contador,'1','+')#inicio contador

        self.colocarLbl(lblWhile) #empieza el while
        self.agregarIf(contador, exponente, '==', lblSalida)
        self.agregarExpresion(base,base,base,'*')
        self.agregarExpresion(contador,contador,'1','+')
        self.agregarGoto(lblWhile)

        self.colocarLbl(lblSalida)
        self.setStack('P',base)
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
        self.getStack(primer_apuntador,posicion_primera) #se obtiene la referencia al heap de la primera cadena

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
        self.getStack(segundo_apuntador,posicion_segunda) #se obtiene la referencia al heap de la segunda cadena

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
        self.setStack('P',inicio_nueva)
        self.addEndFunc()
        self.es_nativa = False