# 🔍 Python Beginner Code Visualizer

An interactive, lightweight, zero-dependency web-based Python execution visualizer designed for students and beginners to see how code runs step-by-step.

![Python Visualizer](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-success?style=for-the-badge)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

---

## ✨ Features

- **Step-by-Step Execution:** Walk forward and backward through code lines using `Next Step ▶` and `◀ Prev Step`.
- **Live Memory Inspector:** Inspect local variables, data types (`int`, `float`, `str`, `list`), and track value changes in real-time.
- **Line Highlighting:** See the exact line currently being executed highlighted in bright blue.
- **Built-in Console:** Watch standard `print()` output appear synchronously with execution.
- **Preset Examples:** Comes with interactive examples covering:
  1. Basic Arithmetic & Variable Reassignment
  2. For Loops & Accumulators
  3. If-Else Conditional Branches
  4. Function Calls & Return Values (Scientific energy calculations)
- **Zero Dependencies:** Pure Python standard library (`http.server`, `sys.settrace`, `json`). No Flask, Django, or external packages required!

---

## 🚀 Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/chemsiva/python-code-visualizer.git
   cd python-code-visualizer
   ```

2. **Launch the Visualizer:**
   ```bash
   python3 server.py
   ```

3. **Open in your browser:**
   ```text
   http://localhost:8089
   ```

---

## 📸 How It Works

```
+------------------------------------+------------------------------------+
| 📝 1. Python Code Editor           | 👀 2. Execution Stepper            |
|                                    |    [◀ Prev Step]   [Next Step ▶]   |
|   x = 5                            |                                    |
|   y = 10                           |    ▶ line 3: total = x + y         |
|   total = x + y                    |                                    |
|                                    +------------------------------------+
|                                    | 📦 Computer Memory                 |
|                                    |    Variable | Type | Value        |
|                                    |    x        | int  | 5            |
|                                    |    y        | int  | 10           |
|                                    |    total    | int  | 15           |
+------------------------------------+------------------------------------+
```

---

## 📄 License

MIT License. Free for educational and teaching use.
