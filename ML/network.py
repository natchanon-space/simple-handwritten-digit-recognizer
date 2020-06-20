import numpy as np
import random

# note about mnist_loader
# training_data => (input, vectorized_output)
# test_data => (input, only a digit) T-T

class Network(object):

    # set up initial network
    def __init__(self, size):
        self.size = size
        self.layers = len(size)
        self.bias = [np.random.randn(y, 1) for y in size[1:]]
        self.weight = [np.random.randn(y, x) for x, y in zip(size[:-1], size[1:])]
        # finding the best network
        self.max_accuracy = 0
        self.best_bias = []
        self.best_weight = []

    # return output of network when arr is input
    def feedforward(self, a):
        for b, w in zip(self.bias, self.weight):
            a = sigmoid(np.dot(w, a) + b)
        return a

    # evaluate network from feedforward of test_data
    # return number of pass test
    def evaluate(self, test_data):
        pass_test = 0
        for x, y in test_data:
            if(np.argmax(self.feedforward(x)) == y):
                pass_test += 1
        return pass_test

    def SGD(self, training_data, epochs, mini_batch_size, eta, test_data=None):
        training_data = list(training_data)
        n_training = len(training_data)

        if test_data:
            test_data = list(test_data)
            n_test = len(test_data)

        for i in range(epochs):
            random.shuffle(training_data)

            # condition mini_batch_size * epochs <= n_training
            mini_batches = [training_data[k:k+mini_batch_size] for k in range(0, n_training, mini_batch_size)]

            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, eta)

            if test_data:
                pass_test = self.evaluate(test_data)
                print("epoch {} : {}/{}".format(i, pass_test, n_test))

                # update best result
                if self.max_accuracy < pass_test/n_test:
                    self.max_accuracy = pass_test/n_test
                    self.best_bias = self.bias
                    self.best_weight = self.weight
            else:
                print("epoch {} complete".format(i))

    def update_mini_batch(self, mini_batch, eta):
        # template for nabla_b, nabla_w to sum all delta_nabla then avg to SGD
        nabla_b = [np.zeros(b.shape) for b in self.bias]
        nabla_w = [np.zeros(w.shape) for w in self.weight]

        # sum it all!!!
        for x, y in mini_batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            nabla_b = [nb+dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw+dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]

        # network updating (decreasing cost function to make more accurate network with SGD)
        m = len(mini_batch)
        self.bias = [b - (eta/m)*nb for b, nb in zip(self.bias, nabla_b)]
        self.weight = [w - (eta/m)*nw for w, nw in zip(self.weight, nabla_w)]

    # return np.array of nabla_b, nabla_w for single test_data
    def backprop(self, x, y):
        # template for nabla_b, nabla_w
        nabla_b = [np.zeros(b.shape) for b in self.bias]
        nabla_w = [np.zeros(w.shape) for w in self.weight]
        
        a = [x]# activation
        zs = [] # z value
        
        # feedforward to get delta
        for b, w in zip(self.bias, self.weight):
            z = np.dot(w, a[-1]) + b
            zs.append(z)
            a.append(sigmoid(z))

        # backprop apply delta to all bias and weight
        delta = (a[-1] - y) * sigmoid_derivative(zs[-1])
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, a[-2].transpose())

        for l in range(2, self.layers):
            delta = np.dot(self.weight[-l+1].transpose(), delta) * sigmoid_derivative(zs[-l])
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, a[-l-1].transpose())

        return (nabla_b, nabla_w)

# save trained network
def save_network(net_obj, filename):
    with open(filename, "wb") as f:
        np.save(f, net_obj.best_bias)
        np.save(f, net_obj.best_weight)
        np.save(f, net_obj.max_accuracy)

# load trained network return net.bias, net.weight
def load_network(filename):
    with open(filename, "rb") as f:
        b = np.load(f, allow_pickle=True)
        w = np.load(f, allow_pickle=True)
        mmax = np.load(f, allow_pickle=True)
    return (b, w, mmax)

# own input -> output return single int refer to digit
def recognition(mnist_data, net_obj_bias, net_obj_weight):
    a = mnist_data
    for b, w in zip(net_obj_bias, net_obj_weight):
        a = sigmoid(np.dot(w, a) + b)
    return (a, np.argmax(a))

# sigmoid function
def sigmoid(z):
    return 1.0/(1.0 + np.exp(-z))

def sigmoid_derivative(z):
    return sigmoid(z)*(1-sigmoid(z))