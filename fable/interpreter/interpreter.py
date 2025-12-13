"""
Core Forth interpreter logic.

This module contains the main ForthInterpreter class that executes
Forth code and emits signals for GUI integration.
"""

from typing import Any, List, Optional, Callable
from PyQt6.QtCore import QObject, pyqtSignal, QTimer, QEventLoop

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
        self.delay = 0  # Execution delay in ms
        self.running = False
        
        # Register primitive words
        
        # Register primitive words
        self._step_event_loop = None
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
        try:
            self.running = True
            tokens = self._lexer.tokenize(source)

            for token in tokens:
                if self.execution_mode == "stop":
                    break

                if token.type == TokenType.EOF:
                    break

                if token.type == TokenType.COMMENT:
                    continue  # Skip comments

                try:
                    self._process_token(token)
                except ForthError as e:
                    self.error_occurred.emit(str(e))
                    raise

                # Wait AFTER processing token (so first step shows result)
                self._wait_for_step()
        finally:
            self.running = False
    
    def _process_token(self, token: Token) -> None:
        """Process a single token.

        Args:
            token: The token to process
        """
        if token.type == TokenType.NUMBER:
            if self.compiling:
                self._current_definition.append(('LIT', token.value))
            else:
                # Emit signals for literal push so stack widget animates
                self.word_starting.emit(str(token.value), '( -- n )')
                self.push(token.value)
                self.word_complete.emit(str(token.value), list(self.data_stack))
            return

        if token.type == TokenType.STRING:
            if self.compiling:
                # Check if previous item in compiled code is ." word
                print_string = (len(self._current_definition) > 0 and
                               self._current_definition[-1] == '."')
                if print_string:
                    # Remove the ." word and compile as PRINT operation
                    self._current_definition.pop()
                    self._current_definition.append(('PRINT', token.value))
                else:
                    # For S" - compile as string literal
                    self._current_definition.append(('STR', token.value))
            else:
                # Check if previous word was ." (print string)
                print_string = hasattr(self, '_print_next_string') and self._print_next_string
                if print_string:
                    self._print_next_string = False
                    # Print immediately
                    self.output.emit(token.value)
                else:
                    # Normal string push (for S")
                    # Emit signals for string push so stack widget animates
                    self.word_starting.emit(f'"{token.value}"', '( -- str )')
                    self.push(token.value)
                    self.word_complete.emit(f'"{token.value}"', list(self.data_stack))
            return

        if token.type == TokenType.WORD:
            self._process_word(token.value)
            return
    
    def _process_word(self, word: str) -> None:
        """Process a word token.
        
        Args:
            word: The word name
        """
        # Check for colon definition start
        if word == ':':
            self._start_definition()
            return
        
        # Check for semicolon definition end
        if word == ';' and self.compiling:
            self._end_definition()
            return
        
        # If we're compiling and don't have a name yet, this is the word name
        if self.compiling and not self._definition_name:
            self._definition_name = word.upper()
            return
        
        entry = self.dictionary.lookup(word)
        
        if entry is None:
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
        # Emit signal after execution
        self.word_complete.emit(entry.name, list(self.data_stack))
    
    def set_delay(self, delay_ms: int):
        """Set execution delay in milliseconds."""
        self.delay = delay_ms
    
    def _execute_compiled(self, code: List) -> None:
        """Execute compiled threaded code with control flow support.

        Args:
            code: List of operations to execute

        Supports:
            - LIT: Push literal value
            - STR: Push string value
            - BRANCH: Unconditional branch (offset)
            - 0BRANCH: Branch if TOS is 0 (offset)
            - DO: Start loop (limit, index on stack)
            - LOOP: Increment and check loop
            - +LOOP: Add n and check loop
            - I: Push loop index
            - J: Push outer loop index
            - LEAVE: Exit loop early
        """
        ip = 0  # Instruction pointer
        loop_stack = []  # Stack of (limit, index, loop_start_ip)

        while ip < len(code):
            if self.execution_mode == "stop":
                break

            item = code[ip]
            ip += 1

            # Track if this operation should trigger a step pause
            should_pause = True

            if isinstance(item, tuple):
                op = item[0]

                if op == 'LIT':
                    # Emit signals for literal push animation
                    self.word_starting.emit(str(item[1]), '( -- n )')
                    self.push(item[1])
                    self.word_complete.emit(str(item[1]), list(self.data_stack))

                elif op == 'STR':
                    # Emit signals for string push animation
                    self.word_starting.emit(f'"{item[1]}"', '( -- str )')
                    self.push(item[1])
                    self.word_complete.emit(f'"{item[1]}"', list(self.data_stack))

                elif op == 'PRINT':
                    # Print string (from .")
                    self.output.emit(item[1])

                elif op == 'BRANCH':
                    # Unconditional branch - no stack change, no signal needed
                    ip = item[1]
                    should_pause = False  # Don't pause on internal branching

                elif op == '0BRANCH':
                    # Branch if top of stack is 0 (false)
                    flag = self.pop()
                    if flag == 0:
                        ip = item[1]
                    should_pause = False  # Don't pause on internal branching

                elif op == 'DO':
                    # Start a DO loop: ( limit index -- )
                    # Emit signal to show DO consuming values and updating return stack
                    self.word_starting.emit('DO', '( limit index -- )')
                    index = self.pop()
                    limit = self.pop()
                    loop_stack.append((limit, index, ip))
                    self.word_complete.emit('DO', list(self.data_stack))

                elif op == 'LOOP':
                    # Increment index and check
                    should_pause = False  # Internal loop control
                    if loop_stack:
                        limit, index, loop_start = loop_stack[-1]
                        index += 1
                        if index >= limit:
                            loop_stack.pop()
                            # Continue past loop
                        else:
                            loop_stack[-1] = (limit, index, loop_start)
                            ip = loop_start

                elif op == '+LOOP':
                    # Add increment and check
                    self.word_starting.emit('+LOOP', '( n -- )')
                    n = self.pop()
                    self.word_complete.emit('+LOOP', list(self.data_stack))
                    if loop_stack:
                        limit, index, loop_start = loop_stack[-1]
                        index += n
                        if (n > 0 and index >= limit) or (n < 0 and index <= limit):
                            loop_stack.pop()
                        else:
                            loop_stack[-1] = (limit, index, loop_start)
                            ip = loop_start

                elif op == 'UNLOOP':
                    # Discard loop parameters
                    should_pause = False  # Internal control
                    if loop_stack:
                        loop_stack.pop()

                elif op == 'I':
                    # Push current loop index
                    if loop_stack:
                        self.word_starting.emit('I', '( -- n )')
                        _, index, _ = loop_stack[-1]
                        self.push(index)
                        self.word_complete.emit('I', list(self.data_stack))

                elif op == 'J':
                    # Push outer loop index
                    if len(loop_stack) >= 2:
                        self.word_starting.emit('J', '( -- n )')
                        _, index, _ = loop_stack[-2]
                        self.push(index)
                        self.word_complete.emit('J', list(self.data_stack))

                elif op == 'LEAVE':
                    # Exit current loop
                    should_pause = False  # Internal control
                    if loop_stack:
                        loop_stack.pop()
                        # Find matching LOOP/+LOOP to skip to
                        depth = 1
                        while ip < len(code) and depth > 0:
                            check = code[ip]
                            ip += 1
                            if isinstance(check, tuple):
                                if check[0] == 'DO':
                                    depth += 1
                                elif check[0] in ('LOOP', '+LOOP'):
                                    depth -= 1

            elif isinstance(item, str):
                # Word call - _execute_entry already emits signals
                entry = self.dictionary.lookup(item)
                if entry:
                    self._execute_entry(entry)

            # Wait AFTER processing operation (so step shows the result)
            if should_pause:
                self._wait_for_step()

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
    
    def step(self):
        """Execute the next step (resume from pause)."""
        if self._step_event_loop and self._step_event_loop.isRunning():
            self._step_event_loop.quit()

    def stop(self):
        """Stop execution."""
        self.execution_mode = "stop"  # Flag to stop loops
        if self._step_event_loop and self._step_event_loop.isRunning():
            self._step_event_loop.quit()
        self.reset()

    def _wait_for_step(self):
        """Handle execution delay or synchronization pause."""
        if self.execution_mode == "stop":
            return

        if self.execution_mode == "step":
            self._step_event_loop = QEventLoop()
            self._step_event_loop.exec()
            self._step_event_loop = None
            
        elif self.delay > 0 and self.execution_mode == "run":
            loop = QEventLoop()
            QTimer.singleShot(self.delay, loop.quit)
            loop.exec()

    def is_running(self) -> bool:
        """Check if interpreter is currently executing."""
        return self.running

    # --- Stack Operations ---
    
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
