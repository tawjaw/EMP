import copy
from EMP.EMP import _rotate, _validPiece, _emptyPiece, _pieceMatch, _removePiece, _nextPosition, _combinePieces, _addCombinedPiece

class BT:
    
    def __init__(self, pieces, grid, EMPType='SF', rotate=True):
        if EMPType not in ['SF','S']:
            raise AssertionError("EMPType "+EMPType+" not defined.")

        if type(pieces) != list: raise AssertionError("pieces should be a list.")
        if type(grid) == tuple:
            # create the grid with None for colors
            if(EMPType == 'SF' or EMPType == 'S'):
                grid=[[[ -2 for x in range(4)]for y in range(grid[0])] for p in range(grid[1])]
            
        elif type(grid) != list: raise AssertionError("grid should be a tuple or list.")
        
        self.pieces = pieces
        self.grid = grid
        self.EMPType = EMPType
        self.solution = None
        self.rotate = rotate
        self.combinedPieces = _combinePieces(self.pieces, rotate=self.rotate)
    
    def search(self, position=[0,0]):
        if position == False:
            return True

        pos = list(position)
        #tempPieces = copy.deepcopy(self.combinedPieces)
        #print(self.combinedPieces)
        for piece in self.combinedPieces:
            if piece[1] > 0:
                if self.rotate:
                    for i in range(4):
                        piece[0] = _rotate(piece[0], 1)
                        
                        if _pieceMatch(self.grid, piece[0], pos, EMPType=self.EMPType):
                            self.grid[pos[0]][pos[1]] = piece[0]
                            if piece[1] > 0: 
                                piece[1] -= 1
                            else: raise Exception("piece not in list to remove")

                            if self.search(position=_nextPosition(self.grid, pos)):
                                return True
                            else:                               
                                piece[1] += 1
                                self.grid[pos[0]][pos[1]] = [-2, -2, -2, -2]
                else:
                    if _pieceMatch(self.grid, piece[0], pos, EMPType=self.EMPType):
                        self.grid[pos[0]][pos[1]] = piece[0]
                        if piece[1] > 0: 
                            piece[1] -= 1
                        else: raise Exception("piece not in list to remove")
                        if self.search(position=_nextPosition(self.grid, pos)):
                            return True
                        else:
                            piece[1] += 1
                            self.grid[pos[0]][pos[1]] = [-2, -2, -2, -2]
        return False
    
"""
class BT:
    
    def __init__(self, pieces, grid, EMPType='SF', rotate=True):
        if EMPType not in ['SF','S']:
            raise AssertionError("EMPType "+EMPType+" not defined.")


        if type(grid) == tuple:
            # create the grid with None for colors
            if(EMPType == 'SF' or EMPType == 'S'):
                grid=[[[ -2 for x in range(4)]for y in range(grid[0])] for p in range(grid[1])]
            
        elif type(grid) != list: raise AssertionError("grid should be a tuple or list.")
        
        self.pieces = pieces
        self.grid = grid
        self.EMPType = EMPType
        self.solution = None
        self.rotate = rotate
    
    def search(self, position=[0,0]):
        if position == False:
            return True

        pos = list(position)
        tempPieces = copy.deepcopy(self.pieces)
        for piece in tempPieces:
            if self.rotate:
                for i in range(4):
                    piece[:] = _rotate(piece, 1)
                    if _pieceMatch(self.grid, piece, pos, EMPType=self.EMPType):
                        self.grid[pos[0]][pos[1]] = piece
                        _removePiece(piece, self.pieces, rotate=self.rotate)
                        if self.search(position=_nextPosition(self.grid, pos)):
                            return True
                        else:
                            self.pieces.append(self.grid[pos[0]][pos[1]])
                            self.grid[pos[0]][pos[1]] = [-2, -2, -2, -2]
            else:
                if _pieceMatch(self.grid, piece, pos, EMPType=self.EMPType):
                    self.grid[pos[0]][pos[1]] = piece
                    _removePiece(piece, self.pieces, rotate=self.rotate)
                    if self.search(position=_nextPosition(self.grid, pos)):
                        return True
                    else:
                        self.pieces.append(self.grid[pos[0]][pos[1]])
                        self.grid[pos[0]][pos[1]] = [-2, -2, -2, -2]
        return False
    """