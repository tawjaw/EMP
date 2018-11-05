import copy
from EMP.EMP import _rotate, _validPiece, _emptyPiece, _pieceMatch, _removePiece, _nextPosition, _combinePieces, _addCombinedPiece, _findUnassignedNeighbours

class BTFC:
    
    def __init__(self, pieces, grid, EMPType='S', compBudget=None):
        if EMPType not in ['S']:
            raise AssertionError("EMPType "+EMPType+" not defined.")

        if type(pieces) != list: raise AssertionError("pieces should be a list.")
        if type(grid) == tuple:
            # create the grid with -2 for colors
            if(EMPType == 'S'):
                grid=[[[ -2 for x in range(4)]for y in range(grid[0])] for p in range(grid[1])]
            
        elif type(grid) != list: raise AssertionError("grid should be a tuple or list.")
        
        self.pieces = pieces
        self.grid = grid
        self.EMPType = EMPType
        self.solution = None
        #self.rotate = rotate
        self.combinedPieces = _combinePieces(self.pieces, rotate=False)
        self.compCost = 0
        self.bestSolution = None
        self.bestLevel = 0
        self.compBudget = compBudget
        self._searchLevel = 0
    
    def _isEmptyDomainFC(self, position):
        unassignedNeighbours = _findUnassignedNeighbours(self.grid, position)
        emptyDomain = False
        for n in unassignedNeighbours:
            empty = True
            for piece in self.combinedPieces:
                if piece[1] > 0:
                    if self.compBudget != None and self.compCost >= self.compBudget:
                        return False
                    self.compCost = self.compCost + 1
                    if _pieceMatch(self.grid, piece[0], n, EMPType=self.EMPType):
                        empty = False
                        break
            emptyDomain = emptyDomain or empty
        return emptyDomain





    def search(self, position=[0,0]):
        if position == False:
            return True

        pos = list(position)
        for piece in self.combinedPieces:
            if piece[1] > 0:    
                if self.compBudget != None and self.compCost >= self.compBudget:
                    return False
                self.compCost = self.compCost + 1

                if _pieceMatch(self.grid, piece[0], pos, EMPType=self.EMPType):


                    self.grid[pos[0]][pos[1]] = piece[0]
                    if piece[1] > 0: 
                        piece[1] -= 1
                        if self.compBudget != None:
                            self._searchLevel += 1
                            if(self._searchLevel > self.bestLevel):
                                self.bestSolution = copy.deepcopy(self.grid)
                                self.bestLevel = self._searchLevel

                    
                    else: raise Exception("piece not in list to remove")
                 
                    if not self._isEmptyDomainFC(pos) and self.search(position=_nextPosition(self.grid, pos)):
                        return True
                    else:
                        piece[1] += 1
                        self.grid[pos[0]][pos[1]] = [-2, -2, -2, -2]
                        if self.compBudget != None:
                            self._searchLevel -= 1


        return False