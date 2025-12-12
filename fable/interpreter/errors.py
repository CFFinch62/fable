"""
Custom exception classes for the Forth interpreter.

Error messages are designed to be educational, explaining what went wrong
and suggesting how to fix the issue.
"""

from dataclasses import dataclass
from typing import Optional


class ForthError(Exception):
    """Base class for all Forth interpreter errors."""
    
    def __init__(self, message: str, hint: str = ""):
        self.message = message
        self.hint = hint
        super().__init__(self.format_message())
    
    def format_message(self) -> str:
        """Format the full error message with hint."""
        if self.hint:
            return f"{self.message}\n{self.hint}"
        return self.message


class StackUnderflowError(ForthError):
    """Raised when an operation requires more stack items than available."""
    
    def __init__(self, word: str, needed: int, available: int, hint: str = ""):
        self.word = word
        self.needed = needed
        self.available = available
        
        if not hint:
            hint = self._generate_hint()
        
        message = (
            f"Stack underflow: '{word}' needs {needed} value{'s' if needed > 1 else ''}, "
            f"but the stack only has {available}."
        )
        super().__init__(message, hint)
    
    def _generate_hint(self) -> str:
        """Generate a helpful hint based on the word."""
        hints = {
            '+': "The '+' word adds two numbers together. Try: 3 5 +",
            '-': "The '-' word subtracts (second - top). Try: 10 3 -",
            '*': "The '*' word multiplies two numbers. Try: 4 7 *",
            '/': "The '/' word divides (second / top). Try: 20 4 /",
            'DUP': "DUP duplicates the top value. Push a value first: 5 DUP",
            'DROP': "DROP removes the top value. Push a value first: 5 DROP",
            'SWAP': "SWAP exchanges top two values. Try: 1 2 SWAP",
            'OVER': "OVER copies the second value to top. Try: 1 2 OVER",
            'ROT': "ROT rotates three values. Try: 1 2 3 ROT",
            '.': "The '.' word prints and removes top value. Try: 42 .",
        }
        word_upper = self.word.upper()
        if word_upper in hints:
            return hints[word_upper]
        return f"Try pushing {self.needed - self.available} more value(s) before using '{self.word}'."


class UnknownWordError(ForthError):
    """Raised when a word is not found in the dictionary."""
    
    def __init__(self, word: str, suggestions: list[str] = None, hint: str = ""):
        self.word = word
        self.suggestions = suggestions or []
        
        message = f"Unknown word: '{word}'"
        
        if self.suggestions:
            if len(self.suggestions) == 1:
                message += f". Did you mean '{self.suggestions[0]}'?"
            else:
                message += f". Did you mean one of: {', '.join(self.suggestions[:3])}?"
        
        if not hint:
            hint = "Forth words are case-insensitive. Use WORDS to list available words."
        
        super().__init__(message, hint)


class DivisionByZeroError(ForthError):
    """Raised when attempting to divide by zero."""
    
    def __init__(self, dividend: int, hint: str = ""):
        self.dividend = dividend
        
        message = f"Division by zero: Cannot divide {dividend} by 0."
        if not hint:
            hint = "Check the value on top of the stack before dividing."
        
        super().__init__(message, hint)


class TypeMismatchError(ForthError):
    """Raised when a word receives an unexpected type."""
    
    def __init__(self, word: str, expected: str, got: str, hint: str = ""):
        self.word = word
        self.expected = expected
        self.got = got
        
        message = f"Type mismatch: '{word}' expects {expected}, but found {got}."
        super().__init__(message, hint)


class CompileOnlyError(ForthError):
    """Raised when a compile-only word is used in interpret mode."""
    
    def __init__(self, word: str, hint: str = ""):
        self.word = word
        
        message = f"'{word}' is a compile-only word."
        if not hint:
            hint = f"It can only be used inside a colon definition (: word ... ;)."
        
        super().__init__(message, hint)


class ControlStructureError(ForthError):
    """Raised for unbalanced control structures."""
    
    def __init__(self, word: str, missing: str, hint: str = ""):
        self.word = word
        self.missing = missing
        
        message = f"Unmatched '{word}': missing '{missing}'."
        if not hint:
            hint = f"Every '{word}' needs a matching '{missing}'. Check that your control structures are balanced."
        
        super().__init__(message, hint)


class InvalidNumberError(ForthError):
    """Raised when a word cannot be parsed as a number."""
    
    def __init__(self, word: str, hint: str = ""):
        message = f"'{word}' is not a valid number or known word."
        if not hint:
            hint = "Numbers can be decimal (42), hex ($FF or 0xFF), or float (3.14)."
        
        super().__init__(message, hint)
