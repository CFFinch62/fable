\ ===============================================
\ FABLE Tutorial 3: Practical Examples
\ ===============================================
\
\ Real-world Forth programs and patterns.

\ --- EXAMPLE 1: Temperature Conversion ---

: F>C  ( fahrenheit -- celsius )
  32 - 5 * 9 / ;

: C>F  ( celsius -- fahrenheit )
  9 * 5 / 32 + ;

212 F>C .       \ 100 (boiling point of water)
100 C>F .       \ 212
0 C>F .         \ 32 (freezing point)

\ --- EXAMPLE 2: Factorial ---

: FACTORIAL  ( n -- n! )
  1 SWAP        \ put accumulator under n
  1+ 1 DO       \ loop from 1 to n
    I *
  LOOP ;

5 FACTORIAL .   \ 120 (5 * 4 * 3 * 2 * 1)
6 FACTORIAL .   \ 720

\ --- EXAMPLE 3: Fibonacci Sequence ---

: FIB  ( n -- fib[n] )
  0 1 ROT 0 DO
    OVER +      \ next = a + b
    SWAP        \ swap to prepare for next iteration
  LOOP DROP ;

10 FIB .        \ 55

\ Print first 10 Fibonacci numbers:
: FIBS 10 0 DO I FIB . LOOP ;
FIBS CR

\ --- EXAMPLE 4: Greatest Common Divisor ---

: GCD  ( a b -- gcd )
  BEGIN
    DUP 0>
  WHILE
    SWAP OVER MOD
  REPEAT DROP ;

48 18 GCD .     \ 6
100 35 GCD .    \ 5

\ --- EXAMPLE 5: Prime Check ---

: PRIME?  ( n -- flag )
  DUP 2 < IF DROP 0 EXIT THEN
  DUP 2 = IF DROP -1 EXIT THEN
  DUP 2 / 2 DO
    DUP I MOD 0= IF
      DROP 0 UNLOOP EXIT
    THEN
  LOOP DROP -1 ;

\ Note: UNLOOP not implemented, simplified version:
: ISPRIME?  ( n -- flag )
  DUP 2 < IF DROP 0 EXIT THEN
  DUP 2 = IF DROP -1 EXIT THEN
  2 \ divisor
  BEGIN
    2DUP DUP * >
  WHILE
    2DUP MOD 0= IF
      2DROP 0 EXIT
    THEN
    1+
  REPEAT 2DROP -1 ;

\ --- EXAMPLE 6: Drawing Boxes ---

: HLINE  ( n -- )
  0 DO 45 EMIT LOOP ;  \ 45 = '-'

: BOX  ( width height -- )
  SWAP
  DUP HLINE CR
  SWAP 2 - 0 DO
    124 EMIT            \ '|'
    DUP 2 - SPACES
    124 EMIT CR
  LOOP
  HLINE CR ;

10 5 BOX

\ --- EXAMPLE 7: Number Guessing Game Logic ---

: TOO-LOW  ." Too low! " ;
: TOO-HIGH ." Too high! " ;
: CORRECT  ." Correct! " ;

: CHECK  ( guess secret -- )
  2DUP < IF 2DROP TOO-LOW EXIT THEN
  2DUP > IF 2DROP TOO-HIGH EXIT THEN
  2DROP CORRECT ;

5 7 CHECK       \ Too low!
9 7 CHECK       \ Too high!
7 7 CHECK       \ Correct!

\ --- End of Tutorial 3 ---
