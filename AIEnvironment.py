from AIObject import *
from AIAnimal import *
from AIFood import *

class AIEnvironment(object):
	"""
	Defines game world for competing species

	Args:
		None
	"""
	def __init__(self, food_mappings):
		super(AIEnvironment, self).__init__()
		self.food_mappings = food_mappings

	def generate(self, species1, species2):
		raise NotImplementedError("Randomly place food and species")

	def evolve(network):
		raise NotImplementedError("Evole given network using evolver")

	def runGeneration(self):
		raise NotImplementedError("Runs one game competition of species")

	def evaluateFitness(self, animals):
		raise NotImplementedError("Calculates result of fitness function")