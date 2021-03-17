import Repository
import time
import heapq
import math
import pygame
from Exceptions import *
from random import random, randint

class Controller:
    def __init__(self, repository):
        self.repository = repository

    def getMap(self):
        return self.repository.getMap()

    def getPath(self, finalNode, initialNode, predecessors):
        currentNode = finalNode
        print("finalNode: {}".format(finalNode))
        path = []
        
        while currentNode != initialNode:
            currentNode = predecessors[currentNode]
            path = [currentNode] + path
        
        path.append(finalNode)
        return path


    def heuristic(self, node, goalNode):
        # This is just the straight-line distance between (x,y) and the goal
        return math.sqrt((node[0]-goalNode[0])**2 + (node[1]-goalNode[1])**2)


    def validNode(self, x, y):
        if x >= 0 and x <= 19 and y >= 0 and y <= 19:
            return True
        return False


    def searchAStar(self, mapM, droneD, initialX, initialY, finalX, finalY):
        startTime = time.time()

        openSet = []
        initialNode = (initialX, initialY)
        finalNode = (finalX, finalY)

        predecessors = {}
        gScore = {}
        fScore = {}
        for i in range(0, mapM.getWidth()):
            for j in range(0, mapM.getHeight()):
                gScore[(i, j)] = float('inf')
                fScore[(i, j)] = float('inf')
        gScore[initialNode] = 0
        fScore[initialNode] = self.heuristic(initialNode, finalNode)
        heapq.heappush(openSet, (fScore[initialNode], initialNode))
        offsets = [[0, 1], [1, 0], [0, -1], [-1, 0]]

        while len(openSet) != 0:
            currentNode = heapq.heappop(openSet)[1]

            if currentNode == (finalX, finalY):
                endTime = time.time()
                return (self.getPath(finalNode, initialNode, predecessors), endTime - startTime)

            for offset in range(0, 4):
                neighbourX = offsets[offset][0] + currentNode[0]
                neighbourY = offsets[offset][1] + currentNode[1]
                neighbourNode = (neighbourX, neighbourY)

                if not self.validNode(neighbourX, neighbourY) or mapM.surface[neighbourX][neighbourY] != 0: # if the node can't be accessed
                    continue 

                possibleGScore = gScore[currentNode] + 1 
                if possibleGScore < gScore[neighbourNode]:
                    predecessors[neighbourNode] = currentNode
                    gScore[neighbourNode] = possibleGScore
                    fScore[neighbourNode] = gScore[neighbourNode] + self.heuristic(neighbourNode, (finalX, finalY))
                    if neighbourNode not in openSet:
                        heapq.heappush(openSet, (fScore[neighbourNode], neighbourNode))
        
        raise FailedSearchException("The algorithm failed because the final position could not be reached.\nCheck if the final position is reachable.")
        
        
    def searchGreedy(self, mapM, droneD, initialX, initialY, finalX, finalY):
        startTime = time.time()
        openSet = []
        initialNode = (initialX, initialY)
        finalNode = (finalX, finalY)
        visited = []

        predecessors = {}
        heapq.heappush(openSet, (self.heuristic(initialNode, finalNode), initialNode))
        offsets = [[0, 1], [1, 0], [0, -1], [-1, 0]]

        while len(openSet) != 0:
            currentNode = heapq.heappop(openSet)[1]

            if currentNode == (finalX, finalY):
                endTime = time.time()
                return (self.getPath(finalNode, initialNode, predecessors), endTime - startTime)

            minimumHScore = float('inf')
            for offset in range(0, 4):
                neighbourX = offsets[offset][0] + currentNode[0]
                neighbourY = offsets[offset][1] + currentNode[1]
                neighbourNode = (neighbourX, neighbourY)

                if neighbourNode in visited or not self.validNode(neighbourX, neighbourY) or mapM.surface[neighbourX][neighbourY] != 0: # if the node can't be accessed
                    continue 

                visited.append(neighbourNode)
                heapq.heappush(openSet, (self.heuristic(currentNode, finalNode), neighbourNode))
                predecessors[neighbourNode] = currentNode

        raise FailedSearchException("The algorithm failed because the final position could not be reached.\nCheck if the final position is reachable.")

    def dummysearch(self):
        #example of some path in test1.map from [5,7] to [7,11]
        return [[5,7],[5,8],[5,9],[5,10],[5,11],[6,11],[7,11]]
        
    def displayWithPath(self, image, path, color):
        mark = pygame.Surface((20,20))
        mark.fill(color)
        for move in path:
            image.blit(mark, (move[1] *20, move[0] * 20))
            
        return image


    def getGreedyDrone(self):
        return self.repository.getGreedyDrone()


    def getAStarDrone(self):
        return self.repository.getAStarDrone()


    def setAStarDronePosition(self, x, y):
        drone = self.repository.getAStarDrone()
        drone.setPosition(x, y)
        self.repository.setAStarDrone(drone)


    def setGreedyDronePosition(self, x, y):
        drone = self.repository.getGreedyDrone()
        drone.setPosition(x, y)
        self.repository.setGreedyDrone(drone)


    def generateStartAndFinishPosition(self):
        x = randint(0, 19)
        y = randint(0, 19)
        while self.getMap().surface[x][y]:
            (x, y) = (randint(0,19), randint(0,19))
        initialPosition = (x, y)

        finalPosition = (randint(0,19), randint(0,19))
        while self.getMap().surface[finalPosition[0]][finalPosition[1]]:
            finalPosition = (randint(0,19), randint(0,19))

        return [initialPosition, finalPosition]