import random
import copy
from EMP.EMP import isCorrect, _rotate, _validPiece

class Random:
    
    def __init__(self, pieces, grid, EMPType='SF', rotate=True, seed=None):
        if EMPType not in ['SF','S']:
            raise AssertionError("EMPType "+EMPType+" not defined.")


        if type(grid) == tuple:
            # create the grid with None for colors
            if(EMPType == 'SF' or EMPType == 'S'):
                grid=[[[ None for x in range(4)]for y in range(grid[0])] for p in range(grid[1])]
            
        elif type(grid) != list: raise AssertionError("grid should be a tuple or list.")

        if seed == None: seed = random.randint(0,1000000)
        if type(seed) != int: raise AssertionError("seed must be an int.")
        
        self.pieces = pieces
        self.grid = grid
        self.EMPType = EMPType
        self.solution = None
        self.rotate = rotate
        self.seed = seed
    
    def search(self):
        random.seed(self.seed)
        i = 0

        while self.solution == None:
            
            pieces = copy.deepcopy(self.pieces)
            grid = copy.deepcopy(self.grid)
            random.shuffle(pieces)

            if self.rotate:
                for piece in pieces: 
                    piece[:] = _rotate(piece, random.randint(0,3))

            for idxRow, row in enumerate(grid):
                for idxPiece, piece in enumerate(row):
                    if _validPiece(piece):
                        piece[:] = pieces.pop(0)
            
            if isCorrect(grid, EMPType=self.EMPType):
                print("correct")
                self.solution = grid
            
    
        

        


        