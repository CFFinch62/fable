# FABLE: Forth Animated Beginners Learning Environment

## Complete Technical Specification

**Version:** 1.0  
**Author:** Chuck / Fragillidae Software  
**Date:** December 2025  
**Tagline:** *Every stack tells a story*

---

# Part 1: Animated Stack Widget Specification

## 1.1 Overview

The Animated Stack Widget is the pedagogical centerpiece of FABLE. It provides real-time visual feedback of stack operations, transforming the abstract concept of stack manipulation into a concrete, observable process. The widget displays both the Data Stack and the Return Stack, with smooth animations that illustrate how Forth words consume and produce values.

## 1.2 Visual Design

### Stack Container

The stack widget occupies the right panel of the main application window and remains always visible. It consists of two vertically arranged stack displays: the Data Stack (primary, larger) on top, and the Return Stack (secondary, smaller) below. Each stack is rendered as a vertical column of stack item widgets, with the top of stack (TOS) positioned at the top of the display.

The container includes a header bar displaying the stack name, current depth count, and control buttons. A subtle grid or ruled background helps users visually track item positions during animations.

### Stack Item Widget

Each stack item is implemented as a custom QFrame subclass with the following visual elements:

The value display shows the numeric or string value in a clear, monospaced font (such as Consolas or Source Code Pro) at a readable size (14-16pt). A type indicator strip along the left edge uses color coding: blue for integers, green for floats, amber for addresses/pointers, and purple for strings or other types.

The item includes a subtle drop shadow and rounded corners (4px radius) to give depth and separation. The background color is a light neutral (off-white or very light gray) with the ability to transition to highlight colors during operations.

### Color Scheme

