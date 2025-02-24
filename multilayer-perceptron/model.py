import sys
import numpy as np


def softmax(values):
    return np.exp(values) / np.sum(np.exp(values))

class DenseLayer:
    """
 class representing a layer of the multilayer perceptron.
    """
    def __init__(self, n_inputs, n_neurons):
        self.weights = 0.10 * np.random.randn(n_inputs, n_neurons)
        self.biases = np.zeros((1, n_neurons))
    
    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases


class ReLU:
    """
 class representing the ReLU activation function.
    """
    @staticmethod
    def forward(self, inputs):
        self.output = np.maximum(0, inputs)
