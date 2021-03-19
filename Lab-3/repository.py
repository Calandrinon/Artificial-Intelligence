# -*- coding: utf-8 -*-

import pickle
from domain import *


class Repository():
    def __init__(self):
        self.__populations = []
        self.__cmap = Map()
        

    def createPopulation(self, args): 
        # args = [populationSize, individualSize] -- you can add more args    
        return Population(args[0], args[1])
        

    def getMap(self):
        return self.__cmap

    # TO DO : add the other components for the repository: 
    #    load and save from file, etc
            