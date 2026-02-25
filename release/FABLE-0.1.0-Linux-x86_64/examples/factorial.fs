\ --- EXAMPLE 2: Factorial ---

: FACTORIAL  ( n -- n! )
  1 SWAP        \ put accumulator under n
  1+ 1 DO       \ loop from 1 to n
    I *
  LOOP ;

5 FACTORIAL .   \ 120 (5 * 4 * 3 * 2 * 1)
6 FACTORIAL .   \ 720