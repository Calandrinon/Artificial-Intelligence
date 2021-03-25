# -*- coding: utf-8 -*-


# imports
from gui import *
from controller import *
from repository import *
from domain import *


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

def main():
    numberOfGenerations = 30
    selectedIndividualsFromAGeneration = 10
    startingPosition = (5, 5)
    populationSize = 20
    individualSize = 10 # 10 is the length of the longest path the drone can take

    repository = Repository()
    repository.createPopulation([startingPosition[0], startingPosition[1], populationSize, individualSize])
    controller = Controller(repository)
    
    finalStatistics = controller.solver([numberOfGenerations, selectedIndividualsFromAGeneration, startingPosition[0], startingPosition[1], populationSize, individualSize])
    print("Average & standard deviation: {}".format(finalStatistics))


main()