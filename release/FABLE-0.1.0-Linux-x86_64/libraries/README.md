# FABLE Library Collection

This directory contains bundled Forth libraries that extend FABLE's capabilities.

## Available Libraries

### 📐 math-extended.fth
Extended mathematical operations beyond basic arithmetic.

**Words included:**
- `ABS` - Absolute value
- `MIN`, `MAX` - Minimum and maximum
- `SQUARE`, `CUBE` - Power functions
- `POW` - General power (n^exp)
- `FACTORIAL` - Factorial calculation
- `GCD`, `LCM` - Greatest common divisor and least common multiple
- `EVEN?`, `ODD?` - Parity checks
- `CLAMP` - Constrain value to range
- `AVG` - Average of two numbers
- `SIGN` - Sign of number (-1, 0, 1)
- `SQRT` - Integer square root
- `SQUARE?` - Check if perfect square
- `SUM-TO` - Sum of integers 1 to n
- `FIB` - Fibonacci number
- `PRIME?` - Primality test

**Example usage:**
```forth
INCLUDE "math-extended.fth"
5 FACTORIAL .     \ Prints 120
12 18 GCD .       \ Prints 6
10 SQRT .         \ Prints 3
17 PRIME? .       \ Prints -1 (true)
```

### 📝 strings.fth
String and text formatting utilities.

**Words included:**
- `LINE`, `DOUBLE-LINE` - Print horizontal lines
- `BOX-TOP`, `BOX-BOTTOM` - Box drawing
- `CENTER` - Center text with spaces
- `REPEAT-CHAR` - Print character multiple times
- `STARS` - Print asterisks
- `BLANK-LINE`, `BLANK-LINES` - Spacing
- `SEPARATOR` - Visual separator
- `HEADER`, `BANNER` - Formatted headers

**Example usage:**
```forth
INCLUDE "strings.fth"
BANNER
50 LINE
```

### 📚 stack-helpers.fth
Advanced stack manipulation operations.

**Words included:**
- `2DUP`, `2DROP`, `2SWAP`, `2OVER` - Double-cell operations
- `PICK`, `ROLL` - Arbitrary stack access
- `?DUP` - Conditional duplicate
- `DEPTH` - Stack depth
- `CLEAR` - Clear entire stack
- `3DUP`, `3DROP` - Triple-cell operations
- `TUCK2`, `SPIN` - Advanced rotations

**Example usage:**
```forth
INCLUDE "stack-helpers.fth"
1 2 3 3DUP .S     \ Shows: 1 2 3 1 2 3
CLEAR             \ Empty stack
```

### 🧮 algorithms.fth
Common algorithms and computational patterns.

**Words included:**
- `COUNTDOWN`, `COUNTUP` - Number sequences
- `TIMES-TABLE` - Multiplication table
- `SUM-STACK`, `PRODUCT-STACK` - Stack aggregation
- `REVERSE` - Reverse stack items
- `COLLATZ`, `COLLATZ-STEP` - Collatz sequence
- `DIGITAL-ROOT`, `SUM-DIGITS` - Digit operations
- `REVERSE-NUMBER` - Reverse digits
- `PALINDROME?` - Check palindrome
- `.BIN` - Binary representation
- `POPCOUNT` - Count set bits
- `NEXT-POW2` - Next power of 2

**Example usage:**
```forth
INCLUDE "algorithms.fth"
10 COLLATZ        \ Print Collatz sequence
123 REVERSE-NUMBER .  \ Prints 321
```

### 🎨 graphics.fth
ASCII art and visual output.

**Words included:**
- `RECTANGLE`, `HOLLOW-RECT` - Rectangle drawing
- `RIGHT-TRIANGLE`, `INV-TRIANGLE` - Triangles
- `PYRAMID`, `DIAMOND` - Geometric shapes
- `CHECKERBOARD` - Pattern generation
- `BAR` - Horizontal bar chart
- `BORDER` - Decorative borders
- `CROSS` - Cross/plus symbol
- `TITLE-BOX` - Titled box
- `PROGRESS` - Progress bar
- `AXIS` - Graph axis
- `STAIRS`, `WAVE` - Patterns

**Example usage:**
```forth
INCLUDE "graphics.fth"
5 PYRAMID
10 5 RECTANGLE
7 DIAMOND
```

## Using Libraries

### Load a library:
```forth
INCLUDE "math-extended.fth"
```

### Save your own words to a library:
```forth
: DOUBLE 2 * ;
: TRIPLE 3 * ;
SAVE-LIBRARY "my-math.fth"
```

### View loaded libraries:
```forth
LOADED-LIBRARIES
```

### View library search paths:
```forth
LIBRARY-PATH
```

## Library Locations

Libraries are searched in this order:
1. Current working directory
2. `~/.config/fable/libraries/` (user libraries)
3. `<fable-install>/libraries/` (bundled libraries)

## Creating Your Own Libraries

1. Define your words in the REPL
2. Use `SAVE-LIBRARY "mylib.fth"` to save them
3. Your library will be saved to `~/.config/fable/libraries/`
4. Load it anytime with `INCLUDE "mylib.fth"`

## Tips

- Libraries are only loaded once (duplicate INCLUDE calls are ignored)
- Use comments (`\`) to document your library words
- Follow Forth naming conventions (uppercase, descriptive)
- Test your words before saving to a library
- Use `SEE wordname` to view word definitions

