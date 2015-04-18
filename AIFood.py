from AIObject import *
from util import *

class AIFood(AIObject):
	"""
	Defines food specific behavior

	Args:
		name: type of food
	"""

	def __init__(self, name, position):
		super(AIFood, self).__init__(name, position)

	def __str__(self):
		if USE_COLORS:
			color_a = '\033[92m'
			color_b = '\033[0m'
		else:
			color_a = ''
			color_b = ''
		return color_a + self.name + color_b
