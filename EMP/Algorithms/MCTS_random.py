import copy
import math
from graphviz import Digraph
from EMP.EMP import _rotate, _validPiece, _emptyPiece, _pieceMatch, _removePiece, _nextPosition, _combinePieces, _addCombinedPiece
from EMP.EMP import drawPuzzle, generatePuzzle, isCorrect
import random
dot = Digraph(comment='The Round Table')

class Node:
    def __init__(self):
        self.parent   = 'NaN'
        self.children = []
        self.score    = 0
        self.n        = 0
        self.value    = []
        self.ucb      = 0.0

class MCTS:

    def __init__(self, pieces, grid, EMPType='SF', rotate=True,parm=0):
        if EMPType not in ['SF','S']:
            raise AssertionError("EMPType "+EMPType+" not defined.")

        if type(pieces) != list: raise AssertionError("pieces should be a list.")
        if type(grid) == tuple:
            # create the grid with None for colors
            if(EMPType == 'SF' or EMPType == 'S'):
                grid=[[[ -2 for x in range(4)]for y in range(grid[0])] for p in range(grid[1])]

        elif type(grid) != list: raise AssertionError("grid should be a tuple or list.")

        self.parm = parm
        self.pieces = pieces
        self.grid = grid
        self.EMPType = EMPType
        self.solution = None
        self.rotate = rotate
        self.combinedPieces = _combinePieces(self.pieces, rotate=self.rotate)

        #print ("To begin with the available pieces")
        #print (self.combinedPieces)

    def mcts_search(self, position=[0,0]):
        flag = True
        root = Node()
        root.n = 1
        initGrid = copy.deepcopy(self.grid)
        initcombinedPieces = copy.deepcopy(self.combinedPieces)
        score = 0

        while flag:
            parent = root
            pos = [0,0]

            #always start with empy grid and total combined pieces
            self.grid = copy.deepcopy(initGrid)
            self.combinedPieces = copy.deepcopy(initcombinedPieces)

            #starting to MCTS search
            for l in range(len(self.grid)*len(self.grid)):

                #checking if the current parent has any children
                if len(parent.children) == 0:
                    #if the parent has no children then expand the parent
                    #print ("Remaining Pieces at for expansion")
                    #print (self.combinedPieces)
                    for piece in self.combinedPieces:
                        if piece[1] > 0:
                            if self.rotate:
                                child_found = False

                                for i in range(4):
                                    piece[0] = _rotate(piece[0], 1)

                                    already_exists = False

                                    for ch in parent.children: #ignore duplicate pieces in the same level
                                        if ch.value == piece[0]:
                                            already_exists = True
                                            break

                                    if already_exists:
                                        continue

                                    if _pieceMatch(self.grid, piece[0], pos, EMPType=self.EMPType):
                                        if piece[1] > 0:
                                            child = Node()
                                            child_found = True
                                            child.parent = parent
                                            child.value = piece[0]
                                            parent.children.append(child)

                                if child_found:
                                    piece[1] -= 1
                        #no rotation
                            else:
                                already_exists = False

                                #ignore duplicate pieces in the same level
                                for ch in parent.children:
                                    if ch.value == piece[0]:
                                        already_exists = True
                                if already_exists:
                                    continue

                                if _pieceMatch(self.grid, piece[0], pos, EMPType=self.EMPType):
                                        if piece[1] > 0:
                                            child = Node()
                                            piece[1] -= 1
                                            child.parent = parent
                                            child.value = piece[0]
                                            parent.children.append(child)


                    #print ("Expanding Parent",parent.value)
                    #for piece in parent.children:
                    #    print ("child=",piece.value)
                    break
                    #print("End of expansion")
                else:
                    #print ("Calculating the UCB values", parent.value,l)
                    for j in parent.children:
                        if j.n > 0 and j.ucb >= 0:
                            j.ucb = float(float(j.score)/float(j.n) + \
                                            #float(math.sqrt(2)) * float(math.sqrt(float(2*math.log(root.n))/float(j.n))))
                                            float(self.parm) * float(math.sqrt(float(2*math.log(root.n))/float(j.n))))
                        #print ("Children=",j.value,"Score=",j.score,"n=",j.n,"UCB=",j.ucb)
                    #print ("EOF UCB calculation")

                    best_fit = parent.children[0].ucb
                    best_child = []
                    #best_child.append(parent.children[0])
                    #find the best child
                    #print ("printing all the children")
                    for j in parent.children:
                        #print ("child",j.value,j.ucb)
                        if j.ucb < 0:
                            continue

                        if j.ucb == 0:
                            #print ("best",j.ucb)
                            if best_fit != 0:
                                best_child = []
                            best_child.append(j)
                            best_fit = j.ucb
                            continue

                        elif best_fit != 0 and j.ucb > best_fit:
                            best_child = []
                            best_child.append(j)
                            best_fit = j.ucb

                        elif j.ucb == best_fit:
                            best_child.append(j)

                    #for k in best_child:
                    #    print ("array of best children",k.value,k.ucb)
                    if best_fit < 0:
                        flag = False
                        break
                    if not best_child:
                        flag = False
                        break

                    parent = random.choice(best_child)

                    #print ("Selection")
                    #print ("Best Piece is ",parent.value,"at position ",l)
                    #print ("EOF selection")

                    self.grid[pos[0]][pos[1]] = parent.value #placing the current value on to  the grid

                    mark = False
                    for markPiece in self.combinedPieces: # marking all the pieces that are placed
                        if markPiece[1] > 0:
                            if self.rotate:
                                for i in range(4):
                                    markPiece[0] = _rotate(markPiece[0], 1)
                                    if markPiece[0] == parent.value:
                                        markPiece[1] -= 1
                                        mark = True
                                        break

                            else:
                                if markPiece[0] == parent.value:
                                    markPiece[1] -= 1
                                    mark =  True
                                    break

                        if mark: # piece marked
                            break

                    #if the fitness of score of the best child is not 0, it indicates that it was chosen/simulated atleast once
                    # In that case we consider it as the current parent and continue the search

                    if best_fit != 0:
                        #print ("Gonna Expand",parent.value)
                        pos = list (_nextPosition(self.grid, pos))
                        continue
                    else:
                        #print ("Simulation")
                        #If the current parent has not undergone simulation,
                        #then simulate the and get the score = depth from the current position
                        #print("Combined pieces before simulation")
                        #print(self.combinedPieces)
                        #print ("Grid before simulation")
                        #print (self.grid)
                        score = self.simulation(pos)
                        #print ("score after simulation",score)
                        #print("Combined pieces before simulation")
                        #print(self.combinedPieces)
                        #print ("Grid after simulation")
                        #print (self.grid)

                        #print("EOF Simulation")


                        if score == 0: #meaning no matching piece from current piece, so a block
                            parent.ucb = -99999
                            current = parent.parent
                            #print (parent.value)
                            f = False

                            #checking if all the children of a parent is blocked, if so,
                            #the parent is also a blocked
                            while (current != 'NaN'):
                                for c in current.children:
                                    if c.ucb >= 0:
                                        f = True
                                        break
                                if not(f):
                                    current.ucb = -99999
                                else:
                                    break

                                current = current.parent
                            break

                        #if depth + the current position in the grid is = total no of pieces
                        #It indicates that we have reached a solution
                        if score  + l >= len(self.grid)*len(self.grid):
                            flag = False
                        parent.n += 1
                        root.n +=  1
                        parent.score = score

                        #backpropagation
                        #print ("backpropagation")
                        #print ("root N=",root.n)
                        while parent.parent != 'NaN' :
                            parent = parent.parent
                            parent.score += score
                            parent.n += 1
                            #print ("Parent =",parent.value,"n=",parent.n,"Score=",parent.score)
                        break
                        #print ("EOF backpropagation")


    def simulation(self,pos):
        pos=_nextPosition(self.grid, pos)
        count = 0

        #count indicates the total number of pieces that could be placed from current parent
        # which itself is a fitness evaluation

        #start looking for pieces that can fit in the grid starting from the current position
        for piece in self.combinedPieces:
            if piece[1] > 0:
                if self.rotate:
                    for i in range(4):
                        piece[0] = _rotate(piece[0], 1)

                        if _pieceMatch(self.grid, piece[0], pos, EMPType=self.EMPType):
                            if piece[1] > 0:
                                self.grid[pos[0]][pos[1]] = piece[0]
                                piece[1] -= 1
                                count += 1

                                if (pos[0]+1)*(pos[1]+1) >= len(self.grid)*len(self.grid):
                                    return len(self.combinedPieces)

                                pos = list(_nextPosition(self.grid, pos))
                                break
                            else:
                                raise Exception("piece not in list to remove",piece)

                else:
                    if _pieceMatch(self.grid, piece[0], pos, EMPType=self.EMPType):
                        if piece[1] > 0:

                            self.grid[pos[0]][pos[1]] = piece[0]
                            piece[1] -= 1
                            count += 1

                            if (pos[0]+1)*(pos[1]+1) >= len(self.grid)*len(self.grid):
                                return len(self.combinedPieces)

                            pos = list(_nextPosition(self.grid, pos))
                        else:
                            raise Exception("piece not in list to remove",piece)

        return count
