import random
import csv

def savePieces(pieces, outputFile):
    file = open(outputFile, 'w')
    for piece in pieces:
        file.write(str(piece[0])+','+str(piece[1])+','+str(piece[2])+','+str(piece[3])+'\n')
    file.close()

def loadPieces(inputFile):
    """Reads the puzzle pieces from a csv file and returns a list with all the pieces.  
    """
    file = open(inputFile)
    reader = csv.reader(file,delimiter=',')
    puzzle = list()
    for row in reader:
        piece = list(map(int,row))
        puzzle.append(piece)
    file.close()
    return puzzle


def _drawPiece(dr, position, piece, colors, pieceLength):
    """
    Position: top left corner of the square to draw the puzzle
    """
    from PIL import Image, ImageDraw

    if all(x == -1 for x in piece): return 
    elif all(x == -2 or x == None for x in piece):
        dr.polygon([(position[0],position[1]), (position[0]+pieceLength/2, position[1]+pieceLength/2),
            (position[0],position[1]+pieceLength)], fill="white", outline="black")
        dr.polygon([(position[0],position[1]), (position[0]+pieceLength/2, position[1]+pieceLength/2),\
            (position[0]+pieceLength,position[1])], fill="white",outline="black")
        dr.polygon([(position[0]+pieceLength,position[1]), (position[0]+pieceLength/2, position[1]+pieceLength/2),\
            (position[0]+pieceLength,position[1]+pieceLength)], fill="white",outline="black")
        dr.polygon([(position[0],position[1]+pieceLength), (position[0]+pieceLength/2, position[1]+pieceLength/2),\
            (position[0]+pieceLength,position[1]+pieceLength)], fill="white",outline="black")
    else:
        dr.polygon([(position[0],position[1]), (position[0]+pieceLength/2, position[1]+pieceLength/2),
            (position[0],position[1]+pieceLength)], fill=colors[piece[0]], outline="black")
        dr.polygon([(position[0],position[1]), (position[0]+pieceLength/2, position[1]+pieceLength/2),\
            (position[0]+pieceLength,position[1])], fill=colors[piece[1]],outline="black")
        dr.polygon([(position[0]+pieceLength,position[1]), (position[0]+pieceLength/2, position[1]+pieceLength/2),\
            (position[0]+pieceLength,position[1]+pieceLength)], fill=colors[piece[2]],outline="black")
        dr.polygon([(position[0],position[1]+pieceLength), (position[0]+pieceLength/2, position[1]+pieceLength/2),\
            (position[0]+pieceLength,position[1]+pieceLength)], fill=colors[piece[3]],outline="black")



def drawPuzzle(puzzle, pieceLength=100, colors=None):
    """
    Draws the puzzle and returns an image. 
    puzzle: grid of the puzzle containing the pieces.
            For example, a 3x3 grid has the shape:
            [ [ [1,2,3,4],[1,2,3,4],[1,2,3,4] ],
              [ [1,2,3,4],[1,2,3,4],[1,2,3,4] ],
              [ [1,2,3,4],[1,2,3,4],[1,2,3,4] ] ]
            
            Each pice contains the number referring to a color.
            color = 0 is black and is used to represent the frame in framed EMPs.
            [-1,-1,-1,-1] piece is an empty space on the grid that is not part of the puzzle.
            [-2,-2,-2,-2] piece draws a piece in that position with white colors. This is used if not all the pieces drawn are used in the puzzle.
    
    pieceLength: the length of the side of each piece in pixels.
                 Default = 100 pixels.
    
    colors: A list of colors that will be used to map the number of the color to the color used to draw the piece.
            The index of the color in the list is represented by the piece in puzzle.
            Default color list: ["black","blue","brown","red","yellow","green","orange","beige","turquoise","pink"]
            It is recommended to keep "black" at index 0 as it is used to draw frames in framed EMPs.
    """
    from PIL import Image, ImageDraw

    if colors == None:
        colors =["black","blue","brown","red","yellow","green","orange","beige","turquoise","pink",'indianred',
 'magenta', 'darkviolet', 'salmon', 'lightcyan', 'darkslateblue', 'snow', 'blueviolet', 'dimgrey', 'cyan', 'deeppink',
 'sienna', 'lightyellow',   'goldenrod', 'darkgreen', 'deepskyblue', 'forestgreen', 'lawngreen', 'linen', 'darkmagenta',
 'gray', 'olivedrab', 'mediumslateblue', 'dimgray', 'violet', 'lightskyblue', 'peru', 'brown', 'royalblue', 'aqua', 'darkgray',
  'coral', 'ivory', 'slategrey', 'lavender',   'crimson',  'orchid', 'moccasin', 'gold']
        
