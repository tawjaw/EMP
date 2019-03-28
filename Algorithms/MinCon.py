import random
from random import shuffle
import time
from EMP.EMP import _isCorrectWithCompCost
import copy
class MinCon:

    def __init__(self, pieces, grid, EMPType='S', rotate=False, compBudget=None, maxIterations=None, maxTime=None):
        #for now only have type S, nothing special for type SF
        if EMPType not in ['S']:
            raise AssertionError("EMPType "+EMPType+" not defined.")

        if type(pieces) != list: raise AssertionError("pieces should be a list.")
        if type(grid) == tuple:
            # create the grid with -2 for colors
            grid=[[[ -2 for x in range(4)]for y in range(grid[0])] for p in range(grid[1])]
            
        elif type(grid) != list: raise AssertionError("grid should be a tuple or list.")
        #for now rotate is not available. 
        if rotate: raise AssertionError("Rotation is not implemented yet.")

        self.pieces = pieces #store the pieces
        self.grid = grid    #the grid will be used in search 
        self.EMPType = EMPType  #type of puzzle
        self.rotate = rotate    #if rotate allowed
        self.compCost = 0   #computational cost of the search
        self.perfectSolution = None    #True if a perfect solution is found
        self.compBudget = compBudget    #Computational cost budget that should stop the search if exceeded
        self.maxIterations = maxIterations  #maximum number of iterational for minConflict 
        self.iterations = 0     #Number of iterations used in the search 
        self.size = len(grid[0])    #size of the EMP assuming SxS size for now. No custom sizes.
        self.maxTime = maxTime  #Maximum time in minutes
        
    def search(self):
        if self.maxTime != None:    self.startTime = time.time()
        shuffle(self.pieces)
        #Assign pieces to grid randomly
        piece=0
        for idxrow, row in enumerate(self.grid):
            for idxpos, position in enumerate(row):
                #print()
                self.grid[idxrow][idxpos] = list(self.pieces[piece])
                piece+=1
        checkPF = False
        while not self.perfectSolution:
            #check constraints to return
            if self.compBudget!= None and self.compCost > self.compBudget: return False
            if self.maxIterations!= None and self.iterations > self.maxIterations: return False
            if self.maxTime != None and (time.time()-self.startTime)/60 > self.maxTime: return False

            #if checkPS, check if the solution of the grid is perfect
            if checkPF:
                PS, CC = _isCorrectWithCompCost(self.grid, EMPType=self.EMPType)
                #print("checkPF")
                #print(PS)
                #print(CC)
                #print(str(self.iterations))
                self.compCost+=CC
                if PS: 
                    self.perfectSolution = copy.deepcopy(self.grid)
                    return True
                else: checkPF = False
            self.iterations+=1  #increment number of iterations
            #select a random piece
            x = random.randint(0, self.size-1)
            y = random.randint(0, self.size-1)

            #Find all the conflicts between the randomly 
            #selected piece and the all the other pieces
            conflicts = [[ -1 for y in range(self.size)] for p in range(self.size)]
            for idxrow, row in enumerate(self.grid):
                for idxpos, position in enumerate(row):
                    conflicts[idxrow][idxpos] = self._conflict((x,y),(idxpos, idxrow))

            #find all the minimum conflicts
            minimum = min(min(r) for r in conflicts)
            minConflict = list()
            for idxrow, row in enumerate(conflicts):
                for idxpos, conf in enumerate(row):
                    if conf == minimum: minConflict.append((idxrow,idxpos))
            #choose one by random if multiple have minimum conflicts
            pieceToSwap = random.choice(minConflict)

            #do the swap
            self.grid[y][x], self.grid[pieceToSwap[0]][pieceToSwap[1]] = self.grid[pieceToSwap[0]][pieceToSwap[1]], self.grid[y][x]
            if minimum == 0: 
                #print("minimum = 0")
                checkPF = True
    
    def _conflict(self,pos1, pos2):
        #get the conflict if piece at x1,y1 and piece at x2,y2
        #are swapped
        #conflict = number of not matching edges 
        x1 = pos1[0]
        y1 = pos1[1]
        x2 = pos2[0]
        y2 = pos2[1]
        #add 2 computational cost as we are checking the constraint of a piece twice
        self.compCost+=2
        #Calculate conflict for piece 1 in place of piece 2
        conflict1 = 0
        #left edge
        if not(x2 == 0):
            if self.grid[y1][x1][0] != self.grid[y2][x2-1][2]: conflict1 += 1
        #top edge
        if not(y2 == 0):
            if self.grid[y1][x1][1] != self.grid[y2-1][x2][3]: conflict1 += 1
        #right edge
        if not(x2 == self.size-1):
            if self.grid[y1][x1][2] != self.grid[y2][x2+1][0]: conflict1 += 1
        #bottom edge
        if not(y2 == self.size-1):
            if self.grid[y1][x1][3] != self.grid[y2+1][x2][1]: conflict1 += 1

        #Calculate conflict for piece 2 in place of piece 1
        conflict2 = 0
        #left edge
        if not(x1 == 0):
            if self.grid[y2][x2][0] != self.grid[y1][x1-1][2]: conflict2 += 1
        #top edge
        if not(y1 == 0):
            if self.grid[y2][x2][1] != self.grid[y1-1][x1][3]: conflict2 += 1
        #right edge
        if not(x1 == self.size-1):
            if self.grid[y2][x2][2] != self.grid[y1][x1+1][0]: conflict2 += 1
        #bottom edge
        if not(y1 == self.size-1):
            if self.grid[y2][x2][3] != self.grid[y1+1][x1][1]: conflict2 += 1

        return conflict1+conflict2

        