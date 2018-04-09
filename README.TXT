Squares

by Paul H Alfille 2018

Solves the task of best packing of squares in a larger rectangle.
Best means fewest sub-squares

An example is a 13x13 square can be filled with as few as 11 smaller squares
Filled means tiled completely without overlap

Syntax:
-----------------
$ python3 ./squares.py -h
usage: squares.py [-h] [-s] [N] [M]

Fit Squares in large Square (rectangle) -- find fewest needed. 2018 by Paul H
Alfille

positional arguments:
  N           Width of large rectangle (default 13)
  M           Height of large rectangle (default square)

optional arguments:
  -h, --help  show this help message and exit
  -s, --SHOW  Show the solutions graphically
  
--------------------

In use:
$ python3 ./squares.py 7
14 < 0x0-6 > < 0x6-1 > < 1x6-1 > < 2x6-1 > < 3x6-1 > < 4x6-1 > < 5x6-1 > < 6x0-1 > < 6x1-1 > < 6x2-1 > < 6x3-1 > < 6x4-1 > < 6x5-1 > < 6x6-1 >
10 < 0x0-5 > < 0x5-2 > < 2x5-2 > < 4x5-2 > < 5x0-2 > < 5x2-2 > < 5x4-1 > < 6x4-1 > < 6x5-1 > < 6x6-1 >
9 < 0x0-4 > < 0x4-3 > < 3x4-2 > < 3x6-1 > < 4x0-3 > < 4x3-1 > < 4x6-1 > < 5x3-2 > < 5x5-2 >
Fewest squares for 7x7 = 9

---------------------
Each line shows proressively better solutions.
Elements < 0x0-6 > is a square with upper corner at 0,0 and side length 6

---------------------
Requires python 3 and Zelle's graphics module (included)
