import time

class UI:

    def __init__(self, controller):
        self.__controller = controller


    def runTheAlgorithm(self, k):
        iterationIndex = 0
        self.__controller.pickTheInitialCentroidsRandomly(k)

        while True:
            iterationIndex += 1
            print("Iteration #{}".format(iterationIndex))
            centroids = self.__controller.runAnIteration()

            for centroid in centroids:
                print((centroid.getX(), centroid.getY()))
            
            print("Sleeping for 2 seconds...")
            time.sleep(2)

        