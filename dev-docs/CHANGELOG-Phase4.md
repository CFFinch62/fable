# FABLE Phase 4 Changelog: REPL Integration

**Completed:** December 12, 2025  
**Commit:** (see git log)

---

## Summary

Enhanced the REPL with syntax-highlighted output, persistent command history, ok/error feedback, and compile mode prompt switching.

---

## Files Created/Modified

### REPL Widget
- **`fable/widgets/repl.py`** — Complete rewrite with:
  - `ForthSyntaxHighlighter` for colored output
  - Persistent history in `~/.config/fable/history.json`
  - "ok" feedback after successful commands
  - Error display in red with "Error:" prefix
  - Compile mode prompt switching (ok> / ]>)
  - CLEAR command to reset terminal
  - Stack preview display

### Integration
- **`fable/app.py`** — Added:
  - `_update_repl_mode()` for compile/interpret prompt switching
  - Connected `state_changed` to REPL mode updates

---

## REPL Features

| Feature | Description |
|---------|-------------|
| ok> prompt | Green prompt in interpret mode |
| ]> prompt | Purple prompt in compile mode |
| ok feedback | Shows "ok" after successful commands |
| Error display | Red "Error:" prefix for failures |
| History | Up/Down arrows, persists to disk |
| CLEAR | Type CLEAR to reset terminal |

---

## Color Scheme

| Category | Color | Example Words |
|----------|-------|---------------|
| Keywords | Purple | : ; IF THEN |
| Stack | Blue | DUP DROP SWAP |
| Math | Cyan | + - * / |
| Logic | Green | = < > AND OR |
| Output | Amber | . .S CR |
| Numbers | Light Green | 42 $FF 3.14 |
| Comments | Green Italic | \ ( ) |

---

## Next Phase

**Phase 5: Code Editor** — Syntax highlighting, bracket matching, and enhanced editing.
