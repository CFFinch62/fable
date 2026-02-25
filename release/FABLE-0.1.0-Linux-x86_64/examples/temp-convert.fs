\ --- EXAMPLE 1: Temperature Conversion ---

: F>C  ( fahrenheit -- celsius )
  32 - 5 * 9 / ;

: C>F  ( celsius -- fahrenheit )
  9 * 5 / 32 + ;

212 F>C .       \ 100 (boiling point of water)
100 C>F .       \ 212
0 C>F .         \ 32 (freezing point)