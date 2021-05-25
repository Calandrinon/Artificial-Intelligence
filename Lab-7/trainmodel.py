import math, torch, os, shutil
import myModel
import matplotlib.pyplot as plt

trainingDataTensor = torch.load("mydataset.dat")
inputValues = trainingDataTensor[:,:2]
givenFunctionValues = trainingDataTensor[:,2:]

lossFunction = torch.nn.MSELoss()
inputLayerSize = 2
hiddenLayerSize = 10
outputLayerSize = 1
approximationNeuralNetwork = myModel.ApproximationNeuralNetwork(inputLayerSize, hiddenLayerSize, outputLayerSize)

optimizer = torch.optim.SGD(approximationNeuralNetwork.parameters(), lr=0.05)
listOfErrors = []

batchSize = 100
numberOfBatches = int(len(trainingDataTensor) / batchSize)
numberOfEpochs = 10000
epochList = []

for epochIndex in range(numberOfEpochs):
    for batchIndex in range(numberOfBatches):
        inputBatch = inputValues[batchSize * batchIndex:batchSize * (batchIndex + 1),]
        outputBatch = givenFunctionValues[batchSize * batchIndex:batchSize * (batchIndex + 1),]
        predictedFunctionValue = approximationNeuralNetwork(inputBatch)
        lossFunctionValue = lossFunction(predictedFunctionValue, outputBatch)

        optimizer.zero_grad()
        lossFunctionValue.backward()
        optimizer.step()

    if epochIndex % 100 == 0:
        predictedFunctionValues = approximationNeuralNetwork(inputValues)
        lossFunctionValue = lossFunction(predictedFunctionValues, givenFunctionValues).tolist()
        listOfErrors.append(lossFunctionValue)
        epochList.append(epochIndex)

        plt.xlabel("Epoch")
        plt.ylabel("Value of the loss function")
        plt.plot(epochList, listOfErrors, color="green")
        plt.legend(["Loss function values for each epoch"], labelcolor=["green"])
        plt.pause(0.05)
        print("Epoch: {}; Loss: {}".format(epochIndex, lossFunctionValue))


files = os.listdir(os.getcwd()+"/plots")
images = list(filter(lambda filename: filename.split(".")[-1] == "png", files))
imageIndexes = list(map(lambda filename: int(filename.split(".")[0].split("_")[1]), images))
imageIndex = max(imageIndexes)

imageFilename = "plot_" + str(imageIndex + 1) + ".png"
plt.savefig(imageFilename)
shutil.move(os.getcwd()+"/"+imageFilename, os.getcwd()+"/plots")
plt.show()

filename = "ApproximationNeuralNetwork.pt"
torch.save(approximationNeuralNetwork.state_dict(), filename)