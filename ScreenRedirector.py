class ScreenRedirector:
	'''
	Classe morte.
	Auparavant, glisser dans une certaine direction dans une application entrainait forcement
	une transition entre cette aplication et une nouvelle.
	Et la nouvelle application changeait en fonction du sens de glisser. On enregistrait ces directions
	dans des fichiers texte, et cette classe sert a les lire.

	On garde cette classe au cas ou.
	'''
	def next_screen(self, screen_name, direction):
		file = open("ScreenMaps/" + screen_name + ".txt", 'r')
		text = file.read()

		for line in text.split("\n", 5):
			line_info = line.split(' ', 2)
			print line_info[0] + " " + direction
			if line_info[0] == direction:
				try:
					return line_info[1]
				except:
					pass

		return ""
