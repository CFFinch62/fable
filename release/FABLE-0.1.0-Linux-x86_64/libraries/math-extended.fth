\ Library: math-extended.fth
\ Extended mathematical operations for FABLE
\ Author: FABLE Team
\ Description: Additional math functions beyond basic arithmetic

\ Absolute value
: ABS ( n -- |n| )
  DUP 0 < IF NEGATE THEN ;

\ Minimum of two numbers
: MIN ( n1 n2 -- min )
  2DUP < IF DROP ELSE NIP THEN ;

\ Maximum of two numbers
: MAX ( n1 n2 -- max )
  2DUP > IF DROP ELSE NIP THEN ;

\ Square a number
: SQUARE ( n -- n^2 )
  DUP * ;

\ Cube a number
: CUBE ( n -- n^3 )
  DUP DUP * * ;

\ Power function (n^exp) - simple version for positive integers
: POW ( n exp -- n^exp )
  1 SWAP 0 DO OVER * LOOP NIP ;

\ Factorial (iterative)
: FACTORIAL ( n -- n! )
  DUP 2 < IF DROP 1 EXIT THEN
  1 SWAP 1+ 1 DO I * LOOP ;

\ Greatest Common Divisor (Euclidean algorithm)
: GCD ( a b -- gcd )
  BEGIN DUP WHILE SWAP OVER MOD REPEAT DROP ;

\ Least Common Multiple
: LCM ( a b -- lcm )
  2DUP GCD >R * R> / ;

\ Check if number is even
: EVEN? ( n -- flag )
  2 MOD 0= ;

\ Check if number is odd
: ODD? ( n -- flag )
  2 MOD 0<> ;

\ Clamp a value between min and max
: CLAMP ( n min max -- n' )
  ROT MIN MAX ;

\ Average of two numbers
: AVG ( n1 n2 -- avg )
  + 2 / ;

\ Sign of a number (-1, 0, or 1)
: SIGN ( n -- -1|0|1 )
  DUP 0= IF EXIT THEN
  0 < IF -1 ELSE 1 THEN ;

\ Integer square root (Newton's method approximation)
: SQRT ( n -- sqrt )
  DUP 0= IF EXIT THEN
  DUP 2 /
  10 0 DO
    OVER OVER / OVER + 2 /
  LOOP
  NIP ;

\ Check if number is a perfect square
: SQUARE? ( n -- flag )
  DUP SQRT DUP * = ;

\ Sum of integers from 1 to n
: SUM-TO ( n -- sum )
  DUP 1+ * 2 / ;

\ Fibonacci number (iterative)
: FIB ( n -- fib[n] )
  DUP 2 < IF EXIT THEN
  0 1 ROT 1- 0 DO
    OVER + SWAP
  LOOP NIP ;

\ Check if prime (simple trial division)
: PRIME? ( n -- flag )
  DUP 2 < IF DROP 0 EXIT THEN
  DUP 2 = IF DROP -1 EXIT THEN
  DUP EVEN? IF DROP 0 EXIT THEN
  DUP SQRT 1+
  3 DO
    DUP I MOD 0= IF DROP 0 EXIT THEN
  2 +LOOP
  DROP -1 ;

