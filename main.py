#! /usr/bin/python

import AIEnvironment as aie
from NeuralNetwork import *
from NeuralNetworkEvolver import *

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

POP_A = 2
POP_B = 2
NUM_FOOD_1 = 45
NUM_FOOD_2 = 45
STEPS = 5
DIM = 10

if __name__ == '__main__':
	evolverA = NeuralNetworkEvolver()
	evolverB = NeuralNetworkEvolver()
	genomesA = [NeuralNetwork(), NeuralNetwork(), NeuralNetwork()]
	genomesB = [NeuralNetwork(), NeuralNetwork(), NeuralNetwork()]
	arena = aie.AIEnvironment([speciesA_map, speciesB_map])

	fit_countA = [(0.0,0.0)] * len(genomesA)
	fit_countB = [(0.0,0.0)] * len(genomesB)
	for i in range(len(genomesA)):
		networkA = genomesA[i]
		for j in range(len(genomesB)):
			networkB = genomesB[j]

			specificationA = (POP_A, networkA)
			specificationB = (POP_B, networkB)
			fitA, fitB = arena.generate(DIM, specificationA, specificationB, NUM_FOOD_1, NUM_FOOD_2, STEPS)

			(old_fit, old_count) = fit_countA[i]
			fit_countA[i] = (old_fit + fitA, old_count + 1.0)

			(old_fit, old_count) = fit_countB[j]
			fit_countB[j] = (old_fit + fitB, old_count + 1.0)

	fitnessA = []
	fitnessB = []

	for i in range(len(genomesA)):
		fitnessA.append((genomesA[i], fit_countA[i][0]/fit_countA[i][1]))

	for i in range(len(genomesB)):
		fitnessB.append((genomesB[i], fit_countB[i][0]/fit_countB[i][1]))

	genomesA = evolverA.evolve(fitnessA)
	genomesB = evolverB.evolve(fitnessB)