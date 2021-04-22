import time, copy
from matplotlib import pyplot as plt 

class UI:

    def __init__(self, controller):
        self.__controller = controller
        plt.figure(figsize=(10, 10))


    def drawScatterplot(self, k):
        points = self.__controller.getTheUnlabelledPoints()
        colors = self.__controller.getClusterColors()

        for clusterIndex in range(0, k):
            pointsBelongingToTheCurrentCluster = list(filter(lambda x: x.getTheExpectedCluster() == clusterIndex, points))
            xCoordinates = list(map(lambda x: x.getX(), copy.deepcopy(pointsBelongingToTheCurrentCluster)))
            yCoordinates = list(map(lambda y: y.getY(), copy.deepcopy(pointsBelongingToTheCurrentCluster)))
            plt.scatter(xCoordinates, yCoordinates, s=10, color=(colors[clusterIndex][0], colors[clusterIndex][1], colors[clusterIndex][2]))
            plt.pause(0.05)


    def runTheAlgorithm(self, k):
        self.__controller.generateColors(k)
        iterationIndex = 0
        self.__controller.pickTheInitialCentroidsRandomly(k)
        converged = False

        while not converged:
            iterationIndex += 1
            print("Iteration #{}".format(iterationIndex))
            centroids = self.__controller.runAnIteration()

            for centroid in centroids:
                print((centroid.getX(), centroid.getY()))
                points = self.__controller.getTheUnlabelledPoints()
            
            converged = self.__controller.didTheModelConverge()
            print("Did the model converge? The answer is: {}".format(converged))
            print("Sleeping for 2 seconds...")
            self.drawScatterplot(k)
            time.sleep(2)
        
        print("Done!")
        plt.show()