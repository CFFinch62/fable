"""
Code editor widget with Forth-specific features.
Includes syntax highlighting, bracket matching, and stack effect tooltips.
"""

import re
from PyQt6.QtCore import Qt, pyqtSignal, QPoint
from PyQt6.QtGui import (
    QFont, QColor, QPainter, QSyntaxHighlighter, 
    QTextDocument, QTextCharFormat, QTextCursor
)
from PyQt6.QtWidgets import QPlainTextEdit, QWidget, QTextEdit, QToolTip


# Stack effects for known words (for tooltips)
STACK_EFFECTS = {
    # Stack manipulation
    'DUP': '( n -- n n )',
    'DROP': '( n -- )',
    'SWAP': '( n1 n2 -- n2 n1 )',
    'OVER': '( n1 n2 -- n1 n2 n1 )',
    'ROT': '( n1 n2 n3 -- n2 n3 n1 )',
    '-ROT': '( n1 n2 n3 -- n3 n1 n2 )',
    'NIP': '( n1 n2 -- n2 )',
    'TUCK': '( n1 n2 -- n2 n1 n2 )',
    '2DUP': '( n1 n2 -- n1 n2 n1 n2 )',
    '2DROP': '( n1 n2 -- )',
    '2SWAP': '( n1 n2 n3 n4 -- n3 n4 n1 n2 )',
    'DEPTH': '( -- n )',
    'PICK': '( n -- item )',
    'ROLL': '( n -- )',
    'CLEAR': '( ... -- )',
    # Arithmetic
    '+': '( n1 n2 -- sum )',
    '-': '( n1 n2 -- diff )',
    '*': '( n1 n2 -- prod )',
    '/': '( n1 n2 -- quot )',
    'MOD': '( n1 n2 -- rem )',
    '/MOD': '( n1 n2 -- rem quot )',
    'NEGATE': '( n -- -n )',
    'ABS': '( n -- |n| )',
    'MIN': '( n1 n2 -- min )',
    'MAX': '( n1 n2 -- max )',
    '1+': '( n -- n+1 )',
    '1-': '( n -- n-1 )',
    # Comparison
    '=': '( n1 n2 -- flag )',
    '<>': '( n1 n2 -- flag )',
    '<': '( n1 n2 -- flag )',
    '>': '( n1 n2 -- flag )',
    '0=': '( n -- flag )',
    '0<': '( n -- flag )',
    '0>': '( n -- flag )',
    # Logic
    'AND': '( n1 n2 -- n )',
    'OR': '( n1 n2 -- n )',
    'XOR': '( n1 n2 -- n )',
    'INVERT': '( n -- ~n )',
    'TRUE': '( -- -1 )',
    'FALSE': '( -- 0 )',
    # Output
    '.': '( n -- )',
    '.S': '( -- )',
    'CR': '( -- )',
    'SPACE': '( -- )',
    'SPACES': '( n -- )',
    'EMIT': '( char -- )',
    # Control
    'IF': '( flag -- )',
    'THEN': '( -- )',
    'ELSE': '( -- )',
    'BEGIN': '( -- )',
    'UNTIL': '( flag -- )',
    'WHILE': '( flag -- )',
    'REPEAT': '( -- )',
    'DO': '( limit index -- )',
    'LOOP': '( -- )',
    '+LOOP': '( n -- )',
    'I': '( -- n )',
    'J': '( -- n )',
}


class ForthHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for Forth code."""
    
    # Word categories
    KEYWORDS = {
        ':', ';', 'VARIABLE', 'CONSTANT', 'CREATE', 'DOES>', 
        'IF', 'ELSE', 'THEN', 'BEGIN', 'UNTIL', 'WHILE', 'REPEAT',
        'DO', 'LOOP', '+LOOP', 'LEAVE', 'EXIT', 'I', 'J',
        'RECURSE', 'IMMEDIATE', 'POSTPONE',
    }
    
    STACK_WORDS = {
        'DUP', 'DROP', 'SWAP', 'OVER', 'ROT', '-ROT', 'NIP', 'TUCK',
        '2DUP', '2DROP', '2SWAP', '2OVER', 'PICK', 'ROLL', 'DEPTH', 'CLEAR',
        '>R', 'R>', 'R@',
    }
    
    MATH_WORDS = {
        '+', '-', '*', '/', 'MOD', '/MOD', 'NEGATE', 'ABS',
        'MIN', 'MAX', '1+', '1-', '2+', '2-', '2*', '2/',
    }
    
    LOGIC_WORDS = {
        '=', '<>', '<', '>', '<=', '>=', '0=', '0<', '0>',
        'AND', 'OR', 'XOR', 'INVERT', 'NOT', 'TRUE', 'FALSE',
        'LSHIFT', 'RSHIFT',
    }
    
    OUTPUT_WORDS = {
        '.', '.S', 'CR', 'SPACE', 'SPACES', 'EMIT', 'TYPE', '."',
        'WORDS', 'SEE',
    }
    
    def __init__(self, parent: QTextDocument):
        super().__init__(parent)
        
        # Format definitions
        self.formats = {
            'keyword': self._make_format('#C586C0', bold=True),  # Purple
            'stack': self._make_format('#569CD6'),               # Blue
            'math': self._make_format('#4EC9B0'),                # Cyan
            'logic': self._make_format('#6A9955'),               # Green
            'output': self._make_format('#D4A017'),              # Amber
            'number': self._make_format('#B5CEA8'),              # Light green
            'string': self._make_format('#CE9178'),              # Orange
            'comment': self._make_format('#6A9955', italic=True),# Green italic
            'definition': self._make_format('#DCDCAA'),          # Yellow (word names)
        }
        
        # State for tracking word definitions
        self._in_definition = False
        self._expect_name = False
    
    def _make_format(self, color: str, bold: bool = False, italic: bool = False) -> QTextCharFormat:
        """Create a text format."""
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))
        if bold:
            fmt.setFontWeight(700)
        if italic:
            fmt.setFontItalic(True)
        return fmt
    
    def highlightBlock(self, text: str):
        """Apply syntax highlighting to a block of text."""
        # Handle comments first
        
        # Line comment: \ to end of line
        if '\\' in text:
            comment_start = text.find('\\')
            self.setFormat(comment_start, len(text) - comment_start, self.formats['comment'])
            text = text[:comment_start]  # Don't process comment section
        
        # Parenthetical comment ( ... )
        paren_pattern = re.compile(r'\(\s[^)]*\)')
        for match in paren_pattern.finditer(text):
            self.setFormat(match.start(), match.end() - match.start(), self.formats['comment'])
        
        # String literals ." ..."
        string_pattern = re.compile(r'\."\s[^"]*"')
        for match in string_pattern.finditer(text):
            self.setFormat(match.start(), match.end() - match.start(), self.formats['string'])
        
        # Process words
        word_pattern = re.compile(r'\S+')
        for match in word_pattern.finditer(text):
            word = match.group()
            upper_word = word.upper()
            start = match.start()
            length = len(word)
            
            # Check if this position is already formatted (comment/string)
            if self.format(start).foreground().color().name() in ['#6a9955', '#ce9178']:
                continue
            
            # Check word type
            if upper_word in self.KEYWORDS:
                self.setFormat(start, length, self.formats['keyword'])
                if upper_word == ':':
                    self._expect_name = True
            elif self._expect_name:
                self.setFormat(start, length, self.formats['definition'])
                self._expect_name = False
            elif upper_word in self.STACK_WORDS:
                self.setFormat(start, length, self.formats['stack'])
            elif upper_word in self.MATH_WORDS:
                self.setFormat(start, length, self.formats['math'])
            elif upper_word in self.LOGIC_WORDS:
                self.setFormat(start, length, self.formats['logic'])
            elif upper_word in self.OUTPUT_WORDS:
                self.setFormat(start, length, self.formats['output'])
            elif self._is_number(word):
                self.setFormat(start, length, self.formats['number'])
    
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
        - Syntax highlighting
        - Line numbers
        - Current line highlighting
        - Bracket matching
        - Stack effect tooltips
    
    Signals:
        cursor_word_changed(str): Emitted when word under cursor changes
        run_requested(str): Emitted when code should be executed
    """
    
    cursor_word_changed = pyqtSignal(str)
    run_requested = pyqtSignal(str)
    
    # Matching bracket pairs
    BRACKET_PAIRS = {
        ':': ';',
        'IF': 'THEN',
        'BEGIN': 'UNTIL',
        'DO': 'LOOP',
        '(': ')',
    }
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._setup_highlighter()
        self._setup_line_numbers()
        self._last_word = ""
    
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
        
        # Enable mouse tracking for tooltips
        self.setMouseTracking(True)
    
    def _setup_highlighter(self):
        """Set up syntax highlighter."""
        self.highlighter = ForthHighlighter(self.document())
    
    def _setup_line_numbers(self):
        """Set up line number area."""
        self.line_number_area = LineNumberArea(self)
        
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        self.cursorPositionChanged.connect(self._on_cursor_position_changed)
        
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
        
        current_line = self.textCursor().blockNumber()
        
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                # Highlight current line number
                if block_number == current_line:
                    painter.setPen(QColor("#D4D4D4"))
                else:
                    painter.setPen(QColor("#808080"))
                painter.drawText(0, top, self.line_number_area.width() - 5,
                               self.fontMetrics().height(),
                               Qt.AlignmentFlag.AlignRight, number)
            
            block = block.next()
            top = bottom
            bottom = top + round(self.blockBoundingRect(block).height())
            block_number += 1
    
    def highlight_current_line(self):
        """Highlight the line containing the cursor and matching brackets."""
        extra_selections = []
        
        if not self.isReadOnly():
            # Current line highlight
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(QColor("#2D2D2D"))
            selection.format.setProperty(
                selection.format.Property.FullWidthSelection, True
            )
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
            
            # Bracket matching
            extra_selections.extend(self._find_matching_brackets())
        
        self.setExtraSelections(extra_selections)
    
    def _find_matching_brackets(self) -> list:
        """Find and highlight matching brackets."""
        extra_selections = []
        cursor = self.textCursor()
        
        # Get word at cursor
        cursor.select(QTextCursor.SelectionType.WordUnderCursor)
        word = cursor.selectedText().upper()
        
        if word in self.BRACKET_PAIRS or word in self.BRACKET_PAIRS.values():
            # Highlight current bracket
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(QColor("#3A3D41"))
            selection.cursor = cursor
            extra_selections.append(selection)
        
        return extra_selections
    
    def _on_cursor_position_changed(self):
        """Handle cursor position changes for word detection."""
        cursor = self.textCursor()
        cursor.select(QTextCursor.SelectionType.WordUnderCursor)
        word = cursor.selectedText()
        
        if word != self._last_word:
            self._last_word = word
            self.cursor_word_changed.emit(word)
    
    def mouseMoveEvent(self, event):
        """Show stack effect tooltip on hover."""
        super().mouseMoveEvent(event)
        
        cursor = self.cursorForPosition(event.pos())
        cursor.select(QTextCursor.SelectionType.WordUnderCursor)
        word = cursor.selectedText().upper()
        
        if word in STACK_EFFECTS:
            effect = STACK_EFFECTS[word]
            QToolTip.showText(
                self.mapToGlobal(event.pos()),
                f"{word} {effect}",
                self
            )
        else:
            QToolTip.hideText()
    
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
    
    def get_word_at_cursor(self) -> str:
        """Get the word under the cursor."""
        cursor = self.textCursor()
        cursor.select(QTextCursor.SelectionType.WordUnderCursor)
        return cursor.selectedText()
