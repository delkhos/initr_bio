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
real_gates = []

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
    print(real_gates , "  " + source_gates.pop(0))
    if (t[1]=='NOT'):
        t[0] += real_gates.pop(0)+"("+t[3]+","+t[5]+","+");"
    else:
        t[0] += real_gates.pop(0)+"("+t[3]+","+t[5]+","+t[7]+");"

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


from typing import Dict, Any
import hashlib
import json
import copy

def dict_hash(dictionary: Dict[str, Any]) -> str:
    """MD5 hash of a dictionary."""
    dhash = hashlib.md5()
    # We need to sort arguments so {'a': 1, 'b': 2} is
    # the same as {'b': 2, 'a': 1}
    encoded = json.dumps(dictionary, sort_keys=True).encode()
    dhash.update(encoded)
    return dhash.hexdigest()

def correct_db(dbgates,dbrelations,gate, tolerance):
    dbgates_new = {}
    for x in gates:
        lst = dbgates[x]
        lstnew = []
        for y in lst:
            gate_name,_ = y
            if gate_name == gate or ( (gate_name in dbrelations[gate]) and (dbrelations[gate][gate_name] > tolerance)):
                continue
            lstnew.append(y)
        dbgates_new[x] = lstnew
    return dbgates_new

def score_sort(n):
    _,score = n
    return score

def find_real_gates(src_gates,dbgates, dbrelations, tolerance):
    hsmap = {}
    possibilities = []
    max_iter = len(dbgates[src_gates[0]])
    j = 0
    found = False
    while True:
        if j >= max_iter :
            break
        copy_dbgates = copy.deepcopy(dbgates)
        try_gates = []
        score = 0.0
        for id_g,g in enumerate(src_gates):
            real_gates = copy_dbgates[g]
            if len(real_gates)==0:
                break
            else :
                for i in range(len(real_gates)):
                    elected,escore = real_gates[i]
                    corrected_db = correct_db(copy_dbgates,dbrelations,elected,tolerance)
                    hashed = dict_hash(corrected_db)
                    if hashed in hsmap :
                        continue
                    else:
                        if id_g==0:
                            j+=1
                        try_gates.append(elected)
                        score += escore
                        hsmap[hashed] = True
                        copy_dbgates = corrected_db
                        found = True
                        break

                if found:
                    found = False
                else:
                    break

        if len(try_gates)==len(src_gates):
            possibilities.append((try_gates,score))

    if(len(possibilities)==0):
        print("Error : Couldn't find a solution")
        sys.exit()
    else:
        possibilities.sort(key = score_sort)
        print("\nSolution = \n",possibilities[0])
        return possibilities[0]

def parse_verilog(s,tolerance,gatesdb,relationsdb):
    lexer.input(s)

    global real_gates

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok: 
            break      # No more input
        if tok.type in gates:
            source_gates.append(tok.type)

    print("\nsource gates : \n", source_gates) 

    print("\ndb gates : \n", gatesdb)
    print("\ndb relations : \n", relationsdb)
    print("\ntolerance : ", tolerance)

    real_gates, efficiency = find_real_gates(source_gates,gatesdb, relationsdb, tolerance)

    print("\nThe efficiency of the solution is : ", efficiency)
    
    return parser.parse(s)
