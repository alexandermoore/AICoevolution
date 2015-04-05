from AIObject import *
from AIAnimal import *
from AIFood import *
from NeuralNetwork import *
import random as r

SPECIES_A = "spA"
SPECIES_B = "spB"
FOOD_1 = "fd1"
FOOD_2 = "fd2"


class AIEnvironment(object):
	"""
	Defines game world for competing species

	Args:
		None
	"""
	def __init__(self, food_mappings):
		"""
		Initiailize game world

		Args:
			food_mappings: Two mappings of food to cost/time for species A and B
		"""

		super(AIEnvironment, self).__init__()
		self.food_mappings = food_mappings


	def generate(self, grid, numA, numB, numFood1, numFood2, seed = None):
		"""
		Initialize one instance of the game world

		Args:
			grid: heigh and width of the game world
			numA: number of species A
			numB: number of species B
			numFood1: number of food source 1
			numFood2: number of food source 2
			seed: seed for random numbers, default None (current system time)
		"""

		# Initialize game world
		self.animals = []
		self.food = []

		self.world = [[None for x in range(grid)] for x in range(grid)]

		# Set seed for world
		r.seed(seed)

		# Place speciesA on world
		food_map = self.food_mappings[0]
		for i in range(numA):
			x = r.randint(0, grid - 1)
			y = r.randint(0, grid - 1)
			network = NeuralNetwork("GENOME")
			animal = AIAnimal(food_map, network, SPECIES_A, (x,y))
			self.animals.append(animal)

			self.world[x][y] = animal

		# Place speciesB on world
		food_map = self.food_mappings[1]
		for i in range(numB):
			x = r.randint(0, grid - 1)
			y = r.randint(0, grid - 1)
			network = NeuralNetwork("GENOME")
			animal = AIAnimal(food_map, network, SPECIES_B, (x,y))
			self.animals.append(animal)

			self.world[x][y] = animal

		# Place food on world
		for i in range(numFood1):
			x = r.randint(0, grid - 1)
			y = r.randint(0, grid - 1)
			food = AIFood(FOOD_1, (x,y))
			self.food.append(food)

			self.world[x][y] = food

		for i in range(numFood2):
			x = r.randint(0, grid - 1)
			y = r.randint(0, grid - 1)
			food = AIFood(FOOD_2, (x,y))
			self.food.append(food)

			self.world[x][y] = food

		self.display()
		self.runGeneration(5)

	def display(self):
		for i in range(len(self.world)):
			for j in range(len(self.world)):
				print(self.world[j][i], end="\t")

			print("\n")

		print("animals: ",list(map((lambda x : x.getPosition()), self.animals)))
		print("food: ",list(map((lambda x : x.getPosition()),self.food)))


	def animalAction(self, animal):
		action = animal.run(self.world)

		if action == 0:
			(x,y) = animal.getPosition()
			animal.setPosition((x+1,y))

			self.world[x][y] = None
			self.world[x+1][y] = animal

		elif action == 1:
			(x,y) = animal.getPosition()
			animal.setPosition((x-1,y))

			self.world[x][y] = None
			self.world[x-1][y] = animal

		elif action == 2:
			(x,y) = animal.getPosition()
			animal.setPosition((x,y+1))

			self.world[x][y] = None
			self.world[x][y+1] = animal

		elif action == 3:
			(x,y) = animal.getPosition()
			animal.setPosition((x,y-1))

			self.world[x][y] = None
			self.world[x][y-1] = animal


	def evolve(self, network):
		raise NotImplementedError("Evole given network using evolver")

	def runGeneration(self, runs):
		for j in range(runs):
			for i in range(len(self.animals)):
				animal = self.animals[i]
				self.animalAction(animal)

			self.display()

	def evaluateFitness(self):
		scoreA = 0
		totalA = 0
		scoreB = 0
		totalB = 0

		for i in range(len(self.animals)):
			animal = self.animals[i]

			if (animal.getType == SPECIES_A):
				scoreA += animal.getPoints()
				totalA += 1
			else:
				scoreB += animal.getPoints()
				totalB += 1

		fitnessA = scoreA / totalA
		fitnessB = scoreB / totalB
