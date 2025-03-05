import sys
from typing import Type
import numpy as np


class Network:
    """
Class representing the Artificial Neural Network
    """
    def __init__(self):
        self.id = 0
        self.network = []
        self.params = ""
        self.mean = 0
        self.std_dev = 0
        self.train_losses = []
        self.train_accu = []
        self.val_losses = []
        self.val_accu = []
        self.accuracy = 0


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
        self.inputs = inputs
        self.output = np.dot(inputs, self.weights) + self.biases

    def backward(self, grad, lr):
        grad = self.activation.backward(grad)
        weights_grad = np.dot(self.inputs.T, grad)
        self.weights -= lr * weights_grad
        self.biases -= lr * np.mean(grad, axis=0, keepdims=True)
        return np.dot(grad, self.weights.T)


class ReLU(ActivationFunction):
    """
 class representing the ReLU activation function.
    """
    def forward(self, inputs):
        self.inputs = inputs
        self.output = np.maximum(0, inputs)

    def backward(self, grad):
        return grad * (self.inputs > 0)


class Softmax(ActivationFunction):
    """
class representing the Softmax acivation function.
    """
    def forward(self, inputs):
        exp_val = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
        prob = exp_val / np.sum(exp_val, axis=1, keepdims=True)
        self.output = prob

    def backward(self, grad):
        return grad


class CrossEntropy(LossFunction):
    """
class representing the CrossEntropy loss calculation function.
    """
    def forward(self, y_pred, y_true):
        y_pred_clipped = np.clip(y_pred, 1e-7, 1 - 1e-7)
        if len(y_true.shape) == 1:
            confidences = y_pred_clipped[range(len(y_pred)), y_true]
        elif len(y_true.shape) == 2:
            confidences = np.sum(y_pred_clipped * y_true, axis=1)
        return -np.log(confidences)

    def backward(self, y_pred, y_true):
        y_pred_clipped = np.clip(y_pred, 1e-7, 1 - 1e-7)
        if len(y_true.shape) == 1:
            one_hot = np.zeros((len(y_true), y_pred.shape[1]))
            one_hot[range(len(y_true)), y_true] = 1
            y_true = one_hot
        return (y_pred_clipped -  y_true) / len(y_pred)
