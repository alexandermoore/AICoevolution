#! /usr/bin/python

import AIEnvironment as aie
import itertools
import pickle
import os
from collections import defaultdict
from datetime import datetime
from NeuralNetwork import *
from NeuralNetworkEvolver import *
from util import *

speciesA_map = {}
speciesA_map["spA"] = -50
speciesA_map["spB"] = 5
speciesA_map["fd1"] = 10
speciesA_map["fd2"] = 20


speciesB_map = {}
speciesB_map["spA"] = 20
speciesB_map["spB"] = -50
speciesB_map["fd1"] = 5
speciesB_map["fd2"] = 5

DIM = 10
# All this is just to maintain the same proportion of each species that you had when the world was 100x100.
# You had 1500 of each in a 100x100 world, so here I'm just scaling it up/down based on the actual dimension.
POP_A = 5
POP_B = 5
NUM_FOOD_1 = 10
NUM_FOOD_2 = 10
STEPS = int(DIM**2 / 4)
NUM_GENERATIONS = 10000
NUM_GENOMES = 40

if __name__ == '__main__':

	#p_range = range(-100, 101, 50)
	#params = itertools.product(p_range, p_range, p_range, p_range, p_range, p_range, p_range, p_range)
	#params = [[-10000,100,2,0,  0,-10000,0,200]]
	params = [[-10000, -10000, 500, 0,
	 		   -10000, -10000, 0, 500]]

	# p_range = range(-100, 101, 50)
	# params = itertools.product(p_range, p_range, p_range, p_range, p_range, p_range, p_range, p_range)
	# params = [[-100,100,0,0,0,-100,100,20], [-100,0,100,20,100,-100,0,0], [-100,-100,0,50,-100,-100,50,0], [-100,-100,0,50,-100,-100,50,0], [100,100,0,50,-100,-100,50,0]]

	data_file_name = "data"
	now = str(datetime.now())
	file_no = 0

	if not os.path.exists(data_file_name):
	    os.makedirs(data_file_name)

	now = now.replace(":","-")
	if not os.path.exists(data_file_name + "/" + now):
		os.makedirs(data_file_name + "/" + now)

	for param in params:
		print(param)
		speciesA_map["spA"] = param[0]
		speciesA_map["spB"] = param[1]
		speciesA_map["fd1"] = param[2]
		speciesA_map["fd2"] = param[3]
		speciesB_map["spA"] = param[4]
		speciesB_map["spB"] = param[5]
		speciesB_map["fd1"] = param[6]
		speciesB_map["fd2"] = param[7]

		evolverA = NeuralNetworkEvolver()
		evolverB = NeuralNetworkEvolver()
		genomesA = [NeuralNetwork() for i in range(NUM_GENOMES)]
		genomesB = [NeuralNetwork() for i in range(1)]

		stats_record = defaultdict(dict)

		for gen in range(NUM_GENERATIONS):
			print("GENERATION: " + str(gen))
			arena = aie.AIEnvironment([speciesA_map, speciesB_map], display=(gen == NUM_GENERATIONS-1))
			# fit_countA = [(0.0,0.0)] * len(genomesA)
			# fit_countB = [(0.0,0.0)] * len(genomesB)
			fit_countA = [0] * len(genomesA)
			fit_countB = [0] * len(genomesB)

			for i in range(len(genomesA)):
				networkA = genomesA[i]
				for j in range(len(genomesB)):
					networkB = genomesB[j]

					specificationA = (POP_A, networkA)
					specificationB = (POP_B, networkB)
					fitA, fitB, stats = arena.generate(DIM, specificationA, specificationB, NUM_FOOD_1, NUM_FOOD_2, STEPS)

					if (gen == NUM_GENERATIONS - 1):
						stats_record[tuple(networkA.getGenome())][tuple(networkB.getGenome())] = (fitA, fitB, stats)
					fit_countA[i] = max(fit_countA[i], fitA)
					fit_countB[j] = max(fit_countB[j], fitB)
					# (old_fit, old_count) = fit_countA[i]
					# fit_countA[i] = (old_fit + fitA, old_count + 1.0)
					#
					# (old_fit, old_count) = fit_countB[j]
					# fit_countB[j] = (old_fit + fitB, old_count + 1.0)

			fitnessA = []
			fitnessB = []
			for i in range(len(genomesA)):
				fitnessA.append((genomesA[i], fit_countA[i]))
			for i in range(len(genomesB)):
				fitnessB.append((genomesB[i], fit_countB[i]))

			# for i in range(len(genomesA)):
			# 	fitnessA.append((genomesA[i], fit_countA[i][0]/fit_countA[i][1]))
			#
			# for i in range(len(genomesB)):
			# 	fitnessB.append((genomesB[i], fit_countB[i][0]/fit_countB[i][1]))

			genomesA = evolverA.evolve(fitnessA)
			genomesB = evolverB.evolve(fitnessB)

		pickle.dump({"A" : speciesA_map, "B" : speciesB_map, "stat": stats_record}, open(data_file_name + "/" + now + "/" + str(file_no), "wb"))
		print(stats_record)
		file_no += 1