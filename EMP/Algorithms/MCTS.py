import copy
import math

from EMP.EMP import _rotate, _validPiece, _emptyPiece, _pieceMatch, _removePiece, _nextPosition, _combinePieces, _addCombinedPiece

class Node:
    def __init__(self):
        self.parent   = 'NaN'
        self.children = []
        self.score    = 0
        self.n        = 1
        self.value    = []

class MCTS:

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
                    for piece in self.combinedPieces:
                        if piece[1] > 0:
                            if self.rotate:
                                for i in range(4):
                                    piece[0] = _rotate(piece[0], 1)
                                    if _pieceMatch(self.grid, piece[0], pos, EMPType=self.EMPType):
                                            child = Node()
                                            child.parent = parent
                                            child.value = piece[0]
                                            parent.children.append(child)

                        #no rotation
                        else:
                            if _pieceMatch(self.grid, piece[0], pos, EMPType=self.EMPType):
                                    child = Node()
                                    child.parent = parent
                                    child.value = piece[0]
                                    parent.children.append(child)


                # if the parent has children pick the best child
                else:
                    best_fit = parent.children[0].score
                    best_child = parent.children[0]

                    #find the best child
                    for j in parent.children:
                        if j.score < 0:
                            continue
                        if j.score == 0:
                            best_child = j
                            best_fit = j.score
                            break

                        elif j.score > best_fit:
                            best_child = j
                            best_fit = j.score


                    parent = best_child

                    self.grid[pos[0]][pos[1]] = parent.value #placing the current value on to  the grid
                    for markPiece in self.combinedPieces: # marking all the pieces that are placed
                        if markPiece[1] > 0:
                            if self.rotate:
                                for i in range(4):
                                    markPiece[0] = _rotate(markPiece[0], 1)
                                    if markPiece[0] == parent.value:
                                        markPiece[1] -= 1
                                        break

                            else:
                                if markPiece[0] == parent.value:
                                    markPiece[1] -= 1
                                    break

                            if markPiece[1] <= 0: # piece marked
                                break

                    #if the fitness of score of the best child is not 0, it indicates that it was chosen/simulated atleast once
                    # In that case we consider it as the current parent and continue the search

                    if best_fit != 0:
                        pos = list (_nextPosition(self.grid, pos))
                    else:
                        #If the current parent has not undergone simulation,
                        #then simulate the and get the score = depth from the current position
                        score = self.simulation(pos)

                        if score == 0: #meaning no matching piece from current piece, so a block
                            parent.score = -99
                            current = parent.parent
                            f = False

                            #checking if all the children of a parent is blocked, if so,
                            #the parent is also a blocked
                            while (current != 'NaN'):
                                for c in current.children:
                                    if c.score >= 0:
                                        f = True
                                        break
                                if not(f):
                                    current.score = -99
                                else:
                                    break

                                current = current.parent

                            break

                        #if depth + the current position in the grid is = total no of pieces
                        #It indicates that we have reached a solution
                        if score  + l >= len(self.grid)*len(self.grid):
                            print (pos,score,i,len(self.combinedPieces))
                            print (self.combinedPieces)
                            print (self.grid)
                            flag = False

                        parent.n += 1

                        root.n +=  1
                        parent.score   = score/parent.n + \
                                        math.sqrt(2)*math.sqrt(2*math.log(root.n)/parent.n)

                        #backpropagation
                        temp_score = parent.score
                        while parent.parent != 'NaN' :
                            parent = parent.parent
                            parent.score += temp_score
                            parent.n += 1

                        break


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
                            self.grid[pos[0]][pos[1]] = piece[0]

                            if piece[1] > 0:
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
                        self.grid[pos[0]][pos[1]] = piece[0]

                        if piece[1] > 0:
                            piece[1] -= 1
                            count += 1

                            if (pos[0]+1)*(pos[1]+1) >= len(self.grid)*len(self.grid):
                                return len(self.combinedPieces)

                            pos = list(_nextPosition(self.grid, pos))
                            break
                        else:
                            raise Exception("piece not in list to remove",piece)

        return count
