class AIObject(object):
	"""
	Defines methods all objects must have

	Args:
		name: type of object
	"""
	def __init__(self, name, position):
		self.name = name
		self.position = position

	def getType(self):
		return self.name

	def getPosition(self):
		return self.position

	def setPosition(self, position):
		self.position = position

	def __str__(self):
		return self.name