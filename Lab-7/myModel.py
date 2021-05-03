import torch
import torch.nn.functional as F

class ApproximationNeuralNetwork(torch.nn.Module):
    def __init__(self, inputLayerSize, hiddenLayerSize, outputLayerSize):
        super(ApproximationNeuralNetwork, self).__init__()
        self.__hiddenLayer = torch.nn.Linear(inputLayerSize, hiddenLayerSize)
        self.__outputLayer = torch.nn.Linear(hiddenLayerSize, outputLayerSize)


    def forward(self, x):
        weightedSum = self.__hiddenLayer(x) 
        activationValue = F.relu(weightedSum)
        output = self.__outputLayer(activationValue)
        return output
