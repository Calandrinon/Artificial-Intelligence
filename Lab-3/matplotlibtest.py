import matplotlib.pyplot as plt
import numpy as np
import math

figure, axes = plt.subplots()
x_axis = []
y_axis = []
x_axis2 = []
y_axis2 = []
n = 100
for number in range(1, n):
    x_axis.append(number)
    y_axis.append(number)
    x_axis2.append(number)
    y_axis2.append(math.log(number))
    axes.plot(x_axis, y_axis)
    axes.plot(x_axis2, y_axis2)
    plt.pause(0.05)


plt.show()
