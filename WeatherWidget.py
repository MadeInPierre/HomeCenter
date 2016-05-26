﻿import pygame
from Helpers import Helpers

class WeatherWidget():
    '''
    Widget vide pour l'instant, il n'affiche qu'une frame vide en attenddant son developpement.
    '''
    def __init__(self):
        self.WidgetSurface = pygame.Surface((650, 130)).convert_alpha()

        self.Font = pygame.font.Font("Fonts/HelveticaNeue-Light.ttf", 22)

    def Update(self, InputEvents):
        pass

    def Draw(self, gameDisplay):
        self.WidgetSurface.fill((255, 255, 255, 40))
        pygame.draw.line(self.WidgetSurface, (255, 255, 255), [0  , 0  ], [650 , 0  ], 1)
        pygame.draw.line(self.WidgetSurface, (255, 255, 255), [649, 0  ], [649 , 150], 1)
        pygame.draw.line(self.WidgetSurface, (255, 255, 255), [650, 129], [0   , 129], 1)
        pygame.draw.line(self.WidgetSurface, (255, 255, 255), [0  , 150], [0   , 0  ], 1)

        surface = self.Font.render("Weather Widget", True, (255, 255, 255))
        self.WidgetSurface.blit(surface, (self.WidgetSurface.get_rect().width / 2 - surface.get_rect().width / 2,
                                          50))

        return self.WidgetSurface

    def __str__():
        return "WEATHERHOMEWIDGET"
