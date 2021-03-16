from Domain import Map

class Repository:
    def __init__(self):
        self.m = Map() 
        self.m.loadMap("test1.map")        
    
    def getMap(self):
        return self.m
