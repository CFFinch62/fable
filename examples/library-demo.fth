\ Library System Demo
\ This example demonstrates how to use FABLE's library system

\ First, let's see where libraries are searched for
." Library search paths:" CR
LIBRARY-PATH

\ Load the math-extended library
." " CR
." Loading math-extended library..." CR
S" math-extended.fth" INCLUDE

\ Now we can use words from the library!
." " CR
." Testing library words:" CR

." -42 ABS = " -42 ABS . CR
." 10 5 MIN = " 10 5 MIN . CR
." 10 5 MAX = " 10 5 MAX . CR
." 7 SQUARE = " 7 SQUARE . CR
." 5 FACTORIAL = " 5 FACTORIAL . CR
." 12 8 GCD = " 12 8 GCD . CR
." 17 PRIME? = " 17 PRIME? . CR

\ Define some custom words
." " CR
." Defining custom words..." CR

: QUADRUPLE DOUBLE DOUBLE ;
: AVERAGE + 2 / ;
: CELSIUS>FAHRENHEIT 9 * 5 / 32 + ;

\ Test our custom words
." 5 QUADRUPLE = " 5 QUADRUPLE . CR
." 10 20 AVERAGE = " 10 20 AVERAGE . CR
." 100 CELSIUS>FAHRENHEIT = " 100 CELSIUS>FAHRENHEIT . CR

\ Show what libraries are loaded
." " CR
." Currently loaded libraries:" CR
LOADED-LIBRARIES

\ You can save your custom words to a library file:
\ S" my-words.fth" SAVE-LIBRARY

." " CR
." Demo complete! Try loading other libraries:" CR
." - S\" stack-helpers.fth\" INCLUDE" CR
." - S\" strings.fth\" INCLUDE" CR
." - S\" algorithms.fth\" INCLUDE" CR
." - S\" graphics.fth\" INCLUDE" CR

