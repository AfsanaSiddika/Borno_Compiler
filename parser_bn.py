# parser_bn.py

import ply.yacc as yacc
from lexer import tokens, lexer

# Operator precedence and associativity
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIV'),
    ('nonassoc', 'LT', 'GT', 'EQ'),
)

# program -> stmt_list
def p_program(p):
    'program : stmt_list'
    p[0] = ('program', p[1])   # Root node for the program

# stmt_list -> stmt_list stmt
def p_stmt_list_many(p):
    'stmt_list : stmt_list stmt'
    p[0] = p[1] + [p[2]]       # Append statement to list

# stmt_list -> stmt
def p_stmt_list_one(p):
    'stmt_list : stmt'
    p[0] = [p[1]]              # Start new statement list

# Assignment statement
def p_stmt_assign(p):
    'stmt : ID ASSIGN expr SEMICOLON'
    p[0] = ('assign', p[1], p[3])  # Assignment node

# Print statement
def p_stmt_print(p):
    'stmt : PRINT_BN LPAREN expr RPAREN SEMICOLON'
    p[0] = ('print', p[3])         # Print node

# Return statement
def p_stmt_return(p):
    'stmt : RETURN_BN LPAREN expr RPAREN SEMICOLON'
    p[0] = ('return', p[3])        # Return node

# Input statement
def p_stmt_input(p):
    'stmt : ID ASSIGN INPUT_BN LPAREN STRING RPAREN SEMICOLON'
    p[0] = ('input', p[1], p[5])   # Input node (variable, prompt)

# If-Else statement
def p_stmt_ifelse(p):
    'stmt : IF_BN LPAREN expr RPAREN LBRACE stmt_list RBRACE ELSE_BN LBRACE stmt_list RBRACE'
    p[0] = ('ifelse', p[3], p[6], p[10])  # If-else node (condition, then, else)

# While loop
def p_stmt_while(p):
    'stmt : WHILE_BN LPAREN expr RPAREN LBRACE stmt_list RBRACE'
    p[0] = ('while', p[3], p[6])          # While node (condition, body)

# Expression: binary operations
def p_expr_binop(p):
    '''expr : expr PLUS expr
            | expr MINUS expr
            | expr MULT expr
            | expr DIV expr
            | expr LT expr
            | expr GT expr
            | expr EQ expr'''
    p[0] = (p[2], p[1], p[3])            # Binary operation node

# Parenthesized expression
def p_expr_paren(p):
    'expr : LPAREN expr RPAREN'
    p[0] = p[2]                          # Return inner expression

# Integer literal
def p_expr_int(p):
    'expr : INT'
    p[0] = ('num', p[1])                 # Integer literal node

# Float literal
def p_expr_float(p):
    'expr : FLOAT'
    p[0] = ('num', p[1])                 # Float literal node

# String literal
def p_expr_string(p):
    'expr : STRING'
    p[0] = ('str', p[1])                 # String literal node

# Identifier (variable)
def p_expr_id(p):
    'expr : ID'
    p[0] = ('id', p[1])                  # Variable reference node

# Syntax error handler
def p_error(p):
    if p:
        print(f"[Syntax Error] Unexpected token {p.value!r} (type {p.type}) at line {p.lineno}")
    else:
        print("[Syntax Error] Unexpected end of input")

# Build the parser
parser = yacc.yacc()
