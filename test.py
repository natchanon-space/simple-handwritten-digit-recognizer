import ML.mnist_loader as mnist_loader
import ML.network as network
import numpy as np


"""
# training_data, validation_data, test_data = mnist_loader.load_data_wrapper()

net = network.Network([2, 3, 1])
# net.SGD(training_data, 30, 30, 3, test_data=test_data)

import numpy as np

with open('data.npy', 'wb') as f:
    np.save(f, net.bias)
    np.save(f, net.weight)

temp = []
with open('data.npy', 'rb') as f:
    for line in f:
        temp.append(np.load(f, allow_pickle=True))

print("b : {} \n w : {}".format(temp[0], temp[1]))
"""

a = [1, 2, 3, 4]
print(a)

a = np.array(a)
print(a.shape)

a = a.reshape((2, 2))
print(a.shape)
print(a)