#         []

    gridSize = [0,0]
    for row in puzzle:
        if len(row) > gridSize[0]: gridSize[0] = len(row)
    gridSize[1] = len(puzzle)
    
    if len(puzzle[0][0]) == 4:      #square EMP
        im = Image.new('RGB', (gridSize[0]*pieceLength,gridSize[1]*pieceLength), (255,255,255))
        dr = ImageDraw.Draw(im)

        position = [0,0]
        for row in puzzle:
            for piece in row:
                _drawPiece(dr, position, piece, colors, pieceLength=pieceLength)
                position[0] = position[0]+ (pieceLength if position[0] != 0 else pieceLength-1)

            position[1] = position[1]+ (pieceLength if position[1] != 0 else pieceLength-1)
            position[0] = 0

        return im
    else:
        return False



def _rotate(piece, n):
    return piece[n:] + piece[:n]

def _validPiece(piece):
    #print(piece)
    if all(x == -1 for x in piece): return False
    else: return True
    
def _emptyPiece(piece):
    if all((x == -2 or x == None) for x in piece) : return True
    else: return False

def _pieceMatch(grid, piece, position, EMPType='SF'):
    gridSize_Y = len(grid)
    gridSize_X = len(grid[0])
    idxRow = position[0]
    idxPiece = position[1]
    isMatch = False
    
    isMatch = True
    #left edge
    if not(idxPiece == 0  or not _validPiece(grid[idxRow][idxPiece-1])):
        if not _emptyPiece(grid[idxRow][idxPiece-1]):
            if piece[0] != grid[idxRow][idxPiece-1][2]: 
                isMatch = False
        elif EMPType == 'SF' and piece[0] == 0:
            isMatch = False
    elif EMPType == 'SF':
        if piece[0] != 0: isMatch = False

    #top edge
    if not(idxRow == 0 or not _validPiece(grid[idxRow-1][idxPiece])):
        if not _emptyPiece(grid[idxRow-1][idxPiece]):
            if piece[1] != grid[idxRow-1][idxPiece][3]:
                isMatch = False
        elif EMPType == 'SF' and piece[1] == 0:
            isMatch = False
    elif EMPType == 'SF':
        if piece[1] != 0: isMatch = False
            
    #right edge
    if not(idxPiece == gridSize_X-1 or not _validPiece(grid[idxRow][idxPiece+1])):
        if not _emptyPiece(grid[idxRow][idxPiece+1]):
            if piece[2] != grid[idxRow][idxPiece+1][0]:                   
                isMatch = False
        elif EMPType == 'SF' and piece[2] == 0:
            isMatch = False
    elif EMPType == 'SF':
        if piece[2] != 0: isMatch = False
            
    #bottom edge
    if not(idxRow == gridSize_Y-1 or not _validPiece(grid[idxRow+1][idxPiece])):
        if not _emptyPiece(grid[idxRow+1][idxPiece]):
            if piece[3] != grid[idxRow+1][idxPiece][1]: 
                isMatch = False
        elif EMPType == 'SF' and piece[3] == 0:
            isMatch = False
    elif EMPType == 'SF':
        if piece[3] != 0: isMatch = False
        
    if isMatch:
        return True
    
    return False

def _nextPosition(grid, currentPos):
    gridSize_Y = len(grid)
    gridSize_X = len(grid[0])
    pos = None
    if currentPos[1] == gridSize_X-1:
        pos = [currentPos[0]+1, 0]
    else:
        pos = [currentPos[0], currentPos[1]+1]
    if pos[0] >= gridSize_Y:
        return False
    
    while not _validPiece(grid[pos[0]][pos[1]]):
        #print(pos)
        if pos[1] == gridSize_X-1:
            pos = [pos[0]+1, 0]
        else:
            pos = [pos[0], pos[1]+1]
        
        if pos[0] >= gridSize_Y:
            return False


    return pos   
        
def _removePiece(piece, pieces, rotate=True):
    if rotate:
        for i in range(4):
            try:
                piece = _rotate(piece, 1)
                pieces.remove(piece[:])
                return
            except:
                i = 0
        raise Exception("piece not in list to remove")
    else:
        pieces.remove(piece[:])
        


def _addCombinedPiece(piece, combinedPieces, rotate=True):
    if rotate:
        for item in combinedPieces:
            for i in range(4):
                if _rotate(piece, i) == item[0]:
                    item[1] += 1
                    return
        combinedPieces.append([piece[:], 1])
    else:
        for item in combinedPieces:
            if piece == item[0]:
                item[1] += 1
                return
        combinedPieces.append([piece[:], 1])
        
            
