import math, pygame

class TouchGesturesManager():

	def __init__(self):
		'''
		This variable stores the gestures found with the mouse (e.g. when a mousePress happened but not
		the same button's mouseRelease event). This allows us to  store the mouse position when it was clicked
		'''
		self.current_gesture = None

		'''
		Variables
		'''
		self.mouse_pressed = False
		self.previous_mousepos = [0, 0]
		self.previous_frame_events = []

	def Update(self, pygame_events):
		frame_events = []

		mx, my = pygame.mouse.get_pos()
		mousepos = [mx, my]


		for event in pygame_events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				self.mouse_pressed = True
				self.current_gesture = MouseGesture(mousepos)

			if event.type == pygame.MOUSEBUTTONUP:
				self.mouse_pressed = False

				self.current_gesture.mouseReleased(mousepos)
				result = self.current_gesture.result_direction

				if result is not None:
					frame_events.append(result)
				frame_events.append("ENDSCROLL")
				self.current_gesture = None



		if self.mouse_pressed == True:
			frame_movement = [self.previous_mousepos[0] - mousepos[0], self.previous_mousepos[1] - mousepos[1]]
			if not (frame_movement[0] == 0 and frame_movement[1] == 0):
				frame_events.append("SCROLL " + str(frame_movement[0]) + " " + str(frame_movement[1]))



		self.previous_mousepos = mousepos
		self.previous_frame_events = frame_events
		if len(frame_events) > 0: print frame_events
		return frame_events

class MouseGesture():
	def __init__(self, mousePos):
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
			On calcule l'angle et on prend une approximation entre 0 et PI (le signe n'apparait pas encore)
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

			swiping in one direction causes the program to open the screen in the opposite direction (logique).
			'''
			if angle > 315 or angle < 45:
				self.result_direction = "RIGHT"
			elif angle > 45 and angle < 135:
				self.result_direction = "UP"
			elif angle > 135 and angle < 225:
				self.result_direction = "LEFT"
			elif angle > 225 and angle < 315:
				self.result_direction = "DOWN"

		elif r < 20:
			x, y = pygame.mouse.get_pos()
			#DEBUG print "mouse touch : " + str(x) + " " + str(y)
			self.result_direction = "TOUCH " + str(x) + " " + str(y)
