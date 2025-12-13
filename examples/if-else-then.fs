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