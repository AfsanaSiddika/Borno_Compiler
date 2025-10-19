# optimizer.py
import re

# =======================
#  Helpers
# =======================

def is_number(value: str) -> bool:
    """Check if a string is an integer or float literal."""
    return re.match(r'^-?\d+(\.\d+)?$', str(value)) is not None


def compute_binary(a, op, b):
    """Compute binary operation result between two numeric literals."""
    if '.' in str(a) or '.' in str(b) or op == '/':
        a = float(a)
        b = float(b)
    else:
        a = int(a)
        b = int(b)

    if op == '+': res = a + b
    elif op == '-': res = a - b
    elif op == '*': res = a * b
    elif op == '/': res = a / b
    elif op == '<': res = 1 if a < b else 0
    elif op == '>': res = 1 if a > b else 0
    elif op == '==': res = 1 if a == b else 0
    else: raise ValueError(f"Unknown operator: {op}")

    if isinstance(res, float) and res.is_integer():
        res = int(res)
    return res


def parse_binary_expr(rhs: str):
    """Detect and split a binary expression into (a, op, b)."""
    for op in [' + ', ' - ', ' * ', ' / ', ' < ', ' > ', ' == ']:
        if op in rhs:
            a, b = rhs.split(op)
            return a.strip(), op.strip(), b.strip()
    return None


# =======================
#  Optimization Steps
# =======================

def fold_constants(ir_lines, const_values):
    """Perform constant folding and propagation on IR lines."""
    folded = []

    for line in ir_lines:
        parts = line.split()
        if len(parts) >= 3 and parts[1] == '=':
            lhs = parts[0]
            rhs = " ".join(parts[2:])
            expr = parse_binary_expr(rhs)

            if expr:
                a, oper, b = expr
                aval = const_values.get(a, a)
                bval = const_values.get(b, b)

                if is_number(aval) and is_number(bval):
                    try:
                        res = compute_binary(aval, oper, bval)
                        folded.append(f"{lhs} = {res}")
                        const_values[lhs] = str(res)
                        continue
                    except Exception:
                        pass

                folded.append(line)
            else:
                # simple assignment / propagation
                if rhs.startswith('"') and rhs.endswith('"'):
                    const_values[lhs] = rhs
                elif is_number(rhs):
                    const_values[lhs] = rhs
                elif rhs in const_values:
                    rhs_val = const_values[rhs]
                    folded.append(f"{lhs} = {rhs_val}")
                    const_values[lhs] = rhs_val
                    continue

                folded.append(line)
        else:
            folded.append(line)

    return folded


def remove_redundant_gotos(ir_lines):
    """Remove redundant GOTO immediately followed by its target label."""
    optimized = []
    i = 0
    while i < len(ir_lines):
        line = ir_lines[i]
        if line.startswith("GOTO "):
            target = line.split()[1]
            if i + 1 < len(ir_lines) and ir_lines[i + 1].startswith(f"LABEL {target}"):
                i += 1  # skip redundant
                continue
        optimized.append(line)
        i += 1
    return optimized


# =======================
#  Main Function
# =======================

def constant_fold(ir_lines, symbol_table):
    """
    Performs:
      1. Constant folding (e.g. t = 2 + 3 → t = 5)
      2. Constant propagation (e.g. y = t → y = 5)
      3. Redundant GOTO removal
    """
    const_values = {}
    step1 = fold_constants(ir_lines, const_values)
    optimized = remove_redundant_gotos(step1)
    return optimized
