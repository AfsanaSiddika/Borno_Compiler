# -------------------------------------------------------
# lexer.py  —  Lexical Analyzer for Bangla Compiler
# -------------------------------------------------------
# This module uses PLY (Python Lex-Yacc) to tokenize
# Bangla-like keywords and syntax for a simple compiler.
# -------------------------------------------------------

import ply.lex as lex

# -------------------------------------------------------
# Token declarations
# -------------------------------------------------------
tokens = [
    'ID', 'INT', 'FLOAT', 'STRING',
    'ASSIGN',
    'PLUS', 'MINUS', 'MULT', 'DIV',
    'LT', 'GT', 'EQ',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'SEMICOLON', 'COMMA'
]

# -------------------------------------------------------
# Reserved words (Bangla keywords → token types)
# -------------------------------------------------------
reserved = {
    'printkoriyaden': 'PRINT_BN',       # print statement
    'ferotpattiaden': 'RETURN_BN',      # return statement
    'jodi': 'IF_BN',                    # if condition
    'othoba': 'ELSE_BN',                # else condition
    'jotokhon': 'WHILE_BN',             # while loop
    'inputProdanKoren': 'INPUT_BN'      # input function
}

# Add reserved tokens to main token list
tokens += list(reserved.values())

# -------------------------------------------------------
# Token regex rules (operators, punctuation, etc.)
# -------------------------------------------------------
t_ASSIGN    = r'='
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_MULT      = r'\*'
t_DIV       = r'/'
t_LT        = r'<'
t_GT        = r'>'
t_EQ        = r'=='
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LBRACE    = r'\{'
t_RBRACE    = r'\}'
t_SEMICOLON = r';'
t_COMMA     = r','

# -------------------------------------------------------
# Ignored characters (spaces, tabs, carriage returns)
# -------------------------------------------------------
t_ignore = ' \t\r'

# -------------------------------------------------------
# FLOAT: Handles numbers with a decimal point (e.g. 3.14)
# -------------------------------------------------------
def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# -------------------------------------------------------
# INT: Handles integer literals (e.g. 10, 42)
# -------------------------------------------------------
def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

# -------------------------------------------------------
# STRING: Handles text within double quotes (e.g. "Hello")
# -------------------------------------------------------
def t_STRING(t):
    r'\"([^\\\"]|\\.)*\"'
    t.value = t.value[1:-1]  # remove surrounding quotes
    return t

# -------------------------------------------------------
# ID: Variable names or reserved keywords (Bangla or Latin)
# -------------------------------------------------------
def t_ID(t):
    r'[a-zA-Z_]\w*'
    # Check if the identifier is a reserved word
    t.type = reserved.get(t.value, 'ID')
    return t

# -------------------------------------------------------
# NEWLINE: Tracks line numbers for better error reporting
# -------------------------------------------------------
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# -------------------------------------------------------
# COMMENTS: Ignore lines starting with '#' or '//'
# -------------------------------------------------------
def t_comment(t):
    r'(\#|//).*'
    pass  # simply skip comment lines

# -------------------------------------------------------
# ERROR HANDLER: Reports illegal or unknown characters
# -------------------------------------------------------
def t_error(t):
    print(f"[Lexical Error] Illegal character {t.value[0]!r} at line {t.lineno}")
    t.lexer.skip(1)

# -------------------------------------------------------
# Build the lexer
# -------------------------------------------------------
lexer = lex.lex()
