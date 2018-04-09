#!/usr/bin/env python
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


class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class PruneError(Error):
    """Exception for branch too long (longer than current record).
    """

    def __init__(self):
        pass
        
class Draw:
    side = 10
    N = None # X side
    M = None # Y side
    Xmax = 6
    Ymax = 5
    Current = -1
    win = None
    
    def __init__( self, N, M ):
        """ N for number of squares N*M """
        segmentX = Draw.side*(N+1)
        segmentY = Draw.side*(M+1)

        Draw.win = GraphWin( "Square filling for {:d}X{:d}".format(N,M),segmentX*Draw.Xmax+Draw.side,segmentY*Draw.Ymax+Draw.side)

        Draw.N = N
        Draw.M = M

    def Show( self, sqlist ):
        Draw.Current += 1

        indexX = Draw.Current % Draw.Xmax
        indexY = int (Draw.Current / Draw.Xmax ) % Draw.Ymax

        thisX = indexX * Draw.side * (Draw.N+1)
        thisY = indexY * Draw.side * (Draw.M+1)

        for s in sqlist:
            x = Draw.side*(s.x+1)+thisX
            y = Draw.side*(s.y+1)+thisY

            r = Rectangle(Point(x,y),Point(x+s.dx*Draw.side,y+s.dx*Draw.side))
            r.setFill(color_rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
            r.draw(Draw.win)

        Draw.win.update()
        #Draw.win.close()
    

class Square:
    """Holds x,y, and dx=side length"""
    def __init__( self, x, y, dx ):
        self.x = x
        self.y = y
        self.dx = dx
        
    def disjoint( self, other ):
        """Do the squares not overlap at all?"""
        if self.x >= other.x + other.dx:
            return True
        elif self.y >= other.y + other.dx:
            return True
        elif other.x >= self.x + self.dx:
            return True
        elif other.y >= self.y + self.dx:
            return True
        else:
            return False
            
    def differentstart( self, other ):
        """ Upper left corner different?"""
        return self.x!=other.x or self.y!=other.y
            
    def size( self ):
        return self.dx * self.dx
        
    def string( self):
        return "< {:d}x{:d}-{:d} >".format(self.x,self.y,self.dx)

class Tiling:
    """ Holds the current position"""
    MinMoves = None
    Dim=None
    Size = None
    SideX = None
    SideY = None
    BestSoFar=[]
    Draw=None

    def __init__( self, dim, show=True, maximum=None ):
        if isinstance(dim,Tiling):
            # Child Tiling state
            parent = dim
            self.nmoves = parent.nmoves + 1
            if self.nmoves >= Tiling.MinMoves:
                raise PruneError
            s = parent.sqlist[0]

            self.Moves = parent.Moves+[s]
            self.coverage = parent.coverage + s.size()
            #print(s.string(),self.nmoves,self.coverage)
            if self.coverage == Tiling.Size:
                # New best
                Tiling.MinMoves = self.nmoves
                Tiling.BestSoFar = self.Moves[:]
                self.BestShow()
            else:
                self.sqlist = [ m for m in parent.sqlist[1:] if s.disjoint(m) ]
                #self.SqlistShow()
                self.TryAll()
        else:
            # initial Tiling state
            sx = dim[0]
            sy = dim[1]

            # set class vars
            Tiling.SideX = sx
            Tiling.SideY = sy
            Tiling.Dim = dim
            Tiling.MinMoves = sx * sy
            Tiling.Size = sx * sy
            Tiling.Show = show
            if show:
                Tiling.Draw = Draw(sx,sy)
            Tiling.BestSoFar = [ Square(x,y,1) for x in range( sx ) for y in range( sy ) ]
            if maximum:
                Tiling.maximum = maximum
                print("Maximum",maximum)
            else:
                Tiling.maximum = min( sx-1, sy-1 )

            # Base Tiling state
            self.nmoves = 0
            self.Moves = []
            self.coverage = 0
            self.sqlist = self.Sqlist_rankorder()
            #self.sqlist=[ Square(x,y,dx) for dx in range(min(int((sx+1)/2),sx-1),0,-1) for x in range(sx+1-dx) for y in range(sy+1-dx) ]
            #self.SqlistShow()
            
            # Start the recursion
            self.TryAll()

    def TryAll(self):
        """ Recursive search
        but limit to same starting stop (upper left of free spaces
        which is easy sine sqlist is sorted that way
        """
        if self.sqlist:
            index_sq = self.sqlist[0]
        while self.sqlist:
            if index_sq.differentstart( self.sqlist[0] ):
                # the upperleft choices are exhausted
                break
            try:
                Tiling( self )
            except PruneError:
                # Not optimal
                pass
            self.sqlist = self.sqlist[1:]
            
    def SqlistShow( self ):
        print( " ".join([m.string() for m in self.sqlist]) )
        
    def Sqlist_rankorder( self ):
        """ Create a list of all squares
        left->right
        top->down
        big->small
        Also, only the first square can be larger than 1/2 the size
        """
        sx = Tiling.SideX
        sy = Tiling.SideY
        if sx == 1:
            return []
        elif sy == 1:
            return []
        elif sx == sy:
            # square 
            h = max( int(sx/2) , 1 )
            if Tiling.maximum > h:
                return [ Square(0,0,dx) for dx in range( min(Tiling.maximum,sx-1),h,-1 ) ]+[ Square(x,y,dx) for x in range( sx ) for y in range( sy ) for dx in range( max(min(h,sx-x,sy-y), 1, Tiling.maximum ),0,-1 ) ]
            else:
                return [ Square(x,y,dx) for x in range( sx ) for y in range( sy ) for dx in range( max(min(Tiling.maximum,h,sx-x,sy-y), 1 ),0,-1 ) ]

        else:
            return [ Square(x,y,dx) for x in range( sx ) for y in range( sy ) for dx in range( max(1, min(Tiling.maximum,sx-x,sy-y,sx-1,sy,1)),0,-1 ) ]
        
    @staticmethod
    def BestShow( ):
        print( Tiling.MinMoves," ".join([m.string() for m in Tiling.BestSoFar]) )
        if Tiling.Show:
            Tiling.Draw.Show( Tiling.BestSoFar )
        

def CommandLine():
    """Setup argparser object to process the command line"""
    cl = argparse.ArgumentParser(description="Fit Squares in large Square (rectangle) -- find fewest needed. 2018 by Paul H Alfille")
    cl.add_argument("N",help="Width of large rectangle (default 13)",type=int,nargs='?',default=13)
    cl.add_argument("M",help="Height of large rectangle (default square)",type=int,nargs='?',default=None)
    cl.add_argument("-m","--MAX",help="Maximum size of tiling square allowed",type=int,nargs='?',default=None)
    cl.add_argument("-s","--SHOW",help="Show the solutions graphically",action="store_true")
    return cl.parse_args()


def main(args):
    args = CommandLine() # Get args from command line
    
    if args.N > 0:
        N = args.N
        if not args.M:
            M = N
        elif args.M < 1:
            M = N
        else:
            M = args.M
        dim = (N,M)
        if args.MAX:
            maximum = args.MAX
            if maximum >= N or maximum >= M or maximum < 1:
                maximum = min(N,M)-1
            print("Maximum tile size {:d}x{:d}".format(maximum,maximum))
        else:
            maximum = min(N,M)-1
        s = Tiling( dim, show=args.SHOW, maximum = maximum )
        print("Fewest squares for {:d}x{:d} = {:d}".format(N,M,Tiling.MinMoves))
        if args.SHOW:
            Tiling.Draw.win.getMouse()
            Tiling.Draw.win.close()
    return 0

if __name__ == '__main__':
    import sys
    import argparse # for parsing the command line
    from graphics import *
    import random
    
    sys.exit(main(sys.argv))
