'''
The homescreen displays the time, date and invites the user to go to other Screens
	- LEFT : Alarms
	- RIGHT : Calendar
	- DOWN : Notifications
	- UP : Applications
'''

import pygame, math
from time import strftime
import Screen
from AnimationManager import *
from ScreenRedirector import *
from Helpers import Helpers

class HomeScreen():

	def __init__(self, windowres, fade_direction=""):
		'''
		On charge le fond d'ecran
		'''
		self.bg_img = pygame.image.load("Images/landscape1.png").convert_alpha()
		self.horizontal_line = pygame.image.load("Images/horizontal_separator.png").convert_alpha()

		'''
		On charge les polices qui permettent d'afficher du texte
		'''
		self.TimeFont      = pygame.font.Font("Fonts/HelveticaNeue-UltraLight.ttf", 180)
		self.SecondsFont   = pygame.font.Font("Fonts/HelveticaNeue-UltraLight.ttf", 80 )
		self.AppsTitleFont = pygame.font.Font("Fonts/HelveticaNeue-Light.ttf", 22 )
		self.DateFont      = pygame.font.Font("Fonts/HelveticaNeue-Light.ttf",      25 )

		self.WindowRes = windowres
		self.ScreenStatus = "FADING_IN"
		self.fade_direction = fade_direction

		'''
		On cree un chronometre qui nous permet de faire avancer des animations
		Et des variables qui sont l'objet de ces animations
		'''
		self.animation = AnimationManager()
		self.time_color = 0
		self.date_color = 0

		'''
		Variables pour gerer le swipe entre ecran d'acceuil et menu d'applications
		'''
		self.ancrage = 0


	def Update(self, InputEvents):
		for event in InputEvents:
			if "SCROLL " in event:
				scroll_distanceY = Helpers.get_message_x_y(event)[1]
				self.ancrage -= scroll_distanceY
				if self.ancrage < 0   : self.ancrage = 0   	# on limite l'ancrage entre 0 et 450
				if self.ancrage > self.WindowRes[1] : self.ancrage = self.WindowRes[1]	# pour limiter le scroll
			if "ENDSCROLL" in event:
				if self.ancrage < self.WindowRes[1] / 2:
					self.ancrage = 0
				if self.ancrage >= self.WindowRes[1] / 2:
					self.ancrage = self.WindowRes[1]


		if "LEFT" in InputEvents:
			self.ScreenStatus = "FADING_OUT"
			self.fade_direction = "LEFT"
			self.animation.reset()
		if "RIGHT" in InputEvents:
			self.ScreenStatus = "FADING_OUT"
			self.fade_direction = "RIGHT"
			self.animation.reset()


		if self.ScreenStatus is "FADING_IN":
			self.fade_in()
		if self.ScreenStatus is "FADING_OUT":
			self.fade_out()

		#print self.ScreenStatus + self.fade_direction

	def Draw(self, gameDisplay):
		'''
		On affiche le fond d'ecran en fond (en premiere position dans le Draw())
		'''
		Helpers.blit_alpha(gameDisplay, self.bg_img, (0, 0),  -0.229166667 * self.ancrage + 180)


		'''-------------------------------------------------------------------------------------------------------------
		-------------------------------------------------PANEL HOME-----------------------------------------------------
		-------------------------------------------------------------------------------------------------------------'''
		'''
		Renders the Date and Time (date, Hours+Minutes, Seconds)
		'''
		timeSurface    = self.TimeFont.render   (strftime("%H:%M"), True, (255, 255, 255))
		secondsSurface = self.SecondsFont.render(strftime(":%S"), True, (255, 255, 255))
		dateSurface    = self.DateFont.render   ("Today is " + strftime("%A %d, %B %Y"), True, (255, 255, 255))

		'''
		Calculs de positions pour simplifier les blit() en bas
		'''
		secondsWidth = self.SecondsFont.render(strftime(":00"), True, (255, 255, 255)).get_rect().width
		timePos = self.WindowRes[0] / 2 - (timeSurface.get_rect().width + secondsWidth) / 2

		'''
		On dessine tout, avec transparence
		'''
		#on dessine l'heure
		Helpers.blit_alpha(gameDisplay, timeSurface,    (timePos,
														 self.WindowRes[1] * 2/5 - timeSurface.get_rect().height/2 - 60
														 											+ self.ancrage),
														 self.time_color)

		#on dessine les secondes
		Helpers.blit_alpha(gameDisplay, secondsSurface, (timePos + timeSurface.get_rect().width,
														 timeSurface.get_rect().bottom - timeSurface.get_rect().height * 1/5 - 45
														 											+ self.ancrage),
														 self.time_color)

		#on dessine la date situee sous l'heure
		Helpers.blit_alpha(gameDisplay, dateSurface,    (self.WindowRes[0] / 2 - dateSurface.get_rect().width/2,
														 self.WindowRes[1] * 3/5 - dateSurface.get_rect().height/2 - 60
														 											+ self.ancrage),
														 self.date_color)

		'''
		On affiche la ligne separatrice au milieu des deux panels.
		De plus on la decale un petit peu en fonction de quel ecran on regarde pour constamment la cacher,
		sauf pendant qu'on scroll.
		'''
		if self.ancrage == 0:
			self.off = -1
		elif self.ancrage == self.WindowRes[1]:
			self.off = 0
		gameDisplay.blit(self.horizontal_line, (35, self.off + self.ancrage))




		'''-------------------------------------------------------------------------------------------------------------
		---------------------------------------------PANEL APPLICATIONS-------------------------------------------------
		-------------------------------------------------------------------------------------------------------------'''
		'''
		On genere et dessine le titre "applications" en haut du panel
		'''
		AppsTitleSurface    = self.AppsTitleFont.render   ("Applications", True, (255, 255, 255))
		gameDisplay.blit(AppsTitleSurface, (self.WindowRes[0] / 2 - AppsTitleSurface.get_rect().width / 2,
											7 + self.ancrage - self.WindowRes[1]))

		'''
		On dessine la ligne horizontale separatrice sous le titre "Applications"
		'''
		gameDisplay.blit(self.horizontal_line, (35, 43 + self.ancrage - self.WindowRes[1]))

		'''
		TEMPORAIRE On dessine une petite description sympa
		'''
		AppsTitleSurface    = self.DateFont.render("No apps here yet. Download them in the store !", True, (255, 255, 255))
		gameDisplay.blit(AppsTitleSurface, (self.WindowRes[0] / 2 - AppsTitleSurface.get_rect().width / 2,
											230 + self.ancrage - self.WindowRes[1]))

	def fade_in(self):
		animTime = self.animation.elapsed_time()

		if animTime > 0 and animTime < 1:
			self.time_color = 255 / (1 + math.exp(-(animTime - 0.5) / 0.1))

		if animTime > 0.75 and animTime < 1.75:
			self.date_color = 255 / (1 + math.exp(-(animTime - 1.25) / 0.1))

		'''
		Envoie un texto qui signale au MainSC que la transition est finie, et donc qu'il peut supprimer
		l'ecran occupe precedemment.
		'''
		if animTime > 2:
			self.ScreenStatus = "RUNNING"

	def fade_out(self):
		animTime = self.animation.elapsed_time()

		if animTime > 0 and animTime < 1:
			self.time_color = 255 / (1 + math.exp(-(0.5 - animTime) / 0.1))
		if animTime > 0.5 and animTime < 1:
			self.date_color = 255 / (1 + math.exp(-(0.75 - animTime) / 0.05))

		'''
		Envoie un texto quand l'ecran a fini de disparaitre, avec la destination (le nouvel ecran a faire apparaitre).
		'''
		if animTime > 1.5:
			self.ScreenStatus = "GOTO_" + ScreenRedirector().next_screen("HOMESCREEN", self.fade_direction) + "_AND_DEAD"




	def Reset(self):
		pass
	def Quit(self):
		pass
	def __str__(self):
		return "HOMESCREEN"
