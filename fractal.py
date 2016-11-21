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
    """A fractal structure that knows its matrix at every step.
    
    The StepMatrix is constructed from a 2D integer numpy array,
    and uses the internal __color__ table at each step to
    construct the next one. Zero always expands to itself.
    """
    
    colors = {}

    @classmethod
    def add_color(cls, stepmatrix):
        """Adds a color to the expansion and return its index.
        """
        if cls.colors:
            i = max(cls.colors.keys())
        else:
            i = 0
        cls.colors[i+1] = stepmatrix
        return i+1
    
    def __init__(self, matrix):
        self.depths = [ array(matrix, dtype="u1") ]        
        self.__array_interface__ = self.depths[0].__array_interface__
        self.clset = {cell for row in self.depths[0] for cell in row}

    def at_depth(self, n):
        """Returns the matrix after `n` substitutions.
        
        The result is cached.
        """
        if len(self.depths) <= n:
            self.depths.extend([None]*(n-len(self.depths)+1))
        if self.depths[n] is None:
            self.depths[n] = self.expand(n)
        return self.depths[n]
            
    def expand(self, n):
        """Calculates the matrix after `n` substitutions.
        """
        
        submatrices = {k:self.colors[k].at_depth(n-1) for k in self.clset if k!=0}
        
        basis = self.at_depth(0)
        
        H, W = basis.shape
        
        widths = [None]*W
        heights = [None]*H
        
        for x, row in enumerate(basis):
            for y, cell in enumerate(row):
                if cell == 0: # Zero is not expanded
                    continue
                
                hh, ww = submatrices[cell].shape
                
                if widths[y] is None:
                    widths[y] = ww
                elif widths[y] != ww:
                    raise ValueError("Cell {}@({},{}) expands to W={},"
                        " but a previous cell expanded to W={}"
                        .format(cell, x, y, ww, widths[y]))
                
                if heights[x] is None:
                    heights[x] = hh
                elif heights[x] != hh:
                    raise ValueError("Cell {}@({},{}) expands to H={}, "
                        "but a previous cell expanded to H={}"
                        .format(cell, x, y, hh, heights[x]))
                    
        if None in widths:
            raise ValueError("None encountered in column widths : {}".format(widths))
        if None in heights:
            raise ValueError("None encountered in row heights : {}".format(heights))
        
        # New empty matrix
        matrix = zeros((sum(heights), sum(widths)), dtype="u1")
        
        i, j = 0, 0
        for x, row in enumerate(basis):
            hh = heights[x]
            for y, cell in enumerate(row):
                ww = widths[y]
                if cell == 0:
                    i += ww
                    continue
                matrix[j:j+hh, i:i+ww] = submatrices[cell]
                i += ww
            i = 0
            j += hh
        
        return matrix

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

    A, B, C = 1, 2, 3

    # A
    StepMatrix.add_color(StepMatrix([[A, A, A],
                                     [A, C, A],
                                     [A, A, A]]))
    
    # B
    StepMatrix.add_color(StepMatrix([[A, B, A],
                                     [B, C, B],
                                     [A, B, A]]))
    
    # C
    StepMatrix.add_color(StepMatrix([[C, C, C],
                                     [C, B, C],
                                     [C, C, C]]))

    fractal = Image.fromarray(StepMatrix.colors[A].at_depth(n), "P")
    palette = ImagePalette.ImagePalette()
    palette.getcolor((0, 0, 0))
    palette.getcolor((10, 10, 10))
    palette.getcolor((0, 128, 0))
    palette.getcolor((0, 0, 200))
    fractal.putpalette(palette)
    fractal.save(sys.argv[1])
