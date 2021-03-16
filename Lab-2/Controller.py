import Repository
import time
import heapq
import math
import pygame

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
        # TO DO 
        # implement the search function and put it in controller
        # returns a list of moves as a list of pairs [x,y] 
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
        print("Initial position: {}; Final position: {}".format(initialNode, finalNode))
        offsets = [[0, 1], [1, 0], [0, -1], [-1, 0]]

        while len(openSet) != 0:
            currentNode = heapq.heappop(openSet)[1]

            if currentNode == (finalX, finalY):
                endTime = time.time()
                print("A* -> Execution time: {}".format(endTime-startTime))
                return self.getPath(finalNode, initialNode, predecessors)

            validNodes = 0
            for offset in range(0, 4):
                neighbourX = offsets[offset][0] + currentNode[0]
                neighbourY = offsets[offset][1] + currentNode[1]
                neighbourNode = (neighbourX, neighbourY)

                if not self.validNode(neighbourX, neighbourY) or mapM.surface[neighbourX][neighbourY] != 0: # if the node can't be accessed
                    continue 

                validNodes += 1
                possibleGScore = gScore[currentNode] + 1 
                if possibleGScore < gScore[neighbourNode]:
                    predecessors[neighbourNode] = currentNode
                    gScore[neighbourNode] = possibleGScore
                    fScore[neighbourNode] = gScore[neighbourNode] + self.heuristic(neighbourNode, (finalX, finalY))
                    if neighbourNode not in openSet:
                        heapq.heappush(openSet, (fScore[neighbourNode], neighbourNode))
            #print("currentNode: {}; validNodes: {};".format(currentNode, validNodes))
        
        endTime = time.time()
        print("A* -> Execution time: {}".format(endTime-startTime))
        return "Failed."
        
        
    def searchGreedy(self, mapM, droneD, initialX, initialY, finalX, finalY):
        # TO DO 
        # implement the search function and put it in controller
        # returns a list of moves as a list of pairs [x,y]

        startTime = time.time()
        openSet = []
        initialNode = (initialX, initialY)
        finalNode = (finalX, finalY)
        visited = []

        predecessors = {}
        heapq.heappush(openSet, (self.heuristic(initialNode, finalNode), initialNode))
        print("Initial position: {}; Final position: {}".format(initialNode, finalNode))
        offsets = [[0, 1], [1, 0], [0, -1], [-1, 0]]

        while len(openSet) != 0:
            currentNode = heapq.heappop(openSet)[1]

            if currentNode == (finalX, finalY):
                endTime = time.time()
                print("Greedy -> Execution time: {}".format(endTime-startTime))
                return self.getPath(finalNode, initialNode, predecessors)

            validNodes = 0
            minimumHScore = float('inf')
            for offset in range(0, 4):
                neighbourX = offsets[offset][0] + currentNode[0]
                neighbourY = offsets[offset][1] + currentNode[1]
                neighbourNode = (neighbourX, neighbourY)

                if neighbourNode in visited or not self.validNode(neighbourX, neighbourY) or mapM.surface[neighbourX][neighbourY] != 0: # if the node can't be accessed
                    continue 

                validNodes += 1
                visited.append(neighbourNode)
                heapq.heappush(openSet, (self.heuristic(currentNode, finalNode), neighbourNode))
                predecessors[neighbourNode] = currentNode

            #print("currentNode: {}; validNodes: {};".format(currentNode, validNodes))

        endTime = time.time()
        print("Greedy -> Execution time: {}".format(endTime-startTime))
        return "Failed."

    def dummysearch(self):
        #example of some path in test1.map from [5,7] to [7,11]
        return [[5,7],[5,8],[5,9],[5,10],[5,11],[6,11],[7,11]]
        
    def displayWithPath(self, image, path, color):
        mark = pygame.Surface((20,20))
        mark.fill(color)
        for move in path:
            image.blit(mark, (move[1] *20, move[0] * 20))
            
        return image