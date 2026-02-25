\ Using Libraries in FABLE
\ This example shows how to use the library system in your programs
\ 
\ HOW TO RUN THIS FILE:
\ 1. Open this file in the FABLE editor (you're probably already viewing it!)
\ 2. Press F5 to run the entire file
\ 3. Watch the output in the REPL (bottom panel)
\ 4. Watch the stack animate in the Stack Widget (right panel)

\ ============================================================
\ STEP 1: Load the libraries we need
\ ============================================================

." Loading libraries..." CR

S" math-extended.fth" INCLUDE
S" strings.fth" INCLUDE

." Libraries loaded!" CR CR

\ ============================================================
\ STEP 2: Use words from the libraries
\ ============================================================

." " CR
." ========================================" CR
." Math Library Examples" CR  
." ========================================" CR
." " CR

\ Absolute value
." Absolute value of -42: " -42 ABS . CR

\ Min and Max
." Min of 10 and 5: " 10 5 MIN . CR
." Max of 10 and 5: " 10 5 MAX . CR

\ Factorial
." 5 factorial: " 5 FACTORIAL . CR
." 7 factorial: " 7 FACTORIAL . CR

\ GCD and LCM
." GCD of 48 and 18: " 48 18 GCD . CR
." LCM of 12 and 8: " 12 8 LCM . CR

\ Even and odd (using a helper word since IF/THEN only works in compiled words)
: CHECK-EVEN ( n -- )
  DUP ." Is " . ." even? "
  EVEN? IF ." Yes" ELSE ." No" THEN CR ;

10 CHECK-EVEN
11 CHECK-EVEN

\ Sign function
." Sign of -5: " -5 SIGN . CR
." Sign of 0: " 0 SIGN . CR
." Sign of 7: " 7 SIGN . CR

\ ============================================================
\ STEP 3: Use string formatting from strings library
\ ============================================================

." " CR
." ========================================" CR
." String Formatting Examples" CR
." ========================================" CR
." " CR

." Drawing a line:" CR
40 LINE

." " CR
." Drawing a double line:" CR
40 DOUBLE-LINE

." " CR
." Drawing a box top:" CR
30 BOX-TOP

\ ============================================================
\ STEP 4: Define your own words using library words
\ ============================================================

." " CR
." ========================================" CR
." Custom Word Examples" CR
." ========================================" CR
." " CR

\ A word that uses multiple library words
: DESCRIBE-NUMBER ( n -- )
  DUP ." Number " . ." is "
  DUP EVEN? IF ." even " ELSE ." odd " THEN
  ." and its square is " SQUARE . CR ;

5 DESCRIBE-NUMBER
8 DESCRIBE-NUMBER

\ A word that calculates and shows factorial
: SHOW-FACTORIAL ( n -- )
  DUP ." Factorial of " . ." is "
  FACTORIAL . CR ;

6 SHOW-FACTORIAL
8 SHOW-FACTORIAL

\ ============================================================
\ STEP 5: Save your custom words (optional)
\ ============================================================

\ Uncomment the line below to save your custom words to a library:
\ S" my-custom-words.fth" SAVE-LIBRARY

\ ============================================================
\ DONE!
\ ============================================================

." " CR
50 LINE
." " CR
." Demo complete! Try these next:" CR
." " CR
." 1. Press F6 to run just selected code" CR
." 2. Press F7 to run the current line" CR
." 3. Try modifying this file and running it again" CR
." 4. Create your own .fth file with INCLUDE statements" CR
." 5. Check out the other example files in the File Browser" CR
." " CR
50 LINE

