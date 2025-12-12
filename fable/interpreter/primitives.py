"""
Built-in primitive word implementations for the Forth interpreter.

Each primitive is a Python function that takes the interpreter as its
only argument and manipulates the stacks directly.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .interpreter import ForthInterpreter

from .dictionary import DictionaryEntry
from .errors import StackUnderflowError, DivisionByZeroError


def register_all(interp: 'ForthInterpreter') -> None:
    """Register all primitive words with the interpreter.
    
    Args:
        interp: The interpreter to register words with
    """
    # Stack manipulation
    _register_stack_words(interp)
    
    # Arithmetic
    _register_arithmetic_words(interp)
    
    # Comparison and logic
    _register_comparison_words(interp)
    
    # Output
    _register_output_words(interp)
    
    # Control flow (compile-time words)
    _register_control_flow_words(interp)


# =============================================================================
# Stack Manipulation Words
# =============================================================================

def _register_stack_words(interp: 'ForthInterpreter') -> None:
    """Register stack manipulation words."""
    
    def word_dup(i: 'ForthInterpreter'):
        """( n -- n n ) Duplicate top of stack."""
        i.require(1, 'DUP')
        i.push(i.peek(0))
    
    def word_drop(i: 'ForthInterpreter'):
        """( n -- ) Discard top of stack."""
        i.require(1, 'DROP')
        i.pop()
    
    def word_swap(i: 'ForthInterpreter'):
        """( n1 n2 -- n2 n1 ) Exchange top two items."""
        i.require(2, 'SWAP')
        a = i.pop()
        b = i.pop()
        i.push(a)
        i.push(b)
    
    def word_over(i: 'ForthInterpreter'):
        """( n1 n2 -- n1 n2 n1 ) Copy second item to top."""
        i.require(2, 'OVER')
        i.push(i.peek(1))
    
    def word_rot(i: 'ForthInterpreter'):
        """( n1 n2 n3 -- n2 n3 n1 ) Rotate third item to top."""
        i.require(3, 'ROT')
        c = i.pop()  # n3
        b = i.pop()  # n2
        a = i.pop()  # n1
        i.push(b)    # n2
        i.push(c)    # n3
        i.push(a)    # n1
    
    def word_nrot(i: 'ForthInterpreter'):
        """( n1 n2 n3 -- n3 n1 n2 ) Rotate top to third position."""
        i.require(3, '-ROT')
        c = i.pop()  # n3
        b = i.pop()  # n2
        a = i.pop()  # n1
        i.push(c)    # n3
        i.push(a)    # n1
        i.push(b)    # n2
    
    def word_nip(i: 'ForthInterpreter'):
        """( n1 n2 -- n2 ) Drop second item."""
        i.require(2, 'NIP')
        a = i.pop()
        i.pop()
        i.push(a)
    
    def word_tuck(i: 'ForthInterpreter'):
        """( n1 n2 -- n2 n1 n2 ) Copy top below second."""
        i.require(2, 'TUCK')
        a = i.pop()
        b = i.pop()
        i.push(a)
        i.push(b)
        i.push(a)
    
    def word_2dup(i: 'ForthInterpreter'):
        """( n1 n2 -- n1 n2 n1 n2 ) Duplicate top pair."""
        i.require(2, '2DUP')
        i.push(i.peek(1))
        i.push(i.peek(1))
    
    def word_2drop(i: 'ForthInterpreter'):
        """( n1 n2 -- ) Drop top pair."""
        i.require(2, '2DROP')
        i.pop()
        i.pop()
    
    def word_2swap(i: 'ForthInterpreter'):
        """( n1 n2 n3 n4 -- n3 n4 n1 n2 ) Swap pairs."""
        i.require(4, '2SWAP')
        d = i.pop()
        c = i.pop()
        b = i.pop()
        a = i.pop()
        i.push(c)
        i.push(d)
        i.push(a)
        i.push(b)
    
    def word_2over(i: 'ForthInterpreter'):
        """( n1 n2 n3 n4 -- n1 n2 n3 n4 n1 n2 ) Copy second pair."""
        i.require(4, '2OVER')
        i.push(i.peek(3))
        i.push(i.peek(3))
    
    def word_depth(i: 'ForthInterpreter'):
        """( -- n ) Push current stack depth."""
        i.push(len(i.data_stack))
    
    def word_pick(i: 'ForthInterpreter'):
        """( n -- item ) Copy nth item to top (0 = top)."""
        i.require(1, 'PICK')
        n = i.pop()
        i.require(n + 1, 'PICK')
        i.push(i.peek(n))
    
    def word_roll(i: 'ForthInterpreter'):
        """( n -- ) Rotate nth item to top."""
        i.require(1, 'ROLL')
        n = i.pop()
        if n == 0:
            return
        i.require(n + 1, 'ROLL')
        # Remove item at position n and push to top
        item = i.data_stack[-(n + 1)]
        del i.data_stack[-(n + 1)]
        i.push(item)
    
    def word_clear(i: 'ForthInterpreter'):
        """( ... -- ) Clear the stack."""
        i.clear()
    
    # Register all stack words
    words = [
        ('DUP', word_dup, '( n -- n n )', 'Duplicate top of stack'),
        ('DROP', word_drop, '( n -- )', 'Discard top of stack'),
        ('SWAP', word_swap, '( n1 n2 -- n2 n1 )', 'Exchange top two items'),
        ('OVER', word_over, '( n1 n2 -- n1 n2 n1 )', 'Copy second item to top'),
        ('ROT', word_rot, '( n1 n2 n3 -- n2 n3 n1 )', 'Rotate third item to top'),
        ('-ROT', word_nrot, '( n1 n2 n3 -- n3 n1 n2 )', 'Rotate top to third'),
        ('NIP', word_nip, '( n1 n2 -- n2 )', 'Drop second item'),
        ('TUCK', word_tuck, '( n1 n2 -- n2 n1 n2 )', 'Copy top below second'),
        ('2DUP', word_2dup, '( n1 n2 -- n1 n2 n1 n2 )', 'Duplicate top pair'),
        ('2DROP', word_2drop, '( n1 n2 -- )', 'Drop top pair'),
        ('2SWAP', word_2swap, '( n1 n2 n3 n4 -- n3 n4 n1 n2 )', 'Swap pairs'),
        ('2OVER', word_2over, '( n1 n2 n3 n4 -- n1 n2 n3 n4 n1 n2 )', 'Copy second pair'),
        ('DEPTH', word_depth, '( -- n )', 'Push current stack depth'),
        ('PICK', word_pick, '( n -- item )', 'Copy nth item to top'),
        ('ROLL', word_roll, '( n -- )', 'Rotate nth item to top'),
        ('CLEAR', word_clear, '( ... -- )', 'Clear the stack'),
    ]
    
    for name, code, effect, doc in words:
        interp.dictionary.define(DictionaryEntry(
            name=name, code=code, stack_effect=effect, docstring=doc
        ))


# =============================================================================
# Arithmetic Words
# =============================================================================

def _register_arithmetic_words(interp: 'ForthInterpreter') -> None:
    """Register arithmetic words."""
    
    def word_add(i: 'ForthInterpreter'):
        """( n1 n2 -- sum ) Addition."""
        i.require(2, '+')
        b = i.pop()
        a = i.pop()
        i.push(a + b)
    
    def word_sub(i: 'ForthInterpreter'):
        """( n1 n2 -- diff ) Subtraction."""
        i.require(2, '-')
        b = i.pop()
        a = i.pop()
        i.push(a - b)
    
    def word_mul(i: 'ForthInterpreter'):
        """( n1 n2 -- prod ) Multiplication."""
        i.require(2, '*')
        b = i.pop()
        a = i.pop()
        i.push(a * b)
    
    def word_div(i: 'ForthInterpreter'):
        """( n1 n2 -- quot ) Division."""
        i.require(2, '/')
        b = i.pop()
        a = i.pop()
        if b == 0:
            raise DivisionByZeroError(a)
        if isinstance(a, int) and isinstance(b, int):
            i.push(a // b)  # Integer division
        else:
            i.push(a / b)
    
    def word_mod(i: 'ForthInterpreter'):
        """( n1 n2 -- rem ) Modulo."""
        i.require(2, 'MOD')
        b = i.pop()
        a = i.pop()
        if b == 0:
            raise DivisionByZeroError(a)
        i.push(a % b)
    
    def word_divmod(i: 'ForthInterpreter'):
        """( n1 n2 -- rem quot ) Division with remainder."""
        i.require(2, '/MOD')
        b = i.pop()
        a = i.pop()
        if b == 0:
            raise DivisionByZeroError(a)
        i.push(a % b)
        i.push(a // b)
    
    def word_negate(i: 'ForthInterpreter'):
        """( n -- -n ) Negate."""
        i.require(1, 'NEGATE')
        i.push(-i.pop())
    
    def word_abs(i: 'ForthInterpreter'):
        """( n -- |n| ) Absolute value."""
        i.require(1, 'ABS')
        i.push(abs(i.pop()))
    
    def word_min(i: 'ForthInterpreter'):
        """( n1 n2 -- min ) Minimum."""
        i.require(2, 'MIN')
        b = i.pop()
        a = i.pop()
        i.push(min(a, b))
    
    def word_max(i: 'ForthInterpreter'):
        """( n1 n2 -- max ) Maximum."""
        i.require(2, 'MAX')
        b = i.pop()
        a = i.pop()
        i.push(max(a, b))
    
    def word_1plus(i: 'ForthInterpreter'):
        """( n -- n+1 ) Increment."""
        i.require(1, '1+')
        i.push(i.pop() + 1)
    
    def word_1minus(i: 'ForthInterpreter'):
        """( n -- n-1 ) Decrement."""
        i.require(1, '1-')
        i.push(i.pop() - 1)
    
    def word_2plus(i: 'ForthInterpreter'):
        """( n -- n+2 ) Add two."""
        i.require(1, '2+')
        i.push(i.pop() + 2)
    
    def word_2minus(i: 'ForthInterpreter'):
        """( n -- n-2 ) Subtract two."""
        i.require(1, '2-')
        i.push(i.pop() - 2)
    
    def word_2star(i: 'ForthInterpreter'):
        """( n -- n*2 ) Double (shift left)."""
        i.require(1, '2*')
        i.push(i.pop() << 1)
    
    def word_2slash(i: 'ForthInterpreter'):
        """( n -- n/2 ) Halve (shift right)."""
        i.require(1, '2/')
        i.push(i.pop() >> 1)
    
    # Register all arithmetic words
    words = [
        ('+', word_add, '( n1 n2 -- sum )', 'Addition'),
        ('-', word_sub, '( n1 n2 -- diff )', 'Subtraction'),
        ('*', word_mul, '( n1 n2 -- prod )', 'Multiplication'),
        ('/', word_div, '( n1 n2 -- quot )', 'Division'),
        ('MOD', word_mod, '( n1 n2 -- rem )', 'Modulo'),
        ('/MOD', word_divmod, '( n1 n2 -- rem quot )', 'Division with remainder'),
        ('NEGATE', word_negate, '( n -- -n )', 'Negate'),
        ('ABS', word_abs, '( n -- |n| )', 'Absolute value'),
        ('MIN', word_min, '( n1 n2 -- min )', 'Minimum'),
        ('MAX', word_max, '( n1 n2 -- max )', 'Maximum'),
        ('1+', word_1plus, '( n -- n+1 )', 'Increment'),
        ('1-', word_1minus, '( n -- n-1 )', 'Decrement'),
        ('2+', word_2plus, '( n -- n+2 )', 'Add two'),
        ('2-', word_2minus, '( n -- n-2 )', 'Subtract two'),
        ('2*', word_2star, '( n -- n*2 )', 'Double'),
        ('2/', word_2slash, '( n -- n/2 )', 'Halve'),
    ]
    
    for name, code, effect, doc in words:
        interp.dictionary.define(DictionaryEntry(
            name=name, code=code, stack_effect=effect, docstring=doc
        ))


# =============================================================================
# Comparison and Logic Words
# =============================================================================

def _register_comparison_words(interp: 'ForthInterpreter') -> None:
    """Register comparison and logic words."""
    
    # Forth uses -1 for true, 0 for false
    TRUE = -1
    FALSE = 0
    
    def to_flag(b: bool) -> int:
        return TRUE if b else FALSE
    
    def word_eq(i: 'ForthInterpreter'):
        """( n1 n2 -- flag ) Equal."""
        i.require(2, '=')
        b = i.pop()
        a = i.pop()
        i.push(to_flag(a == b))
    
    def word_neq(i: 'ForthInterpreter'):
        """( n1 n2 -- flag ) Not equal."""
        i.require(2, '<>')
        b = i.pop()
        a = i.pop()
        i.push(to_flag(a != b))
    
    def word_lt(i: 'ForthInterpreter'):
        """( n1 n2 -- flag ) Less than."""
        i.require(2, '<')
        b = i.pop()
        a = i.pop()
        i.push(to_flag(a < b))
    
    def word_gt(i: 'ForthInterpreter'):
        """( n1 n2 -- flag ) Greater than."""
        i.require(2, '>')
        b = i.pop()
        a = i.pop()
        i.push(to_flag(a > b))
    
    def word_le(i: 'ForthInterpreter'):
        """( n1 n2 -- flag ) Less than or equal."""
        i.require(2, '<=')
        b = i.pop()
        a = i.pop()
        i.push(to_flag(a <= b))
    
    def word_ge(i: 'ForthInterpreter'):
        """( n1 n2 -- flag ) Greater than or equal."""
        i.require(2, '>=')
        b = i.pop()
        a = i.pop()
        i.push(to_flag(a >= b))
    
    def word_0eq(i: 'ForthInterpreter'):
        """( n -- flag ) Equal to zero."""
        i.require(1, '0=')
        i.push(to_flag(i.pop() == 0))
    
    def word_0lt(i: 'ForthInterpreter'):
        """( n -- flag ) Less than zero."""
        i.require(1, '0<')
        i.push(to_flag(i.pop() < 0))
    
    def word_0gt(i: 'ForthInterpreter'):
        """( n -- flag ) Greater than zero."""
        i.require(1, '0>')
        i.push(to_flag(i.pop() > 0))
    
    def word_and(i: 'ForthInterpreter'):
        """( n1 n2 -- n ) Bitwise AND."""
        i.require(2, 'AND')
        b = i.pop()
        a = i.pop()
        i.push(a & b)
    
    def word_or(i: 'ForthInterpreter'):
        """( n1 n2 -- n ) Bitwise OR."""
        i.require(2, 'OR')
        b = i.pop()
        a = i.pop()
        i.push(a | b)
    
    def word_xor(i: 'ForthInterpreter'):
        """( n1 n2 -- n ) Bitwise XOR."""
        i.require(2, 'XOR')
        b = i.pop()
        a = i.pop()
        i.push(a ^ b)
    
    def word_invert(i: 'ForthInterpreter'):
        """( n -- ~n ) Bitwise NOT."""
        i.require(1, 'INVERT')
        i.push(~i.pop())
    
    def word_lshift(i: 'ForthInterpreter'):
        """( n1 n2 -- n ) Left shift n1 by n2 bits."""
        i.require(2, 'LSHIFT')
        n = i.pop()
        val = i.pop()
        i.push(val << n)
    
    def word_rshift(i: 'ForthInterpreter'):
        """( n1 n2 -- n ) Right shift n1 by n2 bits."""
        i.require(2, 'RSHIFT')
        n = i.pop()
        val = i.pop()
        i.push(val >> n)
    
    def word_true(i: 'ForthInterpreter'):
        """( -- -1 ) Push true flag."""
        i.push(TRUE)
    
    def word_false(i: 'ForthInterpreter'):
        """( -- 0 ) Push false flag."""
        i.push(FALSE)
    
    def word_not(i: 'ForthInterpreter'):
        """( flag -- flag ) Logical NOT."""
        i.require(1, 'NOT')
        val = i.pop()
        i.push(to_flag(val == 0))
    
    # Register all comparison/logic words
    words = [
        ('=', word_eq, '( n1 n2 -- flag )', 'Equal'),
        ('<>', word_neq, '( n1 n2 -- flag )', 'Not equal'),
        ('<', word_lt, '( n1 n2 -- flag )', 'Less than'),
        ('>', word_gt, '( n1 n2 -- flag )', 'Greater than'),
        ('<=', word_le, '( n1 n2 -- flag )', 'Less than or equal'),
        ('>=', word_ge, '( n1 n2 -- flag )', 'Greater than or equal'),
        ('0=', word_0eq, '( n -- flag )', 'Equal to zero'),
        ('0<', word_0lt, '( n -- flag )', 'Less than zero'),
        ('0>', word_0gt, '( n -- flag )', 'Greater than zero'),
        ('AND', word_and, '( n1 n2 -- n )', 'Bitwise AND'),
        ('OR', word_or, '( n1 n2 -- n )', 'Bitwise OR'),
        ('XOR', word_xor, '( n1 n2 -- n )', 'Bitwise XOR'),
        ('INVERT', word_invert, '( n -- ~n )', 'Bitwise NOT'),
        ('LSHIFT', word_lshift, '( n1 n2 -- n )', 'Left shift'),
        ('RSHIFT', word_rshift, '( n1 n2 -- n )', 'Right shift'),
        ('TRUE', word_true, '( -- -1 )', 'Push true flag'),
        ('FALSE', word_false, '( -- 0 )', 'Push false flag'),
        ('NOT', word_not, '( flag -- flag )', 'Logical NOT'),
    ]
    
    for name, code, effect, doc in words:
        interp.dictionary.define(DictionaryEntry(
            name=name, code=code, stack_effect=effect, docstring=doc
        ))


# =============================================================================
# Output Words
# =============================================================================

def _register_output_words(interp: 'ForthInterpreter') -> None:
    """Register output words."""
    
    def word_dot(i: 'ForthInterpreter'):
        """( n -- ) Print and remove top of stack."""
        i.require(1, '.')
        val = i.pop()
        i.emit_output(f"{val} ")
    
    def word_dot_s(i: 'ForthInterpreter'):
        """( -- ) Print stack non-destructively."""
        if not i.data_stack:
            i.emit_output("<empty> ")
        else:
            items = ' '.join(str(x) for x in i.data_stack)
            i.emit_output(f"<{len(i.data_stack)}> {items} ")
    
    def word_cr(i: 'ForthInterpreter'):
        """( -- ) Print newline."""
        i.emit_output("\n")
    
    def word_space(i: 'ForthInterpreter'):
        """( -- ) Print a space."""
        i.emit_output(" ")
    
    def word_spaces(i: 'ForthInterpreter'):
        """( n -- ) Print n spaces."""
        i.require(1, 'SPACES')
        n = i.pop()
        i.emit_output(" " * max(0, n))
    
    def word_emit(i: 'ForthInterpreter'):
        """( char -- ) Print character."""
        i.require(1, 'EMIT')
        char_code = i.pop()
        i.emit_output(chr(char_code))
    
    def word_type(i: 'ForthInterpreter'):
        """( addr n -- ) Print string - simplified for now."""
        i.require(2, 'TYPE')
        n = i.pop()
        addr = i.pop()
        # In our simplified model, addr might be a string
        if isinstance(addr, str):
            i.emit_output(addr[:n])
    
    def word_dot_quote(i: 'ForthInterpreter'):
        """Print a string literal - handled specially by lexer."""
        # String is on stack (pushed by lexer)
        i.require(1, '."')
        s = i.pop()
        i.emit_output(str(s))
    
    def word_words(i: 'ForthInterpreter'):
        """( -- ) List all defined words."""
        words = i.dictionary.words()
        # Print in columns
        col_width = 15
        cols = 5
        output = []
        for idx, word in enumerate(words):
            output.append(word.ljust(col_width))
            if (idx + 1) % cols == 0:
                output.append('\n')
        i.emit_output(''.join(output) + '\n')
    
    def word_see(i: 'ForthInterpreter'):
        """( -- ) Show word definition - needs following word."""
        # This is simplified - normally SEE would parse following word
        i.emit_output("Usage: SEE word-name\n")
    
    # Register all output words
    words = [
        ('.', word_dot, '( n -- )', 'Print and remove top of stack'),
        ('.S', word_dot_s, '( -- )', 'Print stack non-destructively'),
        ('CR', word_cr, '( -- )', 'Print newline'),
        ('SPACE', word_space, '( -- )', 'Print a space'),
        ('SPACES', word_spaces, '( n -- )', 'Print n spaces'),
        ('EMIT', word_emit, '( char -- )', 'Print character'),
        ('TYPE', word_type, '( addr n -- )', 'Print string'),
        ('."', word_dot_quote, '( -- )', 'Print string literal'),
        ('WORDS', word_words, '( -- )', 'List all words'),
        ('SEE', word_see, '( -- )', 'Show word definition'),
    ]
    
    for name, code, effect, doc in words:
        interp.dictionary.define(DictionaryEntry(
            name=name, code=code, stack_effect=effect, docstring=doc
        ))


# =============================================================================
# Control Flow Words (Compile-time / Immediate)
# =============================================================================

def _register_control_flow_words(interp: 'ForthInterpreter') -> None:
    """Register control flow words (mostly immediate/compile-time)."""
    
    # These words manipulate the compilation process
    # They compile branch operations into the current definition
    
    def word_if(i: 'ForthInterpreter'):
        """IF - Start conditional. Compiles 0BRANCH with placeholder."""
        if not i.compiling:
            return  # Only valid during compilation
        # Push current position for later patching
        branch_pos = len(i._current_definition)
        i._current_definition.append(('0BRANCH', None))  # Placeholder
        i.rpush(branch_pos)  # Remember where to patch
    
    def word_else(i: 'ForthInterpreter'):
        """ELSE - Optional branch for IF. Patches IF, compiles BRANCH."""
        if not i.compiling:
            return
        # Compile unconditional branch (to skip THEN part)
        branch_pos = len(i._current_definition)
        i._current_definition.append(('BRANCH', None))  # Placeholder
        
        # Patch the IF's 0BRANCH to jump here (after ELSE)
        if_pos = i.rpop()
        i._current_definition[if_pos] = ('0BRANCH', len(i._current_definition))
        
        # Remember ELSE position for THEN to patch
        i.rpush(branch_pos)
    
    def word_then(i: 'ForthInterpreter'):
        """THEN - End conditional. Patches previous branch."""
        if not i.compiling:
            return
        # Patch the previous branch (from IF or ELSE) to jump here
        branch_pos = i.rpop()
        op, _ = i._current_definition[branch_pos]
        i._current_definition[branch_pos] = (op, len(i._current_definition))
    
    def word_begin(i: 'ForthInterpreter'):
        """BEGIN - Start indefinite loop. Marks loop start."""
        if not i.compiling:
            return
        # Push loop start position
        i.rpush(len(i._current_definition))
    
    def word_until(i: 'ForthInterpreter'):
        """UNTIL - End BEGIN loop. Branches back if false."""
        if not i.compiling:
            return
        loop_start = i.rpop()
        i._current_definition.append(('0BRANCH', loop_start))
    
    def word_while(i: 'ForthInterpreter'):
        """WHILE - Mid-loop test. Branches to after REPEAT if false."""
        if not i.compiling:
            return
        branch_pos = len(i._current_definition)
        i._current_definition.append(('0BRANCH', None))  # Placeholder
        i.rpush(branch_pos)
    
    def word_repeat(i: 'ForthInterpreter'):
        """REPEAT - End BEGIN...WHILE loop. Branches back to BEGIN."""
        if not i.compiling:
            return
        while_pos = i.rpop()
        begin_pos = i.rpop()
        # Branch back to BEGIN
        i._current_definition.append(('BRANCH', begin_pos))
        # Patch WHILE to jump here
        i._current_definition[while_pos] = ('0BRANCH', len(i._current_definition))
    
    def word_do(i: 'ForthInterpreter'):
        """DO - Start counted loop. ( limit index -- )"""
        if not i.compiling:
            return
        i._current_definition.append(('DO', None))
        i.rpush(len(i._current_definition))  # Loop start
    
    def word_loop(i: 'ForthInterpreter'):
        """LOOP - End DO loop. Increments and checks."""
        if not i.compiling:
            return
        loop_start = i.rpop()
        i._current_definition.append(('LOOP', loop_start))
    
    def word_plus_loop(i: 'ForthInterpreter'):
        """+LOOP - End DO loop with custom increment."""
        if not i.compiling:
            return
        loop_start = i.rpop()
        i._current_definition.append(('+LOOP', loop_start))
    
    def word_i(i: 'ForthInterpreter'):
        """I - Push current loop index."""
        if i.compiling:
            i._current_definition.append(('I', None))
        else:
            # Runtime - use return stack
            if i.return_stack:
                i.push(i.rpeek(0))
    
    def word_j(i: 'ForthInterpreter'):
        """J - Push outer loop index."""
        if i.compiling:
            i._current_definition.append(('J', None))
        else:
            if len(i.return_stack) >= 2:
                i.push(i.rpeek(1))
    
    def word_leave(i: 'ForthInterpreter'):
        """LEAVE - Exit loop immediately."""
        if i.compiling:
            i._current_definition.append(('LEAVE', None))

    def word_unloop(i: 'ForthInterpreter'):
        """UNLOOP - Discard loop parameters from return stack."""
        if i.compiling:
            i._current_definition.append(('UNLOOP', None))
    
    def word_exit(i: 'ForthInterpreter'):
        """EXIT - Exit the current word immediately."""
        # This is tricky in threaded code - for now, compile as marker
        if i.compiling:
            i._current_definition.append(('EXIT', None))
    
    # Register control flow words - marked as IMMEDIATE
    words = [
        ('IF', word_if, '( flag -- )', 'Start conditional', True),
        ('ELSE', word_else, '( -- )', 'Alternative branch', True),
        ('THEN', word_then, '( -- )', 'End conditional', True),
        ('BEGIN', word_begin, '( -- )', 'Start indefinite loop', True),
        ('UNTIL', word_until, '( flag -- )', 'End BEGIN loop', True),
        ('WHILE', word_while, '( flag -- )', 'Mid-loop test', True),
        ('REPEAT', word_repeat, '( -- )', 'End BEGIN...WHILE loop', True),
        ('DO', word_do, '( limit index -- )', 'Start counted loop', True),
        ('LOOP', word_loop, '( -- )', 'End DO loop', True),
        ('+LOOP', word_plus_loop, '( n -- )', 'End DO loop with increment', True),
        ('I', word_i, '( -- n )', 'Push loop index', True),
        ('J', word_j, '( -- n )', 'Push outer loop index', True),
        ('LEAVE', word_leave, '( -- )', 'Exit loop', True),
        ('UNLOOP', word_unloop, '( -- )', 'Discard loop params', True),
        ('EXIT', word_exit, '( -- )', 'Exit word', True),
    ]
    
    for name, code, effect, doc, immediate in words:
        interp.dictionary.define(DictionaryEntry(
            name=name, code=code, stack_effect=effect, 
            docstring=doc, immediate=immediate
        ))
