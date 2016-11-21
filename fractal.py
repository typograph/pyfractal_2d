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
        self.depths = [ array(matrix, dtype="u1") ]        
        self.__array_interface__ = self.depths[0].__array_interface__
        self.clset = {cell for row in self.depths[0] for cell in row}

    def at_depth(self, n):
        if len(self.depths) <= n:
            self.depths.extend([None]*(n-len(self.depths)+1))
        if self.depths[n] is None:
            self.depths[n] = self.expand(n)
        return self.depths[n]
            
    def expand(self, n):
        
        submatrices = {k:self.colors[k].at_depth(n-1) for k in self.clset}
        
        basis = self.at_depth(0)
        
        H, W = basis.shape
        
        widths = [None]*W
        heights = [None]*H
        
        for x, row in enumerate(basis):
            for y, cell in enumerate(row):
                if widths[y] is None:
                    widths[y] = submatrices[cell].shape[1]
                elif widths[y] != submatrices[cell].shape[1]:
                    raise ValueError("Cell {}@({},{}) expands to W={},"
                        " but a previous cell expanded to W={}"
                        .format(cell, x, y, submatrices[cell].shape[1], widths[y]))
                
                if heights[x] is None:
                    heights[x] = submatrices[cell].shape[0]
                elif heights[x] != submatrices[cell].shape[0]:
                    raise ValueError("Cell {}@({},{}) expands to H={}, "
                        "but a previous cell expanded to H={}"
                        .format(cell, x, y, submatrices[cell].shape[0], heights[x]))
                    
        if None in widths:
            raise ValueError("None encountered in column widths : {}".format(widths))
        if None in heights:
            raise ValueError("None encountered in row heights : {}".format(heights))
        
        # New empty matrix
        matrix = zeros((sum(widths), sum(heights)), dtype="u1")
        
        i, j = 0, 0
        for x, row in enumerate(basis):
            for y, cell in enumerate(row):
                nstep = submatrices[cell]
                hh, ww = nstep.shape
                matrix[j:j+hh, i:i+ww] = nstep
                i += ww
            i = 0
            j += hh
        
        return matrix
    
    #@classmethod
    #def expand_all(cls):
        #expanded_colors = {}
        #for c in cls.colors:
            #expanded_colors[c] = cls.colors[c].expand()
        #cls.colors = expanded_colors

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

    fractal = Image.fromarray(StepMatrix.colors[A].at_depth(n), "P")
    palette = ImagePalette.ImagePalette()
    palette.getcolor((0, 0, 0))
    palette.getcolor((255, 255, 255))
    palette.getcolor((0, 0, 255))
    fractal.putpalette(palette)
    fractal.save(sys.argv[1])
