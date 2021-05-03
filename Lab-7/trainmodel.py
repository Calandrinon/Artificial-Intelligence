import math, torch
from myModel import ApproximationNeuralNetwork

trainingDataTensor = torch.load("mydataset.dat")
inputValues = trainingDataTensor[:,:2]
givenFunctionValues = trainingDataTensor[:,2:]

lossFunction  = torch.nn.MSELoss()
inputLayerSize = 2
hiddenLayerSize = 10
outputLayerSize = 1
approximationNeuralNetwork = ApproximationNeuralNetwork(inputLayerSize, hiddenLayerSize, outputLayerSize)

optimizer = torch.optim.SGD(approximationNeuralNetwork.parameters(), lr=0.05)
listOfErrors = []

batchSize = 16
numberOfBatches = int(len(trainingDataTensor) / batchSize)
numberOfEpochs = 2000

for epochIndex in range(numberOfEpochs):
    for batchIndex in range(numberOfBatches):
        inputBatch = inputValues[batchSize * batchIndex:batchSize + (batchIndex + 1),]
        outputBatch = givenFunctionValues[batchSize * batchIndex:batchSize + (batchIndex + 1),]
        predictedFunctionValue = approximationNeuralNetwork(inputBatch)
        lossFunctionValue = lossFunction(predictedFunctionValue, outputBatch)

        listOfErrors.append(lossFunctionValue)
        optimizer.zero_grad()
        lossFunctionValue.backward()
        optimizer.step()

    if epochIndex % 100 == 99:
        predictedFunctionValues = approximationNeuralNetwork(inputValues)
        lossFunctionValue = lossFunction(predictedFunctionValues, givenFunctionValues)
        print("Epoch: {}; Loss: {}".format(epochIndex, lossFunctionValue))
    

filename = "ApproximationNeuralNetwork.pt"
torch.save(approximationNeuralNetwork.state_dict(), filename)