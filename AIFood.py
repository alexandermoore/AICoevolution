from AIObject import *

class AIFood(AIObject):
	"""
	Defines food specific behavior

	Args:
		name: type of food
	"""

	def __init__(self, name):
		super(AIFood, self).__init__(name)
