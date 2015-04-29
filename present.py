#! /usr/bin/python

import pickle
import os
from NeuralNetwork import *
import AIEnvironment as aie
import time
try:
	import numpy as np
	import matplotlib.pyplot as plt
except:
	pass
from collections import Counter

data_file_name = "present-data/"

DIM = 50
POP_A = 100
POP_B = 100
NUM_FOOD_1 = 100
NUM_FOOD_2 = 100
STEPS = 300
BAR_GROUPS = 5


def graph(food_counts, fit_counts, title, prefix):
	spA = np.zeros(BAR_GROUPS)
	spB = np.zeros(BAR_GROUPS)
	fd1 = np.zeros(BAR_GROUPS)
	fd2 = np.zeros(BAR_GROUPS)

	i = 0
	for count in fit_counts.most_common(BAR_GROUPS):
		genA = count[0]
		spA[i] += food_counts[genA]["spA"]
		spB[i] += food_counts[genA]["spB"]
		fd1[i] += food_counts[genA]["fd1"]
		fd2[i] += food_counts[genA]["fd2"]
		i += 1

	spA = spA / 40.0
	spB = spB / 40.0
	fd1 = fd1 / 40.0
	fd2 = fd2 / 40.0

	ind = np.arange(BAR_GROUPS)  # the x locations for the groups
	width = 0.1       # the width of the bars

	fig, ax = plt.subplots()
	rects1 = ax.bar(ind, fd1, width, color='g')
	rects2 = ax.bar(ind+width, fd2, width, color='y')
	rects3 = ax.bar(ind+2*width, spA, width, color='r')
	rects4 = ax.bar(ind+3*width, spB, width, color='b')

	title = prefix + str(title).replace("fd", "pl")
	# add some text for labels, title and axes ticks
	ax.set_ylabel('Scores')
	ax.set_xticks(ind+width)
	ax.set_title(title)
	ax.set_xticklabels( ('G1', 'G2', 'G3', 'G4', 'G5') )

	ax.legend( (rects1[0], rects2[0], rects3[0], rects4[0]), ('pl1', 'pl2', 'spA', 'spB') )

	plt.show()

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
			stats = records["stat"]
			genomesA = list(stats.keys())
			genomesB = list(stats[genomesA[0]].keys())

			food_countsA = Counter()
			food_countsB = Counter()
			fit_countsA = Counter()
			fit_countsB = Counter()

			# print("\nFood counts:")
			for genA in genomesA:
				for genB in genomesB:
					fitA = stats[genA][genB][0]
					fitB = stats[genA][genB][1]
					food_counts = stats[genA][genB][2]["food_counts"]

					fit_countsA[genA] += fitA
					fit_countsB[genB] += fitB

					if not genA in food_countsA.keys():
						food_countsA[genA] = Counter(food_counts["spA"])
					else:
						food_countsA[genA].update(Counter(food_counts["spA"]))

					if not genB in food_countsB.keys():
						food_countsB[genB] = Counter(food_counts["spB"])
					else:
						food_countsB[genB].update(Counter(food_counts["spB"]))

					if (fitA > best_fitA):
						best_fitA = fitA
						bestA = genA

					if (fitB > best_fitB):
						best_fitB = fitB
						bestB = genB

			# print("Graph of Food Counts for A")

			# graph(food_countsA, fit_countsA, records["A"], "For spA: ")
			# print("Graph of Food Counts for B")
			# graph(food_countsB, fit_countsB, records["B"], "For spB: ")
			# Uncomment to run game between "best" species
			arena = aie.AIEnvironment([records["A"], records["B"]], True, True)
			# # print(best_fitA)
			# print(best_fitB)
			# print(len(bestA))
			# print(len(bestB))
			networkA = NeuralNetwork(bestA)
			networkB = NeuralNetwork(bestB)
			specA = (POP_A, networkA)
			specB = (POP_B, networkB)

			print("DISPLAYING BEST FOR PARAMS")
			print(records["A"], records["B"])
			time.sleep(5)
			arena.generate(DIM, specA, specB, NUM_FOOD_1, NUM_FOOD_2, STEPS)



if __name__ == '__main__':
	main()