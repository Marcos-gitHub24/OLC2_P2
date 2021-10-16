# --------------------
# Marcos García
# --------------------

from Abstract.NodoReporteArbol import NodoReporteArbol
from Instrucciones.llamadaIntermedia import LlamadaIntermedia
from Instrucciones.Continue import Continue
from TS.Entorno import Entorno
from TS.Generador import Generador
import os
import re
from TS.Excepcion import Excepcion
import sys
grafo = "simon"
c = 0
sys.setrecursionlimit(3000)

errores = []
reservadas = {
    'print'   : 'RPRINT',
    'println' : 'RPRINTLN',
    'if'        : 'RIF',
    'else'      : 'RELSE',
    'elseif'    : 'RELSEIF',
    'end'       : 'REND',
    'while'     : 'RWHILE',
    'for'       : 'RFOR',
    'in'        : 'RIN',
    'true'      : 'RTRUE',
    'false'     : 'RFALSE',
    'break'     : 'RBREAK',
    'continue'  : 'RCONTINUE',
    'function'  : 'RFUNC',
    'return'    : 'RRETURN',
    'log10'     : 'RLOG10',
    'log'       : 'RLOG',
    'sin'       : 'RSIN',
    'cos'       : 'RCOS',
    'tan'       : 'RTAN',
    'sqrt'      : 'RSQRT',
    'uppercase' : 'RUPPER',
    'lowercase' : 'RLOWER',
    'Int64'     : 'RINT',
    'Float64'   : 'RFLOAT',
    'String'    : 'RSTRING',
    'Bool'      : 'RBOOL',
    'Char'      : 'RCHAR',
    'parse'     : 'RPARSE',
    'trunc'     : 'RTRUNC',
    'float'     : 'RFFLOAT',
    'string'    : 'RSSTRING',
    'typeof'    : 'RTYPEOF',
    'push'      : 'RPUSH',
    'pop'       : 'RPOP',
    'length'    : 'RLENGTH',
    'struct'    : 'RSTRUCT',
    'mutable'   : 'RMUTABLE',
    'nothing'   : 'RNOTHING',
    'global'    : 'RGLOBAL'

}

tokens  = [
    'PUNTOCOMA',
    'PUNTO',
    'DOSPUNTOS',
    'INTERROGACION',
    'NOT',
    'DIFERENTE',
    'PARA',
    'PARC',
    'CORA',
    'CORC',
    'LLAVEA',
    'LLAVEC',
    'COMA',
    'MAS',
    'MENOS',
    'DIVISION',
    'POTENCIA',
    'POR',
    'MODULO',
    'MENORQUE',
    'MENORIGUAL',
    'MAYORQUE',
    'MAYORIGUAL',
    'IGUALIGUAL',
    'IGUAL',
    'AND',
    'OR',
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'CARACTER',
    'ID'
] + list(reservadas.values())

# Tokens
t_PUNTOCOMA     = r';'
t_PUNTO         = r'\.'
t_PARA          = r'\('
t_PARC          = r'\)'
t_LLAVEA        = r'{'
t_CORA          = r'\['
t_CORC          = r'\]'
t_LLAVEC        = r'}'
t_COMA          = r','
t_MAS           = r'\+'
t_MENOS         = r'-'
t_DIVISION      = r'/'
t_POTENCIA      = r'\^'
t_POR           = r'\*'
t_MODULO        = r'%'
t_MENORQUE      = r'<'
t_MENORIGUAL    = r'<='
t_MAYORQUE      = r'>'
t_MAYORIGUAL    = r'>='
t_IGUALIGUAL    = r'=='
t_IGUAL         = r'='
t_AND           = r'&&'
t_OR            = r'\|\|'
t_DOSPUNTOS     = r':'
t_INTERROGACION = r'\?'
t_DIFERENTE     = r'!='
t_NOT           = r'!'



def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_ID(t):
     r'[a-zA-Z][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value, 'ID')
     return t

def t_CADENA(t):
    r'(\".*?\")'
    t.value = t.value[1:-1] # remuevo las comillas
    return t

def t_CARACTER(t):
    r'(\'.?\')'
    t.value = t.value[1:-1] # remuevo las comillas
    return t
def t_COMENTARIO_MULTILINEA(t):
    r'\#\=(.|\n)*?\=\#'
    t.lexer.lineno += t.value.count('\n')

# Comentario simple // ...
def t_COMENTARIO_SIMPLE(t):
    r'\#.*\n'
    t.lexer.lineno += 1

# Caracteres ignorados
t_ignore = " \t\r"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    errores.append(Excepcion("Lexico","Error léxico: " + t.value[0] , t.lexer.lineno, find_column(input, t)))
    t.lexer.skip(1)

# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(inp, token):
    line_start = inp.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

# Construyendo el analizador léxico
import ply.lex as lex
lexer = lex.lex()

