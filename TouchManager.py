import math, pygame

class TouchGesturesManager():
	
	def __init__(self):
		'''
		This variable stores the gestures found with the mouse (e.g. when a mousePress happened but not
		the same button's mouseRelease event). This allows us to  store the mouse position when it was clicked
		'''
		self.current_gesture = None

	def Update(self, pygame_events):
		frame_events = None

		for event in pygame_events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				mousepos = pygame.mouse.get_pos()
				self.current_gesture = MouseGesture("LEFT", mousepos)
			if event.type == pygame.MOUSEBUTTONUP:
				mousepos = pygame.mouse.get_pos()
				self.current_gesture.mouseReleased(mousepos)
				result = self.current_gesture.result_direction

				if result is not None:
					frame_events = result
				print frame_events
				self.current_gesture = None

		
		return frame_events

class MouseGesture():
	def __init__(self, button_ID, mousePos):
		self.button = button_ID
		self.mouse_pos = mousePos

		self.result_direction = ""
		self.Done = False

	def mouseReleased(self, mousePos):
		end_mouse_pos = mousePos
		
		direction = (end_mouse_pos[0] - self.mouse_pos[0], (end_mouse_pos[1] - self.mouse_pos[1]) * -1)

		'''
		Trigonometric side
		'''
		r = math.sqrt((direction[0] ** 2) + (direction[1] ** 2))

		if r > 40:
			'''
			on calcule l'angle et on prend une approximation entre 0 et PI (le signe n'apparait pas encore)
			'''
			angle = math.acos(direction[0] / r) 
			'''
			On prend le sinus pour voir si l'angle est negatif ou pas
			'''
			sin_angle = direction[1] / r # on prend 

			'''
			On le convertit en degres pour questions de simplicite d'ecriture
			'''
			angle = angle * 180.0 / math.pi

			'''
			Si le sinuis est negatif, alors on en deduit le vrai angle entre 0 et 360 degres.
			'''
			if sin_angle < 0:
				angle = 360 - angle

			'''
			Finalement, on en deduit la direction du swipe.

			swiping in oner direction causes the program to open the screen in the opposite direction.
			'''
			if angle > 315 or angle < 45:
				self.result_direction = "RIGHT"
				print "swipe LEFT"
			elif angle > 45 and angle < 135:
				self.result_direction = "DOWN"
				print "swipe UP"
			elif angle > 135 and angle < 225:
				self.result_direction = "LEFT"
				print "swipe RIGHT"
			elif angle > 225 and angle < 315:
				self.result_direction = "UP"
				print "swipe DOWN"