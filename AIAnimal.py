from AIObject import *
from util import *
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
		self.food_counts = {}
		for food in self.mapping:
			self.food_counts[food] = 0



	def run(self, ins):
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

		(x,y) = self.getPosition()
		length = len(ins)

		env = [(x-1,y-1), (x, y-1), (x+1, y-1), (x-1, y), (x+1, y), (x-1, y+1), (x, y+1), (x+1, y+1)]

		env = list(map((lambda x: (x[0] % length, x[1] % length)), env))

		input_variables = [0] * 32

		for i in range(len(env)):
			(x,y) = env[i]
			obj = ins[x][y]

			if (obj == None):
				continue
			elif (obj.getType() == SPECIES_A):
				input_variables[i*4 + 0] += 1
			elif (obj.getType() == SPECIES_B):
				input_variables[i*4 + 1] += 1
			elif (obj.getType() == FOOD_1):
				input_variables[i*4 + 2] += 1
			elif (obj.getType() == FOOD_2):
				input_variables[i*4 + 3] += 1

		options = self.network.evaluate(input_variables)
		move = options.index(max(options))

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
		self.food_counts[food.getType()] += 1
		food.die()

	def __str__(self):
		color = '\033[94m'
		if (self.getType() == "spA"):
			color = '\033[91m'
		return color + self.name + '\033[0m'