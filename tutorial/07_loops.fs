\ Lesson 7: Loops
\ ================

\ 1. Counted Loop (DO ... LOOP)
\ Prints 0 1 2 3 4
: COUNT-5 
  5 0 DO
    I .
  LOOP ;

COUNT-5 CR

\ 2. Counted Loop with Step (+LOOP)
\ Prints 0 2 4 6 8
: EVENS
  10 0 DO
    I .
  2 +LOOP ;

EVENS CR

\ 3. Indefinite Loop (BEGIN ... UNTIL)
\ Countdown from n to 1
: COUNTDOWN ( n -- )
  BEGIN
    DUP .   \ Print current number
    1-      \ Decrement
    DUP 0=  \ Check if zero
  UNTIL
  DROP ;

10 COUNTDOWN