def _combinePieces(pieces, rotate=True):
    combinedPieces = list()
    for piece in pieces:
        _addCombinedPiece(piece, combinedPieces, rotate=rotate)
    return combinedPieces
   

def generatePuzzle(grid, colors, EMPType='SF', return_='pieces', shuffle=True, rotate=True, seed=None):
    """
    Generates random puzzle and returns the puzzle and id string representing the puzzle generated "EMPType-colors-gridSizeX-gridSizeY-seed-rotate".

    grid: can be a tuple or a list. tuple (m,n) will generate a puzzle of m x n. A list grid is used to pass a custom grid shape.

    colors: number of colors used in the puzzle.

    EMPType: type of the puzzle.
        'SF' square framed EMP.
        'S'  square none framed EMP.

    return_: type of the return
        'pieces' list of pieces
        'grid'   grid of puzzle
        default: 'pieces'

    shuffle: shuffles the pieces of the puzzle randomly if True.
        default: True

    rotate: rotates each piece randomly if True.
        default: True

    seed: random seed used. 
        defualt: None. random seed will be used.
    """
    if EMPType not in ['SF','S']:
        raise AssertionError("EMPType "+EMPType+" not defined.")
    if return_ not in ['pieces', 'grid']:
        raise AssertionError("return_ " + return_ + " not defined.")

    if type(grid) == tuple:
        # create the grid with None for colors
        if(EMPType == 'SF' or EMPType == 'S'):
            grid=[[[ None for x in range(4)]for y in range(grid[0])] for p in range(grid[1])]
            
    elif type(grid) != list: raise AssertionError("grid should be a tuple or list.")
    
    if type(colors) != int or colors < 0: raise AssertionError("colors should be a positive integer.")
        
    if seed == None: seed = random.randint(0,1000000)
    if type(seed) != int: raise AssertionError("seed must be an int.")
    random.seed(seed)

    gridSize_Y = len(grid)
    gridSize_X = len(grid[0])
    
    id = EMPType + "-" + str(colors) + "-" + str(gridSize_X) + "-"\
            + str(gridSize_Y) + "-" + str(seed) +"-"+ ('R' if rotate else 'NR')

    
    # corners
    if EMPType == 'SF':
        for idxRow, row in enumerate(grid):
            for idxPiece, piece in enumerate(row):
                #left edge
                if _validPiece(piece) and (idxPiece == 0  or not _validPiece(grid[idxRow][idxPiece-1])):
                    piece[0] = 0
                #Top edge
                if _validPiece(piece) and (idxRow == 0 or not _validPiece(grid[idxRow-1][idxPiece])):
                    piece[1] = 0
                #Right edge
                if _validPiece(piece) and (idxPiece == gridSize_X-1 or not _validPiece(grid[idxRow][idxPiece+1])):
                    piece[2] = 0
                #Bottom edge
                if _validPiece(piece) and (idxRow == gridSize_Y-1 or not _validPiece(grid[idxRow+1][idxPiece])):
                    piece[3] = 0
    elif EMPType == 'S':
        for idxRow, row in enumerate(grid):
            for idxPiece, piece in enumerate(row):
                #left edge
                if _validPiece(piece) and (idxPiece == 0  or not _validPiece(grid[idxRow][idxPiece-1])):
                    piece[0] = random.randint(1,colors)
                #Top edge
                if _validPiece(piece) and (idxRow == 0 or not _validPiece(grid[idxRow-1][idxPiece])):
                    piece[1] = random.randint(1,colors)
                #Right edge
                if _validPiece(piece) and (idxPiece == gridSize_X-1 or not _validPiece(grid[idxRow][idxPiece+1])):
                    piece[2] = random.randint(1,colors)
                #Bottom edge
                if _validPiece(piece) and (idxRow == gridSize_Y-1 or not _validPiece(grid[idxRow+1][idxPiece])):
                    piece[3] = random.randint(1,colors)
                    
    #let there be colors
    if EMPType == 'SF' or EMPType == 'S':
        for idxRow, row in enumerate(grid):
            for idxPiece, piece in enumerate(row):
                #left edge
                if piece[0] == None:
                    if grid[idxRow][idxPiece-1][2] != 0 and grid[idxRow][idxPiece-1][2] != None:
                        piece[0] = grid[idxRow][idxPiece-1][2]
                    else:
                        piece[0] = random.randint(1,colors)
                #top edge
                if piece[1] == None:
                    if grid[idxRow-1][idxPiece][3] != 0 and grid[idxRow-1][idxPiece][3] != None:
                        piece[1] = grid[idxRow-1][idxPiece][3]
                    else:
                        piece[1] = random.randint(1,colors)
                #right edge
                if piece[2] == None:
                    if grid[idxRow][idxPiece+1][0] != 0 and grid[idxRow][idxPiece+1][0] != None:
                        piece[2] = grid[idxRow][idxPiece+1][0]
                    else:
                        piece[2] = random.randint(1,colors)
                #bottom edge
                if piece[3] == None:
                    if grid[idxRow+1][idxPiece][1] != 0 and grid[idxRow+1][idxPiece][1] != None:
                        piece[3] = grid[idxRow+1][idxPiece][1]
                    else: 
                        piece[3] = random.randint(1,colors)
    pieces = list()
    for idxRow, row in enumerate(grid):
        for idxPiece, piece in enumerate(row):
            if _validPiece(piece):
                pieces.append(piece[:])
    if shuffle:
        random.shuffle(pieces)
    if rotate:
        for piece in pieces: 
            piece[:] = _rotate(piece, random.randint(0,3))

    if return_ == 'grid':
        if shuffle or rotate:
            for idxRow, row in enumerate(grid):
                for idxPiece, piece in enumerate(row):
                    if _validPiece(piece):
                        piece[:] = pieces.pop(0)
            
            return (grid, id)
        else:
            return (grid, id)
    elif return_ == 'pieces':
        return (pieces, id)


