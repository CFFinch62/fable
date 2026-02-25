\ --- EXAMPLE 4: Greatest Common Divisor ---

: GCD  ( a b -- gcd )
  BEGIN
    DUP 0>
  WHILE
    SWAP OVER MOD
  REPEAT DROP ;

48 18 GCD .     \ 6
100 35 GCD .    \ 5