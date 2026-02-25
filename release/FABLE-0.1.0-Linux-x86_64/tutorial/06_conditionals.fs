\ Lesson 6: Conditionals (IF/ELSE)
\ ================================

: TEST-NUMBER ( n -- )
    DUP 0> IF
        ." Positive"
    ELSE
        DUP 0< IF
            ." Negative"
        ELSE
            ." Zero"
        THEN
    THEN 
    DROP \ Remove the number
;

10 TEST-NUMBER CR
-5 TEST-NUMBER CR
0  TEST-NUMBER CR
