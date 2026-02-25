\ --- SECTION 5: WHILE...REPEAT ---

\ BEGIN...WHILE...REPEAT is like "while" in other languages

: HALVES
  BEGIN
    DUP 1 > 
  WHILE
    DUP . 2/
  REPEAT DROP ;

64 HALVES       \ 64 32 16 8 4 2