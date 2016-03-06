'''
L'ecran d'accueil affiche l'heure et la date, l'heure et les widgets,
et est le centre du systeme pour redigirer l'utilisateur vers les applications
disponibles :
	- LEFT  : Application favorie 1
	- RIGHT : Application favorie 2
	- DOWN  : Notifications
	- UP    : Applications
'''

import pygame, math
from time import strftime
import Screen
from AnimationManager import *
from ScreenRedirector import *
from Helpers import Helpers
from WidgetManager import *

class HomeScreen():

	def __init__(self, windowres, fadeorigin="APP"):
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
		self.AppsTitleFont = pygame.font.Font("Fonts/HelveticaNeue-Light.ttf",      22 )
		self.DateFont      = pygame.font.Font("Fonts/HelveticaNeue-Light.ttf",      25 )

		self.WindowRes = windowres
		self.ScreenStatus = "FADING_IN"
		self.fade_origin = fadeorigin

		'''
		On cree un chronometre qui nous permet de faire avancer des animations
		Et des variables qui sont l'objet de ces animations
		'''
		self.animation = AnimationManager()
		self.time_color = 0
		self.date_color = 0
		self.bg_transp = 20.0

		'''
		Variables pour gerer le swipe entre ecran d'acceuil et menu d'applications
		'''
		self.ancrage = 0
		self.scrolling = False

		self.widget_manager = WidgetManager(self.WindowRes)


	def Update(self, InputEvents):
		'''-------------------------------------------------------------------------------------------------------------
		------------------------------------------------PARTIE SCROLL---------------------------------------------------
		-------------------------------------------------------------------------------------------------------------'''
		'''
		Partie qui recupere les entrees tactiles pour voir s'il y a un scroll, et ajuste le scroll de maniere generale :
			- Quand il y a scroll, bouge tous les panels dans la direction du scroll
			- Limite ce scroll entre la zone des deux panels pour eviter qu'on depasse et aille trop loin
			- Enregistre quand l'utilisateur a fini de scroller pour permettre a la partie suivante de code de se mettre
			 	a recentrer les panels dans le cas ou l'utilisateur a arrete son scroll en plein milieu
		'''
		for event in InputEvents:
			if "SCROLL " in event:
				self.scrolling = True
				scroll_distanceY = Helpers.get_message_x_y(event)[1]
				self.ancrage -= scroll_distanceY
				if self.ancrage < 0   : self.ancrage = 0
				if self.ancrage > self.WindowRes[1] : self.ancrage = self.WindowRes[1]
			if "ENDSCROLL" in event:
				self.scrolling = False

		'''
		Partie qui s'occupe de l'animation du retour de scrolling (quand on lache le doigt et que l'ecran se recentre
		automatiquement)
		'''
		if self.ancrage != 0 and self.ancrage != self.WindowRes[1] and self.scrolling == False:
			if self.ancrage >  self.WindowRes[1] / 2:
				self.ancrage = Helpers.mathlerp(self.ancrage, self.WindowRes[1], 0.55)
				if self.ancrage > self.WindowRes[1] - 2: self.ancrage = self.WindowRes[1]
			if self.ancrage <= self.WindowRes[1] / 2:
				self.ancrage = Helpers.mathlerp(self.ancrage, 0                , 0.55)
				if self.ancrage < 2                    : self.ancrage = 0

		'''-------------------------------------------------------------------------------------------------------------
		----------------------------------------------PARTIE ANIMATIONS-------------------------------------------------
		-------------------------------------------------------------------------------------------------------------'''
		'''
		Si l'utilisateur a fait un swype (et uniquement pendant qu'il est sur le panel ecran d'acceuil),
		On envoie un texto comme quoi on commence a disparaitre et on enregistre la direction de l'utilisateur
		pour plus tard (voir fade_out()).
		'''
		if "LEFT" in InputEvents and self.ancrage < 40:
			self.ScreenStatus = "FADING_OUT"
			self.fade_direction = "LEFT"
			self.animation.reset()
		if "RIGHT" in InputEvents and self.ancrage < 40:
			self.ScreenStatus = "FADING_OUT"
			self.fade_direction = "RIGHT"
			self.animation.reset()


		if self.ScreenStatus is "FADING_IN":
			self.fade_in()
		if self.ScreenStatus is "FADING_OUT":
			self.fade_out()


		'''-------------------------------------------------------------------------------------------------------------
		-------------------------------------------PARTIE FONCTIONNALITES-----------------------------------------------
		-------------------------------------------------------------------------------------------------------------'''
		'''
		On laisse le manager de widgets updater les widgets.
		HomeScreen ne s'occupe pas des widgets, seul WidgetManager dessine, update et distribue les inputs.
		'''
		self.widget_manager.Update(InputEvents)






	def Draw(self, gameDisplay):
		'''
		On affiche le fond d'ecran en fond (cad en premiere position dans le Draw())
		'''
		affine = -0.229166667 * self.ancrage + 180
		if self.ScreenStatus == "RUNNING":
			Helpers.blit_alpha(gameDisplay, self.bg_img, (0, 0),  affine)
		if "FADING" in self.ScreenStatus:
			Helpers.blit_alpha(gameDisplay, self.bg_img, (0, 0),  self.bg_transp)


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
		# on dessine l'heure
		Helpers.blit_alpha(gameDisplay, timeSurface,    (timePos,
														 self.WindowRes[1] * 2/5 - timeSurface.get_rect().height/2 - 60
														 											+ self.ancrage),
														 self.time_color)

		# on dessine les secondes
		Helpers.blit_alpha(gameDisplay, secondsSurface, (timePos + timeSurface.get_rect().width,
														 timeSurface.get_rect().bottom - timeSurface.get_rect().height * 1/5 - 45
														 											+ self.ancrage),
														 self.time_color)

		# on dessine la date situee sous l'heure
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



		self.widget_manager.Draw(gameDisplay, self.ancrage)

	def fade_in(self):
		animTime = self.animation.elapsed_time()

		'''
		Animation du fond d'ecran. Si l'ecran precedent est STARTSCREEN, on ne fait pas d'animation (pour une transition
		plus jolie). Sinon, on fait apparaitre progressivement le fond d'ecran.

		TEMPORAIRE : Choisir l'animation ensemble, l'apparition progressive n'est que temporaire.
		'''
		if self.fade_origin is "STARTSCREEN":
			self.bg_transp = 180
		else:
			if animTime > 0 and animTime < 2:                                       # TEMPORAIRE
				self.bg_transp  = 160 / (1 + math.exp(-(animTime - 1) / 0.2)) + 20  # TEMPORAIRE

		if animTime > 0 and animTime < 1:
			self.time_color = 255 / (1 + math.exp(-(animTime - 0.5) / 0.1))

		if animTime > 0.75 and animTime < 1.75:
			self.date_color = 255 / (1 + math.exp(-(animTime - 1.25) / 0.1))

		'''
		Envoie un texto qui signale au MainSC que la transition est finie, et donc qu'il peut supprimer
		l'ecran occupe precedemment.
		'''
		if animTime > 3:
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
