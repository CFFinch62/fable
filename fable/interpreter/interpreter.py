"""
Core Forth interpreter logic.

This module contains the main ForthInterpreter class that executes
Forth code and emits signals for GUI integration.
"""

from typing import Any, List, Optional, Callable
from PyQt6.QtCore import QObject, pyqtSignal

from .lexer import Lexer, Token, TokenType
from .dictionary import Dictionary, DictionaryEntry
from .errors import (
    ForthError, StackUnderflowError, UnknownWordError,
    DivisionByZeroError
)


class ForthInterpreter(QObject):
    """Main Forth interpreter with GUI integration signals.
    
    The interpreter maintains a data stack, return stack, and dictionary.
    It can operate in different execution modes for animation control.
    
    Signals:
        word_starting(str, str): Emitted before a word executes (name, stack_effect)
        word_complete(str, list): Emitted after a word executes (name, stack_state)
        error_occurred(str): Emitted when an error occurs
        output(str): Emitted when output is produced (., .S, etc.)
        state_changed(): Emitted when interpreter state changes
    
    Attributes:
        data_stack: The main data stack
        return_stack: The return stack (for loops, subroutines)
        dictionary: Word definitions
        compiling: True if in compile mode (inside : ... ;)
        execution_mode: "run", "synchronized", or "step"
    """
    
    # Qt Signals
    word_starting = pyqtSignal(str, str)  # word_name, stack_effect
    word_complete = pyqtSignal(str, list)  # word_name, stack_state
    error_occurred = pyqtSignal(str)       # error_message
    output = pyqtSignal(str)               # output_text
    state_changed = pyqtSignal()           # generic state change
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data_stack: List[Any] = []
        self.return_stack: List[Any] = []
        self.dictionary = Dictionary()
        self.compiling = False
        self.execution_mode = "run"  # "run", "synchronized", "step"
        
        self._lexer = Lexer()
        self._current_definition: List = []  # Words being compiled
        self._definition_name: str = ""      # Name of word being defined
        
        # Register primitive words
        self._register_primitives()
    
    def _register_primitives(self):
        """Register all built-in primitive words."""
        from . import primitives
        primitives.register_all(self)
    
    def evaluate(self, source: str) -> None:
        """Parse and execute Forth source code.
        
        Args:
            source: Forth source code string
            
        Raises:
            ForthError: On any interpreter error
        """
        tokens = self._lexer.tokenize(source)
        
        for token in tokens:
            if token.type == TokenType.EOF:
                break
            
            if token.type == TokenType.COMMENT:
                continue  # Skip comments
            
            try:
                self._process_token(token)
            except ForthError as e:
                self.error_occurred.emit(str(e))
                raise
    
    def _process_token(self, token: Token) -> None:
        """Process a single token.
        
        Args:
            token: The token to process
        """
        if token.type == TokenType.NUMBER:
            if self.compiling:
                self._current_definition.append(('LIT', token.value))
            else:
                self.push(token.value)
            return
        
        if token.type == TokenType.STRING:
            if self.compiling:
                self._current_definition.append(('STR', token.value))
            else:
                self.push(token.value)
            return
        
        if token.type == TokenType.WORD:
            self._process_word(token.value)
            return
    
    def _process_word(self, word: str) -> None:
        """Process a word token.
        
        Args:
            word: The word name
        """
        entry = self.dictionary.lookup(word)
        
        if entry is None:
            # Check for special compile-mode words
            if word == ':':
                self._start_definition()
                return
            if word == ';' and self.compiling:
                self._end_definition()
                return
            
            # Unknown word
            suggestions = self.dictionary.find_similar(word)
            raise UnknownWordError(word, suggestions)
        
        # Handle immediate words (execute even during compilation)
        if entry.immediate or not self.compiling:
            self._execute_entry(entry)
        else:
            # Compile the word
            self._current_definition.append(entry.name)
    
    def _execute_entry(self, entry: DictionaryEntry) -> None:
        """Execute a dictionary entry.
        
        Args:
            entry: The entry to execute
        """
        # Emit signal before execution
        self.word_starting.emit(entry.name, entry.stack_effect)
        
        if entry.is_primitive():
            # Call the Python function
            entry.code(self)
        else:
            # Execute compiled code
            self._execute_compiled(entry.code)
        
        # Emit signal after execution
        self.word_complete.emit(entry.name, list(self.data_stack))
    
    def _execute_compiled(self, code: List) -> None:
        """Execute compiled threaded code.
        
        Args:
            code: List of operations to execute
        """
        for item in code:
            if isinstance(item, tuple):
                op, value = item
                if op == 'LIT':
                    self.push(value)
                elif op == 'STR':
                    self.push(value)
            elif isinstance(item, str):
                entry = self.dictionary.lookup(item)
                if entry:
                    self._execute_entry(entry)
    
    def _start_definition(self) -> None:
        """Start a new colon definition."""
        self.compiling = True
        self._current_definition = []
        self._definition_name = ""
        self.state_changed.emit()
    
    def _end_definition(self) -> None:
        """Complete a colon definition."""
        if self._definition_name:
            entry = DictionaryEntry(
                name=self._definition_name,
                code=self._current_definition,
                stack_effect=""
            )
            self.dictionary.define(entry)
        
        self.compiling = False
        self._current_definition = []
        self._definition_name = ""
        self.state_changed.emit()
    
    # --- Stack Operations ---
    
    def push(self, value: Any) -> None:
        """Push a value onto the data stack.
        
        Args:
            value: Value to push
        """
        self.data_stack.append(value)
    
    def pop(self) -> Any:
        """Pop a value from the data stack.
        
        Returns:
            The popped value
            
        Raises:
            StackUnderflowError: If stack is empty
        """
        if not self.data_stack:
            raise StackUnderflowError("POP", 1, 0)
        return self.data_stack.pop()
    
    def peek(self, index: int = 0) -> Any:
        """Peek at a stack value without removing it.
        
        Args:
            index: 0 = top of stack, 1 = second, etc.
            
        Returns:
            The value at that position
            
        Raises:
            StackUnderflowError: If index is out of range
        """
        if index >= len(self.data_stack):
            raise StackUnderflowError("PEEK", index + 1, len(self.data_stack))
        return self.data_stack[-(index + 1)]
    
    def depth(self) -> int:
        """Return the current stack depth."""
        return len(self.data_stack)
    
    def clear(self) -> None:
        """Clear the data stack."""
        self.data_stack.clear()
        self.state_changed.emit()
    
    def require(self, n: int, word: str) -> None:
        """Ensure the stack has at least n items.
        
        Args:
            n: Number of items required
            word: Word name for error message
            
        Raises:
            StackUnderflowError: If stack doesn't have enough items
        """
        if len(self.data_stack) < n:
            raise StackUnderflowError(word, n, len(self.data_stack))
    
    # --- Return Stack Operations ---
    
    def rpush(self, value: Any) -> None:
        """Push a value onto the return stack."""
        self.return_stack.append(value)
    
    def rpop(self) -> Any:
        """Pop a value from the return stack."""
        if not self.return_stack:
            raise StackUnderflowError("R>", 1, 0, "Return stack is empty.")
        return self.return_stack.pop()
    
    def rpeek(self, index: int = 0) -> Any:
        """Peek at the return stack."""
        if index >= len(self.return_stack):
            raise StackUnderflowError("R@", index + 1, len(self.return_stack))
        return self.return_stack[-(index + 1)]
    
    # --- Output ---
    
    def emit_output(self, text: str) -> None:
        """Emit output text.
        
        Args:
            text: Text to output
        """
        self.output.emit(text)
    
    # --- State Management ---
    
    def reset(self) -> None:
        """Reset interpreter to initial state."""
        self.data_stack.clear()
        self.return_stack.clear()
        self.compiling = False
        self._current_definition = []
        self._definition_name = ""
        self.state_changed.emit()
    
    def get_stack_effect(self, word: str) -> Optional[str]:
        """Get the stack effect notation for a word.
        
        Args:
            word: Word name
            
        Returns:
            Stack effect string or None
        """
        entry = self.dictionary.lookup(word)
        if entry:
            return entry.stack_effect
        return None
