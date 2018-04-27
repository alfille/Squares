#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  squares.py
#  
#  Copyright 2018 Paul Alfille <paul.alfille@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

""" _coverage

Just the sum to make squares part

I.e. the fewest number of squares that makes each integer

Much more complete remaining space check
Optimize first square is the largest
Remaining space not a perfect square means 2 more
Left upper corner largest corner
Full symmetry test
Test with
for n in {1..22} ; do ./squares_f.py -q -q $n >> time_f ; done
"""


class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class PruneError(Error):
    """Exception for branch too long (longer than current record).
    """

    def __init__(self):
        pass

class SquareComponents:
    squarelist = []
    size = None
    def __init__( self,size ):
        SquareComponents.squarelist = [ (i*i,i) for i in range( size, 0, -1 ) ]
        SquareComponents.size = size

    def SqComp1( self, n ):
        for i in SquareComponents.squarelist:
            if n == i[0]:
                return [n,i[1]]
        return None
        
    def SqComp2( self, n ):
        for i in SquareComponents.squarelist:
            for j in SquareComponents.squarelist:
                if n == i[0]+j[0]:
                    return [n,i[1],j[1]]
        return None

    def SqComp3( self, n ):
        for i in SquareComponents.squarelist:
            for j in SquareComponents.squarelist:
                for k in SquareComponents.squarelist:
                    if n == i[0]+j[0]+k[0]:
                        return [n,i[1],j[1],k[1]]
        return None

    def SqComp4( self, n ):
        for i in SquareComponents.squarelist:
            for j in SquareComponents.squarelist:
                for k in SquareComponents.squarelist:
                    for l in SquareComponents.squarelist:
                        if n == i[0]+j[0]+k[0]+l[0]:
                            return [n,i[1],j[1],k[1],l[1]]
        return None
        
    def SqComp( self,n ):
        return self.SqComp1(n) or self.SqComp2(n) or self.SqComp3(n) or self.SqComp4(n)
    


def LeastSquares( N, Max ):
    """ Create a list of minimum nuber of squares that add up to that number """
    max_remain = N*N
    trials = set( [i for i in range(1,max_remain+1) ] )

    # Worst case
    passes = 2*N - 1 + (N*N)//(Max*Max)
    LS = [ passes for i in range( max_remain+1 ) ]
    LS[0] = 1 # special case

    sq_try = [ sq*sq for sq in range(1,Max+1)]
    last_set = set(sq_try)
    for i in last_set:
        LS[i] = 1

    for moves in range(1,passes):
        last_set = set([ i+sq for i in last_set for sq in sq_try if i+sq <= max_remain ])
        for i in last_set:
            LS[i] = min( LS[i], moves )
    
    print( "N= {:d} N^2= {:d} max= {:d} MA = {:d}".format(N,N*N,Max,max(LS)) )
        

def CommandLine():
    """Setup argparser object to process the command line"""
    cl = argparse.ArgumentParser(description="Fit Squares in large Rectangle or Box) -- find fewest needed. 2018 by Paul H Alfille")
    cl.add_argument("N",help="Width of large Rectangle/Box (default 13)",type=int,nargs='?',default=13)
    cl.add_argument("-m","--maximum",help="Maximum size of tiling square allowed",type=int,nargs='?',default=None)
    return cl.parse_args()

def main(args):
    args = CommandLine() # Get args from command line

    sq = SquareComponents( 100 )
    for i in range( 1, SquareComponents.size ):
        print( sq.SqComp(i) )
    
    """
    if args.N > 0:
        N = args.N
        if args.maximum:
            maximum = args.maximum
            if maximum >= N or maximum < 1:
                maximum = N-1
            #print("Maximum tile size {:d}x{:d}".format.maximum.maximum))
        else:
            maximum = N-1
        s = LeastSquares( N,maximum )
    """
    return 0

if __name__ == '__main__':
    import sys
    import argparse # for parsing the command line
    
    sys.exit(main(sys.argv))
