from os import name as os_name
SPECIES_A = "spA"
SPECIES_B = "spB"
FOOD_1 = "fd1"
FOOD_2 = "fd2"
USE_COLORS = (os_name != 'nt') # Don't use colors on Windows
IS_WINDOWS = (os_name == 'nt')

GLOBAL_PARAMS = {
	"normal": {
		SPECIES_A: {"sight_range": 2, "move_speed": 1},
		SPECIES_B: {"sight_range": 2, "move_speed": 1}
	},
	"A_fast_B_far": {
		SPECIES_A: {"sight_range": 2, "move_speed": 2},
		SPECIES_B: {"sight_range": 4, "move_speed": 1}
	},
	"A_far_and_fast_B_far": {
		SPECIES_A: {"sight_range": 4, "move_speed": 2},
		SPECIES_B: {"sight_range": 4, "move_speed": 1}
	},
	"A_fast_B_fast": {
		SPECIES_A: {"sight_range": 2, "move_speed": 2},
		SPECIES_B: {"sight_range": 2, "move_speed": 2}
	},
	"A_far": {
		SPECIES_A: {"sight_range": 4, "move_speed": 1},
		SPECIES_B: {"sight_range": 2, "move_speed": 1}
	},
	"A_fast": {
		SPECIES_A: {"sight_range": 2, "move_speed": 2},
		SPECIES_B: {"sight_range": 2, "move_speed": 1}
	},
	"B_fast": {
		SPECIES_A: {"sight_range": 2, "move_speed": 1},
		SPECIES_B: {"sight_range": 2, "move_speed": 2}
	},
	"A_far_and_fast": {
		SPECIES_A: {"sight_range": 4, "move_speed": 2},
		SPECIES_B: {"sight_range": 2, "move_speed": 1}
	}, 
	"A_far_B_far": {
		SPECIES_A: {"sight_range": 4, "move_speed": 1},
		SPECIES_B: {"sight_range": 4, "move_speed": 1},
	},
	"A_far_B_fast": {
		SPECIES_A: {"sight_range": 4, "move_speed": 1},
		SPECIES_B: {"sight_range": 2, "move_speed": 2},	
	}
}

GLOBAL_PARAM_NAME = "normal"
