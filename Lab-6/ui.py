import time

class UI:

    def __init__(self, controller):
        self.__controller = controller


    def runTheAlgorithm(self, k):
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
            time.sleep(2)

        print("Done!")

        