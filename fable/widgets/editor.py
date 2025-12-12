"""
Code editor widget with Forth-specific features.
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QPainter
from PyQt6.QtWidgets import QPlainTextEdit, QWidget, QTextEdit


class LineNumberArea(QWidget):
    """Widget for displaying line numbers in the editor gutter."""
    
    def __init__(self, editor: 'ForthEditor'):
        super().__init__(editor)
        self.editor = editor
    
    def sizeHint(self):
        return self.editor.line_number_area_width(), 0
    
    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)


class ForthEditor(QPlainTextEdit):
    """Code editor with Forth-specific features.
    
    Features:
        - Line numbers
        - Current line highlighting
        - Monospace font
    
    Signals:
        cursor_word_changed(str): Emitted when word under cursor changes
        run_requested(str): Emitted when code should be executed
    """
    
    cursor_word_changed = pyqtSignal(str)
    run_requested = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._setup_line_numbers()
    
    def _setup_ui(self):
        """Initialize editor appearance."""
        # Monospace font
        font = QFont("Source Code Pro", 14)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.setFont(font)
        
        # Dark theme
        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1E1E1E;
                color: #D4D4D4;
                border: none;
                selection-background-color: #264F78;
            }
        """)
        
        # Tab settings
        self.setTabStopDistance(self.fontMetrics().horizontalAdvance(' ') * 4)
    
    def _setup_line_numbers(self):
        """Set up line number area."""
        self.line_number_area = LineNumberArea(self)
        
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        
        self.update_line_number_area_width(0)
        self.highlight_current_line()
    
    def line_number_area_width(self) -> int:
        """Calculate width needed for line number area."""
        digits = len(str(max(1, self.blockCount())))
        space = 10 + self.fontMetrics().horizontalAdvance('9') * digits
        return space
    
    def update_line_number_area_width(self, _):
        """Update editor margins for line number area."""
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)
    
    def update_line_number_area(self, rect, dy):
        """Update line number area on scroll/edit."""
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), 
                                         self.line_number_area.width(), rect.height())
        
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)
    
    def resizeEvent(self, event):
        """Handle resize to update line number area."""
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(cr.left(), cr.top(),
                                          self.line_number_area_width(), cr.height())
    
    def line_number_area_paint_event(self, event):
        """Paint line numbers in the gutter."""
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor("#252526"))
        
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = round(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + round(self.blockBoundingRect(block).height())
        
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QColor("#808080"))
                painter.drawText(0, top, self.line_number_area.width() - 5,
                               self.fontMetrics().height(),
                               Qt.AlignmentFlag.AlignRight, number)
            
            block = block.next()
            top = bottom
            bottom = top + round(self.blockBoundingRect(block).height())
            block_number += 1
    
    def highlight_current_line(self):
        """Highlight the line containing the cursor."""
        extra_selections = []
        
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor("#2D2D2D")
            selection.format.setBackground(line_color)
            selection.format.setProperty(
                selection.format.Property.FullWidthSelection, True
            )
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        
        self.setExtraSelections(extra_selections)
    
    def get_current_line(self) -> str:
        """Get the text of the current line."""
        cursor = self.textCursor()
        cursor.select(cursor.SelectionType.LineUnderCursor)
        return cursor.selectedText()
    
    def get_selected_text(self) -> str:
        """Get currently selected text, or current line if no selection."""
        cursor = self.textCursor()
        if cursor.hasSelection():
            return cursor.selectedText()
        return self.get_current_line()
