"""
Terminal/REPL widget for interactive Forth evaluation.
Enhanced with syntax highlighting, persistent history, and formatted output.
"""

import json
from pathlib import Path
from typing import List, Optional

from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import (
    QFont, QTextCursor, QColor, QTextCharFormat,
    QSyntaxHighlighter, QTextDocument
)
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QLineEdit, QCompleter
)


class ForthSyntaxHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for Forth code in the REPL input."""
    
    # Define word categories with colors
    KEYWORDS = {
        # Control flow
        'IF', 'ELSE', 'THEN', 'BEGIN', 'UNTIL', 'WHILE', 'REPEAT',
        'DO', 'LOOP', '+LOOP', 'LEAVE', 'EXIT',
        # Definitions
        ':', ';', 'VARIABLE', 'CONSTANT', 'CREATE', 'DOES>',
    }
    
    STACK_WORDS = {
        'DUP', 'DROP', 'SWAP', 'OVER', 'ROT', '-ROT', 'NIP', 'TUCK',
        '2DUP', '2DROP', '2SWAP', '2OVER', 'PICK', 'ROLL', 'DEPTH', 'CLEAR',
    }
    
    MATH_WORDS = {
        '+', '-', '*', '/', 'MOD', '/MOD', 'NEGATE', 'ABS',
        'MIN', 'MAX', '1+', '1-', '2+', '2-', '2*', '2/',
    }
    
    LOGIC_WORDS = {
        '=', '<>', '<', '>', '<=', '>=', '0=', '0<', '0>',
        'AND', 'OR', 'XOR', 'INVERT', 'NOT', 'TRUE', 'FALSE',
    }
    
    OUTPUT_WORDS = {
        '.', '.S', 'CR', 'SPACE', 'SPACES', 'EMIT', 'TYPE', '."',
        'WORDS', 'SEE',
    }
    
    def __init__(self, parent: QTextDocument):
        super().__init__(parent)
        
        # Format definitions
        self.formats = {
            'keyword': self._make_format('#C586C0'),      # Purple
            'stack': self._make_format('#569CD6'),        # Blue
            'math': self._make_format('#4EC9B0'),         # Cyan
            'logic': self._make_format('#6A9955'),        # Green
            'output': self._make_format('#D4A017'),       # Amber
            'number': self._make_format('#B5CEA8'),       # Light green
            'string': self._make_format('#CE9178'),       # Orange
            'comment': self._make_format('#6A9955', True), # Green italic
        }
    
    def _make_format(self, color: str, italic: bool = False) -> QTextCharFormat:
        """Create a text format with given color."""
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))
        if italic:
            fmt.setFontItalic(True)
        return fmt
    
    def highlightBlock(self, text: str):
        """Apply syntax highlighting to a block of text."""
        # Split into words and process each
        pos = 0
        for word in text.split():
            # Find position of this word
            idx = text.find(word, pos)
            if idx == -1:
                continue
            
            length = len(word)
            upper_word = word.upper()
            
            # Check category
            if upper_word in self.KEYWORDS:
                self.setFormat(idx, length, self.formats['keyword'])
            elif upper_word in self.STACK_WORDS:
                self.setFormat(idx, length, self.formats['stack'])
            elif upper_word in self.MATH_WORDS:
                self.setFormat(idx, length, self.formats['math'])
            elif upper_word in self.LOGIC_WORDS:
                self.setFormat(idx, length, self.formats['logic'])
            elif upper_word in self.OUTPUT_WORDS:
                self.setFormat(idx, length, self.formats['output'])
            elif self._is_number(word):
                self.setFormat(idx, length, self.formats['number'])
            
            pos = idx + length
        
        # Handle comments - backslash to end of line
        if '\\' in text:
            comment_start = text.find('\\')
            self.setFormat(comment_start, len(text) - comment_start, self.formats['comment'])
        
        # Handle parenthetical comments
        if '( ' in text and ')' in text:
            start = text.find('( ')
            end = text.find(')', start)
            if end > start:
                self.setFormat(start, end - start + 1, self.formats['comment'])
    
    def _is_number(self, word: str) -> bool:
        """Check if word is a number."""
        if word.startswith('$'):
            try:
                int(word[1:], 16)
                return True
            except ValueError:
                pass
        if word.lower().startswith('0x'):
            try:
                int(word, 16)
                return True
            except ValueError:
                pass
        try:
            float(word)
            return True
        except ValueError:
            return False


class HighlightedLineEdit(QLineEdit):
    """LineEdit with syntax highlighting via overlay."""
    
    def __init__(self, parent=None):
        super().__init__(parent)


class ForthREPL(QWidget):
    """Interactive REPL for Forth evaluation.
    
    Features:
    - Syntax-highlighted output
    - Command history with persistence
    - "ok" feedback after successful commands
    - Error display with context
    - Autocomplete for known words
    
    Signals:
        input_submitted(str): Emitted when user submits input
    """
    
    input_submitted = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._history: List[str] = []
        self._history_index = 0
        self._history_file = Path.home() / '.config' / 'fable' / 'history.json'
        self._pending_ok = False
        self._setup_ui()
        self._load_history()
    
    def _setup_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Output area
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setFont(QFont("Source Code Pro", 12))
        self.output.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                color: #B0B0B0;
                border: none;
                border-bottom: 1px solid #3C3C3C;
                padding: 8px;
            }
        """)
        layout.addWidget(self.output)
        
        # Input line
        self.input = QLineEdit()
        self.input.setFont(QFont("Source Code Pro", 12))
        self.input.setStyleSheet("""
            QLineEdit {
                background-color: #2D2D2D;
                color: #D4D4D4;
                border: none;
                padding: 8px 8px 8px 50px;
            }
        """)
        self.input.returnPressed.connect(self._on_input_submitted)
        layout.addWidget(self.input)
        
        # Prompt label (overlay on input)
        from PyQt6.QtWidgets import QLabel
        self.prompt_label = QLabel("ok> ", self.input)
        self.prompt_label.setFont(QFont("Source Code Pro", 12))
        self.prompt_label.setStyleSheet("color: #6A9955; background: transparent;")
        self.prompt_label.move(8, 8)
        
        # Welcome message
        self._append_colored("FABLE", "#D4A017", bold=True)
        self.append_output(" - Forth Animated Beginners Learning Environment\n")
        self._append_colored("────────────────────────────────────────────────────\n", "#3C3C3C")
        self.append_output("Type Forth commands. Use ↑/↓ for history.\n")
        self.append_output("Type WORDS to see available commands.\n\n")
    
    def _on_input_submitted(self):
        """Handle input submission."""
        text = self.input.text().strip()
        if not text:
            return
        
        # Handle special REPL commands
        if text.upper() == 'CLEAR':
            self.clear()
            self.input.clear()
            return
        
        # Add to history
        if not self._history or self._history[-1] != text:
            self._history.append(text)
            self._save_history()
        self._history_index = len(self._history)
        
        # Echo input with prompt
        self._append_colored("ok> ", "#6A9955")
        self._append_colored(f"{text}\n", "#D4D4D4")
        
        # Set pending ok flag
        self._pending_ok = True
        
        # Emit signal
        self.input_submitted.emit(text)
        
        # Show ok after a brief delay if no error occurred
        QTimer.singleShot(50, self._maybe_show_ok)
        
        self.input.clear()
    
    def _maybe_show_ok(self):
        """Show 'ok' if the command succeeded (no error was appended)."""
        if self._pending_ok:
            self._append_colored(" ok\n", "#6A9955")
            self._pending_ok = False
    
    def keyPressEvent(self, event):
        """Handle key presses for history navigation."""
        if event.key() == Qt.Key.Key_Up:
            self._navigate_history(-1)
            event.accept()
        elif event.key() == Qt.Key.Key_Down:
            self._navigate_history(1)
            event.accept()
        else:
            super().keyPressEvent(event)
    
    def _navigate_history(self, direction: int):
        """Navigate command history."""
        if not self._history:
            return
        
        new_index = self._history_index + direction
        if 0 <= new_index < len(self._history):
            self._history_index = new_index
            self.input.setText(self._history[self._history_index])
        elif new_index >= len(self._history):
            self._history_index = len(self._history)
            self.input.clear()
    
    def _load_history(self):
        """Load command history from file."""
        try:
            if self._history_file.exists():
                with open(self._history_file, 'r') as f:
                    data = json.load(f)
                    self._history = data.get('history', [])[-100:]  # Keep last 100
                    self._history_index = len(self._history)
        except Exception:
            pass
    
    def _save_history(self):
        """Save command history to file."""
        try:
            self._history_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self._history_file, 'w') as f:
                json.dump({'history': self._history[-100:]}, f)
        except Exception:
            pass
    
    def append_output(self, text: str):
        """Append text to output area."""
        self.output.moveCursor(QTextCursor.MoveOperation.End)
        self.output.insertPlainText(text)
        self.output.moveCursor(QTextCursor.MoveOperation.End)
    
    def append_error(self, text: str):
        """Append error text (red) and cancel pending ok."""
        self._pending_ok = False
        self._append_colored(f"Error: {text}\n", "#E57373")
    
    def _append_colored(self, text: str, color: str, bold: bool = False):
        """Append colored text to output."""
        cursor = self.output.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))
        if bold:
            fmt.setFontWeight(700)
        cursor.insertText(text, fmt)
        
        self.output.moveCursor(QTextCursor.MoveOperation.End)
    
    def clear(self):
        """Clear the output area."""
        self.output.clear()
    
    def set_prompt(self, prompt: str, color: str = "#6A9955"):
        """Set the prompt text and color.
        
        Args:
            prompt: Prompt text (e.g., 'ok> ' or ']> ')
            color: Prompt color hex code
        """
        self.prompt_label.setText(prompt)
        self.prompt_label.setStyleSheet(f"color: {color}; background: transparent;")
    
    def set_compile_mode(self, compiling: bool):
        """Update prompt for compile/interpret mode."""
        if compiling:
            self.set_prompt("]> ", "#C586C0")  # Purple for compile mode
        else:
            self.set_prompt("ok> ", "#6A9955")  # Green for interpret mode
    
    def show_stack_preview(self, stack: list):
        """Show a brief stack preview after commands."""
        if not stack:
            return
        preview = ' '.join(str(x) for x in stack[-5:])  # Last 5 items
        if len(stack) > 5:
            preview = "... " + preview
        self._append_colored(f"  [{preview}]\n", "#569CD6")