def isCorrect(grid, EMPType='S'):
    """
    Returns True if the pieces on the grid are correct. Else returns False.

    grid: grid of the puzzle.
    EMPType: 'SF' for square framed EMP. 'S' for square none framed EMP.
    """
    gridSize_Y = len(grid)
    gridSize_X = len(grid[0])
    
    if EMPType not in ['SF','S']:
        raise AssertionError("EMPType "+EMPType+" not defined.")
    if EMPType == 'SF':
        #check corners
        for idxRow, row in enumerate(grid):
            for idxPiece, piece in enumerate(row):
                if _validPiece(piece):
                    #left edge
                    if idxPiece == 0  or not _validPiece(grid[idxRow][idxPiece-1]):
                        if piece[0] != 0: return False
                    #Top edge
                    if idxRow == 0 or not _validPiece(grid[idxRow-1][idxPiece]):
                        if piece[1] != 0: return False
                    #Right edge
                    if idxPiece == gridSize_X-1 or not _validPiece(grid[idxRow][idxPiece+1]):
                        if piece[2] != 0: return False
                    #Bottom edge
                    if idxRow == gridSize_Y-1 or not _validPiece(grid[idxRow+1][idxPiece]):
                        if piece[3] != 0: return False


    if EMPType == 'SF' or EMPType == 'S':
        for idxRow, row in enumerate(grid):
            for idxPiece, piece in enumerate(row):
                if _validPiece(piece):
                    #left edge
                    if not(idxPiece == 0  or not _validPiece(grid[idxRow][idxPiece-1])):
                        if piece[0] != grid[idxRow][idxPiece-1][2]: return False
                    #top edge
                    if not(idxRow == 0 or not _validPiece(grid[idxRow-1][idxPiece])):
                        if piece[1] != grid[idxRow-1][idxPiece][3]: return False
                    #right edge
                    if not(idxPiece == gridSize_X-1 or not _validPiece(grid[idxRow][idxPiece+1])):
                        if piece[2] != grid[idxRow][idxPiece+1][0]: return False
                    #bottom edge
                    if not(idxRow == gridSize_Y-1 or not _validPiece(grid[idxRow+1][idxPiece])):
                        if piece[3] != grid[idxRow+1][idxPiece][1]: return False
                    
    return True

