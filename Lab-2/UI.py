import pickle,pygame,time
from pygame.locals import *
from random import random, randint
from Domain import *
import numpy as np
import heapq
import math
import time

class UI:
    def __init__(self, controller):
        self.controller = controller 
        self.initializePygame()
        self.generateStartAndFinishPosition()
        self.d = Drone(self.x, self.y)
        self.d2 = Drone(self.x, self.y)

    
    def initializePygame(self):
        pygame.init()
        pygame.display.set_icon(pygame.image.load("logo32x32.png"))
        pygame.display.set_caption("Path in simple environment")
        self.controller.getMap().loadMap("test1.map")
        self.screen = pygame.display.set_mode((400,400))
        self.screen.fill(WHITE)


    def generateStartAndFinishPosition(self):
        self.x = randint(0, 19)
        self.y = randint(0, 19)
        while self.controller.getMap().surface[self.x][self.y]:
            (self.x, self.y) = (randint(0,19), randint(0,19))
        self.initialPosition = (self.x, self.y)

        self.finalPosition = (randint(0,19), randint(0,19))
        while self.controller.getMap().surface[self.finalPosition[0]][self.finalPosition[1]]:
            self.finalPosition = (randint(0,19), randint(0,19))


    def readPositions(self):
        self.x = int(input("Enter the initial X coordinate: "))
        self.y = int(input("Enter the initial Y coordinate: "))
        
        while self.controller.getMap().surface[self.x][self.y]:
            print("Invalid position!")
            self.x = int(input("Enter the initial X coordinate: "))
            self.y = int(input("Enter the initial Y coordinate: "))
        self.initialPosition = (self.x, self.y)

        finalX = int(input("Enter the final X coordinate: "))
        finalY = int(input("Enter the final Y coordinate: "))
        self.finalPosition = (finalX, finalY)
        while self.controller.getMap().surface[self.finalPosition[0]][self.finalPosition[1]]:
            print("Invalid position!")
            finalX = int(input("Enter the final X coordinate: "))
            finalY = int(input("Enter the final Y coordinate: "))
            self.finalPosition = (finalX, finalY)


    def runAStarSearch(self):
        self.readPositions()
        runningAStar = True
        lastTime = pygame.time.get_ticks()

        path2, executionTimeAStar = self.controller.searchAStar(self.controller.getMap(), self.d2, self.x, self.y, self.finalPosition[0], self.finalPosition[1])
        print("A* -> Execution time: {}".format(executionTimeAStar))

        if path2 == "Failed.":
            print(path2)
            print(self.controller.getMap().surface)
            return

        pathCopy2 = path2.copy()
        print("Initial position: {}; Final position: {}".format(self.initialPosition, self.finalPosition))
        print("The A* path of length {} (green): {}".format(len(path2), path2))

        while runningAStar:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.screen.blit(self.d2.mapWithDrone(self.controller.getMap().image()),(0,0))
            if pygame.time.get_ticks() - lastTime >= 300:
                lastTime = pygame.time.get_ticks()

                try:
                    self.d2.x, self.d2.y = path2.pop(0)
                except IndexError as ie:
                    print("Done.")
                    runningAStar = False

            pygame.display.flip()
        
        self.screen.blit(self.controller.displayWithPath(self.controller.getMap().image(), pathCopy2, GREEN),(0,0))
        
        pygame.display.flip()
        time.sleep(5)
        pygame.quit()


    def runGreedySearch(self):
        runningGreedy = True
        lastTime = pygame.time.get_ticks()

        path, executionTimeGreedy = self.controller.searchGreedy(self.controller.getMap(), self.d, self.x, self.y, self.finalPosition[0], self.finalPosition[1])
        print("Greedy -> Execution time: {}".format(executionTimeGreedy))

        if path == "Failed.":
            print(path)
            print(self.controller.getMap().surface)
            return

        pathCopy = path.copy()
        print("Initial position: {}; Final position: {}".format(self.initialPosition, self.finalPosition))
        print("The greedy path of length {} (red): {}".format(len(path), path))

        while runningGreedy:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.screen.blit(self.d.mapWithDrone(self.controller.getMap().image()),(0,0))
            if pygame.time.get_ticks() - lastTime >= 300:
                lastTime = pygame.time.get_ticks()

                try:
                    self.d.x, self.d.y = path.pop(0)
                except IndexError as ie:
                    print("Done.")
                    runningGreedy = False

            pygame.display.flip()
        
        self.screen.blit(self.controller.displayWithPath(self.controller.getMap().image(), pathCopy, RED), (0,0))
        
        pygame.display.flip()
        time.sleep(5)
        pygame.quit()

    
    def runGreedyAndAStarSearchWithRandomPositions(self):
        runningAStar = True
        runningGreedy = True
        lastTime = pygame.time.get_ticks()

        path, executionTimeGreedy = self.controller.searchGreedy(self.controller.getMap(), self.d, self.x, self.y, self.finalPosition[0], self.finalPosition[1])
        path2, executionTimeAStar = self.controller.searchAStar(self.controller.getMap(), self.d2, self.x, self.y, self.finalPosition[0], self.finalPosition[1])
        print("A* -> Execution time: {}".format(executionTimeAStar))
        print("Greedy -> Execution time: {}".format(executionTimeGreedy))

        if path == "Failed.":
            print(path)
            print(self.controller.getMap().surface)
            return

        if path2 == "Failed.":
            print(path2)
            print(self.controller.getMap().surface)
            return

        pathCopy = path.copy()
        pathCopy2 = path2.copy()
        print("Initial position: {}; Final position: {}".format(self.initialPosition, self.finalPosition))
        print("The non-optimal greedy path of length {} (red): {}".format(len(path), path))
        print("The correct A* path of length {} (green): {}".format(len(path2), path2))

        while runningAStar and runningGreedy:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.screen.blit(self.d.mapWithDrone(self.controller.getMap().image()),(0,0))
            self.screen.blit(self.d2.mapWithDrone(self.controller.getMap().image()),(0,0))
            if pygame.time.get_ticks() - lastTime >= 300:
                lastTime = pygame.time.get_ticks()

                try:
                    self.d.x, self.d.y = path.pop(0)
                except IndexError as ie:
                    print("Done.")
                    runningGreedy = False

                try:
                    self.d2.x, self.d2.y = path2.pop(0)
                except IndexError as ie:
                    print("Done.")
                    runningAStar = False

            pygame.display.flip()
        
        self.screen.blit(self.controller.displayWithPath(self.controller.displayWithPath(self.controller.getMap().image(), pathCopy, RED), pathCopy2, GREEN),(0,0))
        
        pygame.display.flip()
        time.sleep(5)
        pygame.quit()
    

    def run(self):
        self.runGreedyAndAStarSearchWithRandomPositions()