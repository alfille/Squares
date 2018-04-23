#!/usr/bin/sh
for letter in a b c d e f
  do
  for sides in 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22
    do
    python3 ../optimizations/squares_$letter.py $sides -q -q -q -q >> results_$letter.cvs
  done
done
