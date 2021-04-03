from repository import *
import numpy as np
import sys

class Controller():
    def __init__(self, repository):
        self.__repository = repository
    

    def iteration(self, args):
        # args - list of parameters needed to run one iteration
        # args = [individualsToBeSelected]

        # an iteration:
        # selection of the parents
        # create offsprings by crossover of the parents
        # apply some mutations
        # selection of the survivors

        # individualsToBeSelected = args[0]
        oldPopulationSize = self.getPopulationSize()
        individualsToBeSelected = int(oldPopulationSize * (95/100))

        population = self.__repository.getTheMostRecentPopulation()
        populationFitness = population.evaluate() 
        #print("POPULATION={}".format(population.getAllIndividuals()))
        print("Selecting parents...")
        population.selection(individualsToBeSelected)
        parents = population.getAllIndividuals()
        allOffspring = []
        individualsThatReproduced = []

        while len(parents) >= 2:
            firstParent = parents.pop()
            firstParent.incrementAge()
            secondParent = parents.pop()
            secondParent.incrementAge()

            firstOffspring, secondOffspring = firstParent.crossover(secondParent)
            if firstOffspring == firstParent and secondOffspring == secondParent:
                continue
            firstOffspring.mutate()
            secondOffspring.mutate()

            individualsThatReproduced.append(firstParent)
            individualsThatReproduced.append(secondParent)
            allOffspring.append(firstOffspring)
            allOffspring.append(secondOffspring)

        for parent in individualsThatReproduced:
            population.addIndividual(parent)
        for individual in allOffspring:
            population.addIndividual(individual)
        population.evaluate()

        print("Selecting survivors...")
        individualsToBeSelected = int(oldPopulationSize * 85/100)
        population.selection(individualsToBeSelected)
        self.__repository.addNewPopulation(population)
        fitnesses = np.array(population.getFitnesses())

        mean = np.average(fitnesses)
        standardDeviation = np.std(fitnesses)
        normalizedStandardDeviation = standardDeviation/mean

        if mean == 0:
            print("Null mean...")
            sys.exit()

        return (mean, standardDeviation, normalizedStandardDeviation)

    
    def getTheFittestIndividual(self):
        population = self.__repository.getTheMostRecentPopulation()
        try:
            return population.getTheFittestIndividual()
        except Exception as e:
            raise Exception("No individuals have survived.")


    def getMap(self):
        return self.__repository.getMap()

    
    def createPopulation(self, startX, startY, populationSize, individualSize):
        self.__repository.createPopulation([startX, startY, populationSize, individualSize])


    def createRandomMap(self):
        self.__repository.createRandomMap()


    def loadMap(self, fileName):
        self.__repository.loadMap(fileName)


    def saveMap(self, fileName):
        self.__repository.saveMap(fileName)

    def mergeAllPopulations(self):
        self.__repository.mergePopulations()

    def getPopulationSize(self):
        return len(self.__repository.getTheMostRecentPopulation().getAllIndividuals())

    def resetRepository(self):
        self.__repository.resetRepository()