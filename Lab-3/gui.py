from pygame.locals import *
import pygame, time
from utils import *
from domain import *

import matplotlib.pyplot as plt
import numpy as np
import math

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



class GUI:
    def __init__(self, controller):
        self.__controller = controller 
        self.figure, self.axes = plt.subplots()
        self.axes.set_xlabel("Generation")
        self.axes.set_ylabel("Average fitness of the generation")
        self.x_axis = []
        self.y_axis = []


    def initPyGame(self, dimension):
        # init the pygame
        pygame.init()
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("drone exploration with AE")
        
        # create a surface on screen that has the size of 800 x 480
        screen = pygame.display.set_mode(dimension)
        screen.fill(WHITE)
        screen.blit
        return screen


    def closePyGame(self):
        pygame.quit()


    def closePygameOnEvent(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.closePyGame()
                    running = False


    def visualizeMap(self):
        map = self.__controller.getMap()
        screen = self.initPyGame((400,400))
        screen.blit(self.image(map), (0,0))
        pygame.display.flip()
        self.closePygameOnEvent()


    def validPosition(self, row, column):
        return row >= 0 and row < MAP_LENGTH and column >= 0 and column < MAP_LENGTH


    def movingDrone(self, currentMap, path, speed = 1):
        # animation of a drone on a path
        self.initPyGame((800, 400))
        screen = self.initPyGame((currentMap.n * 20, currentMap.m * 20))
        drona = pygame.image.load("drona.png")
        fittestIndividual = self.__controller.getTheFittestIndividual()
        print("Fittest individual's fitness: {}".format(fittestIndividual.getFitness()))
        exploredMap = copy.deepcopy(self.__controller.getMap()).getSurface()
        exploredCells = []

        for position in path:
            screen.blit(self.image(currentMap), (0,0))
            brick = pygame.Surface((20,20))
            brick.fill(GREEN)

            # mark the cells to the right
            row, column = copy.deepcopy(position[0]), copy.deepcopy(position[1])
            while self.validPosition(row, column) and exploredMap[row][column] != OCCUPIED_CELL:
                exploredCells.append((row, column))
                column += 1


            # mark the cells to the left
            row, column = copy.deepcopy(position[0]), copy.deepcopy(position[1])
            while self.validPosition(row, column) and exploredMap[row][column] != OCCUPIED_CELL:
                exploredCells.append((row, column))
                column -= 1

            # mark the cells upwards
            row, column = copy.deepcopy(position[0]), copy.deepcopy(position[1])
            while self.validPosition(row, column) and exploredMap[row][column] != OCCUPIED_CELL:
                exploredCells.append((row, column))
                row -= 1

            # mark the cells downwards
            row, column = copy.deepcopy(position[0]), copy.deepcopy(position[1])
            while self.validPosition(row, column) and exploredMap[row][column] != OCCUPIED_CELL:
                exploredCells.append((row, column))
                row += 1

            for cell in exploredCells:
                screen.blit(brick, (cell[1] * 20, cell[0] * 20))
            row, column = position[0], position[1]
            screen.blit(drona, (column * 20, row * 20))
            pygame.display.flip()
            time.sleep(1/speed)            
            
        self.closePyGame()
            

    def image(self, currentMap, colour = BLUE, background = WHITE):
        # creates the image of a map
        
        imagine = pygame.Surface((currentMap.n * 20, currentMap.m * 20))
        brick = pygame.Surface((20,20))
        brick.fill(colour)
        imagine.fill(background)
        for i in range(currentMap.n):
            for j in range(currentMap.m):
                if (currentMap.getSurface()[i][j] == 1):
                    imagine.blit(brick, ( j * 20, i * 20))
                    
        return imagine        


    def refreshPlot(self, generation, averageFitness):
        self.x_axis.append(generation)
        self.y_axis.append(averageFitness)
        self.axes.plot(self.x_axis, self.y_axis)
        plt.pause(0.05)


    def renderTheFittestIndividual(self):
        try:
            fittestIndividual = self.__controller.getTheFittestIndividual()
            print("fittestIndividual: ")
            print(fittestIndividual)
            map = self.__controller.getMap()
            self.movingDrone(map, fittestIndividual.getPath(), 15)
        except Exception as e:
            raise Exception("No individuals have survived... R.I.P")


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
        totalAverages = 0
        while generationIndex < numberOfGenerations:
            average, standardDeviation, normalizedStandardDeviation = self.__controller.iteration([parentsToBeSelected])
            allIterationAverages.append(average)
            print("Generation {}: Average={}, Standard deviation={}; Population size: {}".format(generationIndex, average, standardDeviation, self.__controller.getPopulationSize()))
            self.refreshPlot(generationIndex, average)
            try:
                self.renderTheFittestIndividual()
            except Exception as e:
                print("Ashes to ashes, dust to dust...")
                break
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