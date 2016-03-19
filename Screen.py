class Screen():

	def __init__(self, windowres):
		self.WindowRes = windowres
		self.ScreenStatus = "NONE"

	def Update(self, InputEvents):
		pass

	def Draw(self, gameDisplay):
		pass

	def Quit(self):
		pass

	def __str__(self):
		return "SCREEN"
