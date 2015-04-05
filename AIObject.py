DIE_COST = 50

class AIObject(object):
	"""
	Defines methods all objects must have

	Args:
		name: type of object
	"""
	def __init__(self, name, position):
		"""
		Return an instance of an object

		Args:
			name: species of food or animal
			position: placement of object on world grid
		"""

		self.name = name
		self.position = position
		self.points = 0

	def getPoints(self):
		"""
		Return the points of the object

		Args:
			None
		"""

		return self.points

	def getType(self):
		"""
		Return specie of object

		Args:
			None

		Returns:
			Type of specie
		"""

		return self.name

	def getPosition(self):
		"""
		Return placement of object on grid

		Args:
			None

		Returns:
			Tuple with x and y coordinate of object on grid
		"""

		return self.position

	def setPosition(self, position):
		"""
		Set position of object

		Args:
			position: new position for object
		"""

		self.position = position

	def die(self):
		"""
		Have object die, penalize animals

		Args:
			None
		"""

		self.position = None
		self.points -= DIE_COST

	def __str__(self):
		return self.name