from EMP.EMP import generatePuzzle, drawPuzzle, _validPiece, loadPieces
import copy
from random import shuffle
import random

class Individual:
    piecesDict = None
    size = None
    rotate = False
    def __init__(self):
        if Individual.rotate == False:
            self.pieces = [(x,0) for x in range(0,Individual.size*Individual.size)]
            shuffle(self.pieces)
        else:
            assert("with rotate not implemented")
        
        self.evaluateFitness()
        
    
    def _solutionEdgesNotMatch(grid):

        gridSize_Y = Individual.size
        gridSize_X = Individual.size

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

                #print(idxRow, idxPiece, count)


        return edgesNotMatch
    
    def mutateRegionExchange(self):
        size = len(self.pieces) - 1
        notSame = True

        while(notSame):
            randomPiece1 = random.randint(0, size)
            randomPiece2 = random.randint(0, size)
            #print(randomPiece1, randomPiece2)
            if randomPiece1 != randomPiece2:
                notSame = False
                self.pieces[randomPiece1], self.pieces[randomPiece2] = self.pieces[randomPiece2], self.pieces[randomPiece1]

    def crossover(ind1, ind2):
        size = Individual.size*Individual.size -1
        randomRegionStart = random.randint(0, size)
        randomRegionEnd = random.randint(randomRegionStart, size)
        indiv2Temp = copy.deepcopy(ind2)
        offspring = copy.deepcopy(ind1)
        region2 = list()
        temp = list()
        #print(ind1.pieces, ind2.pieces)
        #print(randomRegionStart, randomRegionEnd)
        for i in range(randomRegionStart, randomRegionEnd+1):
            temp.append(offspring.pieces[i])
            region2.append(indiv2Temp.pieces[i])
        
        #print("temp", temp)

        #print("offspring", offspring.pieces)
        #print("region2", region2)
        
        temp = [x for x in temp if x not in region2]
        
        for idx, item in enumerate(offspring.pieces):
            if item in region2:
                offspring.pieces[idx] = None
        #print("offspring", offspring.pieces)

        for i in range(randomRegionStart, randomRegionEnd+1):
            offspring.pieces[i] = indiv2Temp.pieces[i]
        #print("offspring", offspring.pieces)
        #print("temp", temp)
        
        
        
        shuffle(temp)
        for idx, item in enumerate(offspring.pieces):
            if item is None:
                offspring.pieces[idx] = temp.pop(0)
        #print("offspring", offspring.pieces)
        #if len(set(offspring.pieces)) != 9: assert()
        return offspring
    
    def evaluateFitness(self):
        grid =[[[ None for x in range(4)]for y in range(Individual.size)] for p in range(Individual.size)]

        piece = 0

        for idxrow, row in enumerate(grid):
            for idxpos, position in enumerate(row):
                #print()
                grid[idxrow][idxpos] = list(Individual.piecesDict[self.pieces[piece][0]])
                piece += 1
        self.fitness =  Individual._solutionEdgesNotMatch(grid)/2
        
    def to_grid(self):
        grid =[[[ None for x in range(4)]for y in range(Individual.size)] for p in range(Individual.size)]

        piece = 0

        for idxrow, row in enumerate(grid):
            for idxpos, position in enumerate(row):
                #print()
                grid[idxrow][idxpos] = list(Individual.piecesDict[self.pieces[piece][0]])
                piece += 1
        return grid
        
class Population:
    def __init__(self, pieces, EMPsize, popSize, parentSize, offspringSize, mutationParam, crossoverParam, elitism, tournament, maxGeneration=None):
        self.maxGeneration=maxGeneration
        self.pieces = pieces
        self.EMPsize = EMPsize
        Individual.piecesDict = dict(self._assignPieceId(pieces))
        Individual.size = self.EMPsize
        
        self.popSize = popSize
        self.parentSize = parentSize
        self.offspringSize = offspringSize
        self.mutationParam = mutationParam
        self.crossoverParam = crossoverParam
        self.elitism = elitism
        self.tournament = tournament
        self.individuals = list()
        self.generation = 0
        for _ in range(popSize):
            self.individuals.append(Individual())
        self.fittest = None
        
        ## assign fittest indiv
        self.individuals.sort(key=lambda x: x.fitness, reverse=False)
        self.fittest = self.individuals[0]

 
    def _assignPieceId(self,pieces):
        individual = list()
        i = 0
        for piece in pieces:
            individual.append((i,copy.deepcopy(piece)))
            i += 1
        return individual


    def evolve(self):
        while self.fittest.fitness != 0:
            self.generation += 1
            
            if self.maxGeneration != None and self.generation > self.maxGeneration: return
            #print("generation", self.generation, "fittest", self.fittest.fitness)
            ## elitism 
            ## individuals already sorted
            parents = list()

            for x in range(0, self.elitism+1):
                parents.append(self.individuals[x])
    
            ## parent selection
            ## tournament selection size 3
            parents = list()
            while len(parents) != self.parentSize:
                
                tournament = random.sample(self.individuals, self.tournament)
                best = tournament[0]
                for i in range(1, self.tournament):
                    if tournament[i].fitness < best.fitness:
                        best = tournament[i]
                
                parents.append(best)
            
            ## offspring generation
            offsprings = list()
            while len(offsprings) != self.offspringSize:
                randOperation = random.uniform(0, 1)
                if randOperation <= self.mutationParam:
                    randomParent = random.sample(parents, 1)
                    child = copy.deepcopy(randomParent[0])
                    child.mutateRegionExchange()
                    child.evaluateFitness()
                    offsprings.append(child)
                else:
                    randomParents = random.sample(parents, 2)
                    child = Individual.crossover(randomParents[0], randomParents[1])
                    child.evaluateFitness()
                    offsprings.append(child)
                    
            ## survivol selection
            newPopulation = parents + offsprings
            
            newPopulation.sort(key=lambda x: x.fitness, reverse=False)
            self.individuals = newPopulation[:self.popSize]
            self.fittest = self.individuals[0]
                

            
            
        