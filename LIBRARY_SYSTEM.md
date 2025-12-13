# FABLE Library System

## Overview

The FABLE library system allows you to save and reuse collections of Forth word definitions across sessions. This keeps users engaged with the Forth language by making it easy to build up a personal collection of useful words and utilities.

## Quick Start

### Loading a Library

To load a library in the REPL:

```forth
S" math-extended.fth" INCLUDE
```

This loads the `math-extended.fth` library from one of the library search paths.

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

## Example Session

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

Enjoy building your Forth vocabulary!

