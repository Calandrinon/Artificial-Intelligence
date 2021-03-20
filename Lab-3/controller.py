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
        parents = population.selection(args[0])
        individualsWithChildren = []

        while len(parents) % 2 == 0 and len(parents) > 0:
            firstParent = parents.pop()
            firstParent.incrementAge()
            secondParent = parents.pop()
            secondParent.incrementAge()

            firstOffspring, secondOffspring = firstParent.crossover(secondParent)
            firstOffspring.mutate()
            secondOffspring.mutate()

            population.addIndividual(firstOffspring)
            population.addIndividual(secondOffspring)
            individualsWithChildren.append(firstParent)
            individualsWithChildren.append(secondParent)

        quarter = round(len(individualsWithChildren) / 4, 2)
        lastParentToSurvive = len(individualsWithChildren) - quarter
        individualsWithChildren.sort(reverse=True, key=lambda individual: individual.getFitness())

        for parent in range(0, lastParentToSurvive):
            population.addIndividual(parent) 

        fitnesses = np.array(population.getFitnesses())
        return (np.average(fitnesses), np.std(fitnesses))

        
    def run(self, args):
        # args - list of parameters needed in order to run the algorithm
        # args = [numberOfGenerations, selectedIndividualsFromAGeneration]
        if len(args) != 2:
            raise Exception("The number of parameters is incorrect.")
        
        # until stop condition
        #    perform an iteration
        #    save the information needed for the statistics
        # return the results and the info for statistics

        generationIndex = 0
        numberOfGenerations = args[0]
        selectedIndividualsFromAGeneration = args[1]
        allIterationAverages = []

        while generationIndex < numberOfGenerations:
            average, standardDeviation = self.iteration()
            allIterationAverages.append(average)
            print("Generation {}: Average={}, Standard deviation={};".format(generationIndex, average, standardDeviation))
            generationIndex += 1

        allIterationAverages = np.array(allIterationAverages)
        return (np.average(allIterationAverages), np.std(allIterationAverages))
    
    
    def solver(self, args):
        # args - list of parameters needed in order to run the solver
        # args = [numberOfGenerations, selectedIndividualsFromAGeneration, startingPositionX, startingPositionY, populationSize, individualSize]
        
        # create the population,
        # run the algorithm
        # return the results and the statistics
        self.__repository.createPopulation(args[2:])
        average, standardDeviation = self.run(args[0], args[1])

        return (average, standardDeviation)
