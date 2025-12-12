# FABLE Development Prompt

## AI-Assisted Development Guide for Forth Animated Beginners Learning Environment

---

## Project Identity

**Name:** FABLE (Forth Animated Beginners Learning Environment)  
**Tagline:** "Every stack tells a story"  
**Developer:** Chuck / Fragillidae Software  
**Framework:** Python 3.11+ with PyQt6  
**License:** [To be determined by developer]

---

## Project Overview

FABLE is an educational IDE for learning the Forth programming language. Its distinguishing feature is an animated stack visualization that shows stack operations in real time, transforming abstract stack manipulation into observable, concrete processes.

The application consists of four integrated components:

1. **Animated Stack Widget** — Real-time visual display of data and return stacks with smooth animations for push, pop, swap, rot, dup, and other operations
2. **Forth Interpreter** — A purpose-built educational Forth interpreter with execution hooks for animation synchronization
3. **Code Editor** — Syntax-highlighted editor with Forth-specific features (bracket matching for control structures, stack effect tooltips, auto-completion from dictionary)
4. **Terminal/REPL** — Interactive Forth session with history, multi-line input support, and session export

The IDE layout has a file browser on the left (toggleable), editor and REPL in the center (REPL toggleable), and the animated stack on the right (always visible).

---

## Technical Foundation

### Required Dependencies

```
PyQt6>=6.5.0
```

### Project Structure

```
fable/
├── main.py                     # Application entry point
├── requirements.txt            # Dependencies
├── README.md                   # Project documentation
│
├── fable/                      # Main package
│   ├── __init__.py
│   ├── app.py                  # QApplication setup and main window
│   │
│   ├── interpreter/            # Forth interpreter package
│   │   ├── __init__.py
│   │   ├── lexer.py            # Tokenizer
│   │   ├── dictionary.py       # Word dictionary and entries
│   │   ├── interpreter.py      # Core interpreter logic
│   │   ├── primitives.py       # Built-in word implementations
│   │   ├── compiler.py         # Colon definition compiler
│   │   └── errors.py           # Custom exception classes
│   │
│   ├── widgets/                # PyQt6 widgets package
│   │   ├── __init__.py
│   │   ├── stack_widget.py     # Animated stack display
│   │   ├── stack_item.py       # Individual stack item widget
│   │   ├── editor.py           # Code editor widget
│   │   ├── repl.py             # Terminal/REPL widget
│   │   ├── file_browser.py     # File/folder tree view
│   │   └── preferences.py      # Preferences dialog
│   │
│   ├── syntax/                 # Syntax highlighting
│   │   ├── __init__.py
│   │   └── forth_highlighter.py
│   │
│   ├── resources/              # Assets
│   │   ├── icons/              # Application icons
│   │   ├── themes/             # Color scheme definitions
│   │   └── tutorial/           # Built-in tutorial content
│   │
│   └── utils/                  # Utility modules
│       ├── __init__.py
│       ├── settings.py         # Settings management
│       └── signals.py          # Custom Qt signals
│
└── tests/                      # Test suite
    ├── __init__.py
    ├── test_interpreter.py
    ├── test_lexer.py
    ├── test_dictionary.py
    └── test_stack_widget.py
```

### Color Scheme Constants

Use these throughout the application for visual consistency:

```python
# Dark theme (default)
COLORS = {
    'bg_main': '#1E1E1E',
    'bg_panel': '#252526',
    'bg_input': '#2D2D2D',
    'text_primary': '#D4D4D4',
    'text_secondary': '#808080',
    'accent_amber': '#D4A017',
    'accent_blue': '#2E86AB',
    'error': '#C0392B',
    'success': '#27AE60',
    'type_int': '#569CD6',
    'type_float': '#6A9955',
    'type_addr': '#D4A017',
    'type_string': '#C586C0',
    'type_bool': '#4EC9B0',
    'stack_item_bg': '#F5F5F5',
    'stack_item_text': '#1E1E1E',
}
```

