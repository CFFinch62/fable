# FABLE Phase 6 Changelog: File Browser

**Completed:** December 12, 2025  
**Commit:** (see git log)

---

## Summary

Enhanced the file browser with a context menu for file operations, Forth file type awareness, and system file manager integration.

---

## Files Modified

### File Browser Widget
- **`fable/widgets/file_browser.py`** — Complete enhancement:
  - `ForthFileSystemModel` with Forth file type awareness
  - Context menu with file operations
  - Signals for file created/deleted events
  - System file manager integration

---

## Context Menu Actions

| Action | Description |
|--------|-------------|
| New File | Creates a new `.fs` file in selected folder |
| New Folder | Creates a new folder |
| Rename | Renames selected file or folder |
| Delete | Deletes with confirmation dialog |
| Refresh | Refreshes the file tree |
| Reveal in File Manager | Opens folder in system file manager |

---

## Features

- **Forth File Awareness**: Model knows about `.fs`, `.fth`, `.4th`, `.forth`, `.f` extensions
- **Sorted Display**: Files and folders sorted alphabetically
- **Animated Tree**: Smooth expand/collapse animations
- **Dark Theme**: Consistent with IDE styling
- **Signals**: `file_created` and `file_deleted` for app integration

---

## Next Phase

**Phase 7: Control Flow & Step Mode** — IF/ELSE/THEN, loops, and step-through debugging.
