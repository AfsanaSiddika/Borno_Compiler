# -------------------------------------------------------
# main.py — Borno Compiler Main Driver
# -------------------------------------------------------

import sys
from lexer import lexer
from parser_bn import parser
import semantic
from ir_generator import ir_code, generate_ir
from optimizer import constant_fold
from machine_code import generate_machine_code

# -------------------------------------------------------
# Read input code
# -------------------------------------------------------
def read_input_from_file_or_stdin():
    """
    Reads the source code from:
      - A file (if filename is passed as a command-line argument), OR
      - Standard input (user typing Bangla-Python code interactively).

    The function continues reading until the user types '#end' in a new line.
    Returns the full source code as a string.
    """
    if len(sys.argv) >= 2:
        # --- Read code from file ---
        fname = sys.argv[1]
        try:
            with open(fname, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Cannot open {fname}: {e}")
            sys.exit(1)
    else:
        # --- Interactive mode ---
        print("Enter Bangla-Python code. Type '#end' on a new line to finish input:")
        lines = []
        while True:
            try:
                ln = input()
            except EOFError:
                break
            if ln.strip() == "#end":  # <-- custom end marker
                break
            lines.append(ln)
        return "\n".join(lines)

# -------------------------------------------------------
# Lexical Analysis
# -------------------------------------------------------
def print_tokens(code):
    """
    Performs lexical analysis using the lexer.
    Prints each token with its line number, position, type, and value.
    """
    print("\n=== 1) Lexical Analysis (tokens) ===")
    lexer.input(code)
    for tok in lexer:
        print(f"{tok.lineno}:{tok.lexpos}\t{tok.type}\t{tok.value}")

# -------------------------------------------------------
# Full Compiler Pipeline Execution
# -------------------------------------------------------
def run_pipeline(code):
    """
    Runs the full compilation pipeline step-by-step:
      1. Lexical analysis
      2. Parsing (AST)
      3. Semantic analysis (symbol table)
      4. 3-Address Code generation
      5. Optimization
      6. Machine code generation
    Displays outputs at every stage for transparency.
    """

    # 1️⃣ Lexical Analysis
    print_tokens(code)

    # 2️⃣ Parsing
    print("\n=== 2) Parsing -> AST ===")
    tree = parser.parse(code)
    print(tree)

    if tree is None:
        print("[Error] Parse failed. Compilation aborted.")
        return

    # 3️⃣ Semantic Analysis
    semantic.symbol_table.clear()
    semantic.walk_and_fill(tree)
    print("\n=== 3) Semantic Analysis (symbol table) ===")
    print("Name       Type       Value")
    for n, info in semantic.symbol_table.items():
        v = info['value'] if info['value'] is not None else "unknown"
        print(f"{n:<10} {info['type']:<10} {v}")

    # 4️⃣ Intermediate Representation (3-Address Code)
    ir_code.clear()
    generate_ir(tree)
    print("\n=== 4) 3-Address IR ===")
    for L in ir_code:
        print(L)

    # 5️⃣ IR Optimization (Constant Folding)
    opt_ir = constant_fold(ir_code, semantic.symbol_table)
    print("\n=== 5) Optimized IR ===")
    for L in opt_ir:
        print(L)

    # 6️⃣ Target Machine Code Generation
    mc = generate_machine_code(opt_ir)
    print("\n=== 6) Target Machine Code ===")
    for L in mc:
        print(L)

# -------------------------------------------------------
# Entry Point
# -------------------------------------------------------
if __name__ == '__main__':
    """
    The main entry point for the compiler.
    Reads the Bangla-Python source code and executes the compilation pipeline.
    """
    code = read_input_from_file_or_stdin()
    run_pipeline(code)
