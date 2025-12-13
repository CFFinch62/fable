# FABLE Library System

## Overview

The FABLE library system allows you to save and reuse collections of Forth word definitions across sessions. This keeps users engaged with the Forth language by making it easy to build up a personal collection of useful words and utilities.

## Quick Start

### Loading a Library in the REPL

To load a library in the REPL (bottom panel):

```forth
S" math-extended.fth" INCLUDE
```

This loads the `math-extended.fth` library from one of the library search paths.

### Loading a Library in the Editor

You can also use `INCLUDE` in your Forth source files! Write your code in the editor (center panel) and include libraries at the top:

```forth
\ my-program.fth
\ Load libraries we need
S" math-extended.fth" INCLUDE
S" strings.fth" INCLUDE

\ Now use words from those libraries
: GREET
  ." Hello from FABLE!" CR
  LINE
  ." 5 factorial is: " 5 FACTORIAL . CR ;

GREET
```

Then run your file using:
- **F5** - Run entire file
- **F6** - Run selected text
- **F7** - Run current line
- **Menu: Run → Run File**

The libraries will be loaded when the file executes!

### Saving Your Words

After defining some words in the REPL:

```forth
: DOUBLE 2 * ;
: TRIPLE 3 * ;
S" my-words.fth" SAVE-LIBRARY
```

This saves all your user-defined words to `~/.config/fable/libraries/my-words.fth`.

### Viewing Loaded Libraries

```forth
LOADED-LIBRARIES
```

Shows all currently loaded libraries.

### Viewing Library Paths

```forth
LIBRARY-PATH
```

Shows where FABLE searches for library files.

## Library Search Paths

FABLE searches for libraries in this order:

1. **Current directory** - Where you launched FABLE from
2. **User libraries** - `~/.config/fable/libraries/` (your personal libraries)
3. **Bundled libraries** - `<fable-install>/libraries/` (libraries that come with FABLE)

## Bundled Libraries

FABLE comes with 5 starter libraries:

### 1. math-extended.fth
Extended mathematical operations:
- `ABS` - Absolute value
- `MIN`, `MAX` - Minimum/maximum of two numbers
- `SQUARE`, `CUBE` - Powers
- `POW` - General exponentiation
- `FACTORIAL` - Factorial function
- `GCD`, `LCM` - Greatest common divisor, least common multiple
- `SQRT` - Integer square root
- `FIB` - Fibonacci numbers
- `PRIME?` - Prime number test
- And more!

### 2. stack-helpers.fth
Advanced stack manipulation:
- `2DUP`, `2DROP`, `2SWAP`, `2OVER` - Pair operations
- `PICK`, `ROLL` - Advanced stack access
- `DEPTH` - Stack depth
- `CLEAR` - Clear entire stack
- `NIP`, `TUCK` - Stack rearrangement

### 3. strings.fth
Text formatting utilities:
- `LINE`, `DOUBLE-LINE` - Draw horizontal lines
- `BOX-TOP`, `BOX-BOTTOM` - Box drawing
- `BANNER` - Print text in a banner
- `SEPARATOR` - Visual separators

### 4. algorithms.fth
Common algorithms:
- `COLLATZ` - Collatz sequence
- `DIGITAL-ROOT` - Digital root calculation
- `PALINDROME?` - Palindrome test
- `.BIN` - Print binary representation
- `POPCOUNT` - Count set bits

### 5. graphics.fth
ASCII art generation:
- `RECTANGLE` - Draw rectangles
- `PYRAMID` - Draw pyramids
- `DIAMOND` - Draw diamonds
- `CHECKERBOARD` - Draw checkerboard patterns
- `PROGRESS` - Progress bars

## Using Libraries in the IDE

### Typical Workflow

1. **Browse examples** - Use the File Browser (left panel) to navigate to the `libraries/` folder
2. **Open a library** - Double-click any `.fth` file to view it in the editor
3. **Create your program** - File → New to create a new file
4. **Include libraries** - Add `S" library-name.fth" INCLUDE` at the top
5. **Write code** - Use words from the loaded libraries
6. **Run** - Press F5 to run the entire file, or F6 to run selected code
7. **Watch the stack** - The Stack Widget (right panel) animates as your code executes!

