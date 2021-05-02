import torch
import json
import math

def sinusoidalFunction(x1, x2):
    return torch.sin(torch.add(x1, x2 / math.pi))


randomTensorOfIntegersBetweenNegative10And10 = torch.randint(-10, 10, (1000, 2))
randomTensorOfNumbersBetween0And1 = torch.rand(1000, 2)
randomTensor = randomTensorOfIntegersBetweenNegative10And10 * randomTensorOfNumbersBetween0And1

datasetTensor = None

for pointsTensor in randomTensor:
    pointAsList = pointsTensor.tolist()
    pointAsList.append(sinusoidalFunction(pointsTensor[0], pointsTensor[1]))
    pointTensorWithFunctionOutput = torch.tensor([pointAsList])

    if datasetTensor == None:
        datasetTensor = pointTensorWithFunctionOutput
    else:
        datasetTensor = torch.cat((datasetTensor, pointTensorWithFunctionOutput))

torch.save(datasetTensor, "mydataset.dat")
