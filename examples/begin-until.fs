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