import pygame, math
from WeatherWidget import *

class WidgetManager():
    def __init__(self, windowres):
        self.WindowRes = windowres

        '''
        Decider quels widgets afficher/charger
        '''
        self.WidgetList = []
        self.WidgetList.append(WeatherWidget())

        self.FocusedWidgetIndex = 0 # index qui decide quel widget afficher
        '''
        Charger les infos de tous les ecrans (News, meteo, etc)
        '''
        pass

    def Update(self, InputEvents):
        '''
        Updater le widget actif,  ou les deux lorsqu'on est dans une transition
        '''
        for widget in self.WidgetList:
            widget.Update(InputEvents)


    def Draw(self, gameDisplay, ancrage):
        '''
        Dessiner le widget actif, ou les deux lorsqu'on est dans une transition
        '''
        widgetSurface = self.WidgetList[self.FocusedWidgetIndex].Draw(gameDisplay)
        gameDisplay.blit(widgetSurface, (self.WindowRes[0] / 2 - widgetSurface.get_rect().width / 2,
                                         290 + ancrage))
