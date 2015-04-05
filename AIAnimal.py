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
		"""
		Initializes Animal instance

		Args:
			network: neural network that makes decisions about actions
			mapping: mapping of food to costs
			name: name of the species
			position: place in the world on this instance

		"""
		super(AIAnimal, self).__init__(name, position)
		self.network = network
		self.mapping = mapping


	def run(self, input):
		"""
		Have animal make decision about what to do

		Args:
			input: the world which the animal will have as sensory input

		Returns:
			Number representing actions
			0 - move left
			1 - move right
			2 - move up
			3 - move down
			4 - stay still

		Raise:
			None
		"""

		move = r.randint(0,4)

		if move == 4:
			self.points -= 1
		else:
			self.points -= 2

		return move

	def eat(self, food):
		"""
		Have animal eat given food

		Args:
			food: animal or food object that will be eaten
		"""

		self.points += self.mapping[food.getType()]
		food.die()

	def __str__(self):
		color = '\033[94m'
		if (self.getType() == "spA"):
			color = '\033[91m'
		return color + self.name + '\033[0m'