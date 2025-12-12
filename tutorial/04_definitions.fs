\ Lesson 4: Defining Words
\ ==========================

\ Define a word to square a number
: SQUARE ( n -- n^2 )
  DUP * ;

5 SQUARE .  \ Prints 25

\ Define a word to calculate Hypotenuse (Pythagoras)
\ a^2 + b^2 = c^2
: HYPOTENUSE ( a b -- c )
  SQUARE SWAP SQUARE + \ sum of squares could be SQRT but we don't have SQRT yet!
;

3 4 HYPOTENUSE . \ Prints 25 (c^2)

\ Helper words
: DOUBLE ( n -- n*2 ) 2 * ;
: TRIPLE ( n -- n*3 ) 3 * ;

10 DOUBLE TRIPLE . \ 60
