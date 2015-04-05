from AIObject import *
import random as r

class AIAnimal(AIObject):
	"""
	Defines methods all Animals must support

	Args:
		network: neural network that makes decisions
		mapping: mapping of food to cost of eating food
		name: type of species
	"""
	def __init__(self, network, mapping, name, position):
		super(AIAnimal, self).__init__(name, position)
		self.points = 0
		self.network = network
		self.mapping = mapping

	def getPoints(self):
		return self.points

	def run(self, input):
		return r.randint(0,5)
		# raise NotImplementedError("Need to run neural network")


