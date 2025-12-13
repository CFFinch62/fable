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