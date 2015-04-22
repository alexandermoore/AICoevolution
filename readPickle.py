#! /usr/bin/python

import pickle
import os
from NeuralNetwork import *
import AIEnvironment as aie
import time

data_file_name = "data/"
DIM = 10
POP_A = 10
POP_B = 10
NUM_FOOD_1 = 10
NUM_FOOD_2 = 10
STEPS = 30

def main():
	for directory in os.listdir(data_file_name):
		for f in os.listdir(data_file_name+directory):
			bestA = None
			best_fitA = float("-inf")
			bestB = None
			best_fitB = float("-inf")
			records = pickle.load(open(data_file_name+directory+"/"+f, "rb"))
			print("\n\nFood params:")
			print(records["A"], records["B"])
			time.sleep(2)
			stats = records["stat"]
			genomesA = list(stats.keys())
			genomesB = list(stats[genomesA[0]].keys())

			# print("\nFood counts:")
			for genA in genomesA:
				for genB in genomesB:
					fitA = stats[genA][genB][0]
					fitB = stats[genA][genB][1]
					food_counts = stats[genA][genB][2]["food_counts"]

					if (fitA > best_fitA):
						best_fitA = fitA
						bestA = genA

					if (fitB > best_fitB):
						best_fitB = fitB
						bestB = genB

			arena = aie.AIEnvironment([records["A"], records["B"]], True)
			print(best_fitA)
			print(best_fitB)
			networkA = NeuralNetwork(bestA)
			networkB = NeuralNetwork(bestB)
			specA = (POP_A, networkA)
			specB = (POP_B, networkB)

			arena.generate(DIM, specA, specB, NUM_FOOD_1, NUM_FOOD_2, STEPS)


if __name__ == '__main__':
	main()