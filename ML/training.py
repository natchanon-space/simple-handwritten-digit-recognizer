import mnist_loader
import network

# unpack mnist data
training_data, validation_data, test_data = mnist_loader.load_data_wrapper()

# build network for [784, 30, 30, 10] net
net = network.Network([784, 100, 30, 10])

# training
# SGD(traning_data, epochs, mini_batch_size, eta, test_data=None)
net.SGD(training_data, 100, 10, 3, test_data=test_data)

# save and load test
network.save_network(net, "trained.npy")
b, w, mmax = network.load_network("trained.npy")

# checking
print("biases")
for line in b:
    print(line.shape)

print("weight")
for line in w:
    print(line.shape)

print("max : {}".format(mmax))