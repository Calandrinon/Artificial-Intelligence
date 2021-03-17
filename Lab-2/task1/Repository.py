from Domain import Map, Drone

class Repository:
    def __init__(self):
        self.m = Map() 
        self.m.loadMap("test1.map")        
        self.drones = [Drone(0, 0), Drone(0, 0)]
    

    def getMap(self):
        return self.m

    
    def getAStarDrone(self):
        return self.drones[0]


    def setAStarDrone(self, drone):
        self.drones[0] = drone


    def getGreedyDrone(self):
        return self.drones[1]


    def setGreedyDrone(self, drone):
        self.drones[1] = drone