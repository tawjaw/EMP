from EMP.EMP import generatePuzzle, drawPuzzle, _validPiece, loadPieces, _solutionEdgesNotMatch
import copy
from random import shuffle
import random
import numpy as np
import time
import math

class Individual:
    
    
    rotate = False
    def __init__(self, piecesDict, size):
        if Individual.rotate == False:
            self.size=size
            self.representation=np.arange(0, self.size*self.size).reshape(self.size,self.size)
            np.random.shuffle(self.representation)
        else:
            assert("with rotate not implemented")
        
        self.evaluateFitness(piecesDict)
        
    

    
    def mutateRegionExchange(self):
        error = True
        while(error):
            x1 = random.randint(0, self.size-1)
            x2max=self.size if x1 > math.ceil(self.size/2)-1 else (x1+math.ceil(self.size/2))
            x2 = random.randint(x1+1,x2max)
            y1 = random.randint(0, self.size-1)
            y2max=self.size if y1 > math.ceil(self.size/2)-1 else (y1+math.ceil(self.size/2))
            y2 = random.randint(y1+1,y2max)
            #error = False
            xsize = x2-x1
            ysize = y2-y1
            xx1 = random.randint(0, self.size-1)
            xx2= None
            if xx1+xsize > self.size: 
                #error x
                continue
            else: xx2 = xx1+xsize
            yy1 = random.randint(0,self.size-1)
            yy2 = None
            if yy1+ysize > self.size: 
                #error y
                continue
            else: yy2 = yy1+ysize

            if(not (abs(x1-xx1) >= xsize or abs(y1-yy1) >= ysize)): 
                #overlap
                continue

            #make the swap 
            temp = np.copy(self.representation[x1:x2,y1:y2])
            self.representation[x1:x2,y1:y2] = self.representation[xx1:xx2,yy1:yy2]
            self.representation[xx1:xx2,yy1:yy2] = temp
            error=False


    def crossover(indiv1, indiv2):
        if indiv1.size != indiv2.size: assert("individuals must be of same size for crossover")
        size=indiv1.size
        #select region 
        x1 = random.randint(0, size-1)
        x2max= size if x1 > math.ceil(size/2)-1 else (x1+math.ceil(size/2))
        x2 = random.randint(x1+1,x2max)
        y1 = random.randint(0, size-1)
        y2max= size if y1 > math.ceil(size/2)-1 else (y1+math.ceil(size/2))
        y2 = random.randint(y1+1,y2max)
        #clone parentA
        offspring = copy.deepcopy(indiv1)
        #print(offspring.representation)
        regionB_pieces = list(indiv2.representation[x1:x2,y1:y2].flatten())
        offspring_flattened = offspring.representation.flatten()
        for i in range(offspring_flattened.shape[0]):
            if offspring_flattened[i] in regionB_pieces:
                offspring_flattened[i] = -1

        offspring.representation = offspring_flattened.reshape(size,size)
        remaining_tiles = list(offspring.representation[x1:x2,y1:y2].flatten())
        remaining_tiles = [x for x in remaining_tiles if x!=-1]
        offspring.representation[x1:x2,y1:y2] = indiv2.representation[x1:x2,y1:y2].copy()

        random.shuffle(remaining_tiles)

        for i in range(size):
            for j in range(size):
                if offspring.representation[i][j] == -1:
                    offspring.representation[i][j] = remaining_tiles.pop()

        return offspring
    
    def evaluateFitness(self, piecesDict):
        self.fitness =  _solutionEdgesNotMatch(self.to_grid(piecesDict), self.size)
        
    def to_grid(self, piecesDict):
        grid =[[[ None for x in range(4)]for y in range(self.size)] for p in range(self.size)]

        piece = 0

        for idxrow, row in enumerate(grid):
            for idxpos, position in enumerate(row):
                #print()
                grid[idxrow][idxpos] = list(piecesDict[self.representation[idxrow][idxpos]])
                piece += 1
        return grid
        
class Population:
    def __init__(self, pieces, EMPsize, popSize, parentSize, offspringSize, mutationParam, crossoverParam, elitism, tournament, maxGeneration=None, maxTime=None):
        self.maxGeneration=maxGeneration
        self.maxTime=maxTime
        if maxTime != None:
            self.startTime = time.time()
        self.pieces = pieces
        self._createPiecesDictionary()
        self.EMPsize = EMPsize
        self.compCost=0
        
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
            self.individuals.append(Individual(self.piecesDict, self.EMPsize))
            self.compCost+=self.EMPsize*self.EMPsize
        self.fittest = None
        
        ## assign fittest indiv
        self.individuals.sort(key=lambda x: x.fitness, reverse=False)
        self.fittest = self.individuals[0]
        self.fittest_grid = self.individuals[0].to_grid(self.piecesDict)
        
    def _createPiecesDictionary(self):
            temp = list()
            i = 0
            for piece in self.pieces:
                temp.append((i,copy.deepcopy(piece)))
                i += 1

            self.piecesDict = dict(temp)
        


    def evolve(self):
        while self.fittest.fitness != 0:
            self.generation += 1
            
            if self.maxGeneration != None and self.generation > self.maxGeneration: return
            if self.maxTime != None and (time.time()-self.startTime)/60 > self.maxTime: return 
            #print("generation", self.generation, "fittest", self.fittest.fitness)
            ## elitism 
            ## individuals already sorted
            parents = list()

            for x in range(0, self.elitism+1):
                parents.append(self.individuals[x])
    
            ## parent selection
            ## tournament selection
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
                    child.evaluateFitness(self.piecesDict)
                    offsprings.append(child)
                else:
                    randomParents = random.sample(parents, 2)
                    child = Individual.crossover(randomParents[0], randomParents[1])
                    child.evaluateFitness(self.piecesDict)
                    offsprings.append(child)
                
                self.compCost+=self.EMPsize*self.EMPsize
            ## survival selection
            newPopulation = parents + offsprings
            
            newPopulation.sort(key=lambda x: x.fitness, reverse=False)
            self.individuals = newPopulation[:self.popSize]
            self.fittest = self.individuals[0]
            self.fittest_grid = self.individuals[0].to_grid(self.piecesDict)

                

            
            
        