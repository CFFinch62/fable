"""
Lexer module for tokenizing Forth source code.

Forth has a simple syntax: whitespace-separated words with special handling
for strings and comments. This lexer preserves source location for error reporting.
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Iterator, Optional


class TokenType(Enum):
    """Types of tokens in Forth source code."""
    WORD = auto()       # Any word (command, number to be parsed later)
    NUMBER = auto()     # Parsed integer or float
    STRING = auto()     # String literal from ." or S"
    COMMENT = auto()    # Comment (for syntax highlighting, usually skipped)
    EOF = auto()        # End of file


@dataclass
class Token:
    """A single token from Forth source code.
    
    Attributes:
        type: The token type
        value: The token's value (string for WORD, parsed for NUMBER)
        line: Source line number (1-indexed)
        column: Source column number (1-indexed)
        raw: Original source text
    """
    type: TokenType
    value: any
    line: int
    column: int
    raw: str = ""
    
    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, {self.line}:{self.column})"


class Lexer:
    """Tokenizes Forth source code.
    
    Handles:
    - Whitespace-separated words
    - Integer literals (decimal, hex with $ or 0x prefix)
    - Float literals (with decimal point)
    - String literals (." ..." and S" ...")
    - Line comments (\\ to end of line)
    - Parenthetical comments ( ... )
    
    Example:
        >>> lexer = Lexer()
        >>> tokens = lexer.tokenize("3 4 + .")
        >>> [t.value for t in tokens if t.type != TokenType.EOF]
        [3, 4, '+', '.']
    """
    
    def __init__(self):
        self._source = ""
        self._pos = 0
        self._line = 1
        self._column = 1
        self._tokens: List[Token] = []
    
    def tokenize(self, source: str) -> List[Token]:
        """Tokenize Forth source code.
        
        Args:
            source: The source code string
            
        Returns:
            List of tokens, ending with EOF token
        """
        self._source = source
        self._pos = 0
        self._line = 1
        self._column = 1
        self._tokens = []
        
        while not self._at_end():
            self._scan_token()
        
        # Add EOF token
        self._tokens.append(Token(TokenType.EOF, None, self._line, self._column))
        return self._tokens
    
    def _at_end(self) -> bool:
        """Check if we've reached the end of source."""
        return self._pos >= len(self._source)
    
    def _peek(self) -> str:
        """Look at current character without advancing."""
        if self._at_end():
            return '\0'
        return self._source[self._pos]
    
    def _peek_next(self) -> str:
        """Look at next character without advancing."""
        if self._pos + 1 >= len(self._source):
            return '\0'
        return self._source[self._pos + 1]
    
    def _advance(self) -> str:
        """Consume and return current character."""
        char = self._source[self._pos]
        self._pos += 1
        if char == '\n':
            self._line += 1
            self._column = 1
        else:
            self._column += 1
        return char
    
    def _skip_whitespace(self):
        """Skip whitespace characters."""
        while not self._at_end() and self._peek() in ' \t\n\r':
            self._advance()
    
    def _scan_token(self):
        """Scan and add the next token."""
        self._skip_whitespace()
        
        if self._at_end():
            return
        
        start_line = self._line
        start_column = self._column
        start_pos = self._pos
        
        char = self._peek()
        
        # Line comment: \ to end of line
        if char == '\\':
            self._scan_line_comment(start_line, start_column)
            return
        
        # Parenthetical comment: ( ... )
        if char == '(':
            # Check if followed by space (Forth comment convention)
            if self._peek_next() in ' \t\n':
                self._scan_paren_comment(start_line, start_column)
                return
        
        # String literal: ." ..." or S" ..." or .(
        # These are handled specially because they're words followed by string
        
        # Default: scan a word
        word = self._scan_word()
        
        if not word:
            return
        
        # Check for special words that consume following content
        upper_word = word.upper()
        
        # ." prints a string (compile time)
        if upper_word == '."':
            self._skip_one_space()
            string_val = self._scan_string_until('"')
            self._tokens.append(Token(
                TokenType.WORD, '."',
                start_line, start_column, '."'
            ))
            self._tokens.append(Token(
                TokenType.STRING, string_val,
                self._line, self._column, f'"{string_val}"'
            ))
            return
        
        # .( prints a string (immediate)
        if upper_word == '.(': 
            string_val = self._scan_string_until(')')
            self._tokens.append(Token(
                TokenType.WORD, '.(',
                start_line, start_column, '.('
            ))
            self._tokens.append(Token(
                TokenType.STRING, string_val,
                self._line, self._column, f'({string_val})'
            ))
            return
        
        # S" creates a string
        if upper_word == 'S"':
            self._skip_one_space()
            string_val = self._scan_string_until('"')
            self._tokens.append(Token(
                TokenType.WORD, 'S"',
                start_line, start_column, 'S"'
            ))
            self._tokens.append(Token(
                TokenType.STRING, string_val,
                self._line, self._column, f'"{string_val}"'
            ))
            return
        
        # Try to parse as number
        number = self._try_parse_number(word)
        if number is not None:
            self._tokens.append(Token(
                TokenType.NUMBER, number,
                start_line, start_column, word
            ))
            return
        
        # It's a word
        self._tokens.append(Token(
            TokenType.WORD, word,
            start_line, start_column, word
        ))
    
    def _scan_word(self) -> str:
        """Scan a whitespace-delimited word."""
        chars = []
        while not self._at_end() and self._peek() not in ' \t\n\r':
            chars.append(self._advance())
        return ''.join(chars)
    
    def _scan_line_comment(self, start_line: int, start_column: int):
        r"""Scan a line comment (\ to end of line)."""
        chars = []
        while not self._at_end() and self._peek() != '\n':
            chars.append(self._advance())
        # Don't consume the newline, let skip_whitespace handle it
        self._tokens.append(Token(
            TokenType.COMMENT, ''.join(chars),
            start_line, start_column, ''.join(chars)
        ))
    
    def _scan_paren_comment(self, start_line: int, start_column: int):
        """Scan a parenthetical comment ( ... )."""
        chars = []
        self._advance()  # consume (
        depth = 1
        while not self._at_end() and depth > 0:
            char = self._advance()
            if char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
                if depth == 0:
                    break
            chars.append(char)
        self._tokens.append(Token(
            TokenType.COMMENT, ''.join(chars),
            start_line, start_column, '(' + ''.join(chars) + ')'
        ))
    
    def _skip_one_space(self):
        """Skip exactly one space after ." or S\" words."""
        if not self._at_end() and self._peek() == ' ':
            self._advance()
    
    def _scan_string_until(self, terminator: str) -> str:
        """Scan string content until terminator character."""
        chars = []
        while not self._at_end():
            char = self._advance()
            if char == terminator:
                break
            chars.append(char)
        return ''.join(chars)
    
    def _try_parse_number(self, word: str) -> Optional[int | float]:
        """Try to parse a word as a number.
        
        Handles:
        - Decimal integers: 42, -17
        - Hex with $ prefix: $FF, $1A2B
        - Hex with 0x prefix: 0xFF, 0x1a2b
        - Floats: 3.14, -2.5
        
        Returns:
            Parsed number or None if not a valid number
        """
        if not word:
            return None
        
        # Hex with $ prefix (Forth convention)
        if word.startswith('$'):
            try:
                return int(word[1:], 16)
            except ValueError:
                return None
        
        # Hex with 0x prefix
        if word.lower().startswith('0x'):
            try:
                return int(word, 16)
            except ValueError:
                return None
        
        # Try integer
        try:
            return int(word)
        except ValueError:
            pass
        
        # Try float
        try:
            return float(word)
        except ValueError:
            pass
        
        return None


def tokenize(source: str) -> List[Token]:
    """Convenience function to tokenize source code.
    
    Args:
        source: Forth source code
        
    Returns:
        List of tokens
    """
    return Lexer().tokenize(source)
