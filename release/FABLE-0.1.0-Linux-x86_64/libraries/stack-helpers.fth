\ Library: stack-helpers.fth
\ Advanced stack manipulation utilities
\ Author: FABLE Team
\ Description: Additional stack operations for complex manipulations

\ 2DUP - Duplicate top two items
: 2DUP ( n1 n2 -- n1 n2 n1 n2 )
  OVER OVER ;

\ 2DROP - Drop top two items
: 2DROP ( n1 n2 -- )
  DROP DROP ;

\ 2SWAP - Swap top two pairs
: 2SWAP ( n1 n2 n3 n4 -- n3 n4 n1 n2 )
  ROT >R ROT R> ;

\ 2OVER - Copy second pair to top
: 2OVER ( n1 n2 n3 n4 -- n1 n2 n3 n4 n1 n2 )
  >R >R 2DUP R> R> 2SWAP ;

\ PICK - Copy nth item to top (0 PICK = DUP)
: PICK ( ... n -- ... x )
  1+ 0 DO SWAP LOOP DUP >R
  0 DO SWAP LOOP R> ;

\ ROLL - Move nth item to top (1 ROLL = SWAP, 2 ROLL = ROT)
: ROLL ( ... n -- ... x )
  1+ 0 DO SWAP LOOP
  0 DO SWAP LOOP ;

\ ?DUP - Duplicate if non-zero
: ?DUP ( n -- n n | 0 )
  DUP IF DUP THEN ;

\ DEPTH - Return current stack depth
: DEPTH ( -- n )
  0 >R
  BEGIN DUP WHILE
    R> 1+ >R
    DROP
  REPEAT
  R> ;

\ CLEAR - Clear the entire stack
: CLEAR ( ... -- )
  BEGIN DEPTH WHILE DROP REPEAT ;

\ 3DUP - Duplicate top three items
: 3DUP ( n1 n2 n3 -- n1 n2 n3 n1 n2 n3 )
  DUP 2OVER ROT ;

\ 3DROP - Drop top three items
: 3DROP ( n1 n2 n3 -- )
  DROP DROP DROP ;

\ TUCK2 - Copy top below third item
: TUCK2 ( n1 n2 n3 -- n3 n1 n2 n3 )
  DUP >R -ROT R> ;

\ SPIN - Rotate top four items
: SPIN ( n1 n2 n3 n4 -- n2 n3 n4 n1 )
  >R ROT ROT R> ;