### Example: Creating a Program with Libraries

Create a new file `my-calculator.fth`:

```forth
\ Advanced Calculator
\ Uses math-extended library for additional functions

S" math-extended.fth" INCLUDE

\ Define some helper words
: SHOW-RESULT ( n -- )
  ." Result: " . CR ;

\ Test various operations
." Testing Math Library:" CR
." " CR

." Absolute value:" CR
-42 ABS SHOW-RESULT

." Factorial:" CR
5 FACTORIAL SHOW-RESULT

." GCD of 48 and 18:" CR
48 18 GCD SHOW-RESULT

." Is 17 prime?" CR
17 PRIME? IF
  ." Yes, 17 is prime!" CR
ELSE
  ." No, 17 is not prime." CR
THEN
```

Save it (Ctrl+S), then press **F5** to run!

### Keyboard Shortcuts for Running Code

- **F5** - Run entire file
- **F6** - Run selected text (highlight code first)
- **F7** - Run current line (cursor position)
- **Ctrl+R** - Reset interpreter (clears all definitions)

### File Browser Integration

The File Browser shows:
- **examples/** - Sample programs demonstrating Forth features
- **libraries/** - Bundled library files you can include
- Your project files

**Tip:** Double-click any `.fth` or `.fs` file to open it in the editor!

## Example REPL Session

```forth
\ Load the math library
S" math-extended.fth" INCLUDE

\ Use words from the library
-42 ABS .        \ Prints: 42
10 5 MIN .       \ Prints: 5
7 SQUARE .       \ Prints: 49
5 FACTORIAL .    \ Prints: 120

\ Define your own words
: QUADRUPLE DOUBLE DOUBLE ;
: AVERAGE + 2 / ;

\ Save your words
S" my-math.fth" SAVE-LIBRARY

\ Check what's loaded
LOADED-LIBRARIES
```

## Tips

1. **Library files are just Forth code** - You can edit them with any text editor
2. **Libraries are loaded once** - INCLUDE won't reload an already-loaded library
3. **User libraries override bundled** - If you have a library with the same name in your user directory, it will be loaded instead of the bundled version
4. **Start small** - Begin with the bundled libraries to see how they work, then create your own

## New Forth Words Added

- `INCLUDE` - Load a library file
- `SAVE-LIBRARY` - Save user-defined words to a file
- `LOADED-LIBRARIES` - List loaded libraries
- `LIBRARY-PATH` - Show library search paths
- `S"` - String literal (for filenames)

## Additional Forth Words Added

To support the bundled libraries, these standard Forth words were also added:

- `>R` - Move value to return stack
- `R>` - Move value from return stack
- `R@` - Copy value from return stack
- `0<>` - Test if not equal to zero

## Tips and Tricks

### Control Flow Only Works in Compiled Words

Control flow words like `IF/THEN/ELSE`, `BEGIN/UNTIL`, and `DO/LOOP` only work inside word definitions (`: WORD ... ;`), not directly in the REPL.

**This won't work in the REPL:**
```forth
10 EVEN? IF ." Yes" ELSE ." No" THEN  \ Error!
```

**Instead, define a word:**
```forth
: CHECK-EVEN ( n -- )
  EVEN? IF ." Yes" ELSE ." No" THEN ;

10 CHECK-EVEN  \ Works!
```

### String Literals

- Use `S"` to push a string onto the stack (for INCLUDE, SAVE-LIBRARY, etc.)
- Use `."` to print a string immediately

```forth
S" math-extended.fth" INCLUDE  \ S" pushes string for INCLUDE
." Hello World!" CR             \ ." prints immediately
```

### Libraries Are Loaded Once

FABLE tracks which libraries have been loaded and ignores subsequent INCLUDE calls for the same library. This prevents redefinition errors when multiple files include the same library.

### Experimenting in the Editor

The editor's keyboard shortcuts make it easy to experiment:

- **F5** - Run entire file (great for testing complete programs)
- **F6** - Run selected text (perfect for testing specific sections)
- **F7** - Run current line (ideal for step-by-step execution)

Try opening `examples/using-libraries.fth` and experimenting with these shortcuts!

---

Enjoy building your Forth vocabulary!

