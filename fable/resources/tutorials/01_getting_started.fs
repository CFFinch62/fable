\ ===============================================
\ FABLE Tutorial 1: Getting Started
\ ===============================================
\ 
\ Welcome to Forth! This tutorial covers the basics.
\ Run each section by selecting it and pressing F5.

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

\ --- SECTION 2: Simple Math ---

\ Forth uses "postfix" notation (numbers before operators)
\ Instead of "3 + 4", we write "3 4 +"

3 4 +       \ Push 3, push 4, add them
.           \ Print and remove the result: 7

10 3 -      \ 10 - 3 = 7
.

5 6 *       \ 5 * 6 = 30
.

20 4 /      \ 20 / 4 = 5
.

17 5 MOD    \ 17 mod 5 = 2 (remainder)
.

\ --- SECTION 3: Stack Operations ---

CLEAR

\ DUP - Duplicate the top value
5 DUP
.S          \ Stack: 5 5

CLEAR

\ DROP - Remove the top value
1 2 3 DROP
.S          \ Stack: 1 2

CLEAR

\ SWAP - Exchange the top two values
10 20 SWAP
.S          \ Stack: 20 10

CLEAR

\ OVER - Copy the second value to the top
1 2 OVER
.S          \ Stack: 1 2 1

CLEAR

\ --- SECTION 4: Your First Word Definition ---

\ Create new words with : name ... ;

: SQUARE DUP * ;

\ Now use your new word:
5 SQUARE .      \ prints 25
6 SQUARE .      \ prints 36

\ --- End of Tutorial 1 ---
\ Next: Tutorial 2 - Control Flow
