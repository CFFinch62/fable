\ Lesson 5: Boolean Logic
\ =========================
\ True = -1, False = 0

\ Comparisons
5 3 > .  \ Prints -1 (True)
5 3 < .  \ Prints 0 (False)
5 5 = .  \ Prints -1 (True)

\ Logic Ops
-1 -1 AND . \ True AND True = True (-1)
-1  0 AND . \ True AND False = False (0)
-1  0 OR  . \ True OR False = True (-1)

\ Invert (Check if zero)
0 0= . \ True
5 0= . \ False
