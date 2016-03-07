import pygame, math
from WeatherWidget import *
from NewsWidget import *
from Helpers import *

class WidgetManager():
    def __init__(self, windowres):
        self.WindowRes = windowres

        self.swipe_arrow = SwipeArrow(False)
        '''
        Decider quels widgets afficher/charger
        '''
        self.WidgetList = []
        self.WidgetList.append(WeatherWidget())
        self.WidgetList.append(NewsWidget())

        self.FocusedWidgetIndex = 0 # index qui decide quel widget afficher
        '''
        Charger les infos de tous les ecrans (News, meteo, etc)
        '''
        pass

    def Update(self, InputEvents):
        for event in InputEvents:
            if "TOUCH" in event:
                mousepos = Helpers.get_message_x_y(event)
                if Helpers.is_in_rect(mousepos, [50, 290, 25, 130]):
                    if self.FocusedWidgetIndex > 0:
                        self.FocusedWidgetIndex -= 1
                elif Helpers.is_in_rect(mousepos, [725, 290, 25, 130]):
                    if self.FocusedWidgetIndex < len(self.WidgetList) - 1:
                        self.FocusedWidgetIndex += 1
        '''
        Updater le widget actif,  ou les deux lorsqu'on est dans une transition
        '''
        for widget in self.WidgetList:
            widget.Update(InputEvents)


    def Draw(self, gameDisplay, ancrage):
        self.swipe_arrow.Draw(gameDisplay, (50, 345 + ancrage), "LEFT")
        self.swipe_arrow.Draw(gameDisplay, (732, 345 + ancrage), "RIGHT")
        '''
        Dessiner le widget actif, ou les deux lorsqu'on est dans une transition
        '''
        widgetSurface = self.WidgetList[self.FocusedWidgetIndex].Draw(gameDisplay)
        gameDisplay.blit(widgetSurface, (self.WindowRes[0] / 2 - widgetSurface.get_rect().width / 2,
                                         290 + ancrage))
