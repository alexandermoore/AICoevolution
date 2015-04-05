from AIObject import *

class AIFood(AIObject):
	"""
	Defines food specific behavior

	Args:
		name: type of food
	"""

	def __init__(self, name, position):
		super(AIFood, self).__init__(name, position)

	def __str__(self):
		return '\033[92m' + self.name + '\033[0m'
