import pygame, math
from time import strftime
import Screen
from AnimationManager import *
from NewsCollector import *
from ScreenRedirector import *


class NewsScreen():

	def __init__(self, windowres, fade_direction=""):
		self.WindowRes = windowres
		self.ScreenStatus = "RUNNING"
		self.fade_direction = fade_direction

		self.separator_image = pygame.image.load("Images/vertical_separator.png").convert_alpha()

		self.TitleFont = pygame.font.Font("Fonts/HelveticaNeue-Light.ttf", 25)
		self.WaitFont  = pygame.font.Font("Fonts/HelveticaNeue-UltraLight.ttf", 22)
		self.PostTitleFont = pygame.font.Font("Fonts/HelveticaNeue-Medium.ttf", 12, bold=False)

		
		self.animation = AnimationManager()
		self.python_fetched = False
		self.fb_fetched = False
		self.lemonde_fetched = False

		

	def Update(self, InputEvents):
		if "LEFT" in InputEvents:
			self.ScreenStatus = "FADING_OUT_GOTO_" + ScreenRedirector().next_screen("NEWSSCREEN", "LEFT") + "_AND_DEAD"

		if self.ScreenStatus is "RUNNING":
			if not self.python_fetched:
				self.python_news = NewsCollector().get_python_reddit()
				print "python posts collected"
				self.python_fetched = True
				self.animation.reset()

			if not self.fb_fetched:
				self.fb_news = NewsCollector().get_fb_notifications()
				print "facebook posts collected"
				self.fb_fetched = True
				self.animation.reset()

			if not self.lemonde_fetched:
				self.lemonde_news = NewsCollector().get_lemonde_posts()
				print "lemonde posts collected"
				self.lemonde_fetched = True
				self.animation.reset()

	def Draw(self, gameDisplay):
		lemondeSurface = self.TitleFont.render("Le Monde", True, (255, 255, 255))
		fbSurface = self.TitleFont.render("Facebook", True, (255, 255, 255))
		redditSurface = self.TitleFont.render("Python Reddit", True, (255, 255, 255))

		if not self.python_fetched:
			waitSurface = self.WaitFont.render("Fetching data...", False, (255, 255, 255))

		self.renderNews(gameDisplay)

		'''
		Display separators and Titles
		'''
		gameDisplay.blit(self.separator_image, (self.WindowRes[0] / 3, \
			(self.WindowRes[1] - self.separator_image.get_rect().height) / 2))
		gameDisplay.blit(self.separator_image, (self.WindowRes[0] * 2/3, \
			(self.WindowRes[1] - self.separator_image.get_rect().height) / 2))

		gameDisplay.blit(lemondeSurface, (self.WindowRes[0] / 6 - lemondeSurface.get_rect().width / 2, \
			(self.WindowRes[1] - self.separator_image.get_rect().height) / 2 - lemondeSurface.get_rect().height / 2))
		gameDisplay.blit(fbSurface,      (self.WindowRes[0] / 2 - fbSurface.get_rect().width / 2, \
			(self.WindowRes[1] - self.separator_image.get_rect().height) / 2 - fbSurface.get_rect().height / 2))
		gameDisplay.blit(redditSurface,  (self.WindowRes[0] * 5/6 - redditSurface.get_rect().width / 2, \
			(self.WindowRes[1] - self.separator_image.get_rect().height) / 2 - redditSurface.get_rect().height / 2))

		'''
		Display the waiting label when loading info
		'''
		if not self.python_fetched:  # a droite
			gameDisplay.blit(waitSurface,      (self.WindowRes[0] * 5/6 - waitSurface.get_rect().width / 2, \
				self.WindowRes[1] / 2 - waitSurface.get_rect().height / 2))
		if not self.fb_fetched:      # centre
			gameDisplay.blit(waitSurface,      (self.WindowRes[0] / 2 - waitSurface.get_rect().width / 2, \
				self.WindowRes[1] / 2 - waitSurface.get_rect().height / 2))
		if not self.lemonde_fetched: # gauche
			gameDisplay.blit(waitSurface,      (self.WindowRes[0] * 1/6 - waitSurface.get_rect().width / 2, \
				self.WindowRes[1] / 2 - waitSurface.get_rect().height / 2))


	def renderNews(self, gameDisplay):
		if self.python_fetched == True:
			for i in range(0, len(self.python_news)):
				self.render_block_text(gameDisplay, self.python_news[i], i, self.WindowRes[0] * 2/3)

		if self.fb_fetched == True:
			for i in range(0, len(self.fb_news)):
				self.render_block_text(gameDisplay, self.fb_news[i], i, self.WindowRes[0] / 3)

		if self.lemonde_fetched == True:
			for i in range(0, len(self.lemonde_news)):
				self.render_block_text(gameDisplay, self.lemonde_news[i], i, 0)

	def render_block_text(self, gameDisplay, post, i, xpos):
		if 60 + 25 * i < 420:
			if self.animation.elapsed_time() < 5:
				color = int(255 / (1 + math.exp(-(self.animation.elapsed_time() - 0.07*i) / 0.05)))
			else:
				color = 255


			text = post[0]
			if len(post[0]) > 35:
				text = post[0][:35] + "..."

			textSurface = self.PostTitleFont.render(text, True, (color, color, color))
			gameDisplay.blit(textSurface, (xpos + 20, 60 + 25 * i))

	def Quit(self):
		pass

	def __str__(self):
		return "NEWSSCREEN"