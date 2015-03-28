from AIObject import *

class AIAnimal(AIObject):
	"""
	Defines methods all Animals must support

	Args:
		network: neural network that makes decisions
		mapping: mapping of food to cost of eating food
		name: type of species
	"""
	def __init__(self, network, mapping, name):
		super(AIAnimal, self).__init__(name)
		self.points = 0
		self.network = network
		self.mapping = mapping

	def getPoints(self):
		return self.points

	def run(self):
		raise NotImplementedError("Need to run neural network")


