import pygame, time, math
from time import strftime
from AnimationManager import *
from ScreenRedirector import *
from Helpers import Helpers

class StartScreen():

	def __init__(self, windowres, fade_direction=""):
		self.bg_img = pygame.image.load("Images/landscape1.png")

		self.TitleFont = pygame.font.Font("Fonts/HelveticaNeue-UltraLight.ttf", 180)
		self.SwipeFont = pygame.font.Font("Fonts/HelveticaNeue-Light.ttf",      25 )
		self.TimeFont  = pygame.font.Font("Fonts/HelveticaNeue-UltraLight.ttf", 60 )

		self.WindowRes = windowres
		self.ScreenStatus = "FADING_IN"
		self.fade_direction = fade_direction

		'''
		Create the animation structure
		'''
		self.animation = AnimationManager()
		self.bonjour_offset = 0.0
		self.bonjour_color = 0

		self.swipe_color = 0
		self.swipe_offset = 0.0

		self.time_color = 0
		self.time_offset = 0.0
		self.goto_sent = False

	def Update(self, InputEvents):
		if self.ScreenStatus is not "FADING_OUT" and self.ScreenStatus is not "DEAD":
			'''
			Handle Gestures in order to go to the next screen
			'''
			if "UP" in InputEvents:
				self.ScreenStatus = "FADING_OUT"
				self.animation.reset()




		if self.ScreenStatus is "FADING_IN":
			self.fade_in()
		if self.ScreenStatus is "FADING_OUT":
			self.fade_out()


		'''
		LOGISTIC FUNCTION USER GUIDE :

		if animTime > BEGIN_TIME and animTime < END_TIME:
			self.swipe_color = AMPLITUDE / (1 + math.exp(-(INVERT animTime - MOY_TIMES) / DURATION))

			- BEGIN_TIME : when the animation begins after the AnimationMaganer has started.
			- END_TIME : when the animation ends.
			- AMPLITUDE : the movement will go from 0 to the number specified. You can put a minus sign here to go to negatives.
			- MOY_TIMES : it is equal to (BEGIN_TIME + END_TIME) / 2.
			- IVNERT : put the MOY_TIMES here instead if you want the curve to go from AMPLITUDE to 0 (the curve is upside-down).
			- DURATION : you have to adapt this number to the duration of the animation.
				- 0.1 : the animation lasts 1sec
				- 0.2 : the animation lasts 2sec
		'''





	def Draw(self, gameDisplay):
		'''
		On dessine le fond d'ecran
		'''
		Helpers.blit_alpha(gameDisplay, self.bg_img, (0, 0), 180)

		'''
		On cree les textes
		'''
		titleSurface = self.TitleFont.render("Bonjour !",                           True, (255, 255, 255))
		swipeSurface = self.SwipeFont.render("Balayez vers le haut pour continuer", True, (255, 255, 255))
		timeSurface  = self.TimeFont.render( strftime("%H:%M:%S"),                  True, (255, 255, 255))

		'''
		Calculs de positions pour simplifier les blit() en bas
		'''
		secondsWidth = self.TimeFont.render(strftime("00:00:00"), True, (250, 250, 250)).get_rect().width

		'''
		On dessine tout, avec transparence pour les animations
		'''
		# on dessine l'heure situee en bas
		Helpers.blit_alpha(	gameDisplay,
		 					timeSurface,
							(self.WindowRes[0] / 2 - secondsWidth / 2,
							self.WindowRes[1] * 6.4/8 - timeSurface.get_rect().height / 2 + self.time_offset),
							self.time_color)

		# on dessine la ligne qui demande de glisser vers le haut
		Helpers.blit_alpha( gameDisplay,
							swipeSurface,
							(self.WindowRes[0] / 2 - swipeSurface.get_rect().width / 2,
							self.WindowRes[1] / 2 - swipeSurface.get_rect().height / 2 + 50  + self.swipe_offset),
							self.swipe_color)

		# on dessine le Bonjour au centre
		Helpers.blit_alpha( gameDisplay,
							titleSurface,
							(self.WindowRes[0] / 2 - titleSurface.get_rect().width / 2,
							self.WindowRes[1] / 2 - titleSurface.get_rect().height / 2 - 25 + self.bonjour_offset),
							self.bonjour_color)

	def fade_in(self):
		animTime = self.animation.elapsed_time()

		'''
		Bonjour Text animations
		'''
		if animTime > 0.5 and animTime < 1.5:
			self.bonjour_color = 255 / (1 + math.exp(-(animTime - 1) / 0.1))

		if animTime > 2 and animTime < 4:
			self.bonjour_offset = -70 / (1 + math.exp(-(animTime - 3) / 0.2))

		'''
		Swipe Text animations
		'''
		if animTime > 3 and animTime < 4:
			self.swipe_color = 255 / (1 + math.exp(-(animTime - 3.5) / 0.1))

		'''
		Time Text animations
		'''
		if animTime > 4.5 and animTime < 5.5:
			self.time_color = 255 / (1 + math.exp(-(animTime - 5) / 0.1))

		if animTime >= 5.5: self.ScreenStatus = "RUNNING"

	def fade_out(self):
		animTime = self.animation.elapsed_time()

		if animTime > 0.0 and animTime < 0.5:
			self.bonjour_color = 255 / (1 + math.exp(-(0.25 - animTime) / 0.05))
			self.bonjour_offset = -70 / (1 + math.exp(-(4 - 3) / 0.2)) + -50 / (1 + math.exp(-(animTime - 0.25) / 0.05))

		if animTime > 0.25 and animTime < 0.75:
			self.swipe_color = 255 / (1 + math.exp(-(0.5 - animTime) / 0.05))
			self.swipe_offset = -30 / (1 + math.exp(-(animTime - 0.5) / 0.05))

		if animTime > 0.5 and animTime < 1:
			self.time_color = 255 / (1 + math.exp(-(0.75 - animTime) / 0.05))
			self.time_offset = -30 / (1 + math.exp(-(animTime - 0.75) / 0.05))

		if animTime > 0.9 and self.goto_sent == False: # when the animation of the next screen starts
			self.ScreenStatus = "GOTO_" + ScreenRedirector().next_screen("STARTSCREEN", "DOWN") + "_AND_DEAD"
			self.goto_sent = True
		'''if animTime > 1.5: # when the animation is finished, the screen can be killed.
			self.ScreenStatus = "DEAD"'''

	def Reset(self):
		pass

	def Quit(self):
		pass

	def __str__(self):
		return "STARTSCREEN"
