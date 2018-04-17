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

""" _f version
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

class Globals:
    """ Global parameters """
    show = False # Show graphically
    maximum = None # maximum size of inset square
    quiet = 0 # Quiet state
    # 0 show everything
    # 1 no intermediates
    # 2 no solution (just solution number)
    # 3 CVS output: sides,solution number,visited,time
        
class Draw:
    side = 10
    N = None # X side
    M = None # Y side
    Xmax = 4
    Ymax = 3
    Current = -1
    win = None
    textheight = 20
    textfont = 14
    
    def __init__( self, N, M ):
        """ N for number of squares N*M """
        segmentX = Draw.side*(N+1)
        segmentY = Draw.side*(M+1)+Draw.textheight

        Draw.win = GraphWin( "Square filling for {:d}X{:d}  (max tile {:d}X{:d})".format(N,M,Globals.maximum,Globals.maximum),segmentX*Draw.Xmax+Draw.side,segmentY*Draw.Ymax+Draw.side)

        Draw.N = N
        Draw.M = M

    def Show( self, sqlist ):
        Draw.Current += 1

        indexX = Draw.Current % Draw.Xmax
        indexY = int (Draw.Current / Draw.Xmax ) % Draw.Ymax

        thisX = indexX * Draw.side * (Draw.N+1)
        thisY = indexY * (Draw.side * (Draw.M+1) + Draw.textheight )

        for s in sqlist:
            x = Draw.side*(s.x+1)+thisX
            y = Draw.side*(s.y+1)+thisY

            r = Rectangle(Point(x,y),Point(x+s.dx*Draw.side,y+s.dx*Draw.side))
            r.setFill(color_rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
            r.draw(Draw.win)
            
        sqtext = "{:d} tiles".format(len(sqlist))
        t = Text( Point( thisX+(Draw.side*(2+Draw.N))/2, thisY+Draw.side*(Draw.M+1)+Draw.textheight-5), sqtext )
        t.setSize(Draw.textfont)
        t.setFace("times roman")
        t.setFill("black")
        t.draw(Draw.win) 

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
        
    def mirror(self):
        """Square made by flipping on diagonal axis"""
        return Square(self.y,self.x,self.dx)
        
    def string( self):
        return "< {:d}x{:d}-{:d} >".format(self.x,self.y,self.dx)

class Cube:
    """Holds x,y,z and dx=side length"""
    def __init__( self, x, y, z, dx ):
        self.x = x
        self.y = y
        self.z = z
        self.dx = dx
        
    def disjoint( self, other ):
        """Do the squares not overlap at all?"""
        if self.x >= other.x + other.dx:
            return True
        elif self.y >= other.y + other.dx:
            return True
        elif self.z >= other.z + other.dx:
            return True
        elif other.x >= self.x + self.dx:
            return True
        elif other.y >= self.y + self.dx:
            return True
        elif other.z >= self.z + self.dx:
            return True
        else:
            return False
            
    def differentstart( self, other ):
        """ Upper left corner different?"""
        return self.x!=other.x or self.y!=other.y or self.z!=other.z
            
    def size( self ):
        return self.dx * self.dx * self.dx
        
    def string( self):
        return "< {:d}x{:d}x{:d}-{:d} >".format(self.x,self.y,self.z,self.dx)

class Tiling:
    """ Holds the current position"""
    MinMoves = None
    Size = None
    SideX = None
    SideY = None
    BestSoFar=[]
    BestTime = None
    Draw=None
    visited = 0

    def __init__( self, dim ):
        if isinstance(dim,Tiling):
            # Child Tiling state
            Tiling.visited += 1
            parent = dim
            self.nmoves = parent.nmoves + 1
            if self.nmoves >= Tiling.MinMoves:
                raise PruneError

            active_sq   = parent.sqlist[0]

            # Test corners
            if active_sq.x+active_sq.dx == Tiling.SideX:
                # Right edge
                if active_sq.y == 0 or active_sq.y+active_sq.dx == Tiling.SideY:
                    if active_sq.dx > parent.Moves[0].dx:
                        raise PruneError
            elif active_sq.x == 0:
                # Left edge
                if active_sq.y+active_sq.dx == Tiling.SideY:
                    if active_sq.dx > parent.Moves[0].dx:
                        raise PruneError

            self.Moves = parent.Moves+[active_sq]
            self.coverage = parent.coverage - active_sq.size()
            #print(active_sq  .string(),self.nmoves,self.coverage)
            if self.coverage == 0:
                # New best
                Tiling.MinMoves = self.nmoves
                Tiling.BestSoFar = self.Moves[:]
                Tiling.BestTime = time.process_time() # time of best solution
                if Globals.quiet == 0:
                    self.BestShow()
            else:
                if Tiling.LeastSquares[self.coverage] + self.nmoves +2 > Tiling.MinMoves:
                    # Can we get coverage in minimal moves?
                    raise PruneError
                if parent.symmetry:
                    # still possibly symmetric
                    if active_sq.x > active_sq.y:
                        # upper right diagonal
                        if active_sq.y + active_sq.dx > active_sq.x:
                            # crosses diagonal
                            self.sqlist = [ m for m in parent.sqlist[1:] if active_sq.disjoint(m) ]
                            self.symmetry = False
                        else:
                            # prune mirror
                            self.sqlist = [ m for m in parent.sqlist[1:] if active_sq.disjoint(m) and ( active_sq.y != m.x or active_sq.x != m.y or active_sq.dx >= m.dx ) ]
                            self.symmetry = True
                    elif active_sq.x < active_sq.y:
                        # Lower left diagonal -- find mirror and test if size matches
                        self.sqlist = [ m for m in parent.sqlist[1:] if active_sq.disjoint(m) ]
                        self.symmetry = False
                        for m in parent.Moves:
                            if active_sq.x == m.y and active_sq.y == m.x:
                                self.symmetry = (active_sq.dx == m.dx)
                                break ; 
                    else:
                        # On diagonal, just pass on symmetry state
                        self.sqlist = [ m for m in parent.sqlist[1:] if active_sq.disjoint(m) ]
                        self.symmetry = True
                else:
                    # already assymetric
                    self.sqlist = [ m for m in parent.sqlist[1:] if active_sq.disjoint(m) ]
                    self.symmetry = parent.symmetry

                #self.SqlistShow()
                self.TryAll()
        else:
            # initial Tiling state
            sx = dim[0]
            sy = dim[1]

            # set class vars
            Tiling.SideX = sx
            Tiling.SideY = sy
            Tiling.MinMoves = sx * sy
            Tiling.Size = sx * sy
            if Globals.show:
                Tiling.Draw = Draw(sx,sy)
            Tiling.BestSoFar = [ Square(x,y,1) for x in range( sx ) for y in range( sy ) ]
            if not Globals.maximum:
                Globals.maximum = min( sx-1, sy-1 )            
            self.LeastSquares( sx+4-Globals.maximum )

            # Base Tiling state
            self.nmoves = 0
            self.Moves = []
            self.coverage = Tiling.Size
            self.sqlist = self.Sqlist_rankorder()
            # assume symmetric until assymatric element found (or uneven sides)
            self.symmetry = ( sx == sy ) 
            
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
            if Globals.maximum > h:
                r = [ Square(0,0,dx) for dx in range( min(Globals.maximum,sx-1),h,-1 ) ]+[ Square(x,y,dx) for x in range( sx ) for y in range( sy ) for dx in range( max(min(h,sx-x,sy-y,Globals.maximum), 1 ),0,-1 ) ]
            else:
                r = [ Square(x,y,dx) for x in range( sx ) for y in range( sy ) for dx in range( max(min(Globals.maximum,h,sx-x,sy-y), 1 ),0,-1 ) ]
            return [ m for m in r if m.x != 0 or m.y != 0 or m.dx != 1 ]
        else:
            return [ Square(x,y,dx) for x in range( sx ) for y in range( sy ) for dx in range( max(1, min(Globals.maximum,sx-x,sy-y,sx-1,sy-1)),0,-1 ) ]
            
    def LeastSquares( self, size ):
        """ Create a list of minimum nuber of squares that add up to that number """
        max_remain = Tiling.Size - 4
        trials = set( [i for i in range(1,max_remain+1) ] )

        # Worst case
        Tiling.LeastSquares = [ size for i in range( max_remain+1 ) ]

        sq_try = [ sq*sq for sq in range(1,Globals.maximum+1)]
        last_set = set(sq_try)
        for i in last_set:
            Tiling.LeastSquares[i] = 0

        for moves in range(1,size):
            last_set = set([ i+sq for i in last_set for sq in sq_try if i+sq <= max_remain ])
            for i in last_set:
                Tiling.LeastSquares[i] = min( Tiling.LeastSquares[i], moves )
        
        
    @staticmethod
    def BestShow( ):
        print( Tiling.MinMoves," ".join([m.string() for m in Tiling.BestSoFar]) )
        if Globals.show:
            Tiling.Draw.Show( Tiling.BestSoFar )
                
    @staticmethod
    def Report():
        time_solve = time.process_time()
        check_frac = Tiling.BestTime/time_solve
        if Globals.quiet == 1:
            Tiling.BestShow()
        if Globals.quiet < 3:
            print("Fewest squares for {:d}x{:d} = {:d}  Trials={:d} Time={:f} Solve/Check={:4.2f}".format(Tiling.SideX,Tiling.SideY,Tiling.MinMoves,Tiling.visited,time_solve,check_frac))
        else:
            print("{:d},{:d},{:d},{:d},{:f},{:4.2f}".format(Tiling.SideX,Tiling.SideY,Tiling.MinMoves,Tiling.visited,time_solve,check_frac))

class Filling:
    """ Holds the current position"""
    MinMoves = None
    Size = None
    SideX = None
    SideY = None
    SideZ = None
    BestSoFar=[]
    visited = 0

    def __init__( self, dim ):
        if isinstance(dim,Filling):
            # Child Filling state
            Filling.visited += 1
            parent = dim
            self.nmoves = parent.nmoves + 1
            if self.nmoves >= Filling.MinMoves:
                raise PruneError
            s = parent.sqlist[0]

            self.Moves = parent.Moves+[s]
            self.coverage = parent.coverage - s.size()
            #print(s.string(),self.nmoves,self.coverage)
            if self.coverage == 0:
                # New best
                Filling.MinMoves = self.nmoves
                Filling.BestSoFar = self.Moves[:]
                if Globals.quiet == 0:
                    self.BestShow()
            else:
                if self.coverage not in Filling.cubes and self.nmoves == Filling.MinMoves - 1:
                    # non square number of empties. At least 2 more needed
                    raise PruneError
                self.sqlist = [ m for m in parent.sqlist[1:] if s.disjoint(m) ]
                #self.SqlistShow()
                self.TryAll()
        else:
            # initial Filling state
            sx = dim[0]
            sy = dim[1]
            sz = dim[2]

            # set class vars
            Filling.SideX = sx
            Filling.SideY = sy
            Filling.SideZ = sz
            Filling.MinMoves = sx * sy * sz
            Filling.Size = sx * sy * sz
            Filling.cubes = set( [x*xX for x in range(1,max(sx,sy,sz))])
            Filling.BestSoFar = [ Cube(x,y,z,1) for x in range( sx ) for y in range( sy ) for z in range( sz ) ]
            if not Globals.maximum:
                Globals.maximum = min( sx-1, sy-1 , sz-1 )

            # Base Filling state
            self.nmoves = 0
            self.Moves = []
            self.coverage = Filling.Size
            self.sqlist = self.Sqlist_rankorder()
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
                Filling( self )
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
        sx = Filling.SideX
        sy = Filling.SideY
        sz = Filling.SideZ
        if sx == 1:
            return []
        elif sy == 1:
            return []
        elif sz == 1:
            return []
        elif sx == sy and sx == sz:
            # Cube 
            h = max( int(sx/2) , 1 )
            if Globals.maximum > h:
                return [ Cube(0,0,0,dx) for dx in range( min(Globals.maximum,sx-1),h,-1 ) ]+[ Cube(x,y,z,dx) for x in range( sx ) for y in range( sy ) for z in range( sz ) for dx in range( max(min(h,sx-x,sy-y,sz-z,Globals.maximum), 1 ),0,-1 ) ]
            else:
                return [ Cube(x,y,z,dx) for x in range( sx ) for y in range( sy ) for z in range( sz ) for dx in range( max(min(Globals.maximum,h,sx-x,sy-y,sz-z), 1 ),0,-1 ) ]

        else:
            return [ Cube(x,y,z,dx) for x in range( sx ) for y in range( sy ) for z in range( sz ) for dx in range( max(1, min(Globals.maximum,sx-x,sy-y,sz-z,sx-1,sy-1,sz-1)),0,-1 ) ]
        
    @staticmethod
    def BestShow( ):
        print( Filling.MinMoves," ".join([m.string() for m in Filling.BestSoFar]) )
        
    @staticmethod
    def Report():
        if Globals.quiet == 1:
            Filling.BestShow()
        if Globals.quiet < 2:
            print("Fewest cubes for {:d}x{:d}x{:d} = {:d}  Trials={:d} Time={:f}".format(Filling.SideX,Filling.SideY,Filling.SideZ,Filling.MinMoves,Filling.visited,time.proceess_time()))
        else:
            print("{:d},{:d},{:d},{:d},{:d},{:f}".format(Filling.SideX,Filling.SideY,Filling.SideZ,Filling.MinMoves,Filling.visited,time.proceess_time()))
        

def CommandLine():
    """Setup argparser object to process the command line"""
    cl = argparse.ArgumentParser(description="Fit Squares in large Rectangle or Box) -- find fewest needed. 2018 by Paul H Alfille")
    cl.add_argument("N",help="Width of large Rectangle/Box (default 13)",type=int,nargs='?',default=13)
    cl.add_argument("M",help="Height of large Rectangle/Box (default Square)",type=int,nargs='?',default=None)
    cl.add_argument("O",help="Depth of large Box (default Cube)",type=int,nargs='?',default=None)
    cl.add_argument("-m","--maximum",help="Maximum size of tiling square allowed",type=int,nargs='?',default=None)
    cl.add_argument("-s","--show",help="Show the solutions graphically",action="store_true")
    cl.add_argument("-3","--cube",help="3-D solution -- cubes in box",action="store_true")
    cl.add_argument("-q","--quiet",help="Suppress more and more displayed info (can be repeated)",action="count")
    return cl.parse_args()

def main(args):
    args = CommandLine() # Get args from command line

    if args.show:
        Globals.show = True
    if args.quiet:
        Globals.quiet = args.quiet
    
    if args.N > 0:
        N = args.N
        if not args.M:
            M = N
        elif args.M < 1:
            M = N
        else:
            M = args.M
        dim = (N,M)
        if args.maximum:
            Globals.maximum = args.maximum
            if Globals.maximum >= N or Globals.maximum >= M or Globals.maximum < 1:
                Globals.maximum = min(N,M)-1
            print("Maximum tile size {:d}x{:d}".format(Globals.maximum,Globals.maximum))
        else:
            Globals.maximum = min(N,M)-1
        if not args.cube:
            s = Tiling( dim )
            Tiling.Report()
            if Globals.show:
                Tiling.Draw.win.getMouse()
                Tiling.Draw.win.close()
        else:
            # 3-D
            if not args.O:
                O = M
            elif args.O < 1:
                O = M
            else:
                O = args.O
            dim = (N,M,O)
            s = Filling( dim )
            Filling.Report()
    return 0

if __name__ == '__main__':
    import sys
    import argparse # for parsing the command line
    from graphics import *
    import random
    
    sys.exit(main(sys.argv))
