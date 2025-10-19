# machine_code.py
# ====================================================
# Machine Code Generator (from Intermediate Code)
# ====================================================

def generate_machine_code(ir_lines):
    """Main entry: convert IR code lines into pseudo machine code."""
    mc = []
    for line in ir_lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("PRINT "):
            mc.append(_handle_print(line))

        elif line.startswith("RETURN "):
            mc.append(_handle_return(line))

        elif line.startswith("LABEL "):
            mc.append(_handle_label(line))

        elif line.startswith("IF_FALSE "):
            mc.extend(_handle_if_false(line))

        elif line.startswith("GOTO "):
            mc.append(_handle_goto(line))

        elif " = INPUT " in line:
            mc.append(_handle_input(line))

        else:
            mc.append(_handle_assignment(line))

    return mc


# ====================================================
# 1️⃣  Handlers for each IR operation type
# ====================================================

def _handle_print(line):
    """Translate IR: PRINT x  →  MC: OUT x"""
    return "OUT " + line[len("PRINT "):]


def _handle_return(line):
    """Translate IR: RETURN a  →  MC: RET a"""
    return "RET " + line[len("RETURN "):]


def _handle_label(line):
    """Translate IR: LABEL L1  →  MC: L1:"""
    return line.split()[1] + ":"


def _handle_if_false(line):
    """Translate IR: IF_FALSE cond GOTO Lx"""
    parts = line.split()
    if len(parts) < 4:
        return [f"; [Error] Invalid IF_FALSE syntax: {line}"]

    cond = parts[1]
    label = parts[-1]
    return [
        f"CMP {cond} ; if false jump {label}",
        f"JZ {label}"
    ]


def _handle_goto(line):
    """Translate IR: GOTO Lx  →  MC: JMP Lx"""
    label = line.split()[1]
    return "JMP " + label


def _handle_input(line):
    """Translate IR: x = INPUT "msg"  →  MC: INP x ; prompt "msg" """
    var, rest = line.split(" = ", 1)
    prompt = rest[len("INPUT "):]
    return f"INP {var} ; prompt {prompt}"


def _handle_assignment(line):
    """Translate IR: a = b + c  →  MC: MOV a = b + c"""
    return "MOV " + line


# ====================================================
# 2️⃣  Optional Debug Printer
# ====================================================

def show_machine_code(mc_lines):
    """Pretty print the generated machine code."""
    print("\n=== Machine Code ===")
    for line in mc_lines:
        print(line)
