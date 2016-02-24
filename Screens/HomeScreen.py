'''
The homescreen displays the time, date and invites the user to go to other Screens
	- LEFT : Alarms
	- RIGHT : Calendar
	- DOWN : Notifications
	- UP : Tools
'''

import pygame, math
from time import strftime
import Screen
from AnimationManager import *
from ScreenRedirector import *

class HomeScreen():

	def __init__(self, windowres, fade_direction=""):
		self.TimeFont = pygame.font.Font("Fonts/HelveticaNeue-UltraLight.ttf", 180)
		self.SecondsFont = pygame.font.Font("Fonts/HelveticaNeue-UltraLight.ttf", 80 )
		self.DateFont = pygame.font.Font("Fonts/HelveticaNeue-Light.ttf",      25 )

		self.WindowRes = windowres
		self.ScreenStatus = "FADING_IN"
		self.fade_direction = fade_direction

		self.animation = AnimationManager()
		self.time_offset = 0.0
		self.time_color = 0

		self.date_color = 0
		self.date_offset = 0.0


	def Update(self, InputEvents):
		if "DOWN" in InputEvents:
			self.ScreenStatus = "FADING_OUT"
			self.fade_direction = "DOWN"
			self.animation.reset()
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

		print self.ScreenStatus + self.fade_direction

	def Draw(self, gameDisplay):

		'''
		Renders the Date and Time (date, Hours+Minutes, Seconds)
		'''
		timeSurface    = self.TimeFont.render   ( strftime("%H:%M"), True, (self.time_color, self.time_color, self.time_color))
		secondsSurface = self.SecondsFont.render( strftime(":%S"), True, (self.time_color, self.time_color, self.time_color))
		dateSurface    = self.DateFont.render   ( "Today is " + strftime("%A %d, %B %Y"), True, (self.date_color, self.date_color, self.date_color))


		secondsWidth = self.SecondsFont.render(strftime(":00"), True, (self.date_color, self.date_color, self.date_color)).get_rect().width
		timePos = self.WindowRes[0] / 2 - (timeSurface.get_rect().width + secondsWidth) / 2

		gameDisplay.blit(timeSurface,    (timePos, self.WindowRes[1] * 2/5 - timeSurface.get_rect().height/2))
		gameDisplay.blit(secondsSurface, (timePos + timeSurface.get_rect().width, timeSurface.get_rect().bottom - timeSurface.get_rect().height * 1/5))
		gameDisplay.blit(dateSurface,    (self.WindowRes[0] / 2 - dateSurface.get_rect().width/2, self.WindowRes[1] * 3/5 - dateSurface.get_rect().height/2))

	def fade_in(self):
		animTime = self.animation.elapsed_time()

		if self.fade_direction is "UP":
			if animTime > 0 and animTime < 1:
				self.time_color = 255 / (1 + math.exp(-(animTime - 0.5) / 0.1))

			if animTime > 0.75 and animTime < 1.75:
				self.date_color = 255 / (1 + math.exp(-(animTime - 1.25) / 0.1))

			if animTime > 2:
				self.ScreenStatus = "RUNNING"

	def fade_out(self):
		animTime = self.animation.elapsed_time()

		if animTime > 0 and animTime < 1:
				self.time_color = 255 / (1 + math.exp(-(0.5 - animTime) / 0.1))
		if animTime > 0.5 and animTime < 1:
			self.date_color = 255 / (1 + math.exp(-(0.75 - animTime) / 0.05))

		if self.fade_direction is "LEFT":
			if animTime > 1.5:
				self.ScreenStatus = "GOTO_" + ScreenRedirector().next_screen("HOMESCREEN", "LEFT") + "_AND_DEAD"
		if self.fade_direction is "RIGHT":
			if animTime > 1.5:
				self.ScreenStatus = "GOTO_" + ScreenRedirector().next_screen("HOMESCREEN", "RIGHT") + "_AND_DEAD"
		if self.fade_direction is "UP":
			if animTime > 1.5:
				self.ScreenStatus = "GOTO_" + ScreenRedirector().next_screen("HOMESCREEN", "UP") + "_AND_DEAD"
		if self.fade_direction is "DOWN":
			if animTime > 1.5:
				self.ScreenStatus = "GOTO_" + ScreenRedirector().next_screen("HOMESCREEN", "DOWN") + "_AND_DEAD"




	def Reset(self):
		pass

	def Quit(self):
		pass

	def __str__(self):
		return "HOMESCREEN"
