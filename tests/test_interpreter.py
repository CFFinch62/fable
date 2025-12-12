"""
Tests for the Forth interpreter.
"""

import pytest
from fable.interpreter.interpreter import ForthInterpreter
from fable.interpreter.errors import (
    StackUnderflowError, UnknownWordError, DivisionByZeroError
)


class TestStackOperations:
    """Test stack manipulation words."""
    
    def setup_method(self):
        """Create fresh interpreter for each test."""
        self.interp = ForthInterpreter()
    
    def test_push_numbers(self):
        """Numbers push onto stack."""
        self.interp.evaluate("1 2 3")
        assert self.interp.data_stack == [1, 2, 3]
    
    def test_dup(self):
        """DUP duplicates top of stack."""
        self.interp.evaluate("5 DUP")
        assert self.interp.data_stack == [5, 5]
    
    def test_drop(self):
        """DROP removes top of stack."""
        self.interp.evaluate("1 2 3 DROP")
        assert self.interp.data_stack == [1, 2]
    
    def test_swap(self):
        """SWAP exchanges top two items."""
        self.interp.evaluate("1 2 SWAP")
        assert self.interp.data_stack == [2, 1]
    
    def test_over(self):
        """OVER copies second item to top."""
        self.interp.evaluate("1 2 OVER")
        assert self.interp.data_stack == [1, 2, 1]
    
    def test_rot(self):
        """ROT rotates third item to top."""
        self.interp.evaluate("1 2 3 ROT")
        assert self.interp.data_stack == [2, 3, 1]
    
    def test_nrot(self):
        """-ROT rotates top to third."""
        self.interp.evaluate("1 2 3 -ROT")
        assert self.interp.data_stack == [3, 1, 2]
    
    def test_nip(self):
        """NIP drops second item."""
        self.interp.evaluate("1 2 NIP")
        assert self.interp.data_stack == [2]
    
    def test_tuck(self):
        """TUCK copies top below second."""
        self.interp.evaluate("1 2 TUCK")
        assert self.interp.data_stack == [2, 1, 2]
    
    def test_2dup(self):
        """2DUP duplicates top pair."""
        self.interp.evaluate("1 2 2DUP")
        assert self.interp.data_stack == [1, 2, 1, 2]
    
    def test_2drop(self):
        """2DROP drops top pair."""
        self.interp.evaluate("1 2 3 4 2DROP")
        assert self.interp.data_stack == [1, 2]
    
    def test_depth(self):
        """DEPTH reports stack size."""
        self.interp.evaluate("1 2 3 DEPTH")
        assert self.interp.data_stack == [1, 2, 3, 3]
    
    def test_clear(self):
        """CLEAR empties stack."""
        self.interp.evaluate("1 2 3 CLEAR")
        assert self.interp.data_stack == []


class TestArithmetic:
    """Test arithmetic operations."""
    
    def setup_method(self):
        self.interp = ForthInterpreter()
    
    def test_add(self):
        """Addition works correctly."""
        self.interp.evaluate("3 4 +")
        assert self.interp.data_stack == [7]
    
    def test_subtract(self):
        """Subtraction works correctly."""
        self.interp.evaluate("10 3 -")
        assert self.interp.data_stack == [7]
    
    def test_multiply(self):
        """Multiplication works correctly."""
        self.interp.evaluate("6 7 *")
        assert self.interp.data_stack == [42]
    
    def test_divide(self):
        """Division works correctly."""
        self.interp.evaluate("20 4 /")
        assert self.interp.data_stack == [5]
    
    def test_mod(self):
        """Modulo works correctly."""
        self.interp.evaluate("17 5 MOD")
        assert self.interp.data_stack == [2]
    
    def test_negate(self):
        """NEGATE changes sign."""
        self.interp.evaluate("5 NEGATE")
        assert self.interp.data_stack == [-5]
    
    def test_abs(self):
        """ABS returns absolute value."""
        self.interp.evaluate("-7 ABS")
        assert self.interp.data_stack == [7]
    
    def test_min(self):
        """MIN returns minimum."""
        self.interp.evaluate("5 3 MIN")
        assert self.interp.data_stack == [3]
    
    def test_max(self):
        """MAX returns maximum."""
        self.interp.evaluate("5 3 MAX")
        assert self.interp.data_stack == [5]
    
    def test_1plus(self):
        """1+ increments."""
        self.interp.evaluate("5 1+")
        assert self.interp.data_stack == [6]
    
    def test_1minus(self):
        """1- decrements."""
        self.interp.evaluate("5 1-")
        assert self.interp.data_stack == [4]


