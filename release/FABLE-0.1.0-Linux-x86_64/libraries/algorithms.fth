\ Library: algorithms.fth
\ Common algorithms and patterns
\ Author: FABLE Team
\ Description: Useful algorithmic building blocks

\ Bubble sort helper - compare and swap if needed
: ?SWAP ( n1 n2 -- n1 n2 | n2 n1 )
  2DUP > IF SWAP THEN ;

\ Count down from n to 1
: COUNTDOWN ( n -- )
  BEGIN DUP . 1- DUP 0= UNTIL DROP ;

\ Count up from 1 to n
: COUNTUP ( n -- )
  1+ 1 DO I . LOOP ;

\ Print multiplication table for n
: TIMES-TABLE ( n -- )
  1+ 1 DO
    1+ 1 DO
      I J * . SPACE
    LOOP CR
  LOOP ;

\ Sum all numbers on stack (depth must be known)
: SUM-STACK ( n1 n2 ... nk k -- sum )
  0 SWAP 0 DO + LOOP ;

\ Product of all numbers on stack
: PRODUCT-STACK ( n1 n2 ... nk k -- product )
  1 SWAP 0 DO * LOOP ;

\ Reverse top n items on stack
: REVERSE ( ... n -- ... )
  DUP 2 < IF DROP EXIT THEN
  DUP 1- 0 DO
    I PICK
  LOOP
  SWAP 0 DO DROP LOOP ;

\ Collatz sequence step
: COLLATZ-STEP ( n -- n' )
  DUP EVEN? IF 2 / ELSE 3 * 1+ THEN ;

\ Print Collatz sequence
: COLLATZ ( n -- )
  BEGIN DUP . DUP 1 > WHILE
    COLLATZ-STEP
  REPEAT DROP ;

\ Digital root (sum digits until single digit)
: DIGITAL-ROOT ( n -- root )
  BEGIN DUP 10 < IF EXIT THEN
    0 SWAP
    BEGIN DUP WHILE
      10 /MOD ROT +
    REPEAT DROP
  REPEAT ;

\ Sum of digits
: SUM-DIGITS ( n -- sum )
  0 SWAP
  BEGIN DUP WHILE
    10 /MOD ROT +
  REPEAT DROP ;

\ Reverse digits of a number
: REVERSE-NUMBER ( n -- n' )
  0 SWAP
  BEGIN DUP WHILE
    10 /MOD SWAP ROT 10 * +
  REPEAT DROP ;

\ Check if palindrome number
: PALINDROME? ( n -- flag )
  DUP REVERSE-NUMBER = ;

\ Tower of Hanoi move counter
: HANOI-MOVES ( n -- moves )
  2 SWAP POW 1- ;

\ Binary representation (print)
: .BIN ( n -- )
  DUP 0= IF ." 0" DROP EXIT THEN
  0 SWAP
  BEGIN DUP WHILE
    2 /MOD SWAP >R 1+
  REPEAT DROP
  0 DO R> . LOOP ;

\ Count set bits (population count)
: POPCOUNT ( n -- count )
  0 SWAP
  BEGIN DUP WHILE
    DUP 1 AND ROT + SWAP 2 /
  REPEAT DROP ;

\ Next power of 2
: NEXT-POW2 ( n -- 2^k )
  1- DUP 1 RSHIFT OR
  DUP 2 RSHIFT OR
  DUP 4 RSHIFT OR
  DUP 8 RSHIFT OR
  DUP 16 RSHIFT OR
  1+ ;

