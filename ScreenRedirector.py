class ScreenRedirector:
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
