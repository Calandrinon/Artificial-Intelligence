# import the pygame module, so you can use it
import pickle,pygame,time
from pygame.locals import *
from random import random, randint
import numpy as np
import heapq
import math
import time

# Greedy BFS algorithm path is RED 
# A* algorithm path is GREEN



def getPath(finalNode, initialNode, predecessors):
    currentNode = finalNode
    print("finalNode: {}".format(finalNode))
    path = []
    
    while currentNode != initialNode:
        currentNode = predecessors[currentNode]
        path = [currentNode] + path
    
    path.append(finalNode)
    return path


def heuristic(node, goalNode):
    # This is just the straight-line distance between (x,y) and the goal
    return math.sqrt((node[0]-goalNode[0])**2 + (node[1]-goalNode[1])**2)


def validNode(x, y):
    if x >= 0 and x <= 19 and y >= 0 and y <= 19:
        return True
    return False


def searchAStar(mapM, droneD, initialX, initialY, finalX, finalY):
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
    fScore[initialNode] = heuristic(initialNode, finalNode)
    heapq.heappush(openSet, (fScore[initialNode], initialNode))
    print("Initial position: {}; Final position: {}".format(initialNode, finalNode))

    while len(openSet) != 0:
        currentNode = heapq.heappop(openSet)[1]

        if currentNode == (finalX, finalY):
            endTime = time.time()
            print("A* -> Execution time: {}".format(endTime-startTime))
            return getPath(finalNode, initialNode, predecessors)

        validNodes = 0
        for offset in range(0, 4):
            neighbourX = offsets[offset][0] + currentNode[0]
            neighbourY = offsets[offset][1] + currentNode[1]
            neighbourNode = (neighbourX, neighbourY)

            if not validNode(neighbourX, neighbourY) or mapM.surface[neighbourX][neighbourY] != 0: # if the node can't be accessed
                continue 

            validNodes += 1
            possibleGScore = gScore[currentNode] + 1 
            if possibleGScore < gScore[neighbourNode]:
                predecessors[neighbourNode] = currentNode
                gScore[neighbourNode] = possibleGScore
                fScore[neighbourNode] = gScore[neighbourNode] + heuristic(neighbourNode, (finalX, finalY))
                if neighbourNode not in openSet:
                    heapq.heappush(openSet, (fScore[neighbourNode], neighbourNode))
        #print("currentNode: {}; validNodes: {};".format(currentNode, validNodes))
    
    endTime = time.time()
    print("A* -> Execution time: {}".format(endTime-startTime))
    return "Failed."
    
    
def searchGreedy(mapM, droneD, initialX, initialY, finalX, finalY):
    # TO DO 
    # implement the search function and put it in controller
    # returns a list of moves as a list of pairs [x,y]

    startTime = time.time()
    openSet = []
    initialNode = (initialX, initialY)
    finalNode = (finalX, finalY)
    visited = []

    predecessors = {}
    heapq.heappush(openSet, (heuristic(initialNode, finalNode), initialNode))
    print("Initial position: {}; Final position: {}".format(initialNode, finalNode))

    while len(openSet) != 0:
        currentNode = heapq.heappop(openSet)[1]

        if currentNode == (finalX, finalY):
            endTime = time.time()
            print("Greedy -> Execution time: {}".format(endTime-startTime))
            return getPath(finalNode, initialNode, predecessors)

        validNodes = 0
        minimumHScore = float('inf')
        for offset in range(0, 4):
            neighbourX = offsets[offset][0] + currentNode[0]
            neighbourY = offsets[offset][1] + currentNode[1]
            neighbourNode = (neighbourX, neighbourY)

            if neighbourNode in visited or not validNode(neighbourX, neighbourY) or mapM.surface[neighbourX][neighbourY] != 0: # if the node can't be accessed
                continue 

            validNodes += 1
            visited.append(neighbourNode)
            heapq.heappush(openSet, (heuristic(currentNode, finalNode), neighbourNode))
            predecessors[neighbourNode] = currentNode

        #print("currentNode: {}; validNodes: {};".format(currentNode, validNodes))

    endTime = time.time()
    print("Greedy -> Execution time: {}".format(endTime-startTime))
    return "Failed."

def dummysearch():
    #example of some path in test1.map from [5,7] to [7,11]
    return [[5,7],[5,8],[5,9],[5,10],[5,11],[6,11],[7,11]]
    
def displayWithPath(image, path, color):
    mark = pygame.Surface((20,20))
    mark.fill(color)
    for move in path:
        image.blit(mark, (move[1] *20, move[0] * 20))
        
    return image

                  
# define a main function
def main():
    
    # we create the map
    m = Map() 
    #m.randomMap()
    #m.saveMap("test2.map")
    m.loadMap("test1.map")
    
    
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Path in simple environment")
        
    # we position the drone somewhere in the area
    x = randint(0, 19)
    y = randint(0, 19)
    while m.surface[x][y]:
        (x, y) = (randint(0,19), randint(0,19))

    #create drona
    d = Drone(x, y)
    d2 = Drone(x, y)
    
    # create a surface on screen that has the size of 400 x 480
    screen = pygame.display.set_mode((400,400))
    screen.fill(WHITE)
    
    # define a variable to control the main loop
    running = True
    running2 = True
    lastTime = pygame.time.get_ticks()
    finalPosition = (randint(0,19), randint(0,19))
    while m.surface[finalPosition[0]][finalPosition[1]]:
        finalPosition = (randint(0,19), randint(0,19))

    #path = searchAStar(m, d, x, y, finalPosition[0], finalPosition[1])
    path = searchGreedy(m, d, x, y, finalPosition[0], finalPosition[1])
    path2 = searchAStar(m, d2, x, y, finalPosition[0], finalPosition[1])
    print("Done computing.")
    if path == "Failed.":
        print(path)
        print(m.surface)
        return

    if path2 == "Failed.":
        print(path2)
        print(m.surface)
        return
    pathCopy = path.copy()
    pathCopy2 = path2.copy()
    print("The non-optimal greedy path of length {} (red): {}".format(len(path), path))
    print("The correct A* path of length {} (green): {}".format(len(path2), path2))

    while running and running2:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            
            if event.type == KEYDOWN:
                d.move(m) #this call will be erased
        
        
        screen.blit(d.mapWithDrone(m.image()),(0,0))
        screen.blit(d2.mapWithDrone(m.image()),(0,0))
        if pygame.time.get_ticks() - lastTime >= 300:
            lastTime = pygame.time.get_ticks()
            # change drone coordinates
            try:
                d.x, d.y = path.pop(0)
            except IndexError as ie:
                print("Done.")
                running = False

            try:
                d2.x, d2.y = path2.pop(0)
            except IndexError as ie:
                print("Done.")
                running2 = False
            #print("PATH: {}", path.pop())

        pygame.display.flip()
       
    path = pathCopy 
    path2 = pathCopy2 
    screen.blit(displayWithPath(displayWithPath(m.image(), path, RED), path2, GREEN),(0,0))
    #screen.blit(displayWithPath(m.image(), path),(0,0))
    
    pygame.display.flip()
    time.sleep(5)
    pygame.quit()
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()