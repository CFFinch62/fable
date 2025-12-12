# Learning Forth with FABLE

Welcome to the FABLE tutorial! This guide will take you from zero to writing complex algorithms in Forth. FABLE (Forth Animated Beginners Learning Environment) is designed specifically to make this journey easier by visualizing the stack.

## How to use this tutorial
1. Read a lesson below.
2. Open the corresponding example file in FABLE (e.g., `tutorial/01_basics.fs`).
3. Use the **Step** button (or F10) to walk through the code line-by-line.
4. Watch the **Stack** panel to see exactly what's happening!

---

## Lesson 1: The Stack & Integers
**File:** `tutorial/01_basics.fs`

Forth is a "stack-based" language. Imagine a stack of plates. You can only add a plate to the top ("push") or take one off the top ("pop").

- **Integers**: When you type a number like `42`, it is **pushed** onto the stack.
- **Output**: The word `.` (dot) **pops** the top number off the stack and prints it.

### Try it:
```forth
10 20 30    \ Pushes 10, then 20, then 30
.           \ Pops 30 and prints it
.           \ Pops 20 and prints it
.           \ Pops 10 and prints it
```

---

## Lesson 2: Arithmetic (Postfix Notation)
**File:** `tutorial/02_arithmetic.fs`

In Forth, operators come *after* their operands. This is called "Reverse Polish Notation" (RPN).
Instead of `3 + 4`, you write `3 4 +`.
Why? Because `3` and `4` go onto the stack, and then `+` takes them off and pushes the result.

| Operator | Action | Example |
|---|---|---|
| `+` | Add | `10 2 +` → `12` |
| `-` | Subtract | `10 2 -` → `8` |
| `*` | Multiply | `10 2 *` → `20` |
| `/` | Divide | `10 2 /` → `5` |
| `MOD` | Remainder | `10 3 MOD` → `1` |

---

## Lesson 3: Stack Acrobatics
**File:** `tutorial/03_stack_ops.fs`

Sometimes the numbers aren't in the right order for an operation. Forth providers words to rearrange the stack.

- **DUP** `( n -- n n )`: Duplicate the top item.
- **DROP** `( n -- )`: Throw away the top item.
- **SWAP** `( a b -- b a )`: Swap the top two items.
- **OVER** `( a b -- a b a )`: Copy the second item to the top.
- **ROT** `( a b c -- b c a )`: Rotate the third item to the top.

**Stack Effects**: The comments like `( a b -- b a )` describe what a word does. The left side is "before", the right side is "after".

---

## Lesson 4: Defining Words
**File:** `tutorial/04_definitions.fs`

You can extend the language by creating new "Words" (commands).
A definition starts with `:` (colon) and ends with `;` (semicolon).

```forth
: SQUARE ( n -- n^2 )
    DUP * ;
```
Now `SQUARE` is a word just like `DUP` or `*`. You can use it in other definitions!

```forth
: SUM-SQUARES ( a b -- sum )
    SQUARE SWAP SQUARE + ;
```

---

## Lesson 5: Logic & Booleans
**File:** `tutorial/05_logic.fs`

Forth doesn't have a separate "boolean" type. It uses integers:
- **-1** is **TRUE** (all bits set to 1)
- **0** is **FALSE** (all bits are 0)

Comparison operators push a flag onto the stack:
- `=` (Equal)
- `<` (Less than)
- `>` (Greater than)
- `0=` (Is zero?)

Logic operators work on these flags:
- `AND`, `OR`, `XOR`, `INVERT` (Not)

---

## Lesson 6: Making Decisions
**File:** `tutorial/06_conditionals.fs`

Use `IF ... THEN` to execute code only if the top of stack is True (non-zero).

```forth
: ABSOLUTE-VALUE ( n -- |n| )
    DUP 0< IF 
        NEGATE 
    THEN ;
```

You can also include an `ELSE` block:

```forth
: CHECK-SIGN ( n -- )
    DUP 0= IF
        ." Zero" DROP
    ELSE
        0< IF ." Negative" ELSE ." Positive" THEN
    THEN ;
```

---

## Lesson 7: Loops
**File:** `tutorial/07_loops.fs`

### Counted Loops (DO ... LOOP)
Repeat code a specific number of times.
Syntax: `limit start DO ... LOOP`
Using `I` accesses the current loop index.

```forth
: COUNT-TO-5
    5 0 DO
        I . 
    LOOP ;
```

### Indefinite Loops (BEGIN ... UNTIL)
Repeat until a condition is true.

```forth
: COUNT-DOWN ( n -- )
    BEGIN
        DUP . 1-    \ Print and decrement
        DUP 0=      \ Check if 0
    UNTIL
    DROP ;
```

---

## Conclusion

You now know the fundamentals of Forth!
- You can manage the stack.
- You can perform math and logic.
- You can define your own vocabulary.
- You can control flow with loops and conditions.

Experiment with the files in the `tutorial/` folder. Try modifying them to see what happens!
