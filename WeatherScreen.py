import pygame
from AnimationManager import *
from WeatherCollector import *
from InputManager import *


class WeatherScreen():
    def __init__(self, WindowRes):
        self.windowres = WindowRes
        self.infos_meteo = WeatherCollector()
        self.ScreenStatus = "RUNNING"
        self.sunny_icon = pygame.image.load("Images/Icones_Meteo/weather-clear-2.png").convert_alpha()
        self.sunny_cloud_icon = pygame.image.load("Images/Icones_Meteo/weather-few-clouds-2.png").convert_alpha()
        self.cloud_icon = pygame.image.load("Images/Icones_Meteo/weather-overcast-2.png").convert_alpha()
        self.light_rain_icon = pygame.image.load("Images/Icones_Meteo/weather-showers-scattered-2.png").convert_alpha()
        self.heavy_rain_icon = pygame.image.load("Images/Icones_Meteo/weather-showers-2.png").convert_alpha()
        self.storm_icon = pygame.image.load("Images/Icones_Meteo/weather-storm-2.png").convert_alpha()
        self.snow_icon = pygame.image.load("Images/Icones_Meteo/weather-snow-2.png").convert_alpha()
        self.thermometre_icon = pygame.image.load("Images/Icones_Meteo/thermometre.jpg").convert_alpha()
        self.humidite_icon = pygame.image.load("Images/Icones_Meteo/Goutte.png").convert_alpha()
        self.WallPaper = pygame.image.load("Images/Icones_Meteo/sun_sky.jpg").convert_alpha()
        self.RainProb_icon = pygame.image.load("Images/Icones_Meteo/probapluie.jpg").convert_alpha()

        self.FontTemperature = pygame.font.Font("Fonts/HelveticaNeue-Medium.ttf", 80)
        self.FontHumidite = pygame.font.Font("Fonts/HelveticaNeue-Medium.ttf", 80)
        self.FontRainProb = pygame.font.Font("Fonts/HelveticaNeue-Medium.ttf", 80)
        
        self.barre_icon = pygame.Surface((800,100)).convert_alpha()

        self.barre_icon.fill((255,255,255,100))

    def Update(self, InputEvents):
        pass

    def Draw(self, gameDisplay):
        
        gameDisplay.blit(self.WallPaper,(0,0))

        if self.infos_meteo.CurrentWeather.Icon == "sun":
             gameDisplay.blit(self.sunny_icon, (20, 20))
        if self.infos_meteo.CurrentWeather.Icon == "sun_cloud":
            gameDisplay.blit(self.sunny_cloud_icon, (20, 20))
        if self.infos_meteo.CurrentWeather.Icon == "cloud":
            gameDisplay.blit(self.cloud_icon, (20, 20))
        if self.infos_meteo.CurrentWeather.Icon == "light_rain":
            gameDisplay.blit(self.light_rain_icon, (20,20))
        if self.infos_meteo.CurrentWeather.Icon == "heavy_rain":
            gameDisplay.blit(self.heavy_rain_icon, (20, 20))
        if self.infos_meteo.CurrentWeather.Icon == "storm":
            gameDisplay.blit(self.storm_icon, (20, 20))
        if self.infos_meteo.CurrentWeather.Icon == "snow":
            gameDisplay.blit(self.snow_icon, (20, 20))

        gameDisplay.blit(self.thermometre_icon, (220, 20))

        gameDisplay.blit(self.RainProb_icon, (420, 20))

        gameDisplay.blit(self.humidite_icon, (620, 20))


        self.Temperature = self.FontTemperature.render(str(self.infos_meteo.CurrentWeather.Temperature)+" C", True, (255,255,255))
        gameDisplay.blit(self.Temperature, (220, 250))

        self.Humidite = self.FontHumidite.render(str(self.infos_meteo.CurrentWeather.Humidity)+"%", True, (255,255,255))
        gameDisplay.blit(self.Humidite, (620, 250))

        self.RainProb = self.FontRainProb.render(str(self.infos_meteo.CurrentWeather.RainProb)+"%", True, (255,255,255))
        gameDisplay.blit(self.RainProb, (420, 250))

        gameDisplay.blit(self.barre_icon, (0,380))



        
            

            

    def Quit(self):
        pass