"""
Terminal/REPL widget for interactive Forth evaluation.
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QTextCursor, QColor, QTextCharFormat
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QLineEdit
)


class ForthREPL(QWidget):
    """Interactive REPL for Forth evaluation.
    
    Contains an output area (read-only) and an input line.
    Supports command history navigation.
    
    Signals:
        input_submitted(str): Emitted when user submits input
    """
    
    input_submitted = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._history: list[str] = []
        self._history_index = 0
        self._setup_ui()
    
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
                padding: 8px;
            }
        """)
        self.input.setPlaceholderText("ok> ")
        self.input.returnPressed.connect(self._on_input_submitted)
        layout.addWidget(self.input)
        
        # Welcome message
        self.append_output("FABLE - Forth Animated Beginners Learning Environment\n")
        self.append_output("Type Forth commands below. Use UP/DOWN for history.\n")
        self.append_output("─" * 50 + "\n")
    
    def _on_input_submitted(self):
        """Handle input submission."""
        text = self.input.text().strip()
        if text:
            # Add to history
            self._history.append(text)
            self._history_index = len(self._history)
            
            # Echo input
            self._append_colored(f"ok> {text}\n", "#D4A017")
            
            # Emit signal
            self.input_submitted.emit(text)
        
        self.input.clear()
    
    def keyPressEvent(self, event):
        """Handle key presses for history navigation."""
        if event.key() == Qt.Key.Key_Up:
            self._navigate_history(-1)
        elif event.key() == Qt.Key.Key_Down:
            self._navigate_history(1)
        else:
            super().keyPressEvent(event)
    
    def _navigate_history(self, direction: int):
        """Navigate command history.
        
        Args:
            direction: -1 for older, +1 for newer
        """
        if not self._history:
            return
        
        new_index = self._history_index + direction
        if 0 <= new_index < len(self._history):
            self._history_index = new_index
            self.input.setText(self._history[self._history_index])
        elif new_index >= len(self._history):
            self._history_index = len(self._history)
            self.input.clear()
    
    def append_output(self, text: str):
        """Append text to output area.
        
        Args:
            text: Text to append
        """
        self.output.moveCursor(QTextCursor.MoveOperation.End)
        self.output.insertPlainText(text)
        self.output.moveCursor(QTextCursor.MoveOperation.End)
    
    def append_error(self, text: str):
        """Append error text (coral colored).
        
        Args:
            text: Error text to append
        """
        self._append_colored(text, "#E57373")
    
    def _append_colored(self, text: str, color: str):
        """Append colored text to output.
        
        Args:
            text: Text to append
            color: Hex color code
        """
        cursor = self.output.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))
        cursor.insertText(text, fmt)
        
        self.output.moveCursor(QTextCursor.MoveOperation.End)
    
    def clear(self):
        """Clear the output area."""
        self.output.clear()
    
    def set_prompt(self, prompt: str):
        """Set the input placeholder prompt.
        
        Args:
            prompt: Prompt text (e.g., 'ok> ' or ']> ')
        """
        self.input.setPlaceholderText(prompt)
