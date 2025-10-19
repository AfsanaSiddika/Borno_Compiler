# -------------------------------------------------------
# ir_generator.py — Three Address Code (TAC) Generator
# -------------------------------------------------------
# Converts the Abstract Syntax Tree (AST) from the parser
# into intermediate 3-address code (IR).
# This IR is later optimized and translated to machine code.
# -------------------------------------------------------

from semantic import symbol_table

# Global counters
temp_count = 0
label_count = 0

# Holds generated 3-address code instructions
ir_code = []

# -------------------------------------------------------
# Helper functions for generating new temporaries & labels
# -------------------------------------------------------
def new_temp():
    """Generate a unique temporary variable name (t1, t2, ...)."""
    global temp_count
    temp_count += 1
    return f"t{temp_count}"

def new_label():
    """Generate a unique label name (L1, L2, ...)."""
    global label_count
    label_count += 1
    return f"L{label_count}"

# -------------------------------------------------------
# Expression Flattener
# Converts nested expressions into a linear TAC form.
# -------------------------------------------------------
def flatten_expr(expr):
    """Return a variable/literal/temp name for the expression.
       If it's a compound expression, emit intermediate IR lines.
    """
    if expr is None:
        return "0"

    kind = expr[0]

    # --- Literals and identifiers ---
    if kind == 'num':
        return str(expr[1])
    elif kind == 'str':
        return f"\"{expr[1]}\""
    elif kind == 'id':
        return expr[1]

    # --- Binary operation ---
    op = expr[0]
    left = flatten_expr(expr[1])
    right = flatten_expr(expr[2])
    t = new_temp()
    ir_code.append(f"{t} = {left} {op} {right}")
    return t

# -------------------------------------------------------
# Individual node handlers
# -------------------------------------------------------
def handle_assign(node):
    """Handle assignment: x = expr"""
    target = node[1]
    rhs = flatten_expr(node[2])
    ir_code.append(f"{target} = {rhs}")

def handle_input(node):
    """Handle user input: inputProdanKoren(msg)"""
    name = node[1]
    msg = node[2]
    ir_code.append(f"{name} = INPUT \"{msg}\"")

def handle_print(node):
    """Handle print statements: printkoriyaden(expr)"""
    val = flatten_expr(node[1])
    ir_code.append(f"PRINT {val}")

def handle_return(node):
    """Handle return statements: ferotpattiaden(expr)"""
    val = flatten_expr(node[1])
    ir_code.append(f"RETURN {val}")

def handle_ifelse(node):
    """Handle Bangla IF-ELSE: jodi ... othoba ..."""
    cond = flatten_expr(node[1])
    L1 = new_label()
    L2 = new_label()

    ir_code.append(f"IF_FALSE {cond} GOTO {L1}")
    for s in node[2]:  # if block
        generate_ir(s)
    ir_code.append(f"GOTO {L2}")
    ir_code.append(f"LABEL {L1}")
    for s in node[3]:  # else block
        generate_ir(s)
    ir_code.append(f"LABEL {L2}")

def handle_while(node):
    """Handle Bangla while loop: jotokhon (cond) { ... }"""
    Ls = new_label()
    Le = new_label()

    ir_code.append(f"LABEL {Ls}")
    cond = flatten_expr(node[1])
    ir_code.append(f"IF_FALSE {cond} GOTO {Le}")

    for s in node[2]:
        generate_ir(s)

    ir_code.append(f"GOTO {Ls}")
    ir_code.append(f"LABEL {Le}")

# -------------------------------------------------------
# Dispatcher: Main recursive IR generator
# -------------------------------------------------------
def generate_ir(node):
    """Recursively traverse the AST and build 3-address code."""
    if node is None:
        return

    kind = node[0]

    if kind == 'program':
        for s in node[1]:
            generate_ir(s)

    elif kind == 'assign':
        handle_assign(node)

    elif kind == 'input':
        handle_input(node)

    elif kind == 'print':
        handle_print(node)

    elif kind == 'return':
        handle_return(node)

    elif kind == 'ifelse':
        handle_ifelse(node)

    elif kind == 'while':
        handle_while(node)

    else:
        print(f"[IR Warning] Unknown node type: {kind}")

# -------------------------------------------------------
# Utility: Pretty-print or retrieve the generated IR
# -------------------------------------------------------
def get_ir():
    """Return the generated 3-address code list."""
    return ir_code

def print_ir():
    """Print formatted IR code to the console."""
    print("\n=== 4) 3-Address IR ===")
    for line in ir_code:
        print(line)
