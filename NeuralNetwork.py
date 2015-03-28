class NeuralNetwork(object):
	"""
	Wrapper for neural network library with needed methods

	Args:
		None

	"""
	def __init__(self, genome):
		self.genome = genome

	def getGenome(self):
		return self.genome

	def evaluate(self, input_variables):
		raise NotImplementedError("Passes inputs intp neural network and decide action")
