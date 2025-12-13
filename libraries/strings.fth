\ Library: strings.fth
\ String manipulation utilities for FABLE
\ Author: FABLE Team
\ Description: Helper words for working with strings

\ Print a horizontal line of dashes
: LINE ( n -- )
  0 DO 45 EMIT LOOP CR ;

\ Print a horizontal line of equals signs
: DOUBLE-LINE ( n -- )
  0 DO 61 EMIT LOOP CR ;

\ Print a box top
: BOX-TOP ( width -- )
  43 EMIT
  2 - 0 DO 45 EMIT LOOP
  43 EMIT CR ;

\ Print a box bottom
: BOX-BOTTOM ( width -- )
  43 EMIT
  2 - 0 DO 45 EMIT LOOP
  43 EMIT CR ;

\ Print centered text (simplified - just adds spaces)
: CENTER ( n -- )
  2 / SPACES ;

\ Print a character n times
: REPEAT-CHAR ( char n -- )
  0 DO DUP EMIT LOOP DROP ;

\ Print a string of stars
: STARS ( n -- )
  42 SWAP REPEAT-CHAR ;

\ Print a blank line
: BLANK-LINE ( -- )
  CR ;

\ Print multiple blank lines
: BLANK-LINES ( n -- )
  0 DO CR LOOP ;

\ Print a separator
: SEPARATOR ( -- )
  50 LINE ;

\ Print a header with text
: HEADER ( -- )
  50 DOUBLE-LINE
  ." FABLE - Forth Learning Environment" CR
  50 DOUBLE-LINE ;

\ Print a simple banner
: BANNER ( -- )
  CR
  50 STARS CR
  ."   FABLE - Every Stack Tells a Story" CR
  50 STARS CR
  CR ;

