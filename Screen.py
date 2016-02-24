class Screen():

	def __init__(self, windowres, fade_direction=""):
		self.WindowRes = windowres
		self.ScreenStatus = "NONE"
		self.fade_direction = fade_direction

	def Update(self, LeapEvents):
		pass

	def Draw(self, gameDisplay):
		pass

	def Quit(self):
		pass

	def __str__(self):
		return "SCREEN"