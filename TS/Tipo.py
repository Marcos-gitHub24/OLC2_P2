from enum import Enum

class TIPO(Enum):
    ENTERO = 1
    DECIMAL = 2
    BOOLEANO = 3
    CHARACTER = 4
    CADENA = 5
    NULO = 6
    ARREGLO = 7
    ERROR = 8
    CONTINUE = 9
    RETURN = 10
    BREAK = 11
    FUNCION = 12
    STRUCT = 13

class OperadorAritmetico(Enum):
    MAS = 1
    MENOS = 2
    POR = 3
    DIV = 4
    POTENCIA = 5
    MODULO = 6
    MENOSUNARIO = 7
    BASE10 = 8
    BASE = 9
    SENO = 10
    COSENO = 11
    TANGENTE = 12
    RAIZ = 13
    LOWER = 14
    UPPER = 15
    PARSE = 16
    TRUNC = 17
    FLOAT = 18
    STRING = 19
    TYPEOF = 20
    PUSH = 21
    POP = 22
    LENGTH = 23
    

class OperadorRelacional(Enum):
    MENORQUE = 1
    MAYORQUE = 2
    MENORIGUAL = 3
    MAYORIGUAL = 4
    IGUALIGUAL = 5
    DIFERENTE = 6

class OperadorLogico(Enum):
    NOT = 1
    AND = 2
    OR = 3