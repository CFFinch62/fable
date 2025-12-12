# FABLE Phase 1 Changelog: Application Shell

**Completed:** December 12, 2025  
**Commit:** (see git log)

---

## Summary

Built the complete 4-panel IDE layout with functional menus, toolbar, status bar, and settings persistence. All panel widgets are implemented with proper styling and basic functionality.

---

## Files Created/Modified

### Core Application
- **`fable/app.py`** — Complete MainWindow with:
  - 4-panel layout using QSplitter (File Browser | Editor+REPL | Stack)
  - Full menu system (File, Edit, View, Run, Help)
  - Toolbar with New, Open, Save, Undo, Redo, Run, Step, Stop
  - Status bar with mode indicator and cursor position
  - Settings persistence for window geometry and panel visibility

### Widgets
- **`fable/widgets/file_browser.py`** — File tree with QFileSystemModel
- **`fable/widgets/editor.py`** — Code editor with:
  - Line numbers
  - Current line highlighting
  - Dark theme styling
  - Tab support for multiple files
- **`fable/widgets/repl.py`** — Terminal/REPL with:
  - Output display area
  - Input line with history navigation
  - Colored output support
- **`fable/widgets/stack_widget.py`** — Stack display with:
  - Data Stack and Return Stack sections
  - Speed slider control
  - Step button
- **`fable/widgets/stack_item.py`** — Stack item with type indicators

### Utilities
- **`fable/utils/settings.py`** — JSON-based settings persistence
- **`fable/utils/signals.py`** — Central signal definitions

---

## Features Implemented

### Layout
- [x] Horizontal splitter: File Browser | Center | Stack Widget
- [x] Vertical splitter: Editor (tabbed) | REPL
- [x] Panels resize with splitters
- [x] Panel visibility toggling (Ctrl+B, Ctrl+T)

### Menus
- [x] File: New, Open, Open Folder, Save, Save As, Exit
- [x] Edit: Undo, Redo, Cut, Copy, Paste
- [x] View: Toggle File Browser, Toggle REPL
- [x] Run: Run File (F5), Run Selection (F6), Run Line (F7), Reset
- [x] Help: About FABLE

### Toolbar
- [x] New, Open, Save, Undo, Redo, Run, Step, Stop

### Status Bar
- [x] Mode indicator (Interpret/Compile)
- [x] Cursor position (Ln, Col)
- [x] Stack effect display area (placeholder)

### Persistence
- [x] Window geometry saved/restored
- [x] Window state saved/restored
- [x] Panel visibility saved/restored
- [x] Settings stored in ~/.config/fable/settings.json

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+N | New File |
| Ctrl+O | Open File |
| Ctrl+K | Open Folder |
| Ctrl+S | Save |
| Ctrl+Shift+S | Save As |
| Ctrl+Q | Exit |
| Ctrl+Z | Undo |
| Ctrl+Y | Redo |
| Ctrl+B | Toggle File Browser |
| Ctrl+T | Toggle REPL |
| F5 | Run File |
| F6 | Run Selection |
| F7 | Run Line |
| Ctrl+R | Reset Interpreter |

---

## Bug Fixes

- Fixed `QFileSystemModel` import location (PyQt6.QtGui, not QtWidgets)

---

## Next Phase

**Phase 2: Forth Interpreter Core** — Implement lexer, dictionary, and basic Forth evaluation with stack manipulation and arithmetic words.
