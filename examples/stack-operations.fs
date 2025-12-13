\ --- SECTION 3: Stack Operations ---

CLEAR

\ DUP - Duplicate the top value
5 DUP
.S          \ Stack: 5 5

CLEAR

\ DROP - Remove the top value
1 2 3 DROP
.S          \ Stack: 1 2

CLEAR

\ SWAP - Exchange the top two values
10 20 SWAP
.S          \ Stack: 20 10

CLEAR

\ OVER - Copy the second value to the top
1 2 OVER
.S          \ Stack: 1 2 1

CLEAR