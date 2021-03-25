# -*- coding: utf-8 -*-

import pickle
from domain import *


class Repository():
    def __init__(self):
        self.__populations = []
        self.__cmap = Map()
        self.__cmap.loadMap("test1.map")
        

    def createPopulation(self, args): 
        # args = [startX, startY, populationSize, individualSize]
        population = Population(self.__cmap, args[0], args[1], args[2], args[3])
        self.__populations.append(population)

        return population


    def addNewPopulation(self, population):
        self.__populations.append(population)
        

    def getMap(self):
        return self.__cmap


    def getTheMostRecentPopulation(self):
        if len(self.__populations) == 0:
            raise Exception("There are no populations in the repository.")
        return self.__populations[-1]

    # TO DO : add the other components for the repository: 
    #    load and save from file, etc
            