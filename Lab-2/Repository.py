from Domain import Map

class Repository:
    def __init__(self):
        # we create the map
        self.m = Map() 
        #m.randomMap()
        #m.saveMap("test2.map")
        self.m.loadMap("test1.map")        
        self.offsets = [[0, 1], [1, 0], [0, -1], [-1, 0]]
    
    def getMap(self):
        return self.m

    def getOffsets(self):
        return self.offsets