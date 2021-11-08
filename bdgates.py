#-------------------------------------------------------------------------------
# bdgates.py
#
# lexer and parser for the database of logic gates
# 
#-------------------------------------------------------------------------------
import ply.lex as lex
import sys


#-------------------------------------------------------------------------------
#
#    __    ____  _  _  ____  _  _  ___ 
#   (  )  ( ___)( \/ )(_  _)( \( )/ __)
#    )(__  )__)  )  (  _)(_  )  (( (_-.
#   (____)(____)(_/\_)(____)(_)\_)\___/
#
#
#-------------------------------------------------------------------------------

# List of reserved words
reserved = {
    'GATES': 'GATES',
    'OMATRIX': 'OMATRIX',
    'AND' : 'AND',
    'OR' : 'OR',
    'NOT' : 'NOT',
    'NAND' : 'NAND',
    'XOR' : 'XOR',
    'NOR' : 'NOR',
}

# List of tokens
tokens = [
    'NUMBER',
    'ID',
    'SCOLON',
    ] 

tokens = tokens + list(reserved.values())

# Regular expression rules for simple tokens
t_SCOLON  = r'\;'

# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+\.\d+'
    t.value = float(t.value)    
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()



#-------------------------------------------------------------------------------
#
#    ____   __    ____  ___  ____  _  _  ___ 
#   (  _ \ /__\  (  _ \/ __)(_  _)( \( )/ __)
#    )___//(__)\  )   /\__ \ _)(_  )  (( (_-.
#   (__) (__)(__)(_)\_)(___/(____)(_)\_)\___/
#
#
#-------------------------------------------------------------------------------
import ply.yacc as yacc

ids = []

gates = {}
gates["NOT"] = []
gates["AND"] = []
gates["OR"] = []
gates["XOR"] = []
gates["NOR"] = []
gates["NAND"] = []

relations = {}

precedence = (
     ('left', 'AND', 'OR', 'NAND', 'NOR', 'XOR'),
     ('right', 'NOT'),
)

def p_bdgate(t):
    'bdgate : GATES SCOLON defl OMATRIX SCOLON relationlist'

def p_defl(t):
    '''defl : def 
            | defl def '''
    pass

def p_def(t):
    'def : ID NUMBER gate SCOLON'
    gates[t[3]].append((t[1], t[2]))
    relations[t[1]] = {} 
    ids.append(t[1])

def p_gate(t):
    '''gate : NOT
            | AND
            | OR
            | NAND
            | XOR
            | NOR '''
    t[0] = t[1]

def p_relationlist(t):
    '''relationlist :  relationlist relation  
                    |  relation 
                    | empty '''
    pass

def p_relation(t):
    'relation : ID NUMBER ID SCOLON'
    if (not (t[1] in ids)) or (not (t[1] in ids)) :
        print("Error : defining relation for an unlisted gate")
        sys.exit()
    else:
        relations[t[1]][t[3]] = t[2]

def p_empty(t):
    'empty :'
    pass

def p_error(t):
    print("Syntax error at" , t.value, "on line ", lexer.lineno)
    sys.exit()

parser = yacc.yacc()

def gate_speed_sort(n):
    _,speed = n
    return speed


gates["NOT"].sort(key = gate_speed_sort)
gates["AND"].sort(key = gate_speed_sort)
gates["OR"].sort(key = gate_speed_sort)
gates["XOR"].sort(key = gate_speed_sort)
gates["NOR"].sort(key = gate_speed_sort)
gates["NAND"].sort(key = gate_speed_sort)
