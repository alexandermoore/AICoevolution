import AIEnvironment as aie

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

arena = aie.AIEnvironment([speciesA_map, speciesB_map])

# if __name__ == '__main__':
	 # arena.generate(10, 5, 5, 45, 45, 20)
