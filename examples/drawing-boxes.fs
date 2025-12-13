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