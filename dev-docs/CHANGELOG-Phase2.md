# FABLE Phase 2 Changelog: Forth Interpreter Core

**Completed:** December 12, 2025  
**Commit:** (see git log)

---

## Summary

Implemented a complete, educational Forth interpreter with 60 primitive words, Qt signals for GUI integration, and beginner-friendly error messages.

---

## Files Created/Modified

### Interpreter Core
- **`fable/interpreter/lexer.py`** — Tokenizer with:
  - Whitespace-separated word parsing
  - Number parsing (decimal, hex with `$` or `0x`)
  - String literals (`."`, `S"`)
  - Line comments (`\`) and parenthetical comments (`(...)`)
  - Source location tracking (line, column)

- **`fable/interpreter/dictionary.py`** — Dictionary with:
  - Case-insensitive word lookup
  - `FORGET` operation
  - Similar word suggestions for typos
  - `SEE` decompilation support

- **`fable/interpreter/interpreter.py`** — Core interpreter with:
  - Data stack and return stack
  - `evaluate()` method for source execution
  - Compile mode support for `:` definitions
  - Qt signals: `word_starting`, `word_complete`, `output`, `error_occurred`

- **`fable/interpreter/primitives.py`** — 60 primitive words

- **`fable/interpreter/errors.py`** — Educational error classes:
  - `StackUnderflowError` with word-specific hints
  - `UnknownWordError` with "did you mean?" suggestions
  - `DivisionByZeroError`
  - `CompileOnlyError`, `ControlStructureError`

### Integration
- **`fable/app.py`** — Added:
  - `ForthInterpreter` instance in MainWindow
  - REPL input → interpreter evaluation
  - Interpreter output/errors → REPL display
  - Mode display updates in status bar

### Tests
- **`tests/test_lexer.py`** — 15 test cases
- **`tests/test_interpreter.py`** — 25 test cases

---

## Word Sets Implemented (60 words)

### Stack Manipulation (16)
```
DUP DROP SWAP OVER ROT -ROT NIP TUCK
2DUP 2DROP 2SWAP 2OVER DEPTH PICK ROLL CLEAR
```

### Arithmetic (16)
```
+ - * / MOD /MOD
NEGATE ABS MIN MAX
1+ 1- 2+ 2- 2* 2/
```

### Comparison (9)
```
= <> < > <= >= 0= 0< 0>
```

### Logic (9)
```
AND OR XOR INVERT LSHIFT RSHIFT TRUE FALSE NOT
```

### Output (10)
```
. .S CR SPACE SPACES EMIT TYPE ." WORDS SEE
```

---

## Key Features

- **Educational Error Messages**: Errors explain what went wrong and how to fix it
- **Qt Signal Integration**: All word executions emit signals for GUI updates
- **Type-Aware Display**: Stack items tagged with types for future color coding
- **Hex Number Support**: Both `$FF` and `0xFF` syntax
- **Case-Insensitive**: Words match regardless of case

---

## Next Phase

**Phase 3: Stack Widget** — Animated stack display synchronized with interpreter.
