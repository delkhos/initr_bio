#-------------------------------------------------------------------------------
# bdgates.py
#
# lexer and parser for the database of logic gates
# 
#-------------------------------------------------------------------------------
import ply.lex as lex


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
    'TRUE' : 'TRUE',
    'FALSE' : 'FALSE',
}

# List of tokens
tokens = [
    'NUMBER',
    'LPAREN',
    'RPAREN',
    'LBRACKET',
    'RBRACKET',
    'LCBRACKET',
    'RCBRACKET',
    'COMMA',
    'ID',
    'SCOLON',
    ] 

tokens = tokens + list(reserved.values())
print(tokens)


# Regular expression rules for simple tokens
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACKET  = r'\['
t_RBRACKET  = r'\]'
t_LCBRACKET  = r'\{'
t_RCBRACKET  = r'\}'
t_COMMA  = r'\,'
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
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()


data = '''
GATES;

a12 0.723 [ a , b ] { a AND b };
c20 4571.7 [ c , d ] { c OR d };

OMATRIX;

a12 0.3 c20;

'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)

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

gates = {}
relations = {}

precedence = (
     ('left', 'AND', 'OR', 'NAND', 'NOR', 'XOR'),
     ('right', 'NOT'),            # Unary minus operator
)


def p_bdgate(t):
    'bdgate : GATES SCOLON defl  OMATRIX SCOLON relationlist'
    pass

def p_defl(t):
    '''defl : def 
            | defl def '''
    pass

def p_def(t):
    'def : ID NUMBER LBRACKET paramlist RBRACKET LCBRACKET expr RCBRACKET SCOLON'
    pass

def p_paramlist(t):
    '''paramlist :  paramlist COMMA ID
                 |  ID
                 | empty '''
    pass

def p_expr(t):
    '''expr : TRUE
            | FALSE
            | LPAREN expr RPAREN
            | NOT expr
            | expr AND expr
            | expr OR expr
            | expr NAND expr
            | expr NOR expr
            | expr XOR expr '''
    pass

def p_relationlist(t):
    '''relationlist :  relationlist relation  
                    |  relation 
                    | empty '''
    pass

def p_relation(t):
    'relation : ID NUMBER ID SCOLON'

def p_empty(t):
    'empty :'
    pass

def p_error(t):
    print("Syntax error at" , t.value, "on line ", t.lineno)

parser = yacc.yacc()

parser.parse(data)
