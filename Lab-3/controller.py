from repository import *
import numpy as np


class Controller():
    def __init__(self, repository):
        self.__repository = repository
    

    def iteration(self, args):
        # args - list of parameters needed to run one iteration
        # args = [parentsToBeSelected]

        # an iteration:
        # selection of the parents
        # create offsprings by crossover of the parents
        # apply some mutations
        # selection of the survivors

        population = self.__repository.getTheMostRecentPopulation()
        population.evaluate() 
        #print("POPULATION={}".format(population.getAllIndividuals()))
        parents = population.selection(args[0])

        while len(parents) >= 2:
            firstParent = parents.pop()
            firstParent.incrementAge()
            secondParent = parents.pop()
            secondParent.incrementAge()

            firstOffspring, secondOffspring = firstParent.crossover(secondParent)
            if firstOffspring == firstParent and secondOffspring == secondParent:
                population.addIndividual(firstParent)
                population.addIndividual(secondParent)
                continue
            firstOffspring.mutate()
            secondOffspring.mutate()

            population.addIndividual(firstOffspring)
            population.addIndividual(secondOffspring)

        fitnesses = np.array(population.getFitnesses())
        self.__repository.addNewPopulation(population)

        return (np.average(fitnesses), np.std(fitnesses))

    
    def getTheFittestIndividual(self):
        population = self.__repository.getTheMostRecentPopulation()
        return population.getTheFittestIndividual()


    def getMap(self):
        return self.__repository.getMap()