---

## Development Guidelines

### Code Style

Follow these conventions throughout the codebase:

1. **Docstrings:** Every class and public method requires a docstring explaining purpose, parameters, and return values
2. **Type Hints:** Use type hints for all function signatures
3. **Signal Documentation:** Document all Qt signals with their parameter types and when they are emitted
4. **Constants:** Define magic numbers and strings as named constants at module level
5. **Error Messages:** User-facing error messages should be helpful and educational, not terse

### Architecture Principles

1. **Separation of Concerns:** The interpreter knows nothing about the GUI; communication is via signals only
2. **Testability:** Interpreter logic must be fully testable without Qt
3. **Extensibility:** New Forth words can be added by defining functions and registering them with the dictionary
4. **Configuration:** All hardcoded values that a user might want to change should be in settings

### Widget Communication Pattern

Widgets communicate through Qt signals, not direct method calls:

```python
# Interpreter emits signal when word executes
interpreter.word_complete.connect(stack_widget.on_word_complete)

# Stack widget emits signal when animation finishes
stack_widget.animation_complete.connect(interpreter.on_animation_complete)

# REPL sends input to interpreter
repl.input_submitted.connect(interpreter.evaluate)

# Interpreter sends output to REPL
interpreter.output.connect(repl.append_output)
```

---

## Component Specifications

### Component 1: Forth Interpreter

#### Purpose

Execute Forth code and emit signals that drive the stack visualization. Provide beginner-friendly error messages.

#### Key Classes

**ForthInterpreter** — Main interpreter class
- Properties: `data_stack`, `return_stack`, `dictionary`, `compiling`, `execution_mode`
- Methods: `evaluate(source)`, `step()`, `reset()`, `push()`, `pop()`
- Signals: `word_starting`, `word_complete`, `error_occurred`, `output`, `state_changed`

**Lexer** — Tokenizes Forth source
- Methods: `tokenize(source) -> List[Token]`
- Token types: WORD, NUMBER, STRING, COMMENT

**Dictionary** — Stores word definitions
- Methods: `define()`, `lookup()`, `forget()`, `words()`, `see()`

**DictionaryEntry** — Single word definition
- Properties: `name`, `code`, `immediate`, `stack_effect`, `docstring`

#### Execution Modes

1. **Run Mode:** Execute continuously, emit signals for each word
2. **Synchronized Mode:** Wait for `animation_complete` signal after each word
3. **Step Mode:** Execute one word, pause until `step()` called

#### Required Word Set (Implement in Order)

**Phase 1 — Stack Basics:**
```
DUP DROP SWAP OVER ROT .S DEPTH CLEAR
```

**Phase 2 — Arithmetic:**
```
+ - * / MOD NEGATE ABS MIN MAX 1+ 1-
```

**Phase 3 — Comparison and Logic:**
```
= <> < > <= >= 0= 0< 0> AND OR XOR INVERT TRUE FALSE
```

**Phase 4 — Output:**
```
. CR SPACE SPACES EMIT ." .(
```

**Phase 5 — Definitions:**
```
: ; CONSTANT VARIABLE @ ! +!
```

**Phase 6 — Control Flow:**
```
IF ELSE THEN BEGIN UNTIL WHILE REPEAT DO LOOP +LOOP I J LEAVE
```

**Phase 7 — Advanced Stack:**
```
-ROT NIP TUCK 2DUP 2DROP 2SWAP 2OVER PICK ROLL
```

**Phase 8 — Return Stack:**
```
>R R> R@ 2>R 2R> 2R@
```

#### Error Message Format

Errors should educate, not just report:

```python
# Bad
"Stack underflow"

# Good
"Stack underflow: '+' needs 2 values, but the stack only has 1.\n"
"The '+' word adds two numbers together.\n"
"Try pushing another number first, like: 5 3 +"
```

---

### Component 2: Animated Stack Widget

#### Purpose

