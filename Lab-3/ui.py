# -*- coding: utf-8 -*-jj
# imports
# create a menu
#   1. map options:
#         a. create random map
#         b. load a map
#         c. save a map
#         d visualise map
#   2. EA options:
#         a. parameters setup
#         b. run the solver
#         c. visualise the statistics
#         d. view the drone moving on a path
#              function gui.movingDrone(currentMap, path, speed, markseen)
#              ATENTION! the function doesn't check if the path passes trough walls

import matplotlib.pyplot as plt
import numpy as np
import math


class UI:
    def __init__(self, controller):
        self.__controller = controller 
        self.figure, self.axes = plt.subplots()
        self.x_axis = []
        self.y_axis = []


    def refreshPlot(self, generation, averageFitness):
        self.x_axis.append(generation)
        self.y_axis.append(averageFitness)
        self.axes.plot(self.x_axis, self.y_axis)
        plt.pause(0.05)


    def run(self, args):
        # args - list of parameters needed in order to run the algorithm
        # args = [numberOfGenerations, selectedIndividualsFromAGeneration]
        if len(args) != 2:
            raise Exception("The number of parameters is incorrect.")
        
        # until stop condition
        #    perform an iteration
        #    save the information needed for the statistics
        # return the results and the info for statistics
        parentsToBeSelected = args[1]

        generationIndex = 0
        numberOfGenerations = args[0]
        selectedIndividualsFromAGeneration = args[1]
        allIterationAverages = []

        while generationIndex < numberOfGenerations:
            average, standardDeviation = self.__controller.iteration([parentsToBeSelected])
            allIterationAverages.append(average)
            print("Generation {}: Average={}, Standard deviation={};".format(generationIndex, average, standardDeviation))
            self.refreshPlot(generationIndex, average)
            generationIndex += 1

        allIterationAverages = np.array(allIterationAverages)
        plt.show()
        return (np.average(allIterationAverages), np.std(allIterationAverages))


    def solver(self, args):
        # args - list of parameters needed in order to run the solver
        # args = [numberOfGenerations, selectedIndividualsFromAGeneration, startingPositionX, startingPositionY, populationSize, individualSize]
        
        # create the population,
        # run the algorithm
        # return the results and the statistics
        average, standardDeviation = self.run(args[:2])

        return (average, standardDeviation)