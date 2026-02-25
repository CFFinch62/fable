\ --- SECTION 1: Conditionals (IF...THEN) ---

\ IF executes code only when the top of stack is TRUE (-1)
\ Forth uses 0 for FALSE, -1 for TRUE

: POSITIVE? DUP 0> IF ." positive" THEN ;

5 POSITIVE?     \ prints "positive"
-3 POSITIVE?    \ prints nothing