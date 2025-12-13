\ --- EXAMPLE 5: Prime Check ---

: PRIME?  ( n -- flag )
  DUP 2 < IF DROP 0 EXIT THEN
  DUP 2 = IF DROP -1 EXIT THEN
  DUP 2 / 2 DO
    DUP I MOD 0= IF
      DROP 0 UNLOOP EXIT
    THEN
  LOOP DROP -1 ;

\ simplified version:
: ISPRIME?  ( n -- flag )
  DUP 2 < IF DROP 0 EXIT THEN
  DUP 2 = IF DROP -1 EXIT THEN
  2 \ divisor
  BEGIN
    2DUP DUP * >
  WHILE
    2DUP MOD 0= IF
      2DROP 0 EXIT
    THEN
    1+
  REPEAT 2DROP -1 ;