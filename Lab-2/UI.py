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
        pygame.init()
        self.logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(self.logo)
        pygame.display.set_caption("Path in simple environment")
        self.m = self.controller.getMap() 
        self.m.loadMap("test1.map")

        self.x = randint(0, 19)
        self.y = randint(0, 19)
        while self.m.surface[self.x][self.y]:
            (self.x, self.y) = (randint(0,19), randint(0,19))

        self.finalPosition = (randint(0,19), randint(0,19))
        while self.m.surface[self.finalPosition[0]][self.finalPosition[1]]:
            self.finalPosition = (randint(0,19), randint(0,19))

        self.running = True
        self.running2 = True

        self.d = Drone(self.x, self.y)
        self.d2 = Drone(self.x, self.y)

    
    def runGreedySearch(self):
        
        screen = pygame.display.set_mode((400,400))
        screen.fill(WHITE)
        
        lastTime = pygame.time.get_ticks()

        path = self.controller.searchGreedy(self.m, self.d, self.x, self.y, self.finalPosition[0], self.finalPosition[1])
        path2 = self.controller.searchAStar(self.m, self.d2, self.x, self.y, self.finalPosition[0], self.finalPosition[1])

        if path == "Failed.":
            print(path)
            print(self.m.surface)
            return

        if path2 == "Failed.":
            print(path2)
            print(self.m.surface)
            return

        pathCopy = path.copy()
        pathCopy2 = path2.copy()
        print("The non-optimal greedy path of length {} (red): {}".format(len(path), path))
        print("The correct A* path of length {} (green): {}".format(len(path2), path2))

        while self.running and self.running2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            screen.blit(self.d.mapWithDrone(self.m.image()),(0,0))
            screen.blit(self.d2.mapWithDrone(self.m.image()),(0,0))
            if pygame.time.get_ticks() - lastTime >= 300:
                lastTime = pygame.time.get_ticks()

                try:
                    self.d.x, self.d.y = path.pop(0)
                except IndexError as ie:
                    print("Done.")
                    self.running = False

                try:
                    self.d2.x, self.d2.y = path2.pop(0)
                except IndexError as ie:
                    print("Done.")
                    self.running2 = False

            pygame.display.flip()
        
        path = pathCopy 
        path2 = pathCopy2 
        screen.blit(self.controller.displayWithPath(self.controller.displayWithPath(self.m.image(), path, RED), path2, GREEN),(0,0))
        
        pygame.display.flip()
        time.sleep(5)
        pygame.quit()
    

    def run(self):
        self.runGreedySearch()