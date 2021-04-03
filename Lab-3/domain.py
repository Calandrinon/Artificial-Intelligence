from random import *
from utils import *
import numpy as np
import pickle
import copy


class Gene:
    def __init__(self):
        # initialise the Gene randomly according to the representation
        self.__value = randint(0, GENE_VALUES-1)

    def getValue(self):
        # gets the gene's value (can be 0, 1, 2 or 3, due to the fact that there are 4 directions the drone can opt for)
        return self.__value

    def setValue(self, newValue):
        self.__value = newValue

    def __repr__(self):
        return str(self.__value)


class Individual:
    def __init__(self, x, y, size = 0):
        self.__size = size
        self.__chromosome = [Gene() for i in range(self.__size)]
        self.__startingPosition = np.array([x, y])
        self.__currentPosition = self.__startingPosition
        self.__f = 0
        self.__exploredMap = None
        self.__age = 0
        self.__path = []


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


    def getPath(self):
        return self.__path

    
    def getExploredMap(self):
        return self.__exploredMap


    def __analyseSurface(self, row, column):
        if self.__exploredMap.getSurface()[row][column] != 1:
            if self.__exploredMap.getSurface()[row][column] != VISUALISED_CELL:
                self.__f += 1
            surface = self.__exploredMap.getSurface()
            surface[row][column] = VISUALISED_CELL
            self.__exploredMap.setSurface(surface)
            return True
        return False


    def __markVisualisedSurface(self):
        row = self.__currentPosition[0]
        # mark the cells to the right
        for column in range(self.__currentPosition[1], MAP_LENGTH): 
            if not self.__analyseSurface(row, column):
                break

        # mark the cells to the left
        row = self.__currentPosition[0]
        for column in range(self.__currentPosition[1]-1, -1, -1):
            if not self.__analyseSurface(row, column):
                break

        # mark the cells upwards
        column = self.__currentPosition[1]
        for row in range(self.__currentPosition[0], -1, -1):
            if not self.__analyseSurface(row, column):
                break

        # mark the cells downwards
        column = self.__currentPosition[1]
        for row in range(self.__currentPosition[0]+1, MAP_LENGTH):
            if not self.__analyseSurface(row, column):
                break


    def __validPosition(self, row, column):
        return row >= 0 and row < MAP_LENGTH and column >= 0 and column < MAP_LENGTH

                
    def fitness(self, map):
        # computes the fitness for the individual and saves it in self.__f
        self.__f = 0
        self.__exploredMap = copy.deepcopy(map)
        surface = self.__exploredMap.getSurface()
        self.__currentPosition = self.__startingPosition
        self.__path = []
        self.__path.append(self.__currentPosition)

        for gene in self.__chromosome:
            offset = np.array(offsets[gene.getValue()])
            self.__currentPosition = np.add(self.__currentPosition, offset) 

            if not self.__validPosition(self.__currentPosition[0], self.__currentPosition[1]): # in case the chromosome leads the drone to go out of the matrix boundaries
                return self.__f

            if surface[self.__currentPosition[0]][self.__currentPosition[1]] == 1:
                return self.__f

            self.__markVisualisedSurface()
            self.__path.append(self.__currentPosition)

        return self.__f


    def getNormalizedFitness(self, totalPopulationFitness):
        return self.getFitness() / totalPopulationFitness
    

    def mutate(self, mutateProbability = 0.04):
        # bit-flip mutation
        
        if random() < mutateProbability:
            mutatedGeneIndex = randint(0, self.__size - 1)
            newGeneValue = randint(0, GENE_VALUES-1)
            self.__chromosome[mutatedGeneIndex] = Gene()
            self.__chromosome[mutatedGeneIndex].setValue(newGeneValue)
        
    
    def crossover(self, otherParent, crossoverProbability = 0.8):
        startingX, startingY = self.getStartingPosition()
        offspring1, offspring2 = Individual(startingX, startingY, self.__size), Individual(startingX, startingY, self.__size) 
        if random() < crossoverProbability:
            # we perform the single-point crossover between the self and the other parent 
            splitPoint = randint(2, self.__size - 3)
            otherChromosome = otherParent.getChromosome()
            offspring1.setChromosome(self.__chromosome[0:splitPoint] + otherChromosome[splitPoint:])
            offspring2.setChromosome(otherChromosome[0:splitPoint] + self.__chromosome[splitPoint:])

        return offspring1, offspring2 


    def __repr__(self):
        chromosomeAsString = ""
        for gene in self.__chromosome:
            chromosomeAsString += str(gene.getValue())
        return chromosomeAsString


    def __gt__(self, other):
        return self.__f > other.__f
    

class Population():
    def __init__(self, map, startX, startY, populationSize = 0, individualSize = 0):
        self.__populationSize = populationSize
        self.__map = copy.deepcopy(map)
        self.__individualSize = individualSize
        self.__startX, self.__startY = startX, startY
        self.__individuals = [Individual(startX, startY, individualSize) for x in range(populationSize)]
        self.__totalFitness = 0 

    
    def getAllIndividuals(self):
        return self.__individuals

    
    def __setIndividuals(self, individuals):
        self.__individuals = individuals


    def get(self, position):
        return self.__individuals[position]

    
    def addIndividual(self, individual):
        self.__individuals.append(individual)


    def getTheFittestIndividual(self):
        if len(self.__individuals) == 0:
            raise Exception("No individuals have survived... R.I.P")
        return max(self.__individuals)
        

    def evaluate(self):
        # evaluates the population
        self.__totalFitness = 0
        for x in self.__individuals:
            x.fitness(self.__map)
            self.__totalFitness += x.getFitness()

        return self.__totalFitness


    def getFitnesses(self):
        return [individual.getFitness() for individual in self.__individuals]
            
            
    def selection(self, k = 0):
        # roulette-wheel selection 
        selectedIndividuals = []
        self.__individuals.sort(key=lambda x: x.getFitness())
        numberOfIndividuals = len(self.__individuals) 

        for index in range(numberOfIndividuals - 1, int(numberOfIndividuals - k - 1), -1):
            selectedIndividuals.append(self.__individuals[index])

        self.__individuals = selectedIndividuals
        print("Selected individuals: {}".format(self.__individuals))


    def merge(self, other):
        sizeOfTheFirstPopulation = len(self.__individuals)
        sizeOfTheSecondPopulation = len(other.getAllIndividuals())
        newPopulation = Population(self.__map, self.__startX, self.__startY, sizeOfTheFirstPopulation+sizeOfTheSecondPopulation, self.__individualSize) 

        firstPopulationIndividuals = self.__individuals
        secondPopulationIndividuals = other.getAllIndividuals()
        newPopulation.__setIndividuals(firstPopulationIndividuals + secondPopulationIndividuals)
        return newPopulation

    
    def __repr(self):
        return str(self.__individuals)


class Map():
    def __init__(self, n = MAP_LENGTH, m = MAP_LENGTH):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))

    
    def getSurface(self):
        return self.surface


    def setSurface(self, surface):
        self.surface = surface


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
            self.surface = dummy.surface
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