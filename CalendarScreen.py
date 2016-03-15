import pygame, math
from CalendarCollector import *

class CalendarScreen():
    def __init__(self, WindowRes):
        self.MonthsTitleFont = pygame.font.Font("Fonts/HelveticaNeue-Light.ttf", 22)

        self.calendar_events = CalendarCollector()

    def Update(self, InputEvents):
        pass

    def Draw(self, gameDisplay):
        self.monthTitleSurface = self.MonthsTitleFont.render("Janvier", (255, 255, 255))
        gameDisplay.blit(self.monthTitleSurface, (250 - self.monthTitleSurface.get_rect().width / 2, 10))
