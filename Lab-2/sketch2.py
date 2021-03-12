# import the pygame module, so you can use it
import pickle,pygame,time
from pygame.locals import *
from random import random, randint
import numpy as np
import heapq
import math


#Creating some colors
BLUE  = (0, 0, 255)
GRAYBLUE = (50,120,120)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#define directions
UP = 0
DOWN = 2
LEFT = 1
RIGHT = 3

#define indexes variations 
v = [[-1, 0], [1, 0], [0, 1], [0, -1]]
offsets = [[0, 1], [1, 0], [0, -1], [-1, 0]]


class Map():
    def __init__(self, n = 20, m = 20):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))

    def getWidth(self):
        return self.n

    def getHeight(self):
        return self.m
    
    def randomMap(self, fill = 0.2):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill :
                    self.surface[i][j] = 1
                
    def __str__(self):
        string=""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string
                
    def saveMap(self, numFile = "test.map"):
        with open(numFile,'wb') as f:
            pickle.dump(self, f)
            f.close()
        
    def loadMap(self, numfile):
        with open(numfile, "rb") as f:
            dummy = pickle.load(f)
            self.n = dummy.n
            self.m = dummy.m
            self.surface = dummy.surface
            f.close()
        
    def image(self, colour = BLUE, background = WHITE):
        imagine = pygame.Surface((400,400))
        brick = pygame.Surface((20,20))
        brick.fill(BLUE)
        imagine.fill(WHITE)
        for i in range(self.n):
            for j in range(self.m):
                if (self.surface[i][j] == 1):
                    imagine.blit(brick, ( j * 20, i * 20))
                
        return imagine        
        

class Drone():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def move(self, detectedMap):
        pressed_keys = pygame.key.get_pressed()
        if self.x > 0:
            if pressed_keys[K_UP] and detectedMap.surface[self.x-1][self.y]==0:
                self.x = self.x - 1
        if self.x < 19:
            if pressed_keys[K_DOWN] and detectedMap.surface[self.x+1][self.y]==0:
                self.x = self.x + 1
        
        if self.y > 0:
            if pressed_keys[K_LEFT] and detectedMap.surface[self.x][self.y-1]==0:
                self.y = self.y - 1
        if self.y < 19:        
            if pressed_keys[K_RIGHT] and detectedMap.surface[self.x][self.y+1]==0:
                 self.y = self.y + 1
                  
    def mapWithDrone(self, mapImage):
        drona = pygame.image.load("drona.png")
        mapImage.blit(drona, (self.y * 20, self.x * 20))
        
        return mapImage


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
        print("currentNode: {}; validNodes: {};".format(currentNode, validNodes))
    return "Failed."
    
    
def searchGreedy(mapM, droneD, initialX, initialY, finalX, finalY):
    # TO DO 
    # implement the search function and put it in controller
    # returns a list of moves as a list of pairs [x,y]
    pass

def dummysearch():
    #example of some path in test1.map from [5,7] to [7,11]
    return [[5,7],[5,8],[5,9],[5,10],[5,11],[6,11],[7,11]]
    
def displayWithPath(image, path):
    mark = pygame.Surface((20,20))
    mark.fill(GREEN)
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
    """
    x = 9
    y = 1
    """
    #create drona
    d = Drone(x, y)
    
    # create a surface on screen that has the size of 400 x 480
    screen = pygame.display.set_mode((400,400))
    screen.fill(WHITE)
    
    # define a variable to control the main loop
    running = True
    lastTime = pygame.time.get_ticks()
    finalPosition = (randint(0,19), randint(0,19))
    while m.surface[finalPosition[0]][finalPosition[1]]:
        finalPosition = (randint(0,19), randint(0,19))

    path = searchAStar(m, d, x, y, finalPosition[0], finalPosition[1])
    #path = searchAStar(m, d, x, y, 12, 2)
    if path == "Failed.":
        print(path)
        print(m.surface)
        return
    pathCopy = path.copy()
    print("The correct path: {}".format(path))
    for node in path:
        m.surface[node[0]][node[1]] = 9
    #print(m.surface)
    #return
    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            
            if event.type == KEYDOWN:
                d.move(m) #this call will be erased
        
        
        screen.blit(d.mapWithDrone(m.image()),(0,0))
        if pygame.time.get_ticks() - lastTime >= 300:
            lastTime = pygame.time.get_ticks()
            # change drone coordinates
            try:
                d.x, d.y = path.pop(0)
            except IndexError as ie:
                print("Done.")
                running = False
            #print("PATH: {}", path.pop())

        pygame.display.flip()
       
    path = pathCopy 
    screen.blit(displayWithPath(m.image(), path),(0,0))
    
    pygame.display.flip()
    time.sleep(5)
    pygame.quit()
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()