Following the established aesthetic from your other tools, FABLE uses an amber and blue color scheme. Primary accent color is warm amber (#D4A017) for highlights and active states. Secondary accent is cool blue (#2E86AB) for type indicators and selection states. The background uses dark charcoal (#1E1E1E) for the stack container with light items (#F5F5F5) providing contrast. Error states use a muted red (#C0392B) and success states use a muted green (#27AE60).

## 1.3 Animation System

### Core Animation Types

**Push Animation:** When a value is pushed onto the stack, a new item widget appears above the current TOS. The animation sequence begins with the new item fading in (opacity 0 to 1) over 150ms while simultaneously sliding down from 20px above its final position. Existing items do not move since new items always appear at the top.

**Pop Animation:** When a value is consumed, the TOS item highlights briefly with amber (100ms), then fades out (opacity 1 to 0) over 150ms while sliding up 20px. This "consumed" highlight is crucial for showing students which values are being used by an operation.

**Swap Animation:** The two topmost items exchange positions. Both items animate simultaneously, with the first item moving to the second position and vice versa. The animation uses an ease-in-out curve over 300ms. During transit, items are slightly elevated (z-order) to show they're in motion.

**Rot Animation:** Three items rotate positions. TOS moves to third position, second moves to TOS, third moves to second. The animation choreographs all three movements simultaneously over 400ms with a slight arc to the motion paths to make the rotation visually clear.

**Dup Animation:** The TOS item pulses with a brief glow, then a copy "splits off" and slides into position above it. The original remains in place while the duplicate fades in at the new TOS position over 200ms.

**Drop Animation:** Identical to Pop but without any preceding operation. The TOS simply fades and slides away.

**Over Animation:** Similar to Dup, but the second item pulses and produces the copy that moves to TOS.

### Animation Timing Control

A speed slider in the stack widget header allows users to adjust animation duration from 0.25x (very slow, 4x normal duration) to 4x (very fast, 0.25x normal duration). The default is 1x. At the slowest setting, a push animation takes 600ms; at the fastest, 37.5ms.

Step mode, activated via a toggle button or keyboard shortcut, pauses execution after each word. The user must press Space, Enter, or click a "Step" button to advance to the next word. This mode is essential for learning, allowing students to predict what will happen before seeing it.

### Animation Queue

Operations are queued and executed sequentially. If multiple operations occur rapidly (such as in normal execution mode), they animate in sequence with minimal gap (50ms between operations). The queue can be cleared by pressing Escape or clicking Stop, which immediately completes all pending animations and shows the final state.

## 1.4 Stack Effect Preview

Before a word executes, the stack widget can preview which items will be affected. This feature is toggled on by default for beginners and can be disabled by advanced users.

When preview is enabled and execution is paused (step mode or breakpoint), the items that will be consumed by the next word display a dashed border and slight transparency. Ghost items representing the results appear above the stack in a muted color, showing what will be produced.

For example, before executing `+` with `3 4` on the stack, both items show the consumption indicator, and a ghost item labeled `7` appears above. The stack effect notation `( n1 n2 -- sum )` displays in a tooltip or small overlay.

## 1.5 Widget API

### Class: StackWidget(QWidget)

**Constructor:** `__init__(self, parent=None, stack_name="Data Stack")`

**Properties:**
- `items: List[StackItemWidget]` — Current stack item widgets
- `animation_speed: float` — Speed multiplier (0.25 to 4.0)
- `step_mode: bool` — Whether step mode is active
- `preview_enabled: bool` — Whether stack effect preview is shown

**Public Methods:**
- `push(value, value_type="int")` — Animate pushing a value
- `pop() -> value` — Animate popping and return value
- `peek(index=0) -> value` — Return value at index without animation
- `clear()` — Clear all items with fade-out animation
- `set_stack(values: List)` — Set entire stack state (for sync with interpreter)
- `animate_operation(op_name: str)` — Trigger named animation (swap, rot, dup, etc.)
- `show_preview(consumes: int, produces: List)` — Display stack effect preview
- `hide_preview()` — Remove stack effect preview
- `step()` — Advance one step in step mode
- `set_speed(multiplier: float)` — Set animation speed

**Signals:**
- `operation_complete` — Emitted when an animation finishes
- `step_requested` — Emitted when user requests next step
- `stack_changed(depth: int)` — Emitted when stack depth changes

### Class: StackItemWidget(QFrame)

**Constructor:** `__init__(self, value, value_type="int", parent=None)`

**Properties:**
- `value: Any` — The stored value
- `value_type: str` — Type identifier for color coding
- `highlighted: bool` — Current highlight state

**Public Methods:**
- `animate_in()` — Trigger entrance animation
- `animate_out()` — Trigger exit animation
- `animate_move(target_pos: QPoint)` — Animate to new position
- `highlight(color: str, duration_ms: int)` — Flash highlight color
- `set_consumed_preview(enabled: bool)` — Show/hide consumption indicator
- `set_ghost_mode(enabled: bool)` — Show as ghost preview item

## 1.6 Accessibility

The stack widget includes accessibility features for users who may have difficulty with animations. A "reduced motion" setting disables animations and shows instantaneous state changes. All stack operations are announced to screen readers. High contrast mode increases border thickness and uses more saturated colors. The stack state can also be queried as plain text via a "Read Stack" button that outputs to the REPL.

---

# Part 2: Forth Interpreter Specification

## 2.1 Overview

FABLE includes a purpose-built Forth interpreter designed specifically for education. Rather than embedding an existing Forth like Gforth, a custom interpreter provides complete control over execution timing, stack visualization hooks, and pedagogically-appropriate error messages. The interpreter implements a substantial subset of ANS Forth sufficient for learning core concepts.

## 2.2 Architecture

### Core Components

The interpreter consists of four primary components working together:

**Lexer/Tokenizer:** Converts source text into a stream of tokens. Forth's simple syntax (whitespace-separated words) makes this straightforward. The lexer preserves source location information for error reporting and editor integration.

**Dictionary:** A linked-list structure mapping word names to their definitions. Each dictionary entry contains the word name, a pointer to the code (either primitive or compiled), immediate flag, and documentation including stack effect. The dictionary supports vocabulary/wordlist concepts for organizing words.

**Inner Interpreter:** Executes compiled Forth code by traversing threaded code structures. FABLE uses indirect threaded code (ITC) for clarity, though this is an implementation detail hidden from students.

**Outer Interpreter:** The main read-eval-print loop that reads input, looks up words in the dictionary, and either executes them (in interpret mode) or compiles them (in compile mode).

### Execution Hook System

The interpreter exposes hooks that the GUI uses to drive animations. Before each word executes, the interpreter emits a `word_starting` signal with the word name and its stack effect. After execution, it emits `word_complete` with the resulting stack state. These hooks enable the stack widget to animate operations in sync with execution.

The interpreter can operate in several execution modes:

**Run Mode:** Executes continuously, emitting signals that queue animations. The GUI shows animations as fast as the speed setting allows, with execution proceeding immediately.

**Synchronized Mode:** Executes one word, waits for the `operation_complete` signal from the stack widget before proceeding. This ensures animations complete before the next operation.

**Step Mode:** Executes one word, then pauses until explicitly advanced. The GUI waits for user input between each word.

## 2.3 Data Types

FABLE's Forth supports the following data types:

**Integers:** Signed integers, sized to the platform (typically 64-bit). Standard Forth words treat these as the default type. Displayed in the stack widget with a blue type indicator.

**Floats:** Double-precision floating point numbers. Accessed via the separate floating-point wordset (F+, F*, etc.) and stored on a separate float stack in traditional Forth fashion. For simplicity, FABLE may optionally use a unified stack with type tagging. Displayed with a green type indicator.

**Addresses:** Memory addresses/pointers for variables, arrays, and memory operations. Displayed with an amber type indicator.

**Strings:** Counted strings and address-length pairs. String literals are supported. Displayed with a purple type indicator.

**Booleans:** Forth's standard true (-1) and false (0) convention. Displayed as TRUE/FALSE in the stack widget rather than raw numbers, with a cyan type indicator.

## 2.4 Core Word Set

### Stack Manipulation

```
DUP     ( n -- n n )           Duplicate top of stack
DROP    ( n -- )               Discard top of stack
SWAP    ( n1 n2 -- n2 n1 )     Exchange top two items
OVER    ( n1 n2 -- n1 n2 n1 )  Copy second item to top
ROT     ( n1 n2 n3 -- n2 n3 n1 )  Rotate third item to top
-ROT    ( n1 n2 n3 -- n3 n1 n2 )  Rotate top to third position
NIP     ( n1 n2 -- n2 )        Drop second item
TUCK    ( n1 n2 -- n2 n1 n2 )  Copy top below second
2DUP    ( n1 n2 -- n1 n2 n1 n2 )  Duplicate top pair
2DROP   ( n1 n2 -- )           Drop top pair
2SWAP   ( n1 n2 n3 n4 -- n3 n4 n1 n2 )  Swap pairs
2OVER   ( n1 n2 n3 n4 -- n1 n2 n3 n4 n1 n2 )  Copy second pair
DEPTH   ( -- n )               Push current stack depth
PICK    ( n -- item )          Copy nth item to top
ROLL    ( n -- )               Rotate nth item to top
```

### Arithmetic

```
+       ( n1 n2 -- sum )       Addition
-       ( n1 n2 -- diff )      Subtraction
*       ( n1 n2 -- prod )      Multiplication
/       ( n1 n2 -- quot )      Division
MOD     ( n1 n2 -- rem )       Modulo
/MOD    ( n1 n2 -- rem quot )  Division with remainder
*/      ( n1 n2 n3 -- result ) Multiply then divide
ABS     ( n -- |n| )           Absolute value
NEGATE  ( n -- -n )            Negate
MIN     ( n1 n2 -- min )       Minimum
MAX     ( n1 n2 -- max )       Maximum
1+      ( n -- n+1 )           Increment
1-      ( n -- n-1 )           Decrement
2+      ( n -- n+2 )           Add two
2-      ( n -- n-2 )           Subtract two
2*      ( n -- n*2 )           Double (shift left)
2/      ( n -- n/2 )           Halve (shift right)
```

### Comparison

```
=       ( n1 n2 -- flag )      Equal
<>      ( n1 n2 -- flag )      Not equal
<       ( n1 n2 -- flag )      Less than
>       ( n1 n2 -- flag )      Greater than
<=      ( n1 n2 -- flag )      Less than or equal
>=      ( n1 n2 -- flag )      Greater than or equal
0=      ( n -- flag )          Equal to zero
0<      ( n -- flag )          Less than zero
0>      ( n -- flag )          Greater than zero
```

### Logic

```
AND     ( n1 n2 -- n )         Bitwise AND
OR      ( n1 n2 -- n )         Bitwise OR
XOR     ( n1 n2 -- n )         Bitwise XOR
INVERT  ( n -- ~n )            Bitwise NOT
LSHIFT  ( n1 n2 -- n )         Left shift n1 by n2 bits
RSHIFT  ( n1 n2 -- n )         Right shift n1 by n2 bits
TRUE    ( -- -1 )              Push true flag
FALSE   ( -- 0 )               Push false flag
```

### Return Stack

```
>R      ( n -- ) ( R: -- n )   Move to return stack
R>      ( -- n ) ( R: n -- )   Move from return stack
R@      ( -- n ) ( R: n -- n ) Copy from return stack
2>R     ( n1 n2 -- ) ( R: -- n1 n2 )  Move pair to return stack
2R>     ( -- n1 n2 ) ( R: n1 n2 -- )  Move pair from return stack
2R@     ( -- n1 n2 ) ( R: n1 n2 -- n1 n2 )  Copy pair from return stack
```

### Memory

```
@       ( addr -- n )          Fetch from address
!       ( n addr -- )          Store to address
+!      ( n addr -- )          Add to address contents
?       ( addr -- )            Fetch and print
C@      ( addr -- char )       Fetch byte
C!      ( char addr -- )       Store byte
CELLS   ( n -- n*cell )        Convert to cell units
CELL+   ( addr -- addr' )      Add cell size
CHARS   ( n -- n*char )        Convert to char units
CHAR+   ( addr -- addr' )      Add char size
ALLOT   ( n -- )               Allocate n bytes
HERE    ( -- addr )            Current dictionary pointer
,       ( n -- )               Compile n to dictionary
C,      ( char -- )            Compile byte to dictionary
```

### Variables and Constants

```
VARIABLE name   ( -- )         Create a variable
CONSTANT name   ( n -- )       Create a constant
VALUE name      ( n -- )       Create a value
TO name         ( n -- )       Store to value
CREATE name     ( -- )         Create dictionary entry
DOES>           ( -- )         Define runtime behavior
```

### Control Flow

```
IF      ( flag -- )            Begin conditional
ELSE    ( -- )                 Alternative branch
THEN    ( -- )                 End conditional
BEGIN   ( -- )                 Begin loop
UNTIL   ( flag -- )            Loop until true
WHILE   ( flag -- )            Loop while true
REPEAT  ( -- )                 End BEGIN...WHILE loop
AGAIN   ( -- )                 Infinite loop back to BEGIN
DO      ( limit start -- )     Begin counted loop
LOOP    ( -- )                 Increment and loop
+LOOP   ( n -- )               Add n and loop
I       ( -- n )               Current loop index
J       ( -- n )               Outer loop index
LEAVE   ( -- )                 Exit loop immediately
UNLOOP  ( -- )                 Discard loop parameters
EXIT    ( -- )                 Exit current word
RECURSE ( -- )                 Call current word recursively
CASE    ( n -- n )             Begin case statement
OF      ( n1 n2 -- )           Test case
ENDOF   ( -- )                 End case branch
ENDCASE ( n -- )               End case statement
```

### Defining Words

```
: name  ( -- )                 Begin colon definition
;       ( -- )                 End colon definition
IMMEDIATE ( -- )               Mark last word as immediate
POSTPONE name ( -- )           Compile compilation semantics
[       ( -- )                 Enter interpret mode
]       ( -- )                 Enter compile mode
LITERAL ( n -- )               Compile literal
[']     ( -- xt )              Compile word's execution token
'       ( -- xt )              Get execution token
EXECUTE ( xt -- )              Execute execution token
```

### Input/Output

```
.       ( n -- )               Print number
.S      ( -- )                 Print stack (non-destructive)
CR      ( -- )                 Print newline
SPACE   ( -- )                 Print space
SPACES  ( n -- )               Print n spaces
EMIT    ( char -- )            Print character
TYPE    ( addr n -- )          Print string
."      ( -- )                 Print string literal (compile time)
.(      ( -- )                 Print string literal (immediate)
KEY     ( -- char )            Read character
ACCEPT  ( addr n -- n' )       Read line into buffer
```

### String Operations

```
S"      ( -- addr n )          String literal
COUNT   ( addr -- addr' n )    Convert counted string
COMPARE ( a1 n1 a2 n2 -- n )   Compare strings
/STRING ( addr n1 n2 -- addr' n' )  Adjust string
```

## 2.5 Error Handling

The interpreter provides beginner-friendly error messages that explain what went wrong and suggest corrections.

### Error Types

**Stack Underflow:** Occurs when a word requires more items than are on the stack. Message format: "Stack underflow: '+' needs 2 values, but the stack only has 1. The '+' word adds two numbers together. Try pushing another number first."

**Unknown Word:** Occurs when the interpreter cannot find a word in the dictionary. Message format: "Unknown word: 'PRNT'. Did you mean 'PRINT'? (Forth words are case-insensitive.)"

**Type Mismatch:** When strict typing is enabled, occurs when a word receives the wrong type. Message format: "Type mismatch: 'F+' expects floating-point numbers, but found integer 42. Try using '42.0' or 'S>F' to convert."

**Division by Zero:** Message format: "Division by zero: Cannot divide 10 by 0. Check the value on top of the stack before dividing."

**Compile-Only Word:** Occurs when using words like IF or LOOP outside a definition. Message format: "'IF' is a compile-only word. It can only be used inside a colon definition (: word ... ;)."

**Control Structure Mismatch:** Occurs with unbalanced IF/THEN, BEGIN/UNTIL, etc. Message format: "Unmatched 'IF': Every 'IF' needs a matching 'THEN'. Check that your conditionals are properly balanced."

### Error Recovery

After an error, the interpreter resets to a clean state: the stack is optionally cleared (configurable), compile mode is exited, and the input buffer is flushed. The user can immediately try again. An "Undo" feature allows reverting to the state before the error-causing input.

## 2.6 Interpreter API

### Class: ForthInterpreter

**Constructor:** `__init__(self)`

**Properties:**
- `data_stack: List` — The data stack
- `return_stack: List` — The return stack
- `dictionary: Dictionary` — Word definitions
- `compiling: bool` — True if in compile mode
- `execution_mode: str` — "run", "synchronized", or "step"

**Public Methods:**
- `evaluate(source: str)` — Parse and execute source code
- `evaluate_word(word: str)` — Execute a single word
- `push(value, value_type="int")` — Push value onto data stack
- `pop() -> value` — Pop value from data stack
- `peek(index=0) -> value` — Peek at stack without popping
- `define_word(name: str, body: List, immediate=False)` — Add word to dictionary
- `lookup(name: str) -> DictionaryEntry` — Find word in dictionary
- `reset()` — Reset interpreter state
- `get_stack_effect(word: str) -> Tuple[int, int]` — Get word's stack effect
- `set_execution_mode(mode: str)` — Set run/synchronized/step mode
- `step()` — Execute one word in step mode
- `load_file(path: str)` — Load and execute Forth source file

**Signals:**
- `word_starting(name: str, stack_effect: str)` — Before word execution
- `word_complete(name: str, stack: List)` — After word execution
- `error_occurred(error: ForthError)` — When an error occurs
- `output(text: str)` — When output is produced
- `state_changed()` — When interpreter state changes

### Class: Dictionary

**Methods:**
- `define(name: str, entry: DictionaryEntry)` — Add definition
- `lookup(name: str) -> DictionaryEntry` — Find definition
- `forget(name: str)` — Remove definition and all after it
- `words() -> List[str]` — List all defined words
- `see(name: str) -> str` — Decompile word definition

### Class: DictionaryEntry

**Properties:**
- `name: str` — Word name
- `code: Callable or List` — Primitive function or threaded code
- `immediate: bool` — Execute during compilation
- `stack_effect: str` — Stack effect notation
- `docstring: str` — Documentation string
- `source_location: Tuple` — File and line where defined

## 2.7 Built-in Documentation

Every word in the dictionary includes documentation accessible via the HELP word. Typing `HELP +` displays: "Addition ( n1 n2 -- sum ). Adds two numbers and pushes the result. Example: 3 4 + .  => 7"

The SEE word decompiles definitions: `SEE SQUARE` might display `: SQUARE ( n -- n^2 ) DUP * ;`

A WORDS command lists all available words, optionally filtered: `WORDS STACK` shows all words containing "STACK" in their name.

---

# Part 3: IDE/Environment Specification

## 3.1 Overview

The FABLE IDE integrates the Forth interpreter and animated stack widget into a complete development environment. The interface follows a familiar IDE layout with panels for file browsing, code editing, REPL interaction, and stack visualization. The design prioritizes clarity and learning over feature density.

## 3.2 Window Layout

### Main Window Structure

The main window uses a QMainWindow with a central widget containing a horizontal splitter. From left to right, the panels are:

**Left Panel — File Browser:** A collapsible panel (default width 200px) containing a tree view of files and folders. Can be toggled via View menu or keyboard shortcut (Ctrl+B).

**Center Panel — Editor and REPL:** A vertical splitter dividing the main workspace. The upper section contains the code editor (always visible, takes remaining space). The lower section contains the terminal/REPL (default height 200px, collapsible via View menu or Ctrl+T).

**Right Panel — Stack Display:** A fixed panel (default width 250px) containing the animated stack widget. Always visible as it is central to the learning experience.

### Panel Proportions

Default proportions allocate roughly 15% to the file browser, 55% to the editor/REPL area, and 30% to the stack display. The splitters allow user adjustment, and positions are persisted between sessions.

## 3.3 Menu System

### File Menu

```
New File            Ctrl+N      Create new Forth source file
Open File           Ctrl+O      Open existing file
Open Folder         Ctrl+K      Open folder as project
Open Recent         >           Submenu of recent files/folders
Save                Ctrl+S      Save current file
Save As             Ctrl+Shift+S Save with new name
Save All            Ctrl+Alt+S  Save all open files
Close File          Ctrl+W      Close current file
Close All                       Close all files
---
Export Session                  Save REPL session to file
---
Exit                Ctrl+Q      Quit application
```

### Edit Menu

```
Undo                Ctrl+Z      Undo last edit
Redo                Ctrl+Y      Redo undone edit
---
Cut                 Ctrl+X      Cut selection
Copy                Ctrl+C      Copy selection
Paste               Ctrl+V      Paste clipboard
Select All          Ctrl+A      Select all text
---
Find                Ctrl+F      Find in current file
Find and Replace    Ctrl+H      Find and replace
Find in Files       Ctrl+Shift+F Search across project
---
Toggle Comment      Ctrl+/      Comment/uncomment line(s)
Indent              Tab         Increase indent
Unindent            Shift+Tab   Decrease indent
```

### View Menu

```
File Browser        Ctrl+B      Toggle file browser panel
Terminal/REPL       Ctrl+T      Toggle REPL panel
Stack Widget                    (Always visible, grayed out)
---
Data Stack                      Show/focus data stack
Return Stack                    Show/focus return stack
Both Stacks                     Show both stacks
---
Zoom In             Ctrl+=      Increase editor font size
Zoom Out            Ctrl+-      Decrease editor font size
Reset Zoom          Ctrl+0      Reset to default font size
---
Full Screen         F11         Toggle full screen mode
```

### Run Menu

```
Run File            F5          Execute entire current file
Run Selection       F6          Execute selected text
Run Line            F7          Execute current line
---
Step Into           F10         Execute one word (step mode)
Step Over           F11         Execute word without entering
Continue            F8          Continue execution
Stop                Shift+F5    Stop execution
---
Clear Stack                     Clear data stack
Clear Return Stack              Clear return stack
Reset Interpreter   Ctrl+R      Reset to initial state
```

### Tools Menu

```
Dictionary Browser              Open dictionary explorer
Word Lookup         F1          Look up word under cursor
See Definition      Ctrl+D      Decompile word under cursor
---
Stack Effect Check              Verify stack effects in file
Lint File                       Check for common issues
---
Preferences         Ctrl+,      Open settings dialog
```

### Help Menu

```
FABLE Documentation             Open user guide
Forth Tutorial                  Interactive Forth tutorial
---
Word Reference                  Complete word reference
Stack Notation Guide            Explain stack notation
---
About FABLE                     Version and credits
```

## 3.4 File Browser Panel

### Tree View

The file browser displays a hierarchical tree of the current project folder. The root node shows the project folder name with a folder icon. Files and folders are sorted alphabetically with folders first. Standard file icons indicate type: Forth source files (.fs, .fth, .4th, .forth) display with a distinctive Forth icon; other text files show generic text icons.

### Context Menu

Right-clicking in the file browser provides:

```
New File                Create new file in selected folder
New Folder              Create new folder
---
Open                    Open selected file in editor
Open in System          Open with system default application
---
Rename                  Rename selected item
Delete                  Delete selected item (with confirmation)
---
Copy Path               Copy full path to clipboard
Copy Relative Path      Copy project-relative path
---
Reveal in System        Open containing folder in file manager
```

### Project Concepts

A "project" in FABLE is simply a folder. Opening a folder sets it as the project root. FABLE looks for a `.fable/` directory containing project settings, recently opened files, and breakpoint information. If not present, defaults are used.

The file browser shows a "Load Order" indicator for projects that define one. A `load.fth` or `.fable/load-order.txt` file can specify the order in which files should be loaded, and these files display with numeric badges indicating their position.

## 3.5 Code Editor Panel

### Editor Features

The code editor is a custom QPlainTextEdit subclass (or QScintilla if more features are needed) with Forth-specific enhancements.

**Syntax Highlighting:** Core words (stack manipulation, arithmetic, control flow) are highlighted in distinct colors. Definitions (`: ... ;`) are recognized with the word name emphasized. Comments (backslash to end of line, parentheses) are dimmed. Strings are highlighted. Numbers (including hex with `$` or `0x` prefix) are colored distinctly.

**Line Numbers:** A gutter displays line numbers. The current line is highlighted. Lines with breakpoints show a red circle. Lines with errors show a red underline or background.

**Auto-Completion:** Typing triggers completion suggestions from the dictionary after 2 characters. Completion shows word name, stack effect, and brief description. Tab or Enter accepts; Escape dismisses.

**Stack Effect Display:** Hovering over a word shows its stack effect in a tooltip. The status bar also shows the stack effect of the word under the cursor.

**Bracket Matching:** Matching pairs (IF/THEN, BEGIN/UNTIL, DO/LOOP, etc.) are highlighted when the cursor is on one.

**Code Folding:** Colon definitions can be collapsed to a single line showing `: name ... ;`.

### Multiple Files

The editor supports multiple open files via tabs above the editor area. Each tab shows the filename and a close button. Modified files show a dot or asterisk. Tabs can be reordered by dragging. Right-clicking a tab provides Close, Close Others, Close All, Copy Path options.

### Editor Configuration

User-configurable options include font family and size (default: Consolas/Source Code Pro, 14pt), tab width (default: 4 spaces), whether tabs insert spaces, auto-indent, line wrap mode, and visible whitespace characters.

## 3.6 Terminal/REPL Panel

### REPL Interface

The REPL panel provides an interactive Forth session. It displays a prompt (default: `ok> ` in interpret mode, `]> ` in compile mode) and accepts input. Output from executed code appears inline. The REPL maintains command history accessible via Up/Down arrows.

### Visual Elements

The REPL uses a dark background (matching the stack widget container) with light text. Input text is white; output is light gray; error messages are coral/salmon colored. The prompt is amber to match the accent color.

A subtle horizontal line separates each input/output exchange, making it easy to scan history.

### REPL Features

**History:** Command history persists between sessions. Ctrl+Up/Down navigates history. Ctrl+R provides reverse history search.

**Multi-line Input:** Entering an incomplete definition (`:` without `;`) continues on the next line with a continuation prompt (`... `). The entire multi-line input is executed as a unit.

**Output Capture:** All interpreter output (`.' ...'`, `.`, `.S`, etc.) appears in the REPL. Stack dumps from `.S` are formatted readably.

**Session Export:** The entire session can be exported to a text file for reference or submission (useful in educational contexts).

### Integration with Editor

Selecting text in the editor and pressing F6 sends it to the REPL for execution. The REPL can also source files via `INCLUDE filename` or through the Run menu.

## 3.7 Stack Widget Integration

### Synchronization

The stack widget always reflects the interpreter's current stack state. Any operation in the REPL or from running a file updates the display. The execution mode (run/synchronized/step) determines animation behavior.

### Controls

The stack widget header contains: a label showing "Data Stack (n)" where n is the depth; a speed slider; a step/run toggle button; and a preview toggle button. When in step mode, a prominent "Step" button appears.

### Dual Stack Display

The return stack appears below the data stack in a smaller area. It uses the same item widget style but with a different header color to distinguish it. Return stack operations (`>R`, `R>`, etc.) animate in this area.

## 3.8 Preferences Dialog

### General Tab

**Theme:** Light, Dark, or System. Dark theme uses the amber/blue color scheme described earlier.

**Font:** Editor font family and size.

**Session:** Whether to restore open files on startup; auto-save interval.

### Editor Tab

**Indentation:** Tab width, spaces vs. tabs, auto-indent.

**Display:** Line numbers, current line highlight, bracket matching, code folding, visible whitespace.

**Behavior:** Auto-completion enabled/delay, matching bracket highlight style.

### Interpreter Tab

**Execution:** Default execution mode (run/synchronized/step).

**Errors:** Whether to clear stack on error; strict type checking.

**REPL:** History size; prompt customization.

### Stack Widget Tab

**Animation:** Default speed; reduced motion option.

**Display:** Show type indicators; preview enabled by default.

**Colors:** Customize type indicator colors.

### Keyboard Shortcuts Tab

Displays all keyboard shortcuts in a searchable table. Shortcuts can be customized by clicking and pressing a new key combination.

## 3.9 Toolbar

A toolbar below the menu bar provides quick access to common actions:

```
[New] [Open] [Save] | [Undo] [Redo] | [Run] [Step] [Stop] | [Clear Stack]
```

Icons are simple and clear, following platform conventions where possible. The toolbar can be hidden via the View menu.

## 3.10 Status Bar

The status bar at the bottom of the window displays:

**Left section:** Current mode (Interpret/Compile); interpreter status (Ready/Running/Paused/Error).

**Center section:** Stack effect of word under cursor (if any).

**Right section:** Cursor position (line:column); file encoding; end-of-line style.

## 3.11 Application Lifecycle

### Startup

On launch, FABLE restores the previous session if configured: open files, panel sizes, and window position. If no previous session, it opens with an empty untitled file and the REPL ready. A splash screen or welcome tab can provide quick-start options: New File, Open File, Open Recent, Tutorial.

### Shutdown

On close, FABLE prompts to save modified files. It saves session state (open files, panel positions) for restoration. The interpreter state is not preserved between sessions.

### Settings Storage

Settings are stored in a platform-appropriate location: `~/.config/fable/` on Linux, `~/Library/Application Support/FABLE/` on macOS, `%APPDATA%\FABLE\` on Windows. Settings use JSON or INI format for human readability.

## 3.12 Keyboard Shortcuts Summary

### Global

| Shortcut | Action |
|----------|--------|
| Ctrl+N | New File |
| Ctrl+O | Open File |
| Ctrl+S | Save |
| Ctrl+W | Close File |
| Ctrl+Q | Quit |
| Ctrl+B | Toggle File Browser |
| Ctrl+T | Toggle Terminal |
| Ctrl+, | Preferences |
| F1 | Word Lookup |
| F5 | Run File |
| F6 | Run Selection |
| F7 | Run Line |
| F8 | Continue |
| F10 | Step |
| Shift+F5 | Stop |
| Ctrl+R | Reset Interpreter |

### Editor

| Shortcut | Action |
|----------|--------|
| Ctrl+Z | Undo |
| Ctrl+Y | Redo |
| Ctrl+X | Cut |
| Ctrl+C | Copy |
| Ctrl+V | Paste |
| Ctrl+A | Select All |
| Ctrl+F | Find |
| Ctrl+H | Replace |
| Ctrl+/ | Toggle Comment |
| Ctrl+D | See Definition |
| Tab | Indent |
| Shift+Tab | Unindent |
| Ctrl+= | Zoom In |
| Ctrl+- | Zoom Out |
| Ctrl+0 | Reset Zoom |

### REPL

| Shortcut | Action |
|----------|--------|
| Up/Down | History Navigation |
| Ctrl+Up/Down | History by Prefix |
| Ctrl+R | Reverse Search |
| Ctrl+L | Clear REPL |
| Escape | Cancel Input |

---

# Part 4: Implementation Roadmap

## Phase 1: Core Foundation

Build the basic application shell with the four-panel layout using PyQt6. Implement panel toggling, splitter persistence, and the menu structure with placeholder actions. Create the preferences dialog infrastructure.

## Phase 2: Forth Interpreter

Implement the lexer, dictionary, and outer interpreter. Add the core word set (stack manipulation, arithmetic, comparison, logic). Implement control structures and defining words. Build the execution hook system for GUI integration.

## Phase 3: Stack Widget

Create the StackItemWidget with value display and type indicators. Implement StackWidget with basic push/pop display. Add animation system with configurable timing. Implement operation animations (swap, rot, dup, etc.). Connect to interpreter hooks.

## Phase 4: Code Editor

Implement Forth syntax highlighting. Add line numbers, current line highlighting, and breakpoint gutters. Implement auto-completion with dictionary integration. Add bracket matching for control structures.

## Phase 5: REPL Integration

Build the REPL interface with prompt and history. Connect REPL to interpreter for evaluation. Implement output capture and formatting. Add session export functionality.

## Phase 6: File Browser and Project Support

Implement tree view with file/folder operations. Add project concepts and load order support. Implement file watching for external changes.

## Phase 7: Polish and Documentation

Refine animations and visual feedback. Implement keyboard shortcut customization. Write user documentation and built-in tutorial. Create word reference documentation.

---

# Appendix A: File Format Conventions

## Forth Source Files

FABLE recognizes the following extensions as Forth source: `.fs`, `.fth`, `.4th`, `.forth`. Files are assumed to be UTF-8 encoded.

## Project Configuration

Project settings are stored in `.fable/settings.json`:

```json
{
  "load_order": ["core.fs", "utils.fs", "main.fs"],
  "default_execution_mode": "step",
  "custom_words_file": "custom.fs"
}
```

## Session State

Session state is stored in `.fable/session.json`:

```json
{
  "open_files": ["main.fs", "utils.fs"],
  "active_file": "main.fs",
  "cursor_positions": {
    "main.fs": {"line": 42, "column": 10},
    "utils.fs": {"line": 1, "column": 0}
  },
  "breakpoints": {
    "main.fs": [15, 23, 47]
  }
}
```

---

# Appendix B: Stack Effect Notation

FABLE uses standard Forth stack effect notation with extensions for clarity:

```
( before -- after )
```

Common abbreviations:
- `n` — integer number
- `u` — unsigned integer
- `f` — floating-point number
- `flag` — boolean (0 or -1)
- `addr` — memory address
- `c` — character
- `xt` — execution token
- `"name"` — word parsed from input

Examples:
- `( n1 n2 -- sum )` — takes two integers, produces their sum
- `( -- )` — no stack effect
- `( n -- )` — consumes one integer, produces nothing
- `( -- n )` — produces one integer
- `( R: -- n )` — pushes to return stack

---

# Appendix C: Color Scheme Reference

## Dark Theme (Default)

| Element | Color | Hex |
|---------|-------|-----|
| Background (main) | Dark Charcoal | #1E1E1E |
| Background (panels) | Slightly Lighter | #252526 |
| Text (primary) | Off-White | #D4D4D4 |
| Text (secondary) | Gray | #808080 |
| Accent (primary) | Amber | #D4A017 |
| Accent (secondary) | Blue | #2E86AB |
| Error | Coral | #C0392B |
| Success | Green | #27AE60 |
| Type: Integer | Blue | #569CD6 |
| Type: Float | Green | #6A9955 |
| Type: Address | Amber | #D4A017 |
| Type: String | Purple | #C586C0 |
| Type: Boolean | Cyan | #4EC9B0 |

## Light Theme

| Element | Color | Hex |
|---------|-------|-----|
| Background (main) | White | #FFFFFF |
| Background (panels) | Light Gray | #F3F3F3 |
| Text (primary) | Dark Gray | #1E1E1E |
| Text (secondary) | Medium Gray | #6E6E6E |
| Accent (primary) | Dark Amber | #B8860B |
| Accent (secondary) | Dark Blue | #1A5276 |

---

*End of Specification*
