# FABLE User Guide

**Forth Animated Beginners Learning Environment**

---

## Introduction

FABLE is an educational Forth programming environment designed for beginners. It features:

- **Visual stack animations** — See how stack operations work
- **Syntax highlighting** — Color-coded Forth code
- **Interactive REPL** — Immediate feedback on commands
- **Step-through debugging** — Watch code execute step by step

---

## Getting Started

### Running FABLE

```bash
python3 main.py
```

### Your First Forth Commands

Type in the REPL at the bottom:

```forth
42                  \ Push 42 onto the stack
.                   \ Pop and print: 42
3 4 +               \ Push 3, push 4, add them
.                   \ Print: 7
```

### Understanding the Stack

Forth uses a stack to hold values. Numbers push onto the stack, operations pop values and push results:

```forth
5 3 -    \ 5 - 3 = 2 (left on stack)
2 *      \ 2 * 2 = 4
.        \ prints 4
```

---

## Interface Overview

| Panel | Description |
|-------|-------------|
| **Editor** | Write and edit Forth programs |
| **File Browser** | Navigate project files |
| **Stack Display** | Watch stack operations animate |
| **REPL** | Interactive command line |

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+N | New file |
| Ctrl+O | Open file |
| Ctrl+S | Save file |
| Ctrl+R | Run current file |
| F5 | Run selection |
| F10 | Step execution |

---

## Stack Operations

### Basic Operations

| Word | Stack Effect | Description |
|------|--------------|-------------|
| DUP | ( n -- n n ) | Duplicate top |
| DROP | ( n -- ) | Remove top |
| SWAP | ( n1 n2 -- n2 n1 ) | Exchange top two |
| OVER | ( n1 n2 -- n1 n2 n1 ) | Copy second to top |
| ROT | ( n1 n2 n3 -- n2 n3 n1 ) | Rotate third to top |

### Examples

```forth
1 2 DUP     \ Stack: 1 2 2
1 2 3 ROT   \ Stack: 2 3 1
5 3 SWAP    \ Stack: 3 5
```

---

## Arithmetic

| Word | Stack Effect | Description |
|------|--------------|-------------|
| + | ( n1 n2 -- sum ) | Add |
| - | ( n1 n2 -- diff ) | Subtract |
| * | ( n1 n2 -- prod ) | Multiply |
| / | ( n1 n2 -- quot ) | Divide |
| MOD | ( n1 n2 -- rem ) | Remainder |
| NEGATE | ( n -- -n ) | Negate |
| ABS | ( n -- \|n\| ) | Absolute value |

### Examples

```forth
10 3 /      \ Integer division: 3
10 3 MOD    \ Remainder: 1
-5 ABS      \ Absolute value: 5
```

---

## Comparison & Logic

| Word | Stack Effect | Description |
|------|--------------|-------------|
| = | ( n1 n2 -- flag ) | Equal |
| < | ( n1 n2 -- flag ) | Less than |
| > | ( n1 n2 -- flag ) | Greater than |
| 0= | ( n -- flag ) | Equal to zero |
| AND | ( n1 n2 -- n ) | Bitwise AND |
| OR | ( n1 n2 -- n ) | Bitwise OR |
| NOT | ( flag -- flag ) | Logical NOT |

Forth uses -1 for TRUE and 0 for FALSE.

---

## Defining Words

Create new words with `:` (colon) and `;` (semicolon):

```forth
: SQUARE DUP * ;
5 SQUARE .          \ prints 25

: CUBE DUP DUP * * ;
3 CUBE .            \ prints 27
```

---

## Control Flow

### Conditionals

```forth
: ABS DUP 0< IF NEGATE THEN ;
: MAX 2DUP < IF SWAP THEN DROP ;
```

### Counted Loops

```forth
: STARS 0 DO 42 EMIT LOOP ;
5 STARS             \ prints *****

: SQUARES 5 0 DO I DUP * . LOOP ;
SQUARES             \ prints 0 1 4 9 16
```

### Indefinite Loops

```forth
: COUNTDOWN
  10 BEGIN
    DUP . 1-
    DUP 0=
  UNTIL DROP ;
```

---

## Output

| Word | Description |
|------|-------------|
| . | Print and remove top value |
| .S | Show entire stack |
| CR | Print newline |
| SPACE | Print a space |
| EMIT | Print character (ASCII) |
| WORDS | List all defined words |

---

## Tips for Beginners

1. **Think in stacks** — Values go on, operations take them off
2. **Read right to left** — `3 4 +` means "push 3, push 4, add"
3. **Use .S often** — Check your stack state
4. **Define small words** — Build up from simple pieces
5. **Watch the animations** — They show what's happening

---

## Example Programs

### Factorial

```forth
: FACTORIAL
  DUP 1 <= IF DROP 1 EXIT THEN
  DUP 1- RECURSE *
;
5 FACTORIAL .       \ prints 120
```

### Fibonacci

```forth
: FIB
  0 1 ROT 0 DO
    OVER + SWAP
  LOOP DROP
;
10 FIB .            \ prints 55
```

### Temperature Conversion

```forth
: F>C 32 - 5 * 9 / ;
: C>F 9 * 5 / 32 + ;

212 F>C .           \ prints 100
100 C>F .           \ prints 212
```

---

## Error Messages

FABLE provides helpful error messages:

- **Stack underflow** — Not enough values on stack
- **Unknown word** — Word not defined (check spelling)
- **Division by zero** — Cannot divide by zero

---

## Further Learning

- [Starting Forth](https://www.forth.com/starting-forth/) — Classic tutorial
- [Thinking Forth](http://thinking-forth.sourceforge.net/) — Philosophy of Forth
