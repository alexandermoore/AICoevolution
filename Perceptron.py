import math
import random

class Perceptron(object):
	def __init__(self, n_input, n_output):
		self.n_input = n_input
		self.n_output = n_output
		self.weights = [[0]*n_output for _ in range(n_input)]
		self.activate_fn = self.__sigmoid    # self.activate_fn = self.__identity
		self.__randomizeWeights()

	def __sigmoid(self,x):
		"""
		Evaluates the sigmoid activation function for the neural network
		"""
		return 1.0/(1.0 + math.exp(-x))

	def __identity(self, x):
		return x

	def __activate(self, x):
		return self.activate_fn(x)

	def __randomizeWeights(self):
		weights = self.getWeights()
		randoms = [random.random() for _ in range(len(weights))]
		self.setWeights(randoms)

	def getWeights(self):
		return [self.weights[i][j] for j in range(self.n_output) for i in range(self.n_input)]

	def setWeights(self, weights):
		for k in range(len(weights)):
			i = int(k/self.n_output)
			j = k - int(k/self.n_output) * self.n_output
			self.weights[i][j] = weights[k]

	def sendSignal(self, inputs):
		assert(len(inputs) == self.n_input)
		outputs = [0] * self.n_output
		for j in range(self.n_output):
			for i in range(self.n_input):
				outputs[j] += self.weights[i][j] * inputs[i]
			outputs[j] = self.__activate(outputs[j])
		return outputs

if __name__ == '__main__':
	p = Perceptron(3,2)
	w = p.getWeights()
	print("WEIGHTS", w)
	w = [1 for _ in range(len(w))]
	p.setWeights(w)
	print(p.sendSignal([1,3,5]))
	p.getWeights()
	p.setWeights(w)
	print(p.sendSignal([1,3,5]))
