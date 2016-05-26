class Screen():
	'''
	Squelette d'un ecran. On cree une classe 'Screen' vide pour MainSC : quand le fadingScreen de MainSC est
	nul, on met un Screen vide. Cela permet ensuite de faire 'fadingScreen.Update()' meme s'il n'y a pas
	d'ecran actif dans la variable : le fadingScreen ne fait donc rien, mais cette classe permet de faire un code
	plus court et joli dans MainSC.
	'''
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