def _isCorrectWithCompCost(grid, EMPType='S'):
    """
    Returns tuple of True if the pieces on the grid are correct Else returns False,
    and computational cost where the computational cost is everytime the constraints
    of a piece is checked.

    grid: grid of the puzzle.
    EMPType: 'SF' for square framed EMP. 'S' for square none framed EMP.
    """
    gridSize_Y = len(grid)
    gridSize_X = len(grid[0])
    compCost=0
    if EMPType not in ['SF','S']:
        raise AssertionError("EMPType "+EMPType+" not defined.")
    if EMPType == 'SF':
        #check corners
        for idxRow, row in enumerate(grid):
            for idxPiece, piece in enumerate(row):
                if _validPiece(piece):
                    compCost+=1
                    #left edge
                    if idxPiece == 0  or not _validPiece(grid[idxRow][idxPiece-1]):
                        if piece[0] != 0: return (False, compCost)
                    #Top edge
                    if idxRow == 0 or not _validPiece(grid[idxRow-1][idxPiece]):
                        if piece[1] != 0: return (False, compCost)
                    #Right edge
                    if idxPiece == gridSize_X-1 or not _validPiece(grid[idxRow][idxPiece+1]):
                        if piece[2] != 0: return (False, compCost)
                    #Bottom edge
                    if idxRow == gridSize_Y-1 or not _validPiece(grid[idxRow+1][idxPiece]):
                        if piece[3] != 0: return (False, compCost)


    if EMPType == 'SF' or EMPType == 'S':
        for idxRow, row in enumerate(grid):
            for idxPiece, piece in enumerate(row):
                if _validPiece(piece):
                    compCost+=1
                    #left edge
                    if not(idxPiece == 0  or not _validPiece(grid[idxRow][idxPiece-1])):
                        if piece[0] != grid[idxRow][idxPiece-1][2]: return (False, compCost)
                    #top edge
                    if not(idxRow == 0 or not _validPiece(grid[idxRow-1][idxPiece])):
                        if piece[1] != grid[idxRow-1][idxPiece][3]: return (False, compCost)
                    #right edge
                    if not(idxPiece == gridSize_X-1 or not _validPiece(grid[idxRow][idxPiece+1])):
                        if piece[2] != grid[idxRow][idxPiece+1][0]: return (False, compCost)
                    #bottom edge
                    if not(idxRow == gridSize_Y-1 or not _validPiece(grid[idxRow+1][idxPiece])):
                        if piece[3] != grid[idxRow+1][idxPiece][1]: return (False, compCost)
                    
    return (True, compCost)


def _findUnassignedNeighbours(grid, position):
    size = len(grid)
    neighbours = list()
    neighbours.append((position[0], position[1]+1))
    neighbours.append((position[0], position[1]-1))
    neighbours.append((position[0]-1, position[1]))
    neighbours.append((position[0]+1, position[1]))

    unassignedNeighbours = [x for x in neighbours \
    if x[0] > -1 and x[1] > -1 \
    and x[0] < size and x[1] < size\
    and all(p == -2 or p == None for p in grid[x[0]][x[1]]) ]

    return unassignedNeighbours

def _findDomainAffectedPositions(grid, position):
    """
    This function returns the positions of pieces that their domain is affected by
    the pieces fit on the grid. This method assumes the same order of search being followed
    by all the BT version algorithms; starting from the top left corner and filling uo
    row after the other from left to right. It does not check whether those positions are
    empty or filled with pieces as they should be empty if the order of search is followed.
    It also assumes the grid is a square grid where the width and height are equal. NxN puzzle.

    grid: is the grid of the puzzle with the empty positions having -2 or None pieces.
    position: a tuple representing the position of the piece that is last placed. 
    """

    size = len(grid)
    if size < 2: return list()
    positions = list()

    if position[0] < size-1: 
        ## return all the positions below the piece being placed and to the left
        ## till the beginning of the grid except if the row is the last row
        i=position[1]
        while(i > -1):
            positions.append((position[0]+1,i))

            i-=1
    if position[0] > 0:
        ## return the positions to the right of the piece being placed skipping
        ## the position directly to the right as it will be checekd in the next 
        ## iteration of the search immediatly. First row doesnt need the check.
        i=position[1]+2 # +2 for the skip. no need to check if its the end. while will do that.
        while(i < size):
            positions.append((position[0], i))
            i+=1
    return positions




def _solutionEdgesNotMatch(grid, size):

    gridSize_Y = size
    gridSize_X = size

    edgesNotMatch = 0

    for idxRow, row in enumerate(grid):
        for idxPiece, piece in enumerate(row):
            if _validPiece(piece):
                #left edge
                if not(idxPiece == 0  or not _validPiece(grid[idxRow][idxPiece-1])):
                    if piece[0] != grid[idxRow][idxPiece-1][2]: edgesNotMatch += 1
                #top edge
                if not(idxRow == 0 or not _validPiece(grid[idxRow-1][idxPiece])):
                    if piece[1] != grid[idxRow-1][idxPiece][3]: edgesNotMatch += 1
                #right edge
                if not(idxPiece == gridSize_X-1 or not _validPiece(grid[idxRow][idxPiece+1])):
                    if piece[2] != grid[idxRow][idxPiece+1][0]: edgesNotMatch += 1
                #bottom edge
                if not(idxRow == gridSize_Y-1 or not _validPiece(grid[idxRow+1][idxPiece])):
                    if piece[3] != grid[idxRow+1][idxPiece][1]: edgesNotMatch += 1

    return edgesNotMatch/2

