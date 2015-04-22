INPUT_NODES = 16
NODES_PER_HIDDEN_LAYER = [5]
OUTPUT_NODES = 5
import random as r
from FFNeuralNetwork import *
from Perceptron import *

class NeuralNetwork(object):
	"""
	Wrapper for neural network library with needed methods

	Args:
		None

	"""
	def __init__(self, genome = None):
		# network = FFNeuralNetwork(INPUT_NODES, NODES_PER_HIDDEN_LAYER, OUTPUT_NODES)
		network = Perceptron(INPUT_NODES, OUTPUT_NODES)
		if not genome:
			genome = network.getWeights()
		else:
			network.setWeights(genome)
		self.genome = genome
		self.network = network

	def getGenome(self):
		return self.genome

	def evaluate(self, input_variables):
		return self.network.sendSignal(input_variables)