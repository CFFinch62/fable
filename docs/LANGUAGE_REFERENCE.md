# FABLE Language Reference

## Forth Animated Beginners Learning Environment

**Version:** 1.0  
**Complete Language Reference Guide**

---

## Table of Contents

1. [Introduction](#introduction)
2. [Basic Concepts](#basic-concepts)
3. [Lexical Structure](#lexical-structure)
4. [Data Types](#data-types)
5. [Stack Manipulation Words](#stack-manipulation-words)
6. [Arithmetic Words](#arithmetic-words)
7. [Comparison Words](#comparison-words)
8. [Logic and Bitwise Words](#logic-and-bitwise-words)
9. [Control Flow](#control-flow)
10. [Defining Words](#defining-words)
11. [Input/Output Words](#inputoutput-words)
12. [Error Types](#error-types)
13. [Stack Effect Notation](#stack-effect-notation)
14. [Examples](#examples)

---

## Introduction

FABLE (Forth Animated Beginners Learning Environment) is an educational Forth implementation designed to teach stack-based programming through visual feedback. This reference documents all built-in words, syntax rules, and language features.

Forth is a **stack-based**, **concatenative** programming language where:
- Data is manipulated on a stack (LIFO - Last In, First Out)
- Operations are written in **postfix notation** (Reverse Polish Notation)
- New words (functions) can be defined to extend the language
- Words are case-insensitive (`DUP`, `dup`, and `Dup` are equivalent)

---

## Basic Concepts

### The Data Stack

The data stack is the primary workspace in Forth. Numbers are pushed onto the stack, and operations consume values from the stack and push results back.

```forth
5 3 +      \ Push 5, push 3, add them → stack contains 8
```

### The Return Stack

A secondary stack used internally for:
- Loop indices in `DO...LOOP` constructs
- Return addresses during word execution
- Temporary storage (advanced usage with `>R` and `R>`)

### The Dictionary

All words (built-in and user-defined) are stored in the dictionary. Words are looked up case-insensitively.

---

## Lexical Structure

### Whitespace

Words are separated by whitespace (spaces, tabs, newlines). Forth treats all whitespace equivalently.

### Comments

| Syntax | Description | Example |
|--------|-------------|---------|
| `\ comment` | Line comment (backslash to end of line) | `\ This is a comment` |
| `( comment )` | Parenthetical comment (must have space after `(`) | `( This is a comment )` |

**Note:** Stack effect comments like `( n1 n2 -- sum )` are a convention using parenthetical comments.

### Number Literals

| Format | Description | Example |
|--------|-------------|---------|
| Decimal | Standard integers | `42`, `-17`, `0` |
| Hexadecimal (`$`) | Forth-style hex prefix | `$FF`, `$1A2B` |
| Hexadecimal (`0x`) | C-style hex prefix | `0xFF`, `0x1a2b` |
| Floating-point | Numbers with decimal point | `3.14`, `-2.5`, `0.001` |

### String Literals

| Syntax | Description | Example |
|--------|-------------|---------|
| `." string"` | Print string immediately (compile-time) | `." Hello, World!"` |
| `.( string)` | Print string immediately (immediate) | `.( Hello!)` |
| `S" string"` | Create string on stack | `S" test"` |

**Note:** There must be exactly one space after `."` or `S"` before the string content.

### Word Names

Word names can contain almost any printable character except whitespace. Common conventions:
- Uppercase for standard words: `DUP`, `SWAP`, `IF`
- Descriptive names with hyphens: `COUNT-DOWN`, `PRINT-HEADER`

---

## Data Types

| Type | Description | Stack Display | Examples |
|------|-------------|---------------|----------|
| Integer | Signed whole numbers (platform-sized) | Blue indicator | `42`, `-17`, `$FF` |
| Float | Double-precision floating-point | Green indicator | `3.14`, `-2.5` |
| String | Text strings | Purple indicator | `"hello"` |
| Boolean/Flag | `TRUE` (-1) or `FALSE` (0) | Cyan indicator | `-1`, `0` |
| Address | Memory addresses/pointers | Amber indicator | (internal) |

### Boolean Convention

Forth uses integers as boolean values:
- **TRUE** = `-1` (all bits set to 1)
- **FALSE** = `0` (all bits are 0)

Any non-zero value is considered "true" in conditional tests.

---

## Stack Manipulation Words

These words rearrange values on the data stack without performing calculations.

### Basic Stack Operations

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `DUP` | `( n -- n n )` | Duplicate top of stack |
| `DROP` | `( n -- )` | Discard top of stack |
| `SWAP` | `( n1 n2 -- n2 n1 )` | Exchange top two items |
| `OVER` | `( n1 n2 -- n1 n2 n1 )` | Copy second item to top |
| `ROT` | `( n1 n2 n3 -- n2 n3 n1 )` | Rotate third item to top |
| `-ROT` | `( n1 n2 n3 -- n3 n1 n2 )` | Rotate top to third position |
| `NIP` | `( n1 n2 -- n2 )` | Drop second item |
| `TUCK` | `( n1 n2 -- n2 n1 n2 )` | Copy top below second |

### Double-Cell Operations

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `2DUP` | `( n1 n2 -- n1 n2 n1 n2 )` | Duplicate top pair |
| `2DROP` | `( n1 n2 -- )` | Drop top pair |
| `2SWAP` | `( n1 n2 n3 n4 -- n3 n4 n1 n2 )` | Swap pairs |
| `2OVER` | `( n1 n2 n3 n4 -- n1 n2 n3 n4 n1 n2 )` | Copy second pair to top |

### Stack Inspection

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `DEPTH` | `( -- n )` | Push current stack depth |
| `PICK` | `( n -- item )` | Copy nth item to top (0 = top) |
| `ROLL` | `( n -- )` | Rotate nth item to top |
| `CLEAR` | `( ... -- )` | Clear entire stack |

### Stack Operation Examples

```forth
\ DUP example: duplicate for use in multiple operations
5 DUP * .           \ Output: 25 (5 * 5)

\ SWAP example: reorder for subtraction
10 3 SWAP - .       \ Output: -7 (3 - 10)

\ OVER example: access second item without losing it
1 2 OVER . . .      \ Output: 1 2 1

\ ROT example: bring third item to top
1 2 3 ROT . . .     \ Output: 1 3 2
```

---

## Arithmetic Words

All arithmetic operations consume their operands and push the result.

### Basic Arithmetic

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `+` | `( n1 n2 -- sum )` | Addition |
| `-` | `( n1 n2 -- diff )` | Subtraction (n1 - n2) |
| `*` | `( n1 n2 -- prod )` | Multiplication |
| `/` | `( n1 n2 -- quot )` | Division (n1 / n2), integer if both operands are integers |
| `MOD` | `( n1 n2 -- rem )` | Modulo (remainder of n1 / n2) |
| `/MOD` | `( n1 n2 -- rem quot )` | Division with remainder |

### Unary Operations

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `NEGATE` | `( n -- -n )` | Negate (change sign) |
| `ABS` | `( n -- \|n\| )` | Absolute value |
| `1+` | `( n -- n+1 )` | Increment by 1 |
| `1-` | `( n -- n-1 )` | Decrement by 1 |
| `2+` | `( n -- n+2 )` | Add 2 |
| `2-` | `( n -- n-2 )` | Subtract 2 |
| `2*` | `( n -- n*2 )` | Double (left shift by 1) |
| `2/` | `( n -- n/2 )` | Halve (right shift by 1) |

### Binary Operations

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `MIN` | `( n1 n2 -- min )` | Minimum of two values |
| `MAX` | `( n1 n2 -- max )` | Maximum of two values |

### Arithmetic Examples

```forth
\ Basic math
10 3 + .            \ Output: 13
10 3 - .            \ Output: 7
10 3 * .            \ Output: 30
10 3 / .            \ Output: 3 (integer division)
10 3 MOD .          \ Output: 1 (remainder)

\ Division with remainder
10 3 /MOD . .       \ Output: 3 1 (quotient, then remainder)

\ Unary operations
-5 ABS .            \ Output: 5
7 NEGATE .          \ Output: -7
```

---

## Comparison Words

Comparison words push a boolean flag: `-1` (TRUE) or `0` (FALSE).

### Binary Comparisons

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `=` | `( n1 n2 -- flag )` | Equal |
| `<>` | `( n1 n2 -- flag )` | Not equal |
| `<` | `( n1 n2 -- flag )` | Less than (n1 < n2) |
| `>` | `( n1 n2 -- flag )` | Greater than (n1 > n2) |
| `<=` | `( n1 n2 -- flag )` | Less than or equal |
| `>=` | `( n1 n2 -- flag )` | Greater than or equal |

### Zero Comparisons

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `0=` | `( n -- flag )` | Equal to zero (logical NOT) |
| `0<` | `( n -- flag )` | Less than zero (negative) |
| `0>` | `( n -- flag )` | Greater than zero (positive) |

### Comparison Examples

```forth
5 3 > .             \ Output: -1 (TRUE: 5 > 3)
5 3 < .             \ Output: 0 (FALSE: 5 is not < 3)
5 5 = .             \ Output: -1 (TRUE: equal)
0 0= .              \ Output: -1 (TRUE: 0 equals zero)
-5 0< .             \ Output: -1 (TRUE: negative)
```

---

## Logic and Bitwise Words

These words perform bitwise operations on integer values.

### Bitwise Operations

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `AND` | `( n1 n2 -- n )` | Bitwise AND |
| `OR` | `( n1 n2 -- n )` | Bitwise OR |
| `XOR` | `( n1 n2 -- n )` | Bitwise XOR |
| `INVERT` | `( n -- ~n )` | Bitwise NOT (one's complement) |
| `LSHIFT` | `( n1 n2 -- n )` | Left shift n1 by n2 bits |
| `RSHIFT` | `( n1 n2 -- n )` | Right shift n1 by n2 bits |

### Boolean Constants and Operations

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `TRUE` | `( -- -1 )` | Push true flag (-1) |
| `FALSE` | `( -- 0 )` | Push false flag (0) |
| `NOT` | `( flag -- flag )` | Logical NOT (0 becomes -1, non-zero becomes 0) |

### Logic Examples

```forth
TRUE .              \ Output: -1
FALSE .             \ Output: 0

\ Bitwise operations
$FF $0F AND .       \ Output: 15 ($0F)
$F0 $0F OR .        \ Output: 255 ($FF)
$FF $0F XOR .       \ Output: 240 ($F0)
$FF INVERT .        \ Output: -256 (two's complement)

\ Shift operations
1 4 LSHIFT .        \ Output: 16 (1 << 4)
16 2 RSHIFT .       \ Output: 4 (16 >> 2)
```

---

## Control Flow

Control flow words are **immediate** words that execute during compilation to build control structures.

### Conditionals: IF...ELSE...THEN

```forth
IF ... THEN
IF ... ELSE ... THEN
```

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `IF` | `( flag -- )` | Begin conditional; if flag is false, branch to ELSE or THEN |
| `ELSE` | `( -- )` | Alternative branch |
| `THEN` | `( -- )` | End conditional |

**Example:**
```forth
: SIGN ( n -- )
    DUP 0> IF
        DROP ." positive"
    ELSE
        DUP 0< IF
            DROP ." negative"
        ELSE
            DROP ." zero"
        THEN
    THEN ;
```

### Indefinite Loops: BEGIN...UNTIL

Loops until condition becomes true.

```forth
BEGIN ... UNTIL
```

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `BEGIN` | `( -- )` | Mark loop start |
| `UNTIL` | `( flag -- )` | If flag is false, branch back to BEGIN |

**Example:**
```forth
: COUNT-DOWN ( n -- )
    BEGIN
        DUP . CR
        1-
        DUP 0=
    UNTIL DROP ;

10 COUNT-DOWN       \ Prints 10 9 8 7 6 5 4 3 2 1
```

### Indefinite Loops: BEGIN...WHILE...REPEAT

Loops while condition is true.

```forth
BEGIN ... WHILE ... REPEAT
```

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `BEGIN` | `( -- )` | Mark loop start |
| `WHILE` | `( flag -- )` | If flag is false, exit loop; otherwise continue |
| `REPEAT` | `( -- )` | Branch back to BEGIN |

**Example:**
```forth
: HALVES ( n -- )
    BEGIN
        DUP 1 >
    WHILE
        DUP . 2/
    REPEAT DROP ;

64 HALVES           \ Prints 64 32 16 8 4 2
```

### Counted Loops: DO...LOOP

Execute a fixed number of times with an index.

```forth
limit start DO ... LOOP
limit start DO ... n +LOOP
```

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `DO` | `( limit start -- )` | Begin counted loop from start to limit-1 |
| `LOOP` | `( -- )` | Increment index by 1 and continue if index < limit |
| `+LOOP` | `( n -- )` | Add n to index and continue based on sign of n |
| `I` | `( -- n )` | Push current loop index |
| `J` | `( -- n )` | Push outer loop index (for nested loops) |
| `LEAVE` | `( -- )` | Exit loop immediately |
| `UNLOOP` | `( -- )` | Discard loop parameters from return stack |

**Examples:**
```forth
\ Print 0 to 4
: COUNT-5
    5 0 DO
        I .
    LOOP ;
COUNT-5             \ Output: 0 1 2 3 4

\ Print stars
: STARS ( n -- )
    0 DO
        42 EMIT     \ 42 is ASCII for '*'
    LOOP ;
5 STARS             \ Output: *****

\ Step by 2
: EVENS
    10 0 DO
        I .
    2 +LOOP ;
EVENS               \ Output: 0 2 4 6 8
```

### Other Control Words

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `EXIT` | `( -- )` | Exit current word immediately |

---

## Defining Words

### Colon Definitions

Create new words with `:` (colon) and `;` (semicolon).

```forth
: word-name ( stack-effect ) body... ;
```

**Syntax:**
- `:` begins the definition
- The next word becomes the name of the new word
- All following words are compiled (not executed)
- `;` ends the definition

**Example:**
```forth
: SQUARE ( n -- n^2 )
    DUP * ;

5 SQUARE .          \ Output: 25

: CUBE ( n -- n^3 )
    DUP DUP * * ;

3 CUBE .            \ Output: 27

: SUM-SQUARES ( a b -- sum )
    SQUARE SWAP SQUARE + ;

3 4 SUM-SQUARES .   \ Output: 25 (9 + 16)
```

### Recursion

Words can call themselves recursively:

```forth
: FACTORIAL ( n -- n! )
    DUP 1 > IF
        DUP 1- FACTORIAL *
    THEN ;

5 FACTORIAL .       \ Output: 120
```

---

## Input/Output Words

### Printing Values

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `.` | `( n -- )` | Print and remove top of stack (followed by space) |
| `.S` | `( -- )` | Print entire stack non-destructively |
| `CR` | `( -- )` | Print newline (carriage return) |
| `SPACE` | `( -- )` | Print a single space |
| `SPACES` | `( n -- )` | Print n spaces |
| `EMIT` | `( char -- )` | Print character with given ASCII code |

### String Output

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `."` | `( -- )` | Print following string literal (compile-time) |
| `TYPE` | `( addr n -- )` | Print n characters from address |

### Introspection

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `WORDS` | `( -- )` | List all defined words |
| `SEE` | `( -- )` | Show word definition (followed by word name) |

### REPL Commands

These are special commands handled by the REPL interface, not Forth words:

| Command | Description |
|---------|-------------|
| `CLS` | Clear the REPL output text (does not affect the stack) |

**Note:** Don't confuse `CLS` (clears REPL output) with `CLEAR` (clears the data stack).

### I/O Examples

```forth
\ Basic output
42 .                \ Output: 42
1 2 3 .S            \ Output: <3> 1 2 3 (non-destructive)

\ Formatted output
CR ." Hello, World!" CR

\ Character output
72 EMIT             \ Output: H (ASCII 72)
10 0 DO 42 EMIT LOOP    \ Output: ********** (10 asterisks)

\ Spacing
5 SPACES ." indented"
```

---

## Error Types

FABLE provides educational error messages designed to help learners understand what went wrong.

### Stack Underflow Error

Occurs when an operation requires more values than are on the stack.

```
Stack underflow: '+' needs 2 values, but the stack only has 1.
The '+' word adds two numbers together. Try: 3 5 +
```

### Unknown Word Error

Occurs when a word is not found in the dictionary.

```
Unknown word: 'PRNT'. Did you mean 'PRINT'?
Forth words are case-insensitive. Use WORDS to list available words.
```

### Division by Zero Error

Occurs when attempting to divide by zero.

```
Division by zero: Cannot divide 10 by 0.
Check the value on top of the stack before dividing.
```

### Type Mismatch Error

Occurs when a word receives an unexpected type.

```
Type mismatch: 'EMIT' expects integer, but found string.
```

### Compile-Only Word Error

Occurs when using compile-only words outside a definition.

```
'IF' is a compile-only word.
It can only be used inside a colon definition (: word ... ;).
```

### Control Structure Error

Occurs when control structures are unbalanced.

```
Unmatched 'IF': missing 'THEN'.
Every 'IF' needs a matching 'THEN'. Check that your conditionals are balanced.
```

---

## Stack Effect Notation

Stack effect comments describe how a word affects the stack.

### Format

```
( before -- after )
```

- **before**: Stack state before the word executes (top on the right)
- **--**: Separator
- **after**: Stack state after the word executes (top on the right)

### Common Abbreviations

| Symbol | Meaning |
|--------|---------|
| `n` | Integer number |
| `n1 n2` | Two integers (n1 is deeper) |
| `u` | Unsigned integer |
| `f` | Floating-point number |
| `flag` | Boolean value (0 or -1) |
| `addr` | Memory address |
| `char` | Character (ASCII code) |
| `...` | Variable number of items |

### Examples

| Notation | Meaning |
|----------|---------|
| `( n -- n n )` | Takes one item, leaves two copies |
| `( n1 n2 -- sum )` | Takes two items, leaves their sum |
| `( -- n )` | Takes nothing, pushes one item |
| `( n -- )` | Consumes one item, leaves nothing |
| `( -- )` | No effect on stack |
| `( ... -- )` | Clears stack |

---

## Examples

### Example 1: Factorial

```forth
: FACTORIAL ( n -- n! )
    1 SWAP              \ Put accumulator under n
    1+ 1 DO             \ Loop from 1 to n
        I *
    LOOP ;

5 FACTORIAL .           \ Output: 120
6 FACTORIAL .           \ Output: 720
```

### Example 2: Fibonacci Sequence

```forth
: FIB ( n -- fib[n] )
    0 1 ROT 0 DO
        OVER +          \ next = a + b
        SWAP            \ Swap to prepare for next iteration
    LOOP DROP ;

10 FIB .                \ Output: 55

\ Print first 10 Fibonacci numbers
: FIBS 10 0 DO I FIB . LOOP ;
FIBS                    \ Output: 0 1 1 2 3 5 8 13 21 34
```

### Example 3: Greatest Common Divisor (Euclidean Algorithm)

```forth
: GCD ( a b -- gcd )
    BEGIN
        DUP 0>
    WHILE
        SWAP OVER MOD
    REPEAT DROP ;

48 18 GCD .             \ Output: 6
```

### Example 4: Prime Number Check

```forth
: PRIME? ( n -- flag )
    DUP 2 < IF DROP FALSE EXIT THEN
    DUP 2 = IF DROP TRUE EXIT THEN
    DUP 2 MOD 0= IF DROP FALSE EXIT THEN
    DUP 3 DO
        DUP I MOD 0= IF
            DROP FALSE UNLOOP EXIT
        THEN
    2 +LOOP
    DROP TRUE ;

17 PRIME? .             \ Output: -1 (TRUE)
18 PRIME? .             \ Output: 0 (FALSE)
```

### Example 5: Temperature Conversion

```forth
: F>C ( fahrenheit -- celsius )
    32 - 5 * 9 / ;

: C>F ( celsius -- fahrenheit )
    9 * 5 / 32 + ;

212 F>C .               \ Output: 100
100 C>F .               \ Output: 212
```

### Example 6: Drawing a Box

```forth
: STAR 42 EMIT ;
: STARS ( n -- ) 0 DO STAR LOOP ;

: BOX ( width height -- )
    0 DO
        DUP STARS CR
    LOOP DROP ;

5 3 BOX
\ Output:
\ *****
\ *****
\ *****
```

---

## Quick Reference Card

### Essential Stack Words
```
DUP  ( n -- n n )       SWAP ( n1 n2 -- n2 n1 )
DROP ( n -- )           OVER ( n1 n2 -- n1 n2 n1 )
ROT  ( n1 n2 n3 -- n2 n3 n1 )
```

### Essential Arithmetic
```
+  ( n1 n2 -- sum )     -  ( n1 n2 -- diff )
*  ( n1 n2 -- prod )    /  ( n1 n2 -- quot )
MOD ( n1 n2 -- rem )
```

### Essential Comparison
```
=  ( n1 n2 -- flag )    <>  ( n1 n2 -- flag )
<  ( n1 n2 -- flag )    >   ( n1 n2 -- flag )
0= ( n -- flag )
```

### Essential Control Flow
```
: name ... ;            \ Define a word
IF ... THEN             \ Conditional
IF ... ELSE ... THEN    \ Conditional with else
BEGIN ... UNTIL         \ Loop until true
BEGIN ... WHILE ... REPEAT  \ Loop while true
limit start DO ... LOOP \ Counted loop
I                       \ Loop index
```

### Essential Output
```
.   ( n -- )            \ Print number
.S  ( -- )              \ Print stack
CR  ( -- )              \ Newline
." string"              \ Print string
EMIT ( char -- )        \ Print character
```

---

## Appendix: Complete Word List

### Stack Manipulation
`DUP` `DROP` `SWAP` `OVER` `ROT` `-ROT` `NIP` `TUCK` `2DUP` `2DROP` `2SWAP` `2OVER` `DEPTH` `PICK` `ROLL` `CLEAR`

### Arithmetic
`+` `-` `*` `/` `MOD` `/MOD` `NEGATE` `ABS` `MIN` `MAX` `1+` `1-` `2+` `2-` `2*` `2/`

### Comparison
`=` `<>` `<` `>` `<=` `>=` `0=` `0<` `0>`

### Logic and Bitwise
`AND` `OR` `XOR` `INVERT` `LSHIFT` `RSHIFT` `TRUE` `FALSE` `NOT`

### Control Flow
`IF` `ELSE` `THEN` `BEGIN` `UNTIL` `WHILE` `REPEAT` `DO` `LOOP` `+LOOP` `I` `J` `LEAVE` `UNLOOP` `EXIT`

### Defining Words
`:` `;`

### Input/Output
`.` `.S` `CR` `SPACE` `SPACES` `EMIT` `TYPE` `."` `WORDS` `SEE`

---

*End of Language Reference*

