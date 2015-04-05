INPUT_NODES = 32
NODES_PER_HIDDEN_LAYER = [5]
OUTPUT_NODES = 5

class NeuralNetwork(object):
	"""
	Wrapper for neural network library with needed methods

	Args:
		None

	"""
	def __init__(self, genome):
		self.genome = genome
		self.network = None

	def getGenome(self):
		return self.genome

	def evaluate(self, input_variables):
		raise NotImplementedError("Passes inputs into neural network and decide action")