class TestComparison:
    """Test comparison operations."""
    
    def setup_method(self):
        self.interp = ForthInterpreter()
    
    def test_equal_true(self):
        """Equality returns true (-1) when equal."""
        self.interp.evaluate("5 5 =")
        assert self.interp.data_stack == [-1]
    
    def test_equal_false(self):
        """Equality returns false (0) when not equal."""
        self.interp.evaluate("5 3 =")
        assert self.interp.data_stack == [0]
    
    def test_less_than(self):
        """Less than comparison."""
        self.interp.evaluate("3 5 <")
        assert self.interp.data_stack == [-1]
    
    def test_greater_than(self):
        """Greater than comparison."""
        self.interp.evaluate("5 3 >")
        assert self.interp.data_stack == [-1]
    
    def test_0_equal(self):
        """0= tests for zero."""
        self.interp.evaluate("0 0=")
        assert self.interp.data_stack == [-1]
    
    def test_true_false(self):
        """TRUE and FALSE push correct values."""
        self.interp.evaluate("TRUE FALSE")
        assert self.interp.data_stack == [-1, 0]


class TestLogic:
    """Test logic operations."""
    
    def setup_method(self):
        self.interp = ForthInterpreter()
    
    def test_and(self):
        """Bitwise AND."""
        self.interp.evaluate("$FF $0F AND")
        assert self.interp.data_stack == [0x0F]
    
    def test_or(self):
        """Bitwise OR."""
        self.interp.evaluate("$F0 $0F OR")
        assert self.interp.data_stack == [0xFF]
    
    def test_xor(self):
        """Bitwise XOR."""
        self.interp.evaluate("$FF $0F XOR")
        assert self.interp.data_stack == [0xF0]
    
    def test_lshift(self):
        """Left shift."""
        self.interp.evaluate("1 4 LSHIFT")
        assert self.interp.data_stack == [16]
    
    def test_rshift(self):
        """Right shift."""
        self.interp.evaluate("16 4 RSHIFT")
        assert self.interp.data_stack == [1]


class TestErrors:
    """Test error handling."""
    
    def setup_method(self):
        self.interp = ForthInterpreter()
    
    def test_stack_underflow(self):
        """Stack underflow raises error."""
        with pytest.raises(StackUnderflowError):
            self.interp.evaluate("+")
    
    def test_unknown_word(self):
        """Unknown word raises error with suggestions."""
        with pytest.raises(UnknownWordError) as exc_info:
            self.interp.evaluate("DUPP")
        assert "DUP" in str(exc_info.value)  # Should suggest DUP
    
    def test_division_by_zero(self):
        """Division by zero raises error."""
        with pytest.raises(DivisionByZeroError):
            self.interp.evaluate("10 0 /")


class TestOutput:
    """Test output operations."""
    
    def setup_method(self):
        self.interp = ForthInterpreter()
        self.output = []
        self.interp.output.connect(lambda s: self.output.append(s))
    
    def test_dot_prints(self):
        """Dot prints and removes top."""
        self.interp.evaluate("42 .")
        assert "42" in ''.join(self.output)
        assert self.interp.data_stack == []
    
    def test_dot_s_prints_stack(self):
        """.S prints stack non-destructively."""
        self.interp.evaluate("1 2 3 .S")
        output = ''.join(self.output)
        assert "1" in output
        assert "2" in output  
        assert "3" in output
        assert self.interp.data_stack == [1, 2, 3]
