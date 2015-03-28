class AIObject(object):
	"""
	Defines methods all objects must have

	Args:
		name: type of object
	"""
	def __init__(self, name):
		self.name = name


	def getType(self):
		return self.name
