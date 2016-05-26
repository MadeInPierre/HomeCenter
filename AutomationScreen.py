import pygame
from AutomationController import *
from Helpers import *

class AutomationScreen():
    '''
    Application de Domotique, non developpee pour l'instant.
    Ce n'est que la structure de base, liee a la classe AutomationController, qui affiche "Automation"
    en gros au centre en attendant le developpement de l'application entiere.
    '''
    def __init__(self, windowres):
        self.WindowRes = windowres
        self.ScreenStatus = "RUNNING"

        self.Controller = AutomationController()

        self.TitleFont = pygame.font.Font("Fonts/HelveticaNeue-UltraLight.ttf", 88)

    def Update(self, InputEvents):
        for event in InputEvents:
            if "TOUCH" in event:
                mousepos = pygame.mouse.get_pos()

                if Helpers.is_in_rect(mousepos, [0, 0, self.WindowRes[0] / 2, self.WindowRes[1]]):
                    pass

                if Helpers.is_in_rect(mousepos, [self.WindowRes[0], 0, self.WindowRes[0] / 2, self.WindowRes[1]]):
                    pass

    def Draw(self, gameDisplay):
        f = self.TitleFont.render("Automation", True, (255, 255, 255))
        gameDisplay.blit(f, (self.WindowRes[0] / 2 - f.get_rect().width / 2, self.WindowRes[1] / 2 - f.get_rect().height / 2))

    def Quit(self):
        pass

    def __str__(self):
        return "AUTOMATIONSCREEN"
