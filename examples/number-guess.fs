\ --- EXAMPLE 7: Number Guessing Game Logic ---

: TOO-LOW  ." Too low! " ;
: TOO-HIGH ." Too high! " ;
: CORRECT  ." Correct! " ;

: CHECK  ( guess secret -- )
  2DUP < IF 2DROP TOO-LOW EXIT THEN
  2DUP > IF 2DROP TOO-HIGH EXIT THEN
  2DROP CORRECT ;

5 7 CHECK       \ Too low!
9 7 CHECK       \ Too high!
7 7 CHECK       \ Correct!