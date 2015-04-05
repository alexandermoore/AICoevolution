from AIObject import *
from AIAnimal import *
from AIFood import *
from NeuralNetwork import *
from util import *
from NeuralNetworkEvolver import *
import random as r
import time



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
		self.evolver = NeuralNetworkEvolver()

	def generatePosition(self, grid):
		"""
		Finds a free spot on the world for the user

		Args:
			None

		Returns:
			None

		Raise:
			None
		"""

		if not(self.space):
			raise Exception("World is over filled")

		x = r.randint(0, grid - 1)
		y = r.randint(0, grid - 1)

		while (self.world[x][y]):
			x = r.randint(0, grid - 1)
			y = r.randint(0, grid - 1)

		self.space -= 1

		return (x,y)


	def generate(self, grid, numA, numB, numFood1, numFood2, steps = 5, seed = None):
		"""
		Initialize one instance of the game world

		Args:
			grid: height and width of the game world
			numA: number of species A
			numB: number of species B
			numFood1: number of food source 1
			numFood2: number of food source 2
			steps: number of steps to run simulation
			seed: seed for random numbers, default None (current system time)
		"""

		# Initialize game world
		self.animals = []
		self.food = []
		self.world = [[None for x in range(grid)] for x in range(grid)]
		self.space = grid * grid

		# Set seed for world
		r.seed(seed)

		# Place speciesA on world
		food_map = self.food_mappings[0]
		for i in range(numA):
			(x,y) = self.generatePosition(grid)
			network = NeuralNetwork()
			animal = AIAnimal(network, food_map, SPECIES_A, (x,y))
			self.animals.append(animal)

			self.world[x][y] = animal

		# Place speciesB on world
		food_map = self.food_mappings[1]
		for i in range(numB):
			(x,y) = self.generatePosition(grid)
			network = NeuralNetwork()
			animal = AIAnimal(network, food_map, SPECIES_B, (x,y))
			self.animals.append(animal)

			self.world[x][y] = animal

		# Place food on world
		for i in range(numFood1):
			(x,y) = self.generatePosition(grid)
			food = AIFood(FOOD_1, (x,y))
			self.food.append(food)

			self.world[x][y] = food

		for i in range(numFood2):
			(x,y) = self.generatePosition(grid)
			food = AIFood(FOOD_2, (x,y))
			self.food.append(food)

			self.world[x][y] = food

		self.display()
		self.runSteps(steps)

	def display(self):
		"""
		Displayes game world

		Args:
			None
		"""

		print("animals: ",list(map((lambda x : (x.getPosition(), x.getPoints())), self.animals)))
		for i in range(len(self.world)):
			for j in range(len(self.world)):
				print(self.world[j][i], end="\t")

			print("\n")

	def animalAction(self, animal):
		"""
		Has animal decide on an action and execute

		Args:
			animal: the animal that is going to make a decision
		"""

		action = animal.run(self.world)

		if action == 0:
			(x,y) = animal.getPosition()
			animal.setPosition(((x+1) % len(self.world),y))

			self.world[x][y] = None
			self.world[(x+1) % len(self.world)][y] = self.interact(animal, self.world[(x+1) % len(self.world)][y])

		elif action == 1:
			(x,y) = animal.getPosition()
			animal.setPosition((x-1,y))

			self.world[x][y] = None
			self.world[x-1][y] = self.interact(animal, self.world[x-1][y])

		elif action == 2:
			(x,y) = animal.getPosition()
			animal.setPosition((x,(y+1) % len(self.world)))

			self.world[x][y] = None
			self.world[x][(y+1) % len(self.world)] = self.interact(animal, self.world[x][(y+1) % len(self.world)])


		elif action == 3:
			(x,y) = animal.getPosition()
			animal.setPosition((x,y-1))

			self.world[x][y] = None
			self.world[x][y-1] = self.interact(animal, self.world[x][y-1])

	def evolve(self, network):
		raise NotImplementedError("Evole given network using evolver")

	def runSteps(self, steps):
		"""
		Per step has each animal make an action

		Args:
			steps: number of steps to run the world
		"""

		for j in range(steps):
			r.shuffle(self.animals)
			for i in range(len(self.animals)):
				animal = self.animals[i]

				if animal.getPosition():
					self.animalAction(animal)

			self.display()
			time.sleep(2)

		print(self.evaluateFitness())

	def evaluateFitness(self):
		"""
		Calculates the fitness of both species

		Args:
			None

		Returns:
			Tuple where first is the fitness of speciesA, second is speciesB.
		"""
		scoreA = 0
		totalA = 0
		scoreB = 0
		totalB = 0

		for i in range(len(self.animals)):
			animal = self.animals[i]

			if (animal.getType() == SPECIES_A):
				scoreA += animal.getPoints()
				totalA += 1
			else:
				scoreB += animal.getPoints()
				totalB += 1

		fitnessA = scoreA / totalA
		fitnessB = scoreB / totalB

		return (fitnessA, fitnessB)

	def interact(self, aggressor, obj):
		"""
		Resolves conflict when one object langs on another

		Args:
			aggressor: animal that is moving to the object location
			obj: food or other animal that used to occupy spot

		Returns:
			Winner who now occupies spot (TODO: resolve conflict fairly)

		"""

		if not(obj):
			return aggressor

		elif(type(obj) is AIFood):
			aggressor.setPosition(obj.getPosition())
			aggressor.eat(obj)
			return aggressor

		# Currently incoming animal eats other
		battle_ground = obj.getPosition()
		aggressor.eat(obj)
		aggressor.setPosition(battle_ground)
		return aggressor