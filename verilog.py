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
    'SCOLON',
    'COLON',
    ] 

tokens = tokens + list(reserved.values())


# Regular expression rules for simple tokens
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_COMMA  = r'\,'
t_SCOLON = r'\;'
t_COLON = r'\:'

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


source_gates = []
gate_n = 0
 

def p_bdgate(t):
    ''' program : MODULE ID LPAREN idlist RPAREN COLON output input wires exprlist ENDMODULE '''
    t[0] = "module " + t[1] + "(" + t[4] + "):\n\n" + t[7] + "\n" + t[8] + "\n" + t[9] + "\n\n" + t[10] + "\n\nendmodule"

def p_idlist(t):
    '''idlist : ID
              | ID COMMA idlist '''
    if len(t) > 2 : 
        t[0] = t[1] + "," + t[3]
    else: 
        t[0] = t[1]

def p_output(t):
    '''output : OUTPUT idlist SCOLON ''' 
    t[0] = "\toutput "+t[2] +";"

def p_input(t):
    '''input : INPUT idlist SCOLON ''' 
    t[0] = "\tinput "+t[2] +";"

def p_wires(t):
    '''wires : empty
             | WIRE idlist SCOLON ''' 
    t[0] = "\twire "+t[2] +";"

def p_arg(t):
    '''arg : ID
             | TRUE
             | FALSE '''
    t[0] = t[1]

def p_exprlist(t):
    '''exprlist : expr
                | exprlist expr '''
    if len(t) > 2 : 
        t[0] = t[1] + "\n" + t[2]
    else: 
        t[0] = t[1]

def p_expr(t):
    '''expr : gate2 LPAREN ID COMMA arg COMMA arg RPAREN SCOLON
            | NOT LPAREN ID COMMA arg RPAREN SCOLON '''
    t[0] = "\t"
    print(t[1] + "  " + source_gates.pop(0))
    if (t[1]=='NOT'):
        t[0] += "NOT("+t[3]+","+t[5]+","+");"
    else:
        t[0] += t[1]+"("+t[3]+","+t[5]+","+t[7]+");"

def p_gate2(t):
    '''gate2 : AND
             | OR
             | NAND
             | XOR
             | NOR '''
    t[0] = t[1]

def p_empty(t):
    'empty :'
    pass

def p_error(t):
    print("Syntax error at" , t.value, "on line ", lexer.lineno)
    sys.exit()

parser = yacc.yacc()

gates = ["NOT","AND","OR","NAND","NOR","XOR"]

def parse_verilog(s):
    lexer.input(s)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok: 
            break      # No more input
        if tok.type in gates:
            source_gates.append(tok.type)
    print("source gates : ", source_gates)
    return parser.parse(s)
