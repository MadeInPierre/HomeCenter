import pygame, time, math
from time import strftime
from AnimationManager import *
from ScreenRedirector import *
from Helpers import *

class TimeScreen():

	def __init__(self, windowres, fade_direction=""):
		self.WindowRes = windowres
		self.ScreenStatus = "FADING_IN"
		self.fade_direction = fade_direction

		self.CurrentSection_dic = ["ALARMS", "WORLDCLOCK", "TIMER"]
		self.CurrentSection = 1
		
		self.show_swipe_info = True
		self.swipe_color = 0
		self.swipe_animation = AnimationManager()

		self.TimeFont = pygame.font.Font("Fonts/HelveticaNeue-UltraLight.ttf", 120, bold = True)
		self.SwipeFont = pygame.font.Font("Fonts/HelveticaNeue-Light.ttf",      15 )
		self.CitiesFont  = pygame.font.Font("Fonts/HelveticaNeue-Light.ttf", 25 )
		self.DescriptionFont  = pygame.font.Font("Fonts/HelveticaNeue-Light.ttf", 16)

		self.vertical_separator = pygame.image.load("Images/vertical_separator.png")
		self.horizontal_separator = pygame.image.load("Images/horizontal_separator.png")

		self.swipearrow = SwipeArrow("LEFT", False)

		self.CitiesNames = ["Paris", "Sao Paulo", "Noumea", "Jakarta"]



		'''
		modes :
			ALARMS
			WORLDTIME
			STOPWATCH
			TIMER
		'''
		self.display_mode = "ALARMS"

	def Update(self, InputEvents):
		'''
		Showing and hiding swipe hints, and managing input.
		'''
		if "RIGHT" in InputEvents:
			self.ScreenStatus = "FADING_OUT_GOTO_" + ScreenRedirector().next_screen("TIMESCREEN", "RIGHT") + "_AND_DEAD"
		if "UP" in InputEvents:
			if self.CurrentSection > 0 and self.CurrentSection < len(self.CurrentSection_dic):
				self.CurrentSection -= 1
		if "DOWN" in InputEvents:
			if self.CurrentSection > 0 and self.CurrentSection < len(self.CurrentSection_dic):
				self.CurrentSection += 1
		if "HANDS_ENTERED" in InputEvents:
			self.show_swipe_info = True
			self.swipe_animation.reset()
		if "HANDS_LEFT" in InputEvents:
			self.show_swipe_info = False
			if self.swipe_color > 250:
				self.swipe_animation.reset()
		if "HANDS_LEFT" in InputEvents:
			self.show_swipe_info = False

		if self.ScreenStatus == "FADING_IN":
			animTime = self.swipe_animation.elapsed_time()
			self.swipe_color = 255 / (1 + math.exp(-(2.5 -self.swipe_animation.elapsed_time()) / 0.1))
			if animTime >= 3: 
				self.ScreenStatus = "RUNNING"
				self.swipe_color = 0

		else:
			'''
			Swipe info animations (showing when hand is detected)
			'''
			if self.show_swipe_info == True:
				if self.swipe_animation.elapsed_time() < 5:
					self.swipe_color = 255 / (1 + math.exp(-(self.swipe_animation.elapsed_time() - 0.5) / 0.1))
			else:
				if self.swipe_animation.elapsed_time() < 5:
					self.swipe_color = 255 / (1 + math.exp(-(0.5 -self.swipe_animation.elapsed_time()) / 0.1))

			'''
			
			GENERAL UPDATES ACCORDING TO CURRENT SECTION.
			
			'''
			if self.CurrentSection_dic[self.CurrentSection] is "ALARMS":
				pass
			elif self.CurrentSection_dic[self.CurrentSection] is "TIMER":
				pass
			elif self.CurrentSection_dic[self.CurrentSection] is "WORLDCLOCK":
				pass


	def Draw(self, gameDisplay):
		'''
		Show swipe gestures indications
		'''
		EditSwipeSurface = self.SwipeFont.render("EDIT", True, (self.swipe_color, self.swipe_color, self.swipe_color))
		EditSwipeSurface = Helpers.rotate(EditSwipeSurface, 90)
		gameDisplay.blit(EditSwipeSurface, (12, self.WindowRes[1] / 2 - EditSwipeSurface.get_rect().height / 2 + 1))
		AlarmsSwipeSurface = self.SwipeFont.render("ALARMS", True, (self.swipe_color, self.swipe_color, self.swipe_color))
		gameDisplay.blit(AlarmsSwipeSurface, (self.WindowRes[0] / 2 - AlarmsSwipeSurface.get_rect().width / 2, 12))
		WTSwipeSurface = self.SwipeFont.render("WORLD TIME", True, (self.swipe_color, self.swipe_color, self.swipe_color))
		gameDisplay.blit(WTSwipeSurface, (self.WindowRes[0] / 2 - WTSwipeSurface.get_rect().width / 2, \
			self.WindowRes[1] - 10 - WTSwipeSurface.get_rect().height))
		HomeSwipeSurface = self.SwipeFont.render("HOME", True, (self.swipe_color, self.swipe_color, self.swipe_color))
		HomeSwipeSurface = Helpers.rotate(HomeSwipeSurface, -90)
		gameDisplay.blit(HomeSwipeSurface, (self.WindowRes[0] - HomeSwipeSurface.get_rect().width  - 10, \
			self.WindowRes[1] / 2 - HomeSwipeSurface.get_rect().height / 2))


		self.swipearrow.Draw(gameDisplay, (10, 218 - EditSwipeSurface.get_rect().height / 2 - 20), "LEFT", opacity=self.swipe_color)
		self.swipearrow.Draw(gameDisplay, (10, 218 + EditSwipeSurface.get_rect().height / 2 + 20), "LEFT", opacity=self.swipe_color)

		self.swipearrow.Draw(gameDisplay, (393 - AlarmsSwipeSurface.get_rect().width / 2 - 20, 15), "UP", opacity=self.swipe_color)
		self.swipearrow.Draw(gameDisplay, (393 + AlarmsSwipeSurface.get_rect().width / 2 + 20, 15), "UP", opacity=self.swipe_color)

		self.swipearrow.Draw(gameDisplay, (393 - WTSwipeSurface.get_rect().width / 2 - 20, self.WindowRes[1] - 30), "DOWN", opacity=self.swipe_color)
		self.swipearrow.Draw(gameDisplay, (393 + WTSwipeSurface.get_rect().width / 2 + 20, self.WindowRes[1] - 30), "DOWN", opacity=self.swipe_color)
		self.swipearrow.Draw(gameDisplay, (self.WindowRes[0] - 30, 218 - HomeSwipeSurface.get_rect().height / 2 - 20), "RIGHT", opacity=self.swipe_color)
		self.swipearrow.Draw(gameDisplay, (self.WindowRes[0] - 30, 218 + HomeSwipeSurface.get_rect().height / 2 + 20), "RIGHT", opacity=self.swipe_color)
		
		if self.CurrentSection_dic[self.CurrentSection] is "WORLDCLOCK":
			'''
			Show vertical and horizontal separator
			'''
			gameDisplay.blit(self.vertical_separator, (self.WindowRes[0] / 2, 35))
			gameDisplay.blit(self.horizontal_separator, (35, self.WindowRes[1] / 2))

			'''
			Show Cities Names
			'''
			city1Surface = self.CitiesFont.render(self.CitiesNames[0], True, (255, 255, 255))
			city2Surface = self.CitiesFont.render(self.CitiesNames[1], True, (255, 255, 255))
			city3Surface = self.CitiesFont.render(self.CitiesNames[2], True, (255, 255, 255))
			city4Surface = self.CitiesFont.render(self.CitiesNames[3], True, (255, 255, 255))

			gameDisplay.blit(city1Surface, (self.WindowRes[0] / 4 - city1Surface.get_rect().width / 2, \
							30))
			gameDisplay.blit(city2Surface, (self.WindowRes[0]*3/4 - city2Surface.get_rect().width / 2, \
							30))
			gameDisplay.blit(city3Surface, (self.WindowRes[0] / 4 - city3Surface.get_rect().width / 2, \
							self.WindowRes[1] / 2 + 15))
			gameDisplay.blit(city4Surface, (self.WindowRes[0]*3/4 - city4Surface.get_rect().width / 2, \
							self.WindowRes[1] / 2 + 15))

			'''
			Showing Cities Times
			'''
			time1Surface  = self.TimeFont.render( strftime("%H:%M"), True, (255, 255, 255))
			gameDisplay.blit(time1Surface, (self.WindowRes[0] / 4 - time1Surface.get_rect().width / 2, \
							70))
			gameDisplay.blit(time1Surface, (self.WindowRes[0]*3/4 - time1Surface.get_rect().width / 2, \
							70))
			gameDisplay.blit(time1Surface, (self.WindowRes[0] / 4 - time1Surface.get_rect().width / 2, \
							self.WindowRes[1] / 2 + 52))
			gameDisplay.blit(time1Surface, (self.WindowRes[0]*3/4 - time1Surface.get_rect().width / 2, \
							self.WindowRes[1] / 2 + 52))

			'''
			Showing cities dates
			'''
			date1Surface = self.DescriptionFont.render(strftime("%A %d"), True, (255, 255, 255))
			gameDisplay.blit(date1Surface, (self.WindowRes[0] / 4 - date1Surface.get_rect().width / 2, \
							60))
			gameDisplay.blit(date1Surface, (self.WindowRes[0]*3/4 - date1Surface.get_rect().width / 2, \
							60))
			gameDisplay.blit(date1Surface, (self.WindowRes[0] / 4 - date1Surface.get_rect().width / 2, \
							self.WindowRes[1] / 2 + 45))
			gameDisplay.blit(date1Surface, (self.WindowRes[0]*3/4 - date1Surface.get_rect().width / 2, \
							self.WindowRes[1] / 2 + 45))
		elif self.CurrentSection_dic[self.CurrentSection] is "TIMER":
			pass
		elif self.CurrentSection_dic[self.CurrentSection] is "ALARMS":
			pass


	def Quit(self):
		pass

	def __str__(self):
		return "TIMESCREEN"
		

	
