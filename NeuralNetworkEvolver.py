from NeuralNetwork import *
import random

MUTATE_CHANCE = 0.10 # Probability of mutating a given weight
MUTATE_VARIANCE = 0.50 # Mutations are performed according to a 0-mean Gaussian with this variance
NUM_CROSSOVER_PTS = 8 # Number of crossover points to use during crossover
HALL_SIZE = 5 # Number of members of Hall of Fame. Each time, 1 random member from hall is inserted into population.

class NeuralNetworkEvolver(object):
	"""
	Defines evolutionary functons on neural network

	"""
	def __init__(self):
		super(NeuralNetworkEvolver, self).__init__()
		self.hall = []

	def __gaussianMutate(self, value):
		return random.gauss(value, MUTATE_VARIANCE)

	def mutate(self, genome):

		# raise NotImplementedError("Return mutated network")
		genome = [self.__gaussianMutate(v) if random.random()<=MUTATE_CHANCE else v for v in genome]
		return genome

	def __genCrossoverPoints(self, length, num_points):
		"""
		Returns the locations of crossover points along a genome of length LENGTH.
		A crossover point at index i means that indices (i+1) and above are on one side and i
		and below are on the other side. Crossover points go from 0 to (length - 2) [-2 because the last
		point needs to have something after it]

		Args:
			length: The length under consideration
			num_points: The number of crossover points
		"""
		cross_pts = []
		cross_pt = -1
		for i in range(num_points):
			# Crossover point must be after the previous point, but early enough so that there's enough room for all the points
			cross_pt = random.randint(cross_pt + 1, length - (num_points - i + 1))
			cross_pts.append(cross_pt)
		return cross_pts

	def crossover(self, genome1, genome2):
		assert( len(genome1) == len(genome2))
		parent_genomes = [genome1, genome2]

		# Determine where crossover will occur
		cross_pts = self.__genCrossoverPoints(len(genome1),NUM_CROSSOVER_PTS)

		# Add each crossoer segment to childrens' genomes
		child1 = []
		child2 = []
		parent_for_child1 = random.randint(0,1)
		parent_for_child2 = (parent_for_child1 + 1) % 2
		prev_pt = -1
		for p in cross_pts:
			child1.extend(parent_genomes[parent_for_child1][prev_pt+1:p+1])
			child2.extend(parent_genomes[parent_for_child2][prev_pt+1:p+1])
			# Alternate which child gets which parent's genome at each crossover point
			parent_for_child1 = (parent_for_child1 + 1) % 2
			parent_for_child2 = (parent_for_child1 + 1) % 2
			prev_pt = p

		# Add the final segment to genomes
		child1.extend(parent_genomes[parent_for_child1][prev_pt+1:])
		child2.extend(parent_genomes[parent_for_child2][prev_pt+1:])

		# raise NotImplementedError("Return network from crossover")
		return (child1, child2)

	def __tournamentSelection(self, networks):
		"""
		Returns one individual selected via tournament selection
		"""
		# TODO IF WE WANT
		return networks[0][0]

	def __getFitnessPropSelector(self, networks):
		"""
		Returns one individual selected via fitness proportionate selection
		"""

		# Preparatory stuff
		fitness_vals = [n[1] for n in networks]
		min_fitness = abs(min(fitness_vals))
		total = sum([f + min_fitness + 1.0 for f in fitness_vals])
		networks = [(networks[i][0], (min_fitness + networks[i][1] + 1.0)/total) for i in range(len(networks))]

		cumulative_sum = 0
		CDF = []

		for network, fit in networks:
			CDF.append(cumulative_sum + fit)
			cumulative_sum += fit
		# Account for floating point errors-- make last CDF element 1 explicitly (so it's not 0.9999...)
		CDF[-1] = 1.0

		# Perform the random selection
		print(CDF)
		while(True):
			select = random.random()
			for i in range(len(networks)):
				if select <= CDF[i]:
					yield networks[i][0]
					break

	def __normalize_genome(self, genome):
		# max_weight = max([abs(g) for g in genome])
		# genome = [g*1.0/max_weight for g in genome]
		return genome

	def evolve(self, networks):
		"""
		Evolves a list of networks based on their fitnesses

		Args:
			networks: list of network / fitness tuples

		Returns:
			new list of networks that are next generation
		"""
		# Sort by fitness value
		networks.sort(key=lambda x: x[1], reverse=True)
		# Add the best to hall of fame, but remove random member if hall too large
		if len(self.hall) > HALL_SIZE:
			self.hall.pop()
		self.hall.append(networks[0][0])
		random.shuffle(self.hall)


		nextgen = []
		N = len(networks)
		extra = math.ceil(N*1.0/2.0) - math.floor(N/2)
		# Create 2 children from each parent pair. If an odd number of networks, then the last
		# pair will only produce 1 child
		parents = self.__getFitnessPropSelector(networks)
		for _ in range(math.floor(N/2)):
			parent1genome = next(parents).genome
			parent2genome = next(parents).genome
			child1genome, child2genome = self.crossover(parent1genome, parent2genome)
			child1genome = self.mutate(child1genome)
			child2genome = self.mutate(child2genome)
			child1genome = self.__normalize_genome(child1genome)
			child2genome = self.__normalize_genome(child2genome)
			child1 = NeuralNetwork(child1genome)
			child2 = NeuralNetwork(child2genome)
			nextgen.extend([child1, child2])
		for _ in range(extra):
			parent1genome = next(parents).genome
			parent2genome = next(parents).genome
			child1genome, _ = self.crossover(parent1genome, parent2genome)
			child1genome = self.mutate(child1genome)
			child1genome = self.__normalize_genome(child1genome)
			child1 = NeuralNetwork(child1genome)
			nextgen.append(child1)
		# Replace the last child with a random hall of famer
		nextgen = nextgen[:-1] + [random.choice(self.hall)]
		return nextgen


	def getHall(self):
		"""
		Return Hall of Fame
		"""

		return self.hall

if __name__ == "__main__":
	evolver = NeuralNetworkEvolver()
	networks = []
	for i in range(6):
		network = NeuralNetwork()
		fitness = random.random()*50
		networks.append((network, fitness))
	print(len(evolver.evolve(networks)))

