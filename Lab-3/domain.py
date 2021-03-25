# -*- coding: utf-8 -*-

from random import *
from utils import *
import numpy as np
import pickle
import copy


# the glass Gene can be replaced with int or float, or other types
# depending on your problem's representation

class Gene:
    def __init__(self):
        # initialise the Gene randomly according to the representation
        self.__value = randint(0, GENE_VALUES-1)

    def getValue(self):
        # gets the gene's value (can be 0, 1, 2 or 3, due to the fact that there are 4 directions the drone can opt for)
        return self.__value

    def __repr__(self):
        return str(self.__value)


class Individual:
    def __init__(self, x, y, size = 0):
        self.__size = size
        self.__chromosome = [Gene() for i in range(self.__size)]
        self.__startingPosition = np.array([x, y])
        self.__f = None
        self.__exploredMap = None
        self.__age = 0


    def getChromosome(self):
        return self.__chromosome

    
    def incrementAge(self):
        self.__age += 1


    def setChromosome(self, chromosome):
        self.__chromosome = chromosome


    def getStartingPosition(self):
        return self.__startingPosition


    def getFitness(self):
        return self.__f


    def __analyseSurface(self, row, column):
        if self.__exploredMap.getSurface()[row][column] != 1:
            if self.__exploredMap.getSurface()[row][column] != VISUALISED_CELL:
                self.__f += 1
            self.__exploredMap.getSurface()[row][column] = VISUALISED_CELL
            return True
        return False


    def __markVisualisedSurface(self):
        row = self.__startingPosition[0]
        # mark the cells to the right
        for column in range(self.__startingPosition[1]+1, MAP_LENGTH): 
            if not self.__analyseSurface(row, column):
                break

        # mark the cells to the left
        row = self.__startingPosition[0]
        for column in range(self.__startingPosition[1]-1, -1, -1):
            if not self.__analyseSurface(row, column):
                break

        # mark the cells upwards
        column = self.__startingPosition[1]
        for row in range(self.__startingPosition[0]-1, -1, -1):
            if not self.__analyseSurface(row, column):
                break

        # mark the cells downwards
        column = self.__startingPosition[1]
        for row in range(self.__startingPosition[0]+1, MAP_LENGTH):
            if not self.__analyseSurface(row, column):
                break

                
    def fitness(self, map):
        # computes the fitness for the individual and saves it in self.__f
        self.__f = 0
        self.__exploredMap = copy.deepcopy(map)
        surface = self.__exploredMap.getSurface()
        currentPosition = self.__startingPosition

        for gene in self.__chromosome:
            currentPosition = self.__startingPosition
            offset = np.array(offsets[gene.getValue()])
            currentPosition = np.add(currentPosition, offset) 
            if surface[currentPosition[0]][currentPosition[1]] == 1:
                self.__f = 0
                return
            self.__markVisualisedSurface()


    def getNormalizedFitness(self, totalPopulationFitness):
        return self.getFitness() / totalPopulationFitness
    

    def mutate(self, mutateProbability = 0.04):
        # bit-flip mutation
        if random() < mutateProbability:
            mutatedGeneIndex = randint(0, self.__size - 1)
            newGeneValue = randint(0, GENE_VALUES-1)
            self.__chromosome[mutatedGeneIndex] = newGeneValue
        
    
    def crossover(self, otherParent, crossoverProbability = 0.8):
        startingX, startingY = self.getStartingPosition()
        offspring1, offspring2 = Individual(startingX, startingY, self.__size), Individual(startingX, startingY, self.__size) 
        if random() < crossoverProbability:
            # we perform the single-point crossover between the self and the other parent 
            splitPoint = randint(2, self.__size - 3)
            otherChromosome = otherParent.getChromosome()
            offspring1.setChromosome(self.__chromosome[0:splitPoint] + otherChromosome[splitPoint:])
            offspring2.setChromosome(otherChromosome[0:splitPoint] + self.__chromosome[splitPoint:])
            print("Split point: {}; First parent: {}, Second parent: {}, First offspring: {}, Second offspring: {};".format(splitPoint, self, otherParent, offspring1, offspring2))
            return offspring1, offspring2
        return self, otherParent


    def __repr__(self):
        chromosomeAsString = ""
        for gene in self.__chromosome:
            chromosomeAsString += str(gene.getValue())
        return chromosomeAsString
    

class Population():
    def __init__(self, map, startX, startY, populationSize = 0, individualSize = 0):
        self.__populationSize = populationSize
        self.__map = map
        self.__individuals = [Individual(startX, startY, individualSize) for x in range(populationSize)]
        self.__totalFitness = 0 

    
    def getAllIndividuals(self):
        return self.__individuals


    def get(self, position):
        return self.__individuals[position]

    
    def addIndividual(self, individual):
        self.__individuals.append(individual)
        

    def evaluate(self):
        # evaluates the population
        for x in self.__individuals:
            x.fitness(self.__map)
            self.__totalFitness += x.getFitness()


    def getFitnesses(self):
        return [individual.getFitness() for individual in self.__individuals]
            
            
    def selection(self, k = 0):
        # roulette-wheel selection of k individuals
        randomChance = random()
        selectedIndividuals = []
        cdf = 0

        for individual in self.__individuals:
            if len(selectedIndividuals) == k:
                break
            
            cdf += individual.getNormalizedFitness(self.__totalFitness) 
            if cdf >= randomChance:
                selectedIndividuals.append(individual)

        
        print("SELECTED INDIVIDUALS: {}".format(selectedIndividuals))

        return selectedIndividuals 


class Map():
    def __init__(self, n = MAP_LENGTH, m = MAP_LENGTH):
        self.n = n
        self.m = m
        self.__surface = np.zeros((self.n, self.m))

    
    def getSurface(self):
        return self.__surface


    def setSurface(self, surface):
        self.__surface = surface

    
    def randomMap(self, fill = 0.2):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill :
                    self.surface[i][j] = 1


    def saveMap(self, numFile = "test.map"):
        with open(numFile,'wb') as f:
            pickle.dump(self, f)
            f.close()
        

    def loadMap(self, numfile):
        with open(numfile, "rb") as f:
            dummy = pickle.load(f)
            self.n = dummy.n
            self.m = dummy.m
            self.__surface = dummy.surface
            print("SELF.SURFACE AS OPPOSED TO SELF.__SURFACE: {}".format(self.__surface))
            f.close()
        

    def image(self, colour = BLUE, background = WHITE):
        mapImage = pygame.Surface((400,400))
        brick = pygame.Surface((20,20))
        brick.fill(BLUE)
        mapImage.fill(WHITE)
        for i in range(self.n):
            for j in range(self.m):
                if (self.surface[i][j] == 1):
                    mapImage.blit(brick, ( j * 20, i * 20))
                
        return mapImage

                
    def __str__(self):
        string=""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string