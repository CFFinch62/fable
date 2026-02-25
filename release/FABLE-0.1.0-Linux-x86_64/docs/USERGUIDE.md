# FABLE User Guide

**Forth Animated Beginners Learning Environment**

---

## Introduction

FABLE is an education-focused IDE designed to teach the Forth programming language through visualization. It makes the abstract concept of a stack concrete by showing you exactly what happens with every operation.

**Key Features:**
- **Visual Stack** — Color-coded, animated stack visualization
- **Smart Editor** — Syntax highlighting, line numbers, and auto-indentation
- **Project Management** — File browser with bookmarks and persistence
- **Interactive REPL** — Immediate feedback loop for testing code
- **Theming** — Dark and Light modes to suit your preference

---

## Interface Guide

### 1. File Browser
Navigate your project files easily.
- **Bookmarks (★)**: Click the star icon to bookmark the current folder. Click it again to jump to saved locations.
- **Persistence**: FABLE remembers your last open folder and bookmarks between sessions.
- **Context Menu**: Right-click files to Rename, Delete, or Reveal in your system file manager.

### 2. The Editor
A robust code editor for writing Forth source files (`.fs`, `.fth`).
- **Theming**: Switch between Dark and Light themes via the `View > Theme` menu.
- **Line Numbers**: Brightly colored for easy readability.

### 3. Stack Visualizer
The heart of FABLE. It visualizes both the **Data Stack** (left) and **Return Stack** (right).

#### **Color Legend**
Items on the stack are color-coded by type:
- 🔵 **Blue**: Integer numbers
- 🟢 **Green**: Floating-point numbers
- 🟣 **Purple**: Strings
- ⚪ **Teal**: Booleans (includes `TRUE`/-1 and `FALSE`/0)
- 🟠 **Orange**: Addresses

#### **Animation Speed**
Control how fast code executes using the slider at the bottom of the stack panel:
- **Slide Right**: **Faster** (Reduced delay)
- **Slide Left**: **Slower** (Increased delay for debugging)
- **Step Button**: Execute one word at a time for precise inspection.

### 4. The REPL
The Read-Eval-Print Loop allows you to type Forth commands and execute them immediately. Great for testing small snippets or checking the value of words.

#### **Special REPL Commands**
These commands are handled by the REPL itself, not the Forth interpreter:

| Command | Description |
|---------|-------------|
| `CLS` | Clear the REPL output text (does not affect the stack) |

**Note:** The Forth word `CLEAR` clears the data stack. Use `CLS` to clear the REPL terminal output.

---

## Getting Started

### Running FABLE

```bash
python3 main.py
```

### Your First Commands

Type in the REPL:

```forth
42 .                \ Push 42, then print it
1 2 + .             \ Push 1, 2, add them, print result (3)
: SQR DUP * ;       \ Define a word to square a number
5 SQR .             \ Uses SQR to print 25
```

---

## Common Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **Ctrl+N** | New file |
| **Ctrl+O** | Open file |
| **Ctrl+S** | Save file |
| **Ctrl+R** | Run current file |
| **F5** | Run selected text |
| **F10** | Step execution |
| **Ctrl+W** | Close tab |
| **Ctrl+Q** | Quit FABLE |

---

## Forth Reference

### Stack Manipulation

| Word | Stack Effect | Description |
|------|--------------|-------------|
| `DUP` | ( n -- n n ) | Duplicate top item |
| `DROP` | ( n -- ) | Discard top item |
| `SWAP` | ( a b -- b a ) | Swap top two items |
| `OVER` | ( a b -- a b a ) | Copy second item to top |
| `ROT` | ( a b c -- b c a ) | Rotate third item to top |
| `-ROT` | ( a b c -- c a b ) | Rotate top item to third |
| `NIP` | ( a b -- b ) | Drop item below top |
| `TUCK` | ( a b -- b a b ) | Tuck top item below second |
| `.S` | ( -- ) | **Debug**: Print entire stack without modifying it |

### Arithmetic

| Word | Description | Example |
|------|-------------|---------|
| `+` | Add | `3 4 +` → `7` |
| `-` | Subtract | `5 2 -` → `3` |
| `*` | Multiply | `3 3 *` → `9` |
| `/` | Integer Divide | `10 3 /` → `3` |
| `MOD` | Modulo (Remainder) | `10 3 MOD` → `1` |
| `/MOD` | Div & Mod | `10 3 /MOD` → `1 3` |

### Control Flow

**Conditionals:**
```forth
: CHECK ( n -- )
  0= IF ." Zero!" ELSE ." Non-zero!" THEN ;
```

**Counted Loops:**
```forth
: COUNT-UP ( n -- )
  0 DO I . LOOP ;  \ Prints 0 to n-1
```
*Use `UNLOOP` to exit a loop context cleanly if jumping out early.*

**Indefinite Loops:**
```forth
: WAIT-FOR-KEY
  BEGIN KEY? UNTIL ; \ Loops until a key is pressed
```

---

## Troubleshooting

- **"Unknown word":** Check for typos. Forth is case-insensitive in FABLE, but standard Forth is often case-sensitive.
- **"Stack Underflow":** You tried to pop more items than were on the stack. Use `.S` to check stack depth.
- **Loops not matching:** Ensure every `DO` has a `LOOP` (or `+LOOP`) and every `IF` has a `THEN`.

---

## Credits

© 2025 Chuck Finch - Fragillidae Software
Forth logic based on standard ANS Forth specificiations.
