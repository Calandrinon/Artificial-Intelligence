import torch
from myModel import ApproximationNeuralNetwork

filename = "ApproximationNeuralNetwork.pt"
approximationNeuralNetwork = ApproximationNeuralNetwork(2, 10, 1)

approximationNeuralNetwork.load_state_dict(torch.load(filename))
approximationNeuralNetwork.eval()

x1 = float(input("x1="))
x2 = float(input("x2="))
x = torch.tensor((x1, x2))
print(approximationNeuralNetwork(x).tolist())