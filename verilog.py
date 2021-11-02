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
    'module' : 'MODULE',
    'endmodule' : 'ENDMODULE',
    'wire' : 'WIRE',
    'input' : 'INPUT',
    'output' : 'OUTPUT',
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
    'LPAREN',
    'RPAREN',
    'COMMA',
    'ID',
    'EQUAL',
    'SCOLON',
    ] 

tokens = tokens + list(reserved.values())


# Regular expression rules for simple tokens
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_COMMA  = r'\,'
t_EQUAL  = r'\=\=,'
t_SCOLON = r'\;'

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
module main(a,b,c)
    output d;
    intput a,b,c;

    wire w1;
    AND(w1,a,b)
    AND(d,w1,c)

endmodule

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
 
