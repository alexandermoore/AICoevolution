import AIEnvironment as aie
import itertools
import pickle
import os
from collections import defaultdict
from datetime import datetime
from NeuralNetwork import *
from NeuralNetworkEvolver import *
from util import *

POP = 20
GENS = 400
networks = [NeuralNetwork() for i in range(POP)]
evo = NeuralNetworkEvolver()
test_data = [i for i  in range(INPUT_NODES)]
target = 1337
for g in range(GENS):
	print("GEN",g)
	networks = evo.evolve([(n, -abs(sum(n.evaluate(test_data)) - target)) for n in networks])
	print(sum(networks[0].evaluate(test_data)))
