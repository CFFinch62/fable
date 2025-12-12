"""
Tests for the Forth lexer.
"""

import pytest
from fable.interpreter.lexer import Lexer, Token, TokenType, tokenize


class TestLexerBasics:
    """Test basic lexer functionality."""
    
    def test_empty_source(self):
        """Empty source returns only EOF token."""
        tokens = tokenize("")
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.EOF
    
    def test_whitespace_only(self):
        """Whitespace-only source returns only EOF."""
        tokens = tokenize("   \n\t  \n  ")
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.EOF
    
    def test_single_word(self):
        """Single word tokenizes correctly."""
        tokens = tokenize("DUP")
        assert len(tokens) == 2
        assert tokens[0].type == TokenType.WORD
        assert tokens[0].value == "DUP"
        assert tokens[1].type == TokenType.EOF
    
    def test_multiple_words(self):
        """Multiple words tokenize correctly."""
        tokens = tokenize("DUP DROP SWAP")
        words = [t for t in tokens if t.type == TokenType.WORD]
        assert len(words) == 3
        assert [w.value for w in words] == ["DUP", "DROP", "SWAP"]


class TestNumbers:
    """Test number tokenization."""
    
    def test_positive_integer(self):
        """Positive integers parse correctly."""
        tokens = tokenize("42")
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].value == 42
    
    def test_negative_integer(self):
        """Negative integers parse correctly."""
        tokens = tokenize("-17")
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].value == -17
    
    def test_zero(self):
        """Zero parses correctly."""
        tokens = tokenize("0")
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].value == 0
    
    def test_hex_dollar_prefix(self):
        """Hex with $ prefix parses correctly."""
        tokens = tokenize("$FF")
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].value == 255
    
    def test_hex_0x_prefix(self):
        """Hex with 0x prefix parses correctly."""
        tokens = tokenize("0x1A")
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].value == 26
    
    def test_float(self):
        """Floats parse correctly."""
        tokens = tokenize("3.14")
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].value == 3.14


class TestComments:
    """Test comment tokenization."""
    
    def test_line_comment(self):
        """Line comments with backslash."""
        tokens = tokenize("42 \\ this is a comment\n50")
        numbers = [t for t in tokens if t.type == TokenType.NUMBER]
        assert len(numbers) == 2
        assert numbers[0].value == 42
        assert numbers[1].value == 50
    
    def test_paren_comment(self):
        """Parenthetical comments."""
        tokens = tokenize("42 ( this is a comment ) 50")
        numbers = [t for t in tokens if t.type == TokenType.NUMBER]
        assert len(numbers) == 2


class TestStrings:
    """Test string literal tokenization."""
    
    def test_dot_quote_string(self):
        """String literals with ." syntax."""
        tokens = tokenize('." Hello World"')
        assert tokens[0].type == TokenType.WORD
        assert tokens[0].value == '."'
        assert tokens[1].type == TokenType.STRING
        assert tokens[1].value == "Hello World"
    
    def test_s_quote_string(self):
        """String literals with S" syntax."""
        tokens = tokenize('S" test string"')
        words = [t for t in tokens if t.type == TokenType.WORD]
        strings = [t for t in tokens if t.type == TokenType.STRING]
        assert len(words) == 1
        assert len(strings) == 1
        assert strings[0].value == "test string"


class TestSourceLocation:
    """Test source location tracking."""
    
    def test_line_tracking(self):
        """Line numbers are tracked correctly."""
        tokens = tokenize("first\nsecond\nthird")
        words = [t for t in tokens if t.type == TokenType.WORD]
        assert words[0].line == 1
        assert words[1].line == 2
        assert words[2].line == 3
    
    def test_column_tracking(self):
        """Column numbers are tracked correctly."""
        tokens = tokenize("abc def")
        words = [t for t in tokens if t.type == TokenType.WORD]
        assert words[0].column == 1
        assert words[1].column == 5


class TestComplexExpressions:
    """Test complex Forth expressions."""
    
    def test_arithmetic_expression(self):
        """Arithmetic expression tokenizes correctly."""
        tokens = tokenize("3 4 + 5 * .")
        values = [t.value for t in tokens if t.type != TokenType.EOF]
        assert values == [3, 4, '+', 5, '*', '.']
    
    def test_definition(self):
        """Colon definition tokenizes correctly."""
        tokens = tokenize(": SQUARE DUP * ;")
        words = [t.value for t in tokens if t.type == TokenType.WORD]
        assert words == [':', 'SQUARE', 'DUP', '*', ';']
