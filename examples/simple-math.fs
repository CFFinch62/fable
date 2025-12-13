\ --- SECTION 2: Simple Math ---

\ Forth uses "postfix" notation (numbers before operators)
\ Instead of "3 + 4", we write "3 4 +"

3 4 +       \ Push 3, push 4, add them
. CR        \ Print and remove the result: 7

10 3 -      \ 10 - 3 = 7
. CR

5 6 *       \ 5 * 6 = 30
. CR

20 4 /      \ 20 / 4 = 5
. CR

17 5 MOD    \ 17 mod 5 = 2 (remainder)
. CR