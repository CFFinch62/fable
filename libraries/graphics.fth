\ Library: graphics.fth
\ ASCII art and visual output utilities
\ Author: FABLE Team
\ Description: Create simple ASCII graphics and patterns

\ Draw a filled rectangle
: RECTANGLE ( width height -- )
  0 DO
    DUP 0 DO 42 EMIT LOOP CR
  LOOP DROP ;

\ Draw a hollow rectangle
: HOLLOW-RECT ( width height -- )
  OVER 1 DO 42 EMIT LOOP CR
  2 - 0 DO
    42 EMIT
    OVER 2 - SPACES
    42 EMIT CR
  LOOP
  SWAP 1 DO 42 EMIT LOOP CR ;

\ Draw a right triangle
: RIGHT-TRIANGLE ( size -- )
  1+ 1 DO
    I 0 DO 42 EMIT LOOP CR
  LOOP ;

\ Draw an inverted right triangle
: INV-TRIANGLE ( size -- )
  1+ 1 DO
    DUP I - 0 DO 42 EMIT LOOP CR
  LOOP DROP ;

\ Draw a pyramid
: PYRAMID ( height -- )
  1+ 1 DO
    DUP I - SPACES
    I 2 * 1- 0 DO 42 EMIT LOOP CR
  LOOP DROP ;

\ Draw a diamond
: DIAMOND ( size -- )
  DUP PYRAMID
  1- 1 DO
    DUP I - 1+ SPACES
    DUP I - 2 * 1- 0 DO 42 EMIT LOOP CR
  LOOP DROP ;

\ Draw a checkerboard pattern
: CHECKERBOARD ( size -- )
  DUP 0 DO
    DUP 0 DO
      I J + EVEN? IF 35 ELSE 32 THEN EMIT
    LOOP CR
  LOOP DROP ;

\ Draw a horizontal bar chart
: BAR ( value max-width -- )
  SWAP 0 DO 61 EMIT LOOP CR ;

\ Draw a simple border
: BORDER ( width -- )
  DUP 0 DO 61 EMIT LOOP CR
  DUP 0 DO 35 EMIT LOOP CR
  DUP 0 DO 61 EMIT LOOP CR DROP ;

\ Draw a cross/plus sign
: CROSS ( size -- )
  DUP 2 / 1+ 1 DO
    OVER 2 / SPACES 42 EMIT CR
  LOOP
  DUP 0 DO 42 EMIT LOOP CR
  DUP 2 / 1 DO
    OVER 2 / SPACES 42 EMIT CR
  LOOP DROP ;

\ Draw a simple box with title
: TITLE-BOX ( width -- )
  DUP 43 SWAP 0 DO EMIT LOOP 43 EMIT CR
  ." | FABLE Output |" CR
  DUP 43 SWAP 0 DO EMIT LOOP 43 EMIT CR DROP ;

\ Draw a progress bar
: PROGRESS ( current total width -- )
  >R SWAP R> SWAP / *
  91 EMIT
  DUP 0 DO 61 EMIT LOOP
  OVER SWAP - 0 DO 32 EMIT LOOP
  93 EMIT DROP ;

\ Draw a simple graph axis
: AXIS ( width height -- )
  SWAP >R
  0 DO
    124 EMIT CR
  LOOP
  124 EMIT
  R> 0 DO 45 EMIT LOOP CR ;

\ Draw a staircase
: STAIRS ( steps -- )
  0 DO
    I SPACES
    I 1+ 0 DO 35 EMIT LOOP CR
  LOOP ;

\ Draw a wave pattern (simplified)
: WAVE ( width -- )
  0 DO
    I 4 MOD DUP SPACES 126 EMIT CR
  LOOP ;

