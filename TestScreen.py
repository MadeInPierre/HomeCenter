import pygame
import math
# import classe pour recuperer les infos de la meteo
from InputManager import *
from AnimationManager import *
from GifManager import *
from Helpers import *


class TestScreen():

    def __init__(self, windowres):
        self.rain = GifManager("Images/rain2.gif")
        # Charger une image
        self.sunny_icon = pygame.image.load("Images/weather_sunny_transparent.png").convert_alpha()
        # position image (seulement pour animation)
        self.sunny_positionX = 80  # direction : 580
        self.sunny_positionY = 100  # direction : 200
        # texto
        self.ScreenStatus = "RUNNING"
        # police du texte( la rappeler qaund on ecrit le txt) -> temperature/humidite...
        self.TitleFont     = pygame.font.Font("Fonts/HelveticaNeue-Light.ttf", 55)
        self.TitleFont2    = pygame.font.Font("Fonts/HelveticaNeue-UltraLight.ttf", 100)
        self.WaitFont      = pygame.font.Font("Fonts/HelveticaNeue-UltraLight.ttf", 22)
        self.PostTitleFont = pygame.font.Font("Fonts/HelveticaNeue-Medium.ttf", 12, bold=False)

        self.Aujourdhui_color = 0

        self.TemperatureText = self.TitleFont2.render("15 C", True, (255, 255, 255))

        self.chrono = AnimationManager()

    def Update(self, InputEvents):
        '''
        Partie qui regarde si on a clique sur l'ecran :
        '''
        for event in InputEvents:
            if "TOUCH" in event:
                mousepos = Helpers.get_message_x_y(event) # recupere la position ou la personne a clique
                if Helpers.is_in_rect(mousepos, [50, 290, 25, 130]):
                    self.a
                    pass # fait ce que tu veux :)



        if self.chrono.elapsed_time() > 0 and self.chrono.elapsed_time() < 1:
            self.Aujourdhui_color=int(255 / (1 + math.exp(-(self.chrono.elapsed_time() - 0.5) / 0.1)))


        if self.chrono.elapsed_time() > 1 and self.chrono.elapsed_time() < 3:
            self.sunny_positionX=int(80 + 500 / (1 + math.exp(-(self.chrono.elapsed_time() - 2) / 0.2)))
        if self.chrono.elapsed_time() > 1 and self.chrono.elapsed_time() < 3:
            self.sunny_positionY=int(100 + 100 / (1 + math.exp(-(self.chrono.elapsed_time() - 2) / 0.2)))




    def Draw(self, gameDisplay):
        self.rain.render(gameDisplay, (0, 0))

# Afficher une image (ici soleil)

        gameDisplay.blit(self.sunny_icon, (self.sunny_positionX, self.sunny_positionY))
#1er self = "nom" du texte; 2e self = police; 
        self.AujourdhuiText = self.TitleFont.render("Aujourd'hui", True, (255, 255, 255))
        gameDisplay.blit(self.AujourdhuiText, (55, 30))  # pos initiale : 55, 30

        gameDisplay.blit(self.TemperatureText, (550, 100))

        # MODE DEMPLOI POUR AFFICHER UN TEXTE
        # 1 - charger la police dans le init (ci-dessus)
        # 2 - self.NOMDELIMAGE = self.NOMDELAPOLICE.render(str(self.onfos.current), True, (255, 255, 255))
        # 3 - gameDisplay.blit(self.NOMDELIMAGE, (POSITIONX, POSITIONY))
        '''
        for i in range (0, 7):
            temps = WeatherManager.icone[i]
            if temps == "cloudy"
                 # afficher icone cloudy


            self.temperature = TitleFont.render(
                WeatherManager.temperatures[i], True, (255, 255, 255))

            gameDisplay.blit(self.temperature, (ancrageX + 800 * i, 0))
        '''



    def Quit(self):
        pass

    def __str__(self):
        return "TESTSCREEN"
