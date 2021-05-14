import torch
import json
import math

right, left, size = 10, -10, 1000
randomTensor = (right - left) * torch.rand((size, 2)) + left
firstCoordinate = []
secondCoordinate = []

for value in randomTensor:
    firstCoordinate.append(value[0])
    secondCoordinate.append(value[1])

firstCoordinate = torch.tensor(firstCoordinate)
secondCoordinate = torch.tensor(secondCoordinate)

functionValues = torch.sin(firstCoordinate + (secondCoordinate / math.pi))
dataset = torch.column_stack((randomTensor, functionValues))
print(dataset)
torch.save(dataset, "mydataset.dat")