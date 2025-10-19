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
├── 📜 lexer.py              → Token definitions using PLY (Lexical Analyzer)
├── 🧩 parser_bn.py           → Grammar rules for Bangla-Python (Parser via Yacc)
├── 🧠 semantic.py            → Symbol table management & semantic checking
├── ⚙️ ir_generator.py        → 3-Address Intermediate Representation (IR) generator
├── 🚀 optimizer.py           → Constant folding & simple optimizations
├── 🏗️ machine_code.py        → Pseudo machine code / target code generator
├── 🧭 main.py                → Compiler driver — runs the full pipeline
└── 📘 README.md              → You are here 😊