Visually display the data stack and return stack with animations that illustrate how operations transform the stack.

#### Key Classes

**StackWidget(QWidget)** — Container for stack display
- Properties: `items`, `animation_speed`, `step_mode`, `preview_enabled`
- Methods: `push()`, `pop()`, `animate_operation()`, `show_preview()`, `set_speed()`
- Signals: `animation_complete`, `step_requested`, `stack_changed`

**StackItemWidget(QFrame)** — Single stack value display
- Properties: `value`, `value_type`, `highlighted`
- Methods: `animate_in()`, `animate_out()`, `animate_move()`, `highlight()`

#### Animation Specifications

| Operation | Duration (1x) | Visual Effect |
|-----------|---------------|---------------|
| Push | 150ms | Fade in + slide down from above |
| Pop | 150ms | Highlight amber, fade out + slide up |
| Swap | 300ms | Two items exchange positions with ease-in-out |
| Rot | 400ms | Three items rotate with slight arc motion |
| Dup | 200ms | TOS pulses, copy splits off and slides up |
| Drop | 150ms | Fade out + slide up (no highlight) |
| Over | 250ms | Second item pulses, copy moves to TOS |

#### Speed Control

Speed multiplier range: 0.25x to 4.0x (default 1.0x)

```python
actual_duration = base_duration / speed_multiplier
```

#### Stack Item Visual Design

```
┌──────────────────────┐
│ ▌ 42                 │  ← Blue strip = integer type
└──────────────────────┘
   ↑                 ↑
   Type indicator    Value (monospace font)
```

