import torch
import torch.nn.functional as F

class ApproximationNeuralNetwork(torch.nn.Module):
    def __init__(self, inputLayerSize, hiddenLayerSize, outputLayerSize):
        super(ApproximationNeuralNetwork, self).__init__()
        self.__model = torch.nn.Sequential(
            torch.nn.Linear(inputLayerSize, hiddenLayerSize),
            torch.nn.ReLU(),
            torch.nn.Linear(hiddenLayerSize, hiddenLayerSize),
            torch.nn.ReLU(),
            torch.nn.Linear(hiddenLayerSize, outputLayerSize)
        )


    def forward(self, x):
        return self.__model(x)
