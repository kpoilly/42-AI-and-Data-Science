import sys
from typing import Type
import numpy as np


class ActivationFunction:
    """
Template class for activation functions
    """
    pass

class LossFunction:
    """
Template class for loss calculation functions
    """
    def calculate(self, output, Y):
        losses = self.forward(output, Y)
        return np.mean(losses)


class DenseLayer:
    """
 class representing a layer of the multilayer perceptron.
    """
    def __init__(self, n_inputs: int, n_neurons: int, activation: Type[ActivationFunction]):
        self.weights = 0.10 * np.random.randn(n_inputs, n_neurons)
        self.biases = np.zeros((1, n_neurons))
        self.activation = activation
    
    def forward(self, inputs):
        self.output = np.dot(len(inputs[0]), self.weights) + self.biases


class ReLU(ActivationFunction):
    """
 class representing the ReLU activation function.
    """
    def forward(self, inputs):
        self.output = np.maximum(0, inputs)

        
class Softmax(ActivationFunction):
    """
class representing the Softmax acivation function.
    """
    def forward(self, inputs):
        exp_val = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
        prob = exp_val / np.sum(exp_val, axis=1, keepdims=True)
        self.output = prob

class BinaryCrossEntropy(LossFunction):
    """
class representing the BinaryCrossEntropy loss calculation function.
    """
    def forward(self, y_pred, y_true):
        y_pred_clipped = np.clip(y_pred, 1e-7, 1 - 1e-7)
        return -(y_true / y_pred_clipped - (1 - y_true) / (1 - y_pred_clipped)) / len(y_pred)
