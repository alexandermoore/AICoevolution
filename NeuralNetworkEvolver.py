from NeuralNetwork import *

class NeuralNetworkEvolver(object):
	"""
	Defines evolutionary functons on neural network

	"""
	def __init__(self):
		super(NeuralNetworkEvolver, self).__init__()
		self.hall = []

	def mutate(self, network):
		# raise NotImplementedError("Return mutated network")
		return network

	def crossover(self, network1, network2):
		# raise NotImplementedError("Return network from crossover")
		return (network1, network2)

	def evolve(self, networks):
		"""
		Evolves a list of networks based on their fitnesses

		Args:
			networks: list of network / fitness tuples

		Returns:
			new list of networks that are next generation
		"""
		# raise NotImplementedError("Evolve networks")
		return list(map((lambda x: x[0]) ,networks))

	def getHall(self):
		"""
		Return Hall of Fame
		"""

		return self.hall
