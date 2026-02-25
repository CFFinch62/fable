\ --- SECTION 1: Numbers and the Stack ---

\ In Forth, you put numbers on a "stack"
\ Just type a number to push it onto the stack:

42

\ Use .S to see what's on the stack:
.S

\ Try pushing more numbers:
1 2 3 4 5
.S

\ Clear the stack for a fresh start:
CLEAR