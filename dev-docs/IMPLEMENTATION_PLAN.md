# FABLE Implementation Plan

**8-Phase Development Roadmap**

---

## Phase 1: Application Shell

**Goal:** Basic window with 4-panel layout, menus, and panel toggling.

### Tasks
1. Create `MainWindow` with horizontal/vertical splitters
2. Add placeholder widgets for each panel (File Browser, Editor, REPL, Stack)
3. Implement View menu with toggle actions for File Browser and REPL
4. Add toolbar with common actions
5. Add status bar with mode/position display
6. Implement settings persistence for window geometry and splitter positions

### Acceptance Criteria
- [ ] Application launches and displays 4-panel layout
- [ ] File Browser and REPL panels toggle via menu and Ctrl+B/Ctrl+T
- [ ] Window position and panel sizes persist between sessions

### Files Modified
- `fable/app.py` — Full MainWindow implementation
- `fable/utils/settings.py` — Settings persistence
- `fable/widgets/*.py` — Basic widget shells with proper layouts

---

## Phase 2: Forth Interpreter Core

**Goal:** Working interpreter that can execute basic Forth and emit signals.

### Tasks
1. Implement `Lexer` class to tokenize Forth source
2. Implement `Dictionary` class with define/lookup methods
3. Implement `DictionaryEntry` class with metadata
4. Create `ForthInterpreter` class with data_stack, return_stack
5. Implement `evaluate()` method for outer interpreter
6. Add Qt signals: `word_starting`, `word_complete`, `output`, `error_occurred`
7. Implement stack words: DUP DROP SWAP OVER ROT .S DEPTH CLEAR
8. Implement arithmetic words: + - * / MOD NEGATE ABS MIN MAX 1+ 1-
9. Implement comparison/logic: = <> < > <= >= 0= 0< 0> AND OR XOR INVERT TRUE FALSE
10. Write comprehensive tests

### Acceptance Criteria
- [ ] Can evaluate `3 4 + .` and emit correct signals
- [ ] All Phase 1-3 words work correctly
- [ ] Errors emit `error_occurred` signal with helpful message
- [ ] All tests pass

### Files Modified
- `fable/interpreter/lexer.py` — Full tokenizer
- `fable/interpreter/dictionary.py` — Dictionary and entry classes
- `fable/interpreter/interpreter.py` — Core interpreter
- `fable/interpreter/primitives.py` — Word implementations
- `fable/interpreter/errors.py` — Exception classes
- `tests/test_lexer.py` — Lexer tests
- `tests/test_interpreter.py` — Interpreter tests

---

## Phase 3: Stack Widget

**Goal:** Animated stack display synchronized with interpreter.

### Tasks
1. Implement `StackItemWidget` with value display and type indicator
2. Implement `StackWidget` container with vertical layout
3. Add push animation (fade in + slide)
4. Add pop animation (highlight + fade out + slide)
5. Add swap animation (position exchange)
6. Add dup, rot, over animations
7. Add speed slider control
8. Connect to interpreter signals
9. Implement animation queue for sequential operations

### Acceptance Criteria
- [ ] Stack widget displays current stack state
- [ ] Push/pop/swap operations animate smoothly
- [ ] Speed slider adjusts animation duration
- [ ] Widget stays synchronized with interpreter state

### Files Modified
- `fable/widgets/stack_item.py` — Stack item with animations
- `fable/widgets/stack_widget.py` — Container with controls
- `tests/test_stack_widget.py` — Widget tests

---

## Phase 4: REPL Integration

**Goal:** Interactive Forth session with history.

### Tasks
1. Implement `ForthREPL` widget with output area and input line
2. Connect input to `interpreter.evaluate()`
3. Connect `interpreter.output` to REPL display
4. Implement command history with Up/Down navigation
5. Implement prompt display (ok> vs ]>)
6. Add error display formatting (coral color)
7. Implement session export to file

### Acceptance Criteria
- [ ] Can type Forth at prompt and see results
- [ ] Stack changes animate in stack widget
- [ ] History navigation works
- [ ] Errors display with helpful message
- [ ] Session can be exported

### Files Modified
- `fable/widgets/repl.py` — Full REPL implementation
- `fable/app.py` — Wire up REPL to interpreter

---

## Phase 5: Code Editor

**Goal:** Syntax-highlighted editor with Forth features.

### Tasks
1. Implement `ForthEditor` based on QPlainTextEdit
2. Add line number gutter
3. Implement `ForthHighlighter` with Forth syntax rules
4. Add current line highlighting
5. Implement basic bracket matching (: ; pairs)
6. Add Run File (F5) and Run Selection (F6) functionality
7. Implement tab management for multiple files

### Acceptance Criteria
- [ ] Forth code displays with syntax highlighting
- [ ] Line numbers display correctly
- [ ] Current line is highlighted
- [ ] F5 runs entire file, F6 runs selection
- [ ] Multiple files can be open in tabs

### Files Modified
- `fable/widgets/editor.py` — Full editor implementation
- `fable/syntax/forth_highlighter.py` — Syntax highlighter
- `fable/app.py` — Editor integration

---

## Phase 6: File Browser

**Goal:** Project file navigation.

### Tasks
1. Implement `FileBrowser` with QTreeView and QFileSystemModel
2. Add file type icons for Forth files
3. Implement double-click to open file in editor
4. Add context menu (New File, Rename, Delete)
5. Implement Open Folder action to set project root

### Acceptance Criteria
- [ ] File browser shows folder contents in tree
- [ ] Double-clicking .fs file opens it in editor
- [ ] Context menu operations work
- [ ] Can open a folder as project

### Files Modified
- `fable/widgets/file_browser.py` — Full browser implementation
- `fable/app.py` — File browser integration

---

## Phase 7: Control Flow & Step Mode

**Goal:** Complete interpreter with step-through debugging.

### Tasks
1. Implement control flow: IF ELSE THEN BEGIN UNTIL WHILE REPEAT DO LOOP +LOOP I J LEAVE
2. Implement colon definition compiler (: name ... ;)
3. Implement CONSTANT, VARIABLE, @, !, +!
4. Add step mode to interpreter
5. Add Step button to stack widget
6. Implement stack effect preview display
7. Add breakpoint support in editor

### Acceptance Criteria
- [ ] Control flow words work correctly
- [ ] Can define new words with : ;
- [ ] Step mode pauses after each word
- [ ] Stack effect preview shows before execution
- [ ] Breakpoints pause execution

### Files Modified
- `fable/interpreter/primitives.py` — Control flow words
- `fable/interpreter/compiler.py` — Colon definition compiler
- `fable/interpreter/interpreter.py` — Step mode support
- `fable/widgets/stack_widget.py` — Step controls, preview
- `fable/widgets/editor.py` — Breakpoint support

---

## Fixes Phase

**Goal:** Bug fixes, polish, and final refinements.

### Tasks
- Address bugs discovered during development
- UI polish and refinements
- Performance optimizations
- Accessibility improvements
- Documentation updates
- Remaining word implementations (Phase 7-8 words from spec)

### Tracking
All fixes tracked in `CHANGELOG-Fixes.md` with:
- Issue description
- Root cause
- Solution implemented
- Files affected
