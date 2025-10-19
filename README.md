# 🐍 Borno Compiler
### A Bangla-inspired mini-compiler for "Bangla-Python" language 🇧🇩

Borno Compiler is a simple **Bangla-Python** style compiler written in Python.  
It performs **Lexical Analysis**, **Parsing (AST)**, **Semantic Checking**, **3-Address IR generation**,  
**Optimization (Constant Folding)**, and **Target Machine Code Generation** — all step by step!

---

## 🚀 Features

✅ **Lexical Analysis** — tokenizes identifiers, keywords, operators, literals  
✅ **Parser** — builds an Abstract Syntax Tree (AST)  
✅ **Semantic Analyzer** — manages a symbol table and type checking  
✅ **Intermediate Code (3-Address Form)** generation  
✅ **Constant Folding Optimizer**  
✅ **Machine Code Generator** (pseudo assembly-like)  
✅ **Interactive Mode** and **File Input Mode**

---

## 🧠 Project Structure
Borno_Compiler/
│
├── lexer.py # Token definitions (PLY)
├── parser_bn.py # Bangla-Python grammar parser (PLY)
├── semantic.py # Symbol table + type checking
├── ir_generator.py # 3-Address Code generation
├── optimizer.py # Constant folding optimization
├── machine_code.py # Machine code emitter
├── main.py # Compiler entry point (driver)
└── README.md # You are here 😊
