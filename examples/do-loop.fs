\ --- SECTION 3: Counted Loops (DO...LOOP) ---

\ DO takes a limit and index from the stack
\ I gives you the current loop index

: STARS 0 DO 42 EMIT LOOP ;
5 STARS         \ *****
CR

: COUNTDOWN 0 DO I . LOOP ;
5 COUNTDOWN     \ 0 1 2 3 4