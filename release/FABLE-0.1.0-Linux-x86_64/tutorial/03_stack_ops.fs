\ Lesson 3: Stack Acrobatics
\ =============================

\ DUP: Duplicate top
10 DUP
. . \ Print both instances

\ DROP: Discard top
100 200 DROP . \ Only 100 remains

\ SWAP: Switch top two
1 2 SWAP
. \ Prints 1 (was bottom)
. \ Prints 2 (was top)

\ OVER: Copy second item
5 6 OVER . . .

\ ROT: Rotate third item
1 2 3 ROT . . .