Type indicator colors:
- Integer: Blue (#569CD6)
- Float: Green (#6A9955)
- Address: Amber (#D4A017)
- String: Purple (#C586C0)
- Boolean: Cyan (#4EC9B0)

#### Stack Effect Preview

When enabled and paused, before executing a word:
1. Items to be consumed show dashed border + 50% opacity
2. Ghost items (results) appear above stack in muted color
3. Stack effect notation displays in tooltip: `( n1 n2 -- sum )`

---

### Component 3: Code Editor

#### Purpose

Edit Forth source files with syntax highlighting, auto-completion, and Forth-specific features.

#### Key Classes

**ForthEditor(QPlainTextEdit)** — Main editor widget
- Features: Line numbers, current line highlight, bracket matching
- Methods: `set_text()`, `get_text()`, `highlight_line()`, `set_breakpoint()`
- Signals: `text_changed`, `cursor_word_changed`, `breakpoint_toggled`

**ForthHighlighter(QSyntaxHighlighter)** — Syntax highlighting
- Highlight categories: core words, definitions, comments, strings, numbers

**LineNumberArea(QWidget)** — Line number gutter

#### Syntax Highlighting Rules

| Category | Examples | Color |
|----------|----------|-------|
| Stack words | DUP DROP SWAP OVER ROT | Amber |
| Arithmetic | + - * / MOD | Blue |
| Comparison | = < > | Blue |
| Control flow | IF ELSE THEN BEGIN UNTIL DO LOOP | Purple |
| Definitions | : ; CONSTANT VARIABLE | Bold, Amber |
| Comments | \ ... and ( ... ) | Gray, italic |
| Strings | ." ..." and S" ..." | Green |
| Numbers | 42, -17, 3.14, $FF | Cyan |

#### Bracket Matching

Match these Forth control structure pairs:
- `: ... ;`
- `IF ... THEN` and `IF ... ELSE ... THEN`
- `BEGIN ... UNTIL` and `BEGIN ... WHILE ... REPEAT` and `BEGIN ... AGAIN`
- `DO ... LOOP` and `DO ... +LOOP`
- `CASE ... ENDCASE`
- `( ... )`

When cursor is on one element, highlight its matching element.

#### Auto-Completion

Trigger after 2 characters typed. Show popup with:
- Word name
- Stack effect
- Brief description

Source completions from interpreter's dictionary.

---

### Component 4: Terminal/REPL

#### Purpose

Provide interactive Forth evaluation with command history and formatted output.

#### Key Classes

**ForthREPL(QWidget)** — REPL container
- Contains: Output display (QTextEdit, read-only) + Input line (QLineEdit)
- Properties: `history`, `history_index`
- Methods: `append_output()`, `append_error()`, `clear()`, `export_session()`
- Signals: `input_submitted`

#### Prompt Format

```
ok> _           (interpret mode)
]> _            (compile mode, inside definition)
... _           (continuation, incomplete input)
```

#### Visual Formatting

- Input echo: White text
- Normal output: Light gray
- Error output: Coral (#E57373)
- Prompt: Amber

#### History Features

- Up/Down arrows navigate history
- History persists between sessions (save to settings file)
- Ctrl+R for reverse incremental search

#### Multi-line Input

Detect incomplete input:
- `:` without matching `;`
- `IF` without matching `THEN`
- Unclosed string

Show continuation prompt and accumulate lines until complete.

---

### Component 5: File Browser

#### Purpose

Navigate project files and folders with standard file operations.

#### Key Classes

**FileBrowser(QWidget)** — File browser panel
- Contains: QTreeView with QFileSystemModel
- Methods: `set_root_path()`, `get_selected_path()`
- Signals: `file_double_clicked`, `file_selected`

#### Features

- Tree view of project folder
- Context menu: New File, New Folder, Rename, Delete, Copy Path
- File icons distinguish Forth files (.fs, .fth, .4th, .forth)
- Double-click opens file in editor

---

### Component 6: Main Window

#### Purpose

Integrate all components into cohesive IDE layout.

#### Layout Structure

```
┌─────────────────────────────────────────────────────────────────┐
│ Menu Bar                                                         │
├─────────────────────────────────────────────────────────────────┤
│ Toolbar                                                          │
├────────────┬────────────────────────────────┬───────────────────┤
│            │                                │                   │
│   File     │        Code Editor             │    Animated       │
│   Browser  │        (with tabs)             │    Stack          │
│            │                                │    Widget         │
│  (toggle)  ├────────────────────────────────┤                   │
│            │                                │   [Data Stack]    │
│            │        Terminal/REPL           │                   │
│            │        (toggle)                │   [Return Stack]  │
│            │                                │                   │
├────────────┴────────────────────────────────┴───────────────────┤
│ Status Bar                                                       │
└─────────────────────────────────────────────────────────────────┘
```

#### Splitter Configuration

- Horizontal splitter: File Browser | Center | Stack Widget
- Vertical splitter (center): Editor | REPL
- Save/restore splitter positions in settings

#### Menu Structure

Implement menus as specified in the full specification document. Key shortcuts:

| Action | Shortcut |
|--------|----------|
| Run File | F5 |
| Run Selection | F6 |
| Step | F10 |
| Continue | F8 |
| Stop | Shift+F5 |
| Toggle File Browser | Ctrl+B |
| Toggle REPL | Ctrl+T |
| Reset Interpreter | Ctrl+R |

---

## Implementation Phases

### Phase 1: Application Shell

**Goal:** Basic window with four-panel layout, menus, and panel toggling.

**Tasks:**
1. Create main.py entry point with QApplication setup
2. Implement MainWindow with horizontal/vertical splitters
3. Add placeholder widgets for each panel
4. Implement View menu with toggle actions for File Browser and REPL
5. Add status bar with placeholder text
6. Implement settings persistence for window geometry and splitter positions

**Acceptance Criteria:**
- Application launches and displays four-panel layout
- File Browser and REPL panels toggle via menu and keyboard shortcuts
- Window position and panel sizes persist between sessions

---

### Phase 2: Forth Interpreter Core

**Goal:** Working interpreter that can execute basic Forth and emit signals.

**Tasks:**
1. Implement Lexer class to tokenize Forth source
2. Implement Dictionary class with define/lookup methods
3. Implement DictionaryEntry class
4. Create ForthInterpreter class with data_stack, return_stack
5. Implement evaluate() method for outer interpreter
6. Add Qt signals: word_starting, word_complete, output, error_occurred
7. Implement Phase 1 words: DUP DROP SWAP OVER ROT .S DEPTH CLEAR
8. Implement Phase 2 words: + - * / MOD NEGATE ABS MIN MAX 1+ 1-
9. Write comprehensive tests for lexer and interpreter

**Acceptance Criteria:**
- Can evaluate `3 4 + .` and emit correct signals
- All Phase 1 and 2 words work correctly
- Errors emit error_occurred signal with helpful message
- All tests pass

---

### Phase 3: Stack Widget

**Goal:** Animated stack display synchronized with interpreter.

**Tasks:**
1. Implement StackItemWidget with value display and type indicator
2. Implement StackWidget container with vertical layout
3. Add push animation (fade in + slide)
4. Add pop animation (highlight + fade out + slide)
5. Add swap animation (position exchange)
6. Add speed slider control
7. Connect to interpreter signals
8. Implement animation queue for sequential operations

**Acceptance Criteria:**
- Stack widget displays current stack state
- Push/pop operations animate smoothly
- Swap animates correctly
- Speed slider adjusts animation duration
- Widget stays synchronized with interpreter state

---

### Phase 4: REPL Integration

**Goal:** Interactive Forth session with history.

**Tasks:**
1. Implement ForthREPL widget with output area and input line
2. Connect input to interpreter.evaluate()
3. Connect interpreter.output to REPL display
4. Implement command history with Up/Down navigation
5. Implement prompt display (ok> vs ]>)
6. Add error display formatting (coral color)
7. Implement session export to file

**Acceptance Criteria:**
- Can type Forth at prompt and see results
- Stack changes animate in stack widget
- History navigation works
- Errors display in coral with helpful message
- Session can be exported to text file

---

### Phase 5: Code Editor

**Goal:** Syntax-highlighted editor with Forth features.

**Tasks:**
1. Implement ForthEditor based on QPlainTextEdit
2. Add line number gutter
3. Implement ForthHighlighter with Forth syntax rules
4. Add current line highlighting
5. Implement basic bracket matching (: ; pairs)
6. Add Run File (F5) and Run Selection (F6) functionality
7. Implement tab management for multiple files

**Acceptance Criteria:**
- Forth code displays with syntax highlighting
- Line numbers display correctly
- Current line is highlighted
- F5 runs entire file through interpreter
- F6 runs selected text
- Multiple files can be open in tabs

---

### Phase 6: File Browser

**Goal:** Project file navigation.

**Tasks:**
1. Implement FileBrowser with QTreeView and QFileSystemModel
2. Add file type icons for Forth files
3. Implement double-click to open file in editor
4. Add context menu with New File, Rename, Delete
5. Implement Open Folder action to set project root

**Acceptance Criteria:**
- File browser shows folder contents in tree
- Double-clicking .fs file opens it in editor
- Context menu operations work
- Can open a folder as project

---

### Phase 7: Control Flow and Step Mode

**Goal:** Complete interpreter with step-through debugging.

**Tasks:**
1. Implement Phase 6 words: IF ELSE THEN BEGIN UNTIL WHILE REPEAT DO LOOP +LOOP I J LEAVE
2. Implement colon definition compiler
3. Add step mode to interpreter
4. Add Step button to stack widget
5. Implement stack effect preview display
6. Add breakpoint support in editor

**Acceptance Criteria:**
- Control flow words work correctly
- Can define new words with : ;
- Step mode pauses after each word
- Stack effect preview shows before execution
- Breakpoints pause execution

---

### Phase 8: Polish and Documentation

**Goal:** Production-ready application.

**Tasks:**
1. Implement preferences dialog
2. Add all remaining words from specification
3. Implement HELP word with built-in documentation
4. Add SEE word for decompilation
5. Create user documentation
6. Add welcome/tutorial screen
7. Comprehensive testing and bug fixes
8. Package for distribution

**Acceptance Criteria:**
- All specified words implemented
- Preferences dialog allows customization
- HELP word provides useful information
- Application is stable and polished

---

## Testing Requirements

### Interpreter Tests

Test every word in isolation:

```python
def test_dup():
    interp = ForthInterpreter()
    interp.evaluate("5 DUP")
    assert interp.data_stack == [5, 5]

def test_add():
    interp = ForthInterpreter()
    interp.evaluate("3 4 +")
    assert interp.data_stack == [7]

def test_stack_underflow():
    interp = ForthInterpreter()
    with pytest.raises(StackUnderflowError):
        interp.evaluate("+")
```

### Widget Tests

Use pytest-qt for widget testing:

```python
def test_stack_widget_push(qtbot):
    widget = StackWidget()
    qtbot.addWidget(widget)
    widget.push(42)
    assert len(widget.items) == 1
    assert widget.items[0].value == 42
```

### Integration Tests

Test interpreter-widget communication:

```python
def test_interpreter_stack_sync(qtbot):
    interp = ForthInterpreter()
    widget = StackWidget()
    interp.word_complete.connect(widget.sync_stack)
    
    interp.evaluate("1 2 3")
    qtbot.wait(500)  # Wait for animations
    
    assert len(widget.items) == 3
```

---

## Reference Documents

The full FABLE specification document contains additional details on:

- Complete word set with stack effects
- Animation timing specifications
- Color scheme reference
- Keyboard shortcut table
- File format conventions
- Error message templates

Consult the specification when implementing any component.

---

## Development Notes

### When Implementing Words

Each primitive word follows this pattern:

```python
def word_add(interp: ForthInterpreter) -> None:
    """Addition ( n1 n2 -- sum )
    
    Adds two numbers and pushes the result.
    """
    if len(interp.data_stack) < 2:
        raise StackUnderflowError(
            word="+",
            needed=2,
            available=len(interp.data_stack),
            hint="The '+' word adds two numbers together. "
                 "Try pushing another number first."
        )
    b = interp.pop()
    a = interp.pop()
    interp.push(a + b)
```

Register words with their metadata:

```python
interp.dictionary.define("+", DictionaryEntry(
    name="+",
    code=word_add,
    immediate=False,
    stack_effect="( n1 n2 -- sum )",
    docstring="Adds two numbers and pushes the result."
))
```

### When Implementing Animations

Use QPropertyAnimation for smooth transitions:

```python
def animate_in(self):
    self.setWindowOpacity(0)
    self.show()
    
    anim = QPropertyAnimation(self, b"windowOpacity")
    anim.setDuration(int(150 / self.parent().animation_speed))
    anim.setStartValue(0)
    anim.setEndValue(1)
    anim.setEasingCurve(QEasingCurve.Type.OutCubic)
    anim.start()
```

### When Connecting Signals

Keep components decoupled:

```python
# In MainWindow.__init__():
self.interpreter.word_complete.connect(self.stack_widget.on_word_complete)
self.interpreter.output.connect(self.repl.append_output)
self.interpreter.error_occurred.connect(self.repl.append_error)
self.repl.input_submitted.connect(self.interpreter.evaluate)
self.stack_widget.animation_complete.connect(self.interpreter.on_animation_complete)
self.editor.run_requested.connect(self.interpreter.evaluate)
```

---

## Summary

FABLE is an educational Forth IDE centered on an animated stack visualization. The architecture separates the Forth interpreter from the GUI through Qt signals, enabling clean testing and flexible execution modes (run, synchronized, step).

Build incrementally: shell first, then interpreter, then stack widget, then REPL, then editor, then file browser, then polish. Each phase produces a working application with increasing functionality.

The key pedagogical feature is the animated stack—invest time making it clear, smooth, and educational. Students should be able to watch `3 4 + 5 *` execute and understand exactly what happens at each step.
