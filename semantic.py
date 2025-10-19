# semantic.py
# ----------------------------
# Symbol Table & Semantic Analysis
# ----------------------------

symbol_table = {}  # name -> {'type': str, 'value': constant or None}

# ====================================================
# 1️⃣  Expression Type Inference
# ====================================================
def infer_expr_type(expr):
    """Given an AST expr, infer its type and constant value if possible."""
    if expr is None:
        return 'unknown', None

    kind = expr[0]

    # Literals
    if kind == 'num':
        v = expr[1]
        return ('float', v) if isinstance(v, float) else ('int', v)

    if kind == 'str':
        return 'string', expr[1]

    # Identifier
    if kind == 'id':
        name = expr[1]
        info = symbol_table.get(name)
        return (info['type'], info.get('value')) if info else ('unknown', None)

    # Binary Operation
    op, left, right = expr[0], expr[1], expr[2]
    lt, lv = infer_expr_type(left)
    rt, rv = infer_expr_type(right)

    # String concatenation allowed only with '+'
    if lt == 'string' or rt == 'string':
        if op == '+':
            return 'string', None
        return 'unknown', None

    # Float promotion
    if lt == 'float' or rt == 'float':
        const_val = _try_eval_float_op(op, lv, rv)
        return ('float', const_val)

    # Integer operation
    if lt == 'int' and rt == 'int':
        const_val, typ = _try_eval_int_op(op, lv, rv)
        return typ, const_val

    # Unknown combination
    return 'unknown', None


# ====================================================
# 2️⃣  Helper Functions for Constant Folding
# ====================================================

def _try_eval_float_op(op, lv, rv):
    """Try to evaluate float operation if both operands constant."""
    if lv is None or rv is None:
        return None
    try:
        if op == '+': return float(lv) + float(rv)
        if op == '-': return float(lv) - float(rv)
        if op == '*': return float(lv) * float(rv)
        if op == '/': return float(lv) / float(rv)
        if op == '<': return 1 if float(lv) < float(rv) else 0
        if op == '>': return 1 if float(lv) > float(rv) else 0
        if op == '==': return 1 if float(lv) == float(rv) else 0
    except Exception:
        pass
    return None


def _try_eval_int_op(op, lv, rv):
    """Try to evaluate integer operation if both operands constant."""
    if lv is None or rv is None:
        return None, 'int' if op != '/' else 'float'
    try:
        if op == '+': return lv + rv, 'int'
        if op == '-': return lv - rv, 'int'
        if op == '*': return lv * rv, 'int'
        if op == '/': return lv / rv, 'float'
        if op == '<': return (1 if lv < rv else 0), 'int'
        if op == '>': return (1 if lv > rv else 0), 'int'
        if op == '==': return (1 if lv == rv else 0), 'int'
    except Exception:
        pass
    return None, 'int'


# ====================================================
# 3️⃣  ID Collection & Usage Checks
# ====================================================

def collect_ids(expr):
    """Recursively collect identifiers in expressions."""
    if expr is None:
        return
    kind = expr[0]
    if kind == 'id':
        name = expr[1]
        if name not in symbol_table:
            print(f"[Semantic Warning] '{name}' used before assignment — marked unknown.")
            symbol_table[name] = {'type': 'unknown', 'value': None}
    elif kind in ('num', 'str'):
        return
    else:
        collect_ids(expr[1])
        collect_ids(expr[2])


# ====================================================
# 4️⃣  Main Semantic Pass (Walk & Fill)
# ====================================================

def walk_and_fill(node):
    """Walk the AST and fill the symbol table, check undeclared usage."""
    if node is None:
        return

    kind = node[0]

    if kind == 'program':
        for stmt in node[1]:
            walk_and_fill(stmt)

    elif kind == 'assign':
        name = node[1]
        typ, val = infer_expr_type(node[2])
        symbol_table[name] = {'type': typ, 'value': val}

    elif kind == 'input':
        name = node[1]
        symbol_table[name] = {'type': 'unknown', 'value': None}

    elif kind in ('print', 'return'):
        collect_ids(node[1])

    elif kind == 'ifelse':
        collect_ids(node[1])
        for s in node[2]:
            walk_and_fill(s)
        for s in node[3]:
            walk_and_fill(s)

    elif kind == 'while':
        collect_ids(node[1])
        for s in node[2]:
            walk_and_fill(s)

# ====================================================
# 5️⃣  Entry Point
# ====================================================

def perform_semantic_analysis(ast_root):
    """Main entry for semantic analysis."""
    global symbol_table
    symbol_table = {}
    walk_and_fill(ast_root)
    print("\n=== Semantic Analysis Complete ===")
    for name, info in symbol_table.items():
        print(f"{name:<15} type={info['type']:<8} value={info['value']}")
    return symbol_table
