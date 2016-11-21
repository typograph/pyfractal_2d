"""
We assume that every step preserves continuity,
that is all stepmatrices in a row has same height.
and all stepmatrices in a column have the same width.

We assume that there are no cases when the same colors
expand to different matrices.

The color None expands to the smallest possible None matrix.
"""

from numpy import array, zeros

class StepMatrix:
    
    colors = {}

    @classmethod
    def add_color(cls, color, stepmatrix):
        cls.colors[color] = stepmatrix
    
    def __init__(self, matrix):
        self.matrix = array(matrix, dtype="u1")
        self.W, self.H = self.matrix.shape
        self.__array_interface__ = self.matrix.__array_interface__
        
        self.widths = None
        self.heights = None
        
    def upsize(self):
        """Calculate the size on next step.
        
        This checks if the sizes of all component matrices match 
        """
        if self.widths is not None and self.heights is not None:
            return
        
        self.widths = [None]*self.W
        self.heights = [None]*self.H
        
        for x, row in enumerate(self.matrix):
            for y, cell in enumerate(row):
                if cell not in self.colors:
                    raise ValueError("No expansion rule for color {}".format(cell))
                elif self.colors[cell] is not None:
                    if self.widths[y] is None:
                        self.widths[y] = self.colors[cell].W
                    elif self.widths[y] == self.colors[cell].W:
                        pass
                    else:
                        raise ValueError("Cell {}@({},{}) expands to W={}, that is already occupied".format(cell, x, y, self.colors[cell].W))
                    
                    if self.heights[x] is None:
                        self.heights[x] = self.colors[cell].H
                    elif self.heights[x] == self.colors[cell].H:
                        pass
                    else:
                        raise ValueError("Cell {}@({},{}) expands to H={}, that is already occupied".format(cell, x, y, self.colors[cell].H))
                    
        for y, w in enumerate(self.widths):
            if w is None:
                raise ValueError("Row {} expands to None".format(y))
        for x, h in enumerate(self.heights):
            if h is None:
                raise ValueError("Column {} expands to None".format(x))
    
    def expand(self):
        self.upsize()
        
        # New empty matrix
        matrix = zeros((sum(self.widths), sum(self.heights)))
        
        i, j = 0, 0
        for x, row in enumerate(self.matrix):
            for y, cell in enumerate(row):
                ww, hh = 0, 0
                if cell is None: # Everything is already None
                    hh = self.heights[x]
                    ww = self.widths[y]
                elif cell not in self.colors or self.colors[cell] is None:
                    raise ValueError("Cannot expand cell {}@({},{})".format(cell, x, y))
                else:
                    nstep = self.colors[cell]
                    ww, hh = nstep.W, nstep.H
                    matrix[i:i+ww, j:j+hh] = nstep
                i += ww
            i = 0
            j += hh
        
        return StepMatrix(matrix)
    
    @classmethod
    def expand_all(cls):
        expanded_colors = {}
        for c in cls.colors:
            expanded_colors[c] = cls.colors[c].expand()
        cls.colors = expanded_colors

class NoneMatrix(StepMatrix):
    def __init__(self, W, H):
        self.matrix = [[None]*W for i in range(H)]

if __name__ == "__main__":

    from PIL import Image, ImagePalette
    import sys
    
    if len(sys.argv) < 2:
        print("Please supply a filename")
        quit()

    if len(sys.argv) > 2:
        n = int(sys.argv[2])
    else:
        n = 3

    A, B, C = 0, 1, 2

    StepMatrix.add_color(A, StepMatrix([[A, A, A],
                                        [A, C, A],
                                        [A, A, A]]))
    
    StepMatrix.add_color(B, StepMatrix([[A, B, A],
                                        [B, C, B],
                                        [A, B, A]]))
    
    StepMatrix.add_color(C, StepMatrix([[C, C, C],
                                        [C, B, C],
                                        [C, C, C]]))

    for i in range(n-1):
        StepMatrix.expand_all()

    #print()
    #print(StepMatrix.colors[1].matrix)
    #print(q1.expand().expand().expand().expand().expand().W)

    #quit()
    
    fractal = Image.fromarray(StepMatrix.colors[0].expand().matrix, "P")
    
    #mtr = StepMatrix.colors[0].expand().matrix
    
    #fractal = Image.new("P", mtr.shape)
    #for x, row in enumerate(mtr):
        #for y, cell in enumerate(row):
            #fractal.putpixel((x, y), cell)
    
    
    palette = ImagePalette.ImagePalette()
    palette.getcolor((0, 0, 0))
    palette.getcolor((255, 255, 255))
    palette.getcolor((0, 0, 255))
    fractal.putpalette(palette)
    fractal.save(sys.argv[1])
