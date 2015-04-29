from AIObject import *
from AIAnimal import *
from AIFood import *
from util import *
import random as r
import time
from GraphicWrapper import *



class AIEnvironment(object):
	"""
	Defines game world for competing species

	Args:
		None
	"""

	def __init__(self, food_mappings, display = False, use_tkinter = False):
		"""
		Initiailize game world

		Args:
			food_mappings: Two mappings of food to cost/time for species A and B
		"""

		super(AIEnvironment, self).__init__()
		self.food_mappings = food_mappings
		self.will_display = display
		self.use_tkinter = use_tkinter

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


	def generate(self, grid, spA, spB, numFood1, numFood2, steps = 5, seed = None):
		"""
		Initialize one instance of the game world

		Args:
			grid: height and width of the game world
			spA: specication for species A (num, network)
			spB: specication for species B (num, network)
			numFood1: number of food source 1
			numFood2: number of food source 2
			steps: number of steps to run simulation
			seed: seed for random numbers, default None (current system time)
		"""

		numA, networkA = spA
		numB, networkB = spB

		# Initialize game world
		self.animals = []
		self.food = []
		self.world = [[None for x in range(grid)] for x in range(grid)]
		self.space = grid * grid
		self.steps = steps

		# Set seed for world
		r.seed(seed)

		# Declare start of simulation
		# print("Generating New World: ")

		# Place speciesA on world
		food_map = self.food_mappings[0]
		for i in range(numA):
			(x,y) = self.generatePosition(grid)
			animal = AIAnimal(networkA, food_map, SPECIES_A, (x,y))
			self.animals.append(animal)

			self.world[x][y] = animal

		# Place speciesB on world
		food_map = self.food_mappings[1]
		for i in range(numB):
			(x,y) = self.generatePosition(grid)
			animal = AIAnimal(networkB, food_map, SPECIES_B, (x,y))
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

		if self.use_tkinter:
			self.runStepsTkinter()
		else:
			self.runSteps()
		return self.evaluateFitness()

	def display(self, val):
		"""
		Displayes game world

		Args:
			None
		"""
		if not (val):
			return

		print("animals: ",list(map((lambda x : (x.getPosition(), x.getPoints())), self.animals)))
		for i in range(len(self.world)):
			for j in range(len(self.world)):
				print(self.world[j][i], end="\t")

			print("\n")

		print(self.evaluateFitness())
		time.sleep(0.5)

	def animalAction(self, animal):
		"""
		Has animal decide on an action and execute

		Args:
			animal: the animal that is going to make a decision
		"""

		action = animal.run(self.world)

		# Move EAST
		if action == 0:
			(x,y) = animal.getPosition()
			animal.setPosition(((x+1) % len(self.world),y))

			self.world[x][y] = None
			self.world[(x+1) % len(self.world)][y] = self.interact(animal, self.world[(x+1) % len(self.world)][y])

		# Move WEST
		elif action == 1:
			(x,y) = animal.getPosition()
			animal.setPosition(( (x-1) % len(self.world) ,y))

			self.world[x][y] = None

			x_space = x - 1
			if (x_space < 0):
				x_space = len(self.world) - 1
			self.world[x_space][y] = self.interact(animal, self.world[x_space][y])

		# Move NORTH
		elif action == 2:
			(x,y) = animal.getPosition()
			animal.setPosition((x,(y+1) % len(self.world)))

			self.world[x][y] = None
			self.world[x][(y+1) % len(self.world)] = self.interact(animal, self.world[x][(y+1) % len(self.world)])

		# Move SOUTH
		elif action == 3:
			(x,y) = animal.getPosition()
			animal.setPosition((x,(y-1) % len(self.world[0])))

			y_space = y - 1
			if (y_space < 0):
				y_space = len(self.world[0]) - 1

			self.world[x][y] = None
			self.world[x][y_space] = self.interact(animal, self.world[x][y_space])

	def runSingleStepTkinter(self):
		"""
		For use with TKinter, which will handle the execution of multiple steps by itself.
		"""
		r.shuffle(self.animals)
		for i in range(len(self.animals)):
			animal = self.animals[i]

			if animal.getPosition():
				self.animalAction(animal)

	def runStepsTkinter(self):
		steps = self.steps
		# Create wrapper for graphics
		self.graphic_wrapper = GraphicWrapper(self.world, self.runSingleStepTkinter, steps)

		if not self.will_display:
			for j in range(steps):
				runSingleStepTkinter()
		else:
			self.graphic_wrapper.run()


	def runSteps(self):
		"""
		Per step has each animal make an action

		Args:
			steps: number of steps to run the world
		"""
		steps = self.steps
		for j in range(steps):
			# self.display(self.will_display)
			r.shuffle(self.animals)
			for i in range(len(self.animals)):
				animal = self.animals[i]

				if animal.getPosition():
					self.animalAction(animal)


		self.display(self.will_display)

	def evaluateFitness(self):
		"""
		Calculates the fitness of both species

		Args:
			None

		Returns:
			Tuple where first is the fitness of speciesA, second is speciesB.
		"""
		stats = {"food_counts": {SPECIES_A: {}, SPECIES_B: {}}}

		scoreA = 0
		totalA = 0
		scoreB = 0
		totalB = 0

		for i in range(len(self.animals)):
			animal = self.animals[i]

			if (animal.getType() == SPECIES_A):
				scoreA += animal.getPoints()
				totalA += 1
				for key, count in animal.food_counts.items():
					if key not in stats["food_counts"][SPECIES_A]:
						stats["food_counts"][SPECIES_A][key] = 0
					stats["food_counts"][SPECIES_A][key] += count
			else:
				scoreB += animal.getPoints()
				totalB += 1
				for key, count in animal.food_counts.items():
					if key not in stats["food_counts"][SPECIES_B]:
						stats["food_counts"][SPECIES_B][key] = 0
					stats["food_counts"][SPECIES_B][key] += count

		fitnessA = scoreA / totalA
		fitnessB = scoreB / totalB

		return (fitnessA, fitnessB, stats)

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