# Asociación de operadores y precedencia
precedence = (
    ('left','DOSPUNTOS'),
    ('left','INTERROGACION'),
    ('left','OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('left', 'IGUALIGUAL','DIFERENTE','MENORQUE','MENORIGUAL','MAYORQUE','MAYORIGUAL'),
    ('left','MAS','MENOS'),
    ('left','DIVISION', 'POR', 'MODULO'),
    ('left','POTENCIA'),
    ('right','UMENOS'),
    ('PARA', 'PARC'),
    ('left','POR'),
    )

# Definición de la gramática

#Abstract
from Abstract.NodoAST import NodoAST
from Instrucciones.Imprimir import Imprimir
from Instrucciones.imprimirln import Imprimirln
from Expresiones.Constante import Constante
from Objeto.Primitivo import Primitivo
from TS.Tipo import TIPO, OperadorAritmetico, OperadorLogico, OperadorRelacional
from Expresiones.Aritmetica import Aritmetica
from Expresiones.Nativa import Nativa
from Expresiones.Relacional import Relacional
from Expresiones.Logica import Logica
from Expresiones.Identificador import Identificador
from Instrucciones.Asignacion import Asignacion
from Instrucciones.accesoVector import Acceso
from Instrucciones.modificaVector import Modifica
from Instrucciones.If import If
from Instrucciones.While import While
from Instrucciones.For import For
from Instrucciones.ForCadena import ForCadena
from Instrucciones.ForArreglo import ForArreglo
from Instrucciones.Break import Break
from Instrucciones.Continue import Continue
from Instrucciones.Funcion import Funcion
from Instrucciones.Llamada import Llamada
from Instrucciones.Return import Return
from Instrucciones.Metodo import Metodo
from Expresiones.atributo import atributo
from Expresiones.Struct import Struct
from Instrucciones.AsignacionStruct import AsignacionStruct
from Instrucciones.AccesoStruct import AccesoStruct
from Instrucciones.modificaStruct import ModificaStruct
from Instrucciones.llamadaIntermedia import LlamadaIntermedia
def p_init(t) :
    'init            : instrucciones'
    t[0] = t[1]

def p_instrucciones_instrucciones_instruccion(t) :
    'instrucciones    : instrucciones instruccion'
    if t[2] != "":
        t[1].append(t[2])
    t[0] = t[1]
    
#///////////////////////////////////////INSTRUCCIONES//////////////////////////////////////////////////

def p_instrucciones_instruccion(t) :
    'instrucciones    : instruccion'
    if t[1] == "":
        t[0] = []
    else:    
        t[0] = [t[1]]

#///////////////////////////////////////INSTRUCCION//////////////////////////////////////////////////

def p_instruccion(t) :
    '''instruccion      : imprimir_instr PUNTOCOMA
                        | imprimirln_instr PUNTOCOMA
                        | asignacion_instr PUNTOCOMA
                        | asignacion_tipo_instr PUNTOCOMA
                        | modifica_vector PUNTOCOMA
                        | push_instr PUNTOCOMA
                        | if_instr PUNTOCOMA
                        | while_instr
                        | for_instr
                        | break_instr PUNTOCOMA
                        | continue_instr PUNTOCOMA
                        | return_instr PUNTOCOMA
                        | funcion_instr 
                        | llamada_instr PUNTOCOMA
                        | struct_instr PUNTOCOMA
                        | modifica_struct PUNTOCOMA
    '''
    t[0] = t[1]

def p_instruccion_error(t):
    'instruccion        : error PUNTOCOMA'
    errores.append(Excepcion("Sintáctico","Error Sintáctico:" + str(t[1].value) , t.lineno(1), find_column(input, t.slice[1])))
    t[0] = ""
#///////////////////////////////////////IMPRIMIR//////////////////////////////////////////////////

def p_imprimir(t) :
    '''
    imprimir_instr     : RPRINT PARA expresiones PARC
                       | RPRINT PARA PARC
    ''' 
    if t[3] != ')':               
        t[0] = Imprimir(t[3], t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] = Imprimir([Primitivo(TIPO.CADENA, t.lineno(1), find_column(input, t.slice[1]), "")], t.lineno(1), find_column(input, t.slice[1]))

def p_imprimirln(t):
    '''
    imprimirln_instr   : RPRINTLN PARA expresiones PARC
                       | RPRINTLN PARA PARC
    '''
    if t[3] != ')':
        t[0] = Imprimirln(t[3], t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] = Imprimirln([Primitivo(TIPO.CADENA, t.lineno(1), find_column(input, t.slice[1]), "")], t.lineno(1), find_column(input, t.slice[1]))

def p_expresiones(t):
    '''
    expresiones        : expresiones COMA expresion
    '''
    t[1].append(t[3])
    t[0] = t[1]


def p_expresiones_coma(t):
    '''
    expresiones        : expresion
    '''
    t[0] = []
    t[0].append(t[1])

def p_expresion_arreglo(t):
    'expresion         : CORA lista_vector CORC'
    t[0] = Primitivo(TIPO.ARREGLO, t.lineno(1), find_column(input, t.slice[1]), t[2] )

def p_expresion_arreglo2(t):
    'lista_vector      : lista_vector COMA expresion '
    t[1].append(t[3])
    t[0] = t[1]

def p_expresion_arreglo3(t):
    'lista_vector      : expresion '
    t[0] = []
    t[0].append(t[1])

#///////////////////////////////////////DECLARACIÓN Y ASIGNACION PARA STRUCTS//////////////////////////////////////////////////

def p_struct1(t):
    ''' 
    struct_instr  : RSTRUCT ID lista_atributos REND
    '''
    t[0] = Struct(t[2], t[3], False,  t.lineno(1), find_column(input, t.slice[1]))

def p_struct2(t):
    ''' 
    struct_instr  : RMUTABLE RSTRUCT ID lista_atributos REND
    '''
    t[0] = Struct(t[3], t[4], True,  t.lineno(1), find_column(input, t.slice[1]))


def p_modifica_struct(t):
    ''' 
    modifica_struct  : ID PUNTO ID IGUAL expresion
    '''
    t[0] = ModificaStruct(t[1], t[3], t[5],  t.lineno(1), find_column(input, t.slice[1]))

def p_lista_atributos(t):
    '''
    lista_atributos : lista_atributos ID PUNTOCOMA
    '''
    objeto = atributo(t[2], None)
    t[1].append(objeto)
    t[0] = t[1]


def p_lista_atributos2(t):
    '''
    lista_atributos : ID PUNTOCOMA
    '''
    objeto = atributo(t[1], None)
    t[0] = []
    t[0].append(objeto)


def p_lista_atributos3(t):
    '''
    lista_atributos : lista_atributos ID DOSPUNTOS DOSPUNTOS tipo_atributo PUNTOCOMA
    '''
    objeto = atributo(t[2], t[5])
    t[1].append(objeto)
    t[0] = t[1]

def p_lista_atributos4(t):
    '''
    lista_atributos : ID DOSPUNTOS DOSPUNTOS tipo_atributo PUNTOCOMA
    '''
    objeto = atributo(t[1], t[4])
    t[0] = []
    t[0].append(objeto)

def p_lista_atributos5(t):
    '''
    tipo_atributo : RINT
                  | RFLOAT
                  | RSTRING
                  | RCHAR
                  | RBOOL
                  | ID
    '''
    if t[1] == 'Int64':
        t[0] = TIPO.ENTERO
    elif t[1] == 'Float64':
        t[0] = TIPO.DECIMAL
    elif t[1] == 'Bool':
        t[0] = TIPO.BOOLEANO
    elif t[1] == 'Char':
        t[0] = TIPO.CHARACTER
    elif t[1] == 'String':
        t[0] = TIPO.CADENA
    else:
        t[0] == TIPO.STRUCT

#def p_asigna_struct1(t):
 #   'asigna_struct  : ID IGUAL ID PARA expresiones PARC '
  #  t[0] = AsignacionStruct(t[1], t[3], t[5],  t.lineno(1), find_column(input, t.slice[2]))


def p_acceso_struct(t):
    'expresion : ID puntos_struct'
    t[0] = AccesoStruct(t[1], t[2], t.lineno(1), find_column(input, t.slice[1]))

def p_acceso_struct2(t):
    'puntos_struct : puntos_struct PUNTO ID'
    t[1].append(t[3])
    t[0] = t[1]

def p_acceso_struct3(t):
    'puntos_struct  : PUNTO ID'
    t[0] = []
    t[0].append(t[2])

#def p_asigna_struct2(t):
 #   'expresion : asigna_struct'
  #  t[0] = t[1]
    
#///////////////////////////////////////DECLARACIÓN Y ASIGNACION//////////////////////////////////////////////////

def p_asignacion(t) :
    '''
    asignacion_instr     : ID IGUAL expresion
                         | ID IGUAL PARA expresion PARC 
                        
    '''
    if t[3] == '(':
        t[0] = Asignacion(t[1], t[4], None, t.lineno(1), find_column(input, t.slice[1]))
    #elif isinstance(t[3], str) == True:
    #    t[0] = LlamadaIntermedia(t[1], t[3], t[5], t.lineno(1), find_column(input, t.slice[1]) )
    else:
        t[0] = Asignacion(t[1], t[3], None, t.lineno(1), find_column(input, t.slice[1]))

def p_asignacion2(t):
    '''
    asignacion_instr      : RGLOBAL ID IGUAL expresion
                          | RGLOBAL ID IGUAL PARA expresion PARC
    '''
    if t[4] == '(':
        t[0] = Asignacion(t[2], t[5], None, t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] = Asignacion(t[2], t[4], None, t.lineno(1), find_column(input, t.slice[1]))


def p_asignacion3(t) :
    '''
    asignacion_instr     : ID                 
                        
    '''
    t[0] = Asignacion(t[1], None, None, t.lineno(1), find_column(input, t.slice[1]))

def p_asignacion4(t):
    'asignacion_instr    : RGLOBAL ID'
    t[0] = Asignacion(t[2], None, None, t.lineno(1), find_column(input, t.slice[1]))



def p_asignacion5(t) :
    '''
    asignacion_instr    : ID DOSPUNTOS DOSPUNTOS RINT
                        | ID DOSPUNTOS DOSPUNTOS RSTRING
                        | ID DOSPUNTOS DOSPUNTOS RCHAR
                        | ID DOSPUNTOS DOSPUNTOS RBOOL
                        | ID DOSPUNTOS DOSPUNTOS RFLOAT
                        | ID DOSPUNTOS DOSPUNTOS ID
                                    
    '''
    if t[4] == 'Int64':
         t[0] = Asignacion(t[1], None, TIPO.ENTERO, t.lineno(1), find_column(input, t.slice[1]))
    elif t[4] == 'String':
        t[0] = Asignacion(t[1], None, TIPO.CADENA, t.lineno(1), find_column(input, t.slice[1]))    
    elif t[4] == 'Char':
        t[0] = Asignacion(t[1], None, TIPO.CHARACTER, t.lineno(1), find_column(input, t.slice[1]))
    elif t[4] == 'Bool':
        t[0] = Asignacion(t[1], None, TIPO.BOOLEANO, t.lineno(1), find_column(input, t.slice[1]))
    elif t[4] == 'Float64':
        t[0] = Asignacion(t[1], None, TIPO.DECIMAL, t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] = Asignacion(t[1], None, TIPO.STRUCT, t.lineno(1), find_column(input, t.slice[1]))

def p_asignacion6(t) :
    '''
    asignacion_instr    : RGLOBAL ID DOSPUNTOS DOSPUNTOS RINT
                        | RGLOBAL ID DOSPUNTOS DOSPUNTOS RSTRING
                        | RGLOBAL ID DOSPUNTOS DOSPUNTOS RCHAR
                        | RGLOBAL ID DOSPUNTOS DOSPUNTOS RBOOL
                        | RGLOBAL ID DOSPUNTOS DOSPUNTOS RFLOAT
                        | RGLOBAL ID DOSPUNTOS DOSPUNTOS ID
                                    
    '''
    if t[5] == 'Int64':
         t[0] = Asignacion(t[2], None, TIPO.ENTERO, t.lineno(1), find_column(input, t.slice[1]))
    elif t[5] == 'String':
        t[0] = Asignacion(t[2], None, TIPO.CADENA, t.lineno(1), find_column(input, t.slice[1]))    
    elif t[5] == 'Char':
        t[0] = Asignacion(t[2], None, TIPO.CHARACTER, t.lineno(1), find_column(input, t.slice[1]))
    elif t[5] == 'Bool':
        t[0] = Asignacion(t[2], None, TIPO.BOOLEANO, t.lineno(1), find_column(input, t.slice[1]))
    elif t[5] == 'Float64':
        t[0] = Asignacion(t[2], None, TIPO.DECIMAL, t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] = Asignacion(t[2], None, TIPO.STRUCT, t.lineno(1), find_column(input, t.slice[1]))

def p_asignacion_tipo(t):
    '''
    asignacion_tipo_instr : ID IGUAL expresion DOSPUNTOS DOSPUNTOS RINT
                          | ID IGUAL PARA expresion PARC DOSPUNTOS DOSPUNTOS RINT
                          | ID IGUAL expresion DOSPUNTOS DOSPUNTOS RSTRING
                          | ID IGUAL PARA expresion PARC DOSPUNTOS DOSPUNTOS RSTRING
                          | ID IGUAL expresion DOSPUNTOS DOSPUNTOS RCHAR
                          | ID IGUAL PARA expresion PARC DOSPUNTOS DOSPUNTOS RCHAR
                          | ID IGUAL expresion DOSPUNTOS DOSPUNTOS RBOOL
                          | ID IGUAL PARA expresion PARC DOSPUNTOS DOSPUNTOS RBOOL
                          | ID IGUAL expresion DOSPUNTOS DOSPUNTOS RFLOAT
                          | ID IGUAL PARA expresion PARC DOSPUNTOS DOSPUNTOS RFLOAT
                          | ID IGUAL expresion DOSPUNTOS DOSPUNTOS ID
                          | ID IGUAL PARA expresion PARC DOSPUNTOS DOSPUNTOS ID
    '''
    if t[3] == '(':
         if t[8] == 'Int64':
             t[0] = Asignacion(t[1], t[4], TIPO.ENTERO, t.lineno(1), find_column(input, t.slice[1]))
         elif t[8] == 'String':
            t[0] = Asignacion(t[1], t[4], TIPO.CADENA, t.lineno(1), find_column(input, t.slice[1]))    
         elif t[8] == 'Char':
            t[0] = Asignacion(t[1], t[4], TIPO.CHARACTER, t.lineno(1), find_column(input, t.slice[1]))
         elif t[8] == 'Bool':
            t[0] = Asignacion(t[1], t[4], TIPO.BOOLEANO, t.lineno(1), find_column(input, t.slice[1]))
         elif t[8] == 'Float64':
            t[0] = Asignacion(t[1], t[4], TIPO.DECIMAL, t.lineno(1), find_column(input, t.slice[1]))
         else:
             t[0] = Asignacion(t[1], t[4], TIPO.STRUCT, t.lineno(1), find_column(input, t.slice[1]))
    else:
         if t[6] == 'Int64':
             t[0] = Asignacion(t[1], t[3], TIPO.ENTERO, t.lineno(1), find_column(input, t.slice[1]))
         elif t[6] == 'String':
            t[0] = Asignacion(t[1], t[3], TIPO.CADENA, t.lineno(1), find_column(input, t.slice[1]))    
         elif t[6] == 'Char':
            t[0] = Asignacion(t[1], t[3], TIPO.CHARACTER, t.lineno(1), find_column(input, t.slice[1]))
         elif t[6] == 'Bool':
            t[0] = Asignacion(t[1], t[3], TIPO.BOOLEANO, t.lineno(1), find_column(input, t.slice[1]))
         elif t[6] == 'Float64':
            t[0] = Asignacion(t[1], t[3], TIPO.DECIMAL, t.lineno(1), find_column(input, t.slice[1]))
         else:
             t[0] = Asignacion(t[1], t[3], TIPO.STRUCT, t.lineno(1), find_column(input, t.slice[1]))

def p_asignacion_tipo2(t):
    '''
    asignacion_tipo_instr : RGLOBAL ID IGUAL expresion DOSPUNTOS DOSPUNTOS RINT
                          | RGLOBAL ID IGUAL PARA expresion PARC DOSPUNTOS DOSPUNTOS RINT
                          | RGLOBAL ID IGUAL expresion DOSPUNTOS DOSPUNTOS RSTRING
                          | RGLOBAL ID IGUAL PARA expresion PARC DOSPUNTOS DOSPUNTOS RSTRING
                          | RGLOBAL ID IGUAL expresion DOSPUNTOS DOSPUNTOS RCHAR
                          | RGLOBAL ID IGUAL PARA expresion PARC DOSPUNTOS DOSPUNTOS RCHAR
                          | RGLOBAL ID IGUAL expresion DOSPUNTOS DOSPUNTOS RBOOL
                          | RGLOBAL ID IGUAL PARA expresion PARC DOSPUNTOS DOSPUNTOS RBOOL
                          | RGLOBAL ID IGUAL expresion DOSPUNTOS DOSPUNTOS RFLOAT
                          | RGLOBAL ID IGUAL PARA expresion PARC DOSPUNTOS DOSPUNTOS RFLOAT
                          | RGLOBAL ID IGUAL expresion DOSPUNTOS DOSPUNTOS ID
                          | RGLOBAL ID IGUAL PARA expresion PARC DOSPUNTOS DOSPUNTOS ID
    '''
    if t[4] == '(':
         if t[9] == 'Int64':
             t[0] = Asignacion(t[2], t[5], TIPO.ENTERO, t.lineno(1), find_column(input, t.slice[1]))
         elif t[9] == 'String':
            t[0] = Asignacion(t[2], t[5], TIPO.CADENA, t.lineno(1), find_column(input, t.slice[1]))    
         elif t[9] == 'Char':
            t[0] = Asignacion(t[2], t[5], TIPO.CHARACTER, t.lineno(1), find_column(input, t.slice[1]))
         elif t[9] == 'Bool':
            t[0] = Asignacion(t[2], t[5], TIPO.BOOLEANO, t.lineno(1), find_column(input, t.slice[1]))
         elif t[9] == 'Float64':
            t[0] = Asignacion(t[2], t[5], TIPO.DECIMAL, t.lineno(1), find_column(input, t.slice[1]))
         else:
             t[0] = Asignacion(t[2], t[5], TIPO.STRUCT, t.lineno(1), find_column(input, t.slice[1]))
    else:
         if t[6] == 'Int64':
             t[0] = Asignacion(t[2], t[4], TIPO.ENTERO, t.lineno(1), find_column(input, t.slice[1]))
         elif t[6] == 'String':
            t[0] = Asignacion(t[2], t[4], TIPO.CADENA, t.lineno(1), find_column(input, t.slice[1]))    
         elif t[6] == 'Char':
            t[0] = Asignacion(t[2], t[4], TIPO.CHARACTER, t.lineno(1), find_column(input, t.slice[1]))
         elif t[6] == 'Bool':
            t[0] = Asignacion(t[2], t[4], TIPO.BOOLEANO, t.lineno(1), find_column(input, t.slice[1]))
         elif t[6] == 'Float64':
            t[0] = Asignacion(t[2], t[4], TIPO.DECIMAL, t.lineno(1), find_column(input, t.slice[1]))
         else:
             t[0] = Asignacion(t[2], t[4], TIPO.STRUCT, t.lineno(1), find_column(input, t.slice[1]))

#//////////////////////////////////////NATIVAS //////////////////////////////////////////////////
def p_parse(t):
    '''
    expresion      : RPARSE PARA RFLOAT COMA expresion PARC
                   | RPARSE PARA RINT COMA expresion PARC
    '''
    t[0] = Nativa(OperadorAritmetico.PARSE, t[3], t[5], t.lineno(2), find_column(input, t.slice[2]))

def p_trunc(t):
    '''
    expresion      : RTRUNC PARA RINT COMA expresion PARC
                   | RTRUNC PARA expresion PARC
    '''
    if t[3] == "Int64":
        t[0] = Nativa(OperadorAritmetico.TRUNC, t[3], t[5], t.lineno(2), find_column(input, t.slice[2]))
    else:
        t[0] = Nativa(OperadorAritmetico.TRUNC, "", t[3], t.lineno(2), find_column(input, t.slice[2]))

def p_float(t):
    '''
    expresion      : RFFLOAT PARA expresion PARC
    '''
    t[0] = Nativa(OperadorAritmetico.FLOAT, t[3], "", t.lineno(2), find_column(input, t.slice[2]))

def p_string(t):
    '''
    expresion      : RSSTRING PARA expresion PARC
                   | RSSTRING PARA expresiones PARC
                   | RSSTRING PARA acceso_vector PARC
    '''
    t[0] = Nativa(OperadorAritmetico.STRING, t[3], "", t.lineno(2), find_column(input, t.slice[2]))

def p_type(t):
    '''
    expresion      : RTYPEOF PARA expresion PARC
    '''
    t[0] = Nativa(OperadorAritmetico.TYPEOF, t[3], "", t.lineno(2), find_column(input, t.slice[2]))

def p_push(t):
    '''push_instr    : RPUSH NOT PARA ID COMA expresion PARC
                     | RPUSH NOT PARA expresion COMA expresion PARC
    '''
    t[0] = Nativa(OperadorAritmetico.PUSH, t[4], t[6], t.lineno(2), find_column(input, t.slice[2]))

def p_pop(t):
    'expresion     : RPOP NOT PARA ID PARC'
    t[0] = Nativa(OperadorAritmetico.POP, t[4], "", t.lineno(2), find_column(input, t.slice[2]))

def p_length(t):
    '''expresion     : RLENGTH PARA ID PARC
                     | RLENGTH PARA expresion PARC
    '''

    t[0] = Nativa(OperadorAritmetico.LENGTH, t[3], "", t.lineno(2), find_column(input, t.slice[2]))
#///////////////////////////////////////IF//////////////////////////////////////////////////

def p_if1(t):
    'if_instr     : RIF expresion instrucciones mas_instrucciones_if'
    t[0] = If(t[2], t[3], t[4], t.lineno(1), find_column(input, t.slice[1]))

def p_if2(t):
    '''
    mas_instrucciones_if : else_instr
                        | elseif_instr
                        | end_instr
    '''
    t[0] = t[1]

def p_if3(t):
    ' else_instr        : RELSE instrucciones REND'
    t[0] = t[2]

def p_if4(t):
    'elseif_instr       : RELSEIF expresion instrucciones mas_instrucciones_if'
    t[0] = If(t[2], t[3], t[4], t.lineno(1), find_column(input, t.slice[1]))

def p_if5(t):
    'end_instr          : REND '
    t[0] = None

#///////////////////////////////////////WHILE//////////////////////////////////////////////////

def p_while(t) :
    'while_instr     : RWHILE expresion instrucciones REND PUNTOCOMA '
    t[0] = While(t[2], t[3], t.lineno(1), find_column(input, t.slice[1]))


#//////////////////////////////////////FOR////////////////////////////////////////////////////

def p_for(t):
    '''
    for_instr        : RFOR ID RIN expresion DOSPUNTOS expresion instrucciones  REND PUNTOCOMA
    '''
    t[0] = For(t[2], t[4], t[6], t[7], t.lineno(1), find_column(input, t.slice[1]) )

def p_for3(t):
    'for_instr       : RFOR ID RIN ID CORA expresion DOSPUNTOS expresion CORC instrucciones  REND PUNTOCOMA'
    t[0] = ForArreglo(t[2], t[4], t[6],t[8], t[10], t.lineno(1), find_column(input, t.slice[1]) )

def p_for2(t):
    'for_instr       : RFOR ID RIN expresion instrucciones REND PUNTOCOMA '
   
    t[0] = ForCadena(t[2], t[4], t[5], t.lineno(1), find_column(input, t.slice[1]) )



#///////////////////////////////////////BREAK//////////////////////////////////////////////////

def p_break(t) :
    'break_instr     : RBREAK'
    t[0] = Break(t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////CONTINUE//////////////////////////////////////////////////

def p_continue(t) :
    'continue_instr     : RCONTINUE'
    t[0] = Continue(t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////RETURN//////////////////////////////////////////////////
def p_return(t):
    'return_instr       : RRETURN expresion'
    t[0] = Return(t[2], t.lineno(1),find_column(input, t.slice[1]))

def p_return2(t):
    'return_instr       : RRETURN'
    t[0] = Return(None, t.lineno(1),find_column(input, t.slice[1]))

#///////////////////////////////////////FUNCION//////////////////////////////////////////////////

def p_funcion_1(t) :
    'funcion_instr     : RFUNC ID PARA parametros PARC instrucciones REND PUNTOCOMA'
    t[0] = Funcion(t[2], Metodo(t[6], t[4]), t.lineno(1), find_column(input, t.slice[1]))


def p_funcion_2(t) :
    'funcion_instr     : RFUNC ID PARA PARC instrucciones REND PUNTOCOMA'
    t[0] = Funcion(t[2], Metodo(t[5], None), t.lineno(1), find_column(input, t.slice[1]))


#///////////////////////////////////////PARAMETROS//////////////////////////////////////////////////

def p_parametros_1(t) :
    'parametros     : parametros COMA parametro'
    t[1].append(t[3])
    t[0] = t[1]
    
def p_parametros_2(t) :
    'parametros    : parametro'
    t[0] = [t[1]]

#///////////////////////////////////////PARAMETRO//////////////////////////////////////////////////

def p_parametro(t) :
    'parametro     : ID'
    #t[0] = Asignacion(t[1], Primitivo(TIPO.ENTERO,t.lineno(1), find_column(input, t.slice[1]), 0), None, t.lineno(1), find_column(input, t.slice[1]))
    t[0] = t[1]

def p_parametro2(t) :
    '''parametro     : ID DOSPUNTOS DOSPUNTOS RINT 
                     | ID DOSPUNTOS DOSPUNTOS RFLOAT
                     | ID DOSPUNTOS DOSPUNTOS RCHAR
                     | ID DOSPUNTOS DOSPUNTOS RBOOL
                     | ID DOSPUNTOS DOSPUNTOS RSTRING
                     | ID DOSPUNTOS DOSPUNTOS ID
    '''
    t[0] = t[1]


#///////////////////////////////////////LLAMADA A FUNCION//////////////////////////////////////////////////

def p_llamada1(t) :
    'llamada_instr     : ID PARA PARC'
    t[0] = Llamada(t[1], None, t.lineno(1), find_column(input, t.slice[1]))


def p_llamada2(t) :
    'llamada_instr     : ID PARA expresiones PARC'
    t[0] = Llamada(t[1], t[3], t.lineno(1), find_column(input, t.slice[1]))

def p_llamada_extra(t):
    'expresion     : llamada_instr'
    t[0] = t[1]

def p_llamada_extra2(t):
    'expresion     : llamada_instr DOSPUNTOS DOSPUNTOS ID'
    t[0] = t[1]

#def p_llamada3(t) :
 #   'expresion     : ID PARA PARC'
  #  t[0] = Llamada(t[1], None, t.lineno(1), find_column(input, t.slice[1]))

#def p_llamada4(t) :
 #   'expresion     : ID PARA parametros_llamada PARC'
  #  t[0] = Llamada(t[1], t[3], t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////PARAMETROS LLAMADA A FUNCION//////////////////////////////////////////////////

#def p_parametrosLL_1(t) :
#    'parametros_llamada     : parametros_llamada COMA parametro_llamada'
#    t[1].append(t[3])
#    t[0] = t[1]
    
#def p_parametrosLL_2(t) :
#    'parametros_llamada    : parametro_llamada'
#    t[0] = [t[1]]

#///////////////////////////////////////PARAMETRO LLAMADA A FUNCION//////////////////////////////////////////////////

#def p_parametroLL(t) :
#    'parametro_llamada     : expresion'
#    t[0] = t[1]

#///////////////////////////////////////LLAMADA A FUNCION//////////////////////////////////////////////////



#///////////////////////////////////////EXPRESION//////////////////////////////////////////////////

def p_expresion_binaria(t):
    '''
    expresion : expresion MAS expresion
            | expresion MENOS expresion
            | expresion POR expresion
            | expresion DIVISION expresion
            | expresion POTENCIA expresion
            | expresion MODULO expresion
            | MENOS expresion %prec UMENOS
            | expresion MENORQUE expresion
            | expresion MENORIGUAL expresion
            | expresion MAYORQUE expresion
            | expresion MAYORIGUAL expresion
            | expresion IGUALIGUAL expresion
            | expresion DIFERENTE expresion
            | expresion AND expresion
            | expresion OR expresion
            | NOT expresion
            | RLOG10 PARA expresion PARC
            | RLOG PARA expresion COMA expresion PARC
            | RSIN PARA expresion PARC
            | RCOS PARA expresion PARC
            | RTAN PARA expresion PARC
            | RSQRT PARA expresion PARC
            | RUPPER PARA expresion PARC
            | RLOWER PARA expresion PARC
            | PARA expresion PARC
    '''
    if t[2] == '+':
        t[0] = Aritmetica(OperadorAritmetico.MAS, t[1],t[3], "", t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '-':
        t[0] = Aritmetica(OperadorAritmetico.MENOS, t[1],t[3], "", t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '*':
        t[0] = Aritmetica(OperadorAritmetico.POR, t[1],t[3], "", t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '/':
        t[0] = Aritmetica(OperadorAritmetico.DIV, t[1],t[3], "", t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '^':
        t[0] = Aritmetica(OperadorAritmetico.POTENCIA, t[1],t[3], "", t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '%':
        t[0] = Aritmetica(OperadorAritmetico.MODULO, t[1],t[3], "", t.lineno(2), find_column(input, t.slice[2]))
    elif t[1] == '-':
        t[0] = Aritmetica(OperadorAritmetico.MENOSUNARIO, "","", t[2], t.lineno(1), find_column(input, t.slice[1]))
    elif t[2] == '<':
        t[0] = Relacional(OperadorRelacional.MENORQUE, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '<=':
        t[0] = Relacional(OperadorRelacional.MENORIGUAL, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))    
    elif t[2] == '>':
        t[0] = Relacional(OperadorRelacional.MAYORQUE, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '>=':
        t[0] = Relacional(OperadorRelacional.MAYORIGUAL, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '!=':
        t[0] = Relacional(OperadorRelacional.DIFERENTE, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '==':
        t[0] = Relacional(OperadorRelacional.IGUALIGUAL, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '&&':
        t[0] = Logica(OperadorLogico.AND, t[1],t[3],"", t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '||':
        t[0] = Logica(OperadorLogico.OR, t[1],t[3],"", t.lineno(2), find_column(input, t.slice[2]))
    elif t[1] == '!':
        t[0] = Logica(OperadorLogico.NOT, "", "", t[2],t.lineno(1), find_column(input, t.slice[1]))
    elif t[1] == 'log10':
        t[0] = Nativa(OperadorAritmetico.BASE10, t[3], "", t.lineno(1), find_column(input, t.slice[1]))
    elif t[1] == 'log':
        t[0] = Nativa(OperadorAritmetico.BASE, t[3], t[5], t.lineno(1), find_column(input, t.slice[1]))
    elif t[1] == 'sin':
        t[0] = Nativa(OperadorAritmetico.SENO, t[3], "", t.lineno(1), find_column(input, t.slice[1]))
    elif t[1] == 'cos':
        t[0] = Nativa(OperadorAritmetico.COSENO, t[3], "", t.lineno(1), find_column(input, t.slice[1]))
    elif t[1] == 'tan':
        t[0] = Nativa(OperadorAritmetico.TANGENTE, t[3], "", t.lineno(1), find_column(input, t.slice[1]))
    elif t[1] == 'sqrt':
        t[0] = Nativa(OperadorAritmetico.RAIZ, t[3], "", t.lineno(1), find_column(input, t.slice[1]))
    elif t[1] == 'uppercase':
        t[0] = Nativa(OperadorAritmetico.UPPER, t[3], "", t.lineno(1), find_column(input, t.slice[1]))
    elif t[1] == 'lowercase':
        t[0] = Nativa(OperadorAritmetico.LOWER, t[3], "", t.lineno(1), find_column(input, t.slice[1]))
    elif t[1] == '(' and t[3] == ')':
        t[0] = t[2]


#def p_expresion_agrupacion(t):
    ##'''
   ## expresion :   PARA expresion PARC 
   ## '''
   ## t[0] = t[2]

#def p_expresion_llamada(t):
 #   '''expresion : llamada_instr'''
  #  t[0] = t[1]

#def p_expresion_llamada(t):
 #   '''expresion : asignacion_instr'''
  #  t[0] = t[1]

def p_expresion_identificador(t):
    '''expresion : ID'''
    t[0] = Identificador(t[1], t.lineno(1), find_column(input, t.slice[1]))

#def p_expresion_identificador12(t):
 #   '''expresion : RGLOBAL ID'''
  #  t[0] = Identificador(t[2], t.lineno(1), find_column(input, t.slice[1]))

#def p_devolver_struct_llamada(t):
 #   'expresion : ID PARA expresiones PARC'
  #  t[0] = LlamadaIntermedia(None, t[1], t[3], t.lineno(1), find_column(input, t.slice[1]) )

def p_acceder_vector(t):
    'expresion : ID acceso_vector'
    t[0] = Acceso(t[1], t[2], t.lineno(1), find_column(input, t.slice[1]))

def p_modifica_vector(t):
    'modifica_vector  : ID acceso_vector IGUAL expresion'
    t[0] = Modifica(t[1], t[2], t[4], t.lineno(1), find_column(input, t.slice[1]))

def p_acceder_vector2(t):
    'acceso_vector        : acceso_vector CORA expresion CORC'
    t[1].append(t[3])
    t[0] = t[1]

def p_acceder_vector3(t):
    'acceso_vector        : CORA expresion CORC'
    t[0] = []
    t[0].append(t[2])

def p_expresion_entero(t):
    '''expresion : ENTERO'''
    t[0] = Primitivo(TIPO.ENTERO,t.lineno(1), find_column(input, t.slice[1]), t[1])

def p_expresion_decimal(t):
    '''expresion : DECIMAL'''
    t[0] = Primitivo(TIPO.DECIMAL, t.lineno(1), find_column(input, t.slice[1]), t[1])

def p_expresion_cadena(t):
    '''expresion : CADENA'''
    t[0] = Primitivo(TIPO.CADENA, t.lineno(1), find_column(input, t.slice[1],), str(t[1]).replace('\\n', '\n'))

def p_expresion_caracter(t):
    '''expresion : CARACTER'''
    t[0] = Primitivo(TIPO.CHARACTER, t.lineno(1), find_column(input, t.slice[1],), str(t[1]).replace('\\n', '\n'))

def p_expresion_true(t):
    '''expresion : RTRUE'''
    t[0] = Primitivo(TIPO.BOOLEANO, t.lineno(1), find_column(input, t.slice[1]), True)

def p_expresion_false(t):
    '''expresion : RFALSE'''
    t[0] = Primitivo(TIPO.BOOLEANO, t.lineno(1), find_column(input, t.slice[1]), False)

def p_expresion_nothing(t):
    '''expresion : RNOTHING'''
    t[0] = Primitivo(TIPO.NULO, t.lineno(1), find_column(input, t.slice[1]), None)
 

import ply.yacc as yacc
parser = yacc.yacc()
from TS.Arbol import Arbol
from TS.TablaSimbolos import TablaSimbolos

def getErrores():
    return errores

def parse(inp) :
    global errores
    global lexer
    global parser
    errores = []
    #lexer = lex.lex(reflags= re.IGNORECASE)
    parser = yacc.yacc()
    global input
    input = inp
    instrucciones=parser.parse(inp)
    genAux = Generador()
    genAux.cleanAll()
    generator = genAux.obtenerGen()
    newEnv = Entorno(None)
    for i in instrucciones:
        i.interpretar(newEnv)
    '''ast = Arbol(instrucciones)
    TSGlobal = TablaSimbolos()
    TSGlobal.setEntorno("Global")
    ast.setTSglobal(TSGlobal)
    ast.agregarTabla(TSGlobal)
    # for error in errores:                   # CAPTURA DE ERRORES LEXICOS Y SINTACTICOS
    #     ast.getExcepciones().append(error)
    #     ast.updateConsola(error.toString())

    for instruccion in ast.getInstrucciones():
        #if isinstance(instruccion, Funcion):
         #   ast.addFuncion(instruccion)
        # Aqui agregar demás validaciones (return, break o continue en lugar incorrecto)
        #else:
            result  = instruccion.interpretar(ast,TSGlobal)
            if isinstance(result, Excepcion):
                ast.updateConsolaln(result.toString())

    '''
    lexer.lineno = 1
    return generator.getCode()





