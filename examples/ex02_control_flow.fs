\ ===============================================
\ FABLE Tutorial 2: Control Flow
\ ===============================================
\
\ This tutorial covers conditionals and loops.

\ --- SECTION 1: Conditionals (IF...THEN) ---

\ IF executes code only when the top of stack is TRUE (-1)
\ Forth uses 0 for FALSE, -1 for TRUE

: POSITIVE? DUP 0> IF ." positive" THEN ;

5 POSITIVE?     \ prints "positive"
-3 POSITIVE?    \ prints nothing

\ --- SECTION 2: IF...ELSE...THEN ---

: SIGN
  DUP 0> IF 
    DROP ." positive" 
  ELSE 
    DUP 0< IF 
      DROP ." negative" 
    ELSE 
      DROP ." zero" 
    THEN 
  THEN ;

5 SIGN CR       \ positive
-3 SIGN CR      \ negative
0 SIGN CR       \ zero

\ --- SECTION 3: Counted Loops (DO...LOOP) ---

\ DO takes a limit and index from the stack
\ I gives you the current loop index

: STARS 0 DO 42 EMIT LOOP ;
5 STARS         \ *****
CR

: COUNTDOWN 0 DO I . LOOP ;
5 COUNTDOWN     \ 0 1 2 3 4

\ --- SECTION 4: Indefinite Loops (BEGIN...UNTIL) ---

\ BEGIN starts the loop
\ UNTIL pops a flag - if true, exit; if false, loop

: COUNT-DOWN
  10 BEGIN
    DUP . CR
    1-
    DUP 0=
  UNTIL DROP ;

\ Uncomment to run:
\ COUNT-DOWN

\ --- SECTION 5: WHILE...REPEAT ---

\ BEGIN...WHILE...REPEAT is like "while" in other languages

: HALVES
  BEGIN
    DUP 1 > 
  WHILE
    DUP . 2/
  REPEAT DROP ;

64 HALVES       \ 64 32 16 8 4 2

\ --- End of Tutorial 2 ---
\ Next: Tutorial 3 - Practical Examples
