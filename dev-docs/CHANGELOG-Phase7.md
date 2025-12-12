# FABLE Phase 7 Changelog: Control Flow

**Completed:** December 12, 2025

---

## Summary

Implemented complete control flow with conditionals (IF/ELSE/THEN), indefinite loops (BEGIN/UNTIL/WHILE/REPEAT), and counted loops (DO/LOOP/+LOOP).

---

## Files Modified

### Interpreter
- **`fable/interpreter/interpreter.py`**
  - Enhanced `_execute_compiled` with instruction pointer
  - Added BRANCH, 0BRANCH for jumps
  - Added loop_stack for DO/LOOP tracking
  - Supports I, J, LEAVE operations

### Primitives  
- **`fable/interpreter/primitives.py`**
  - Added `_register_control_flow_words` (14 new words)
  - Immediate words for compile-time operation

---

## New Control Flow Words

| Word | Stack Effect | Description |
|------|--------------|-------------|
| IF | ( flag -- ) | Start conditional |
| ELSE | ( -- ) | Alternative branch |
| THEN | ( -- ) | End conditional |
| BEGIN | ( -- ) | Start indefinite loop |
| UNTIL | ( flag -- ) | Loop back if false |
| WHILE | ( flag -- ) | Mid-loop test |
| REPEAT | ( -- ) | End BEGIN...WHILE |
| DO | ( limit index -- ) | Start counted loop |
| LOOP | ( -- ) | Increment and check |
| +LOOP | ( n -- ) | Custom increment |
| I | ( -- n ) | Push loop index |
| J | ( -- n ) | Push outer loop index |
| LEAVE | ( -- ) | Exit loop early |
| EXIT | ( -- ) | Exit current word |

---

## Total Words: 78
