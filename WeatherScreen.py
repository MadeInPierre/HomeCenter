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

        self.sunny_mini_icon = pygame.image.load("Images/Icones_Meteo/weather-clear-2-mini.png").convert_alpha()
        self.sunny_cloud_mini_icon = pygame.image.load("Images/Icones_Meteo/weather-few-clouds-2-mini.png").convert_alpha()
        self.cloud_mini_icon = pygame.image.load("Images/Icones_Meteo/weather-overcast-2-mini.png").convert_alpha()
        self.light_rain_mini_icon = pygame.image.load("Images/Icones_Meteo/weather-showers-scattered-2-mini.png").convert_alpha()
        self.heavy_rain_mini_icon = pygame.image.load("Images/Icones_Meteo/weather-showers-2-mini.png").convert_alpha()
        self.storm_mini_icon = pygame.image.load("Images/Icones_Meteo/weather-storm-2-mini.png").convert_alpha()
        self.snow_mini_icon = pygame.image.load("Images/Icones_Meteo/weather-snow-2-mini.png").convert_alpha()
       
        self.thermometre_icon = pygame.image.load("Images/Icones_Meteo/thermometre.png").convert_alpha()
        self.humidite_icon = pygame.image.load("Images/Icones_Meteo/Goutte.png").convert_alpha()
        self.RainProb_icon = pygame.image.load("Images/Icones_Meteo/probapluie.png").convert_alpha()

        self.WallPaperSun = pygame.image.load("Images/Icones_Meteo/sun_sky.jpg").convert_alpha()
        self.WallPaperCloudandsun = pygame.image.load("Images/Icones_Meteo/cloudandsun_sky.jpg").convert_alpha()
        self.WallPaperCloud = pygame.image.load("Images/Icones_Meteo/cloud_sky.jpg").convert_alpha()
        self.WallPaperLightrain = pygame.image.load("Images/Icones_Meteo/lightrain_sky.jpg").convert_alpha()
        self.WallPaperHeavyrain = pygame.image.load("Images/Icones_Meteo/heavyrain_sky.jpg").convert_alpha()
        self.WallPaperStorm = pygame.image.load("Images/Icones_Meteo/storm_sky.jpg").convert_alpha()
        self.WallPaperSnow = pygame.image.load("Images/Icones_Meteo/snow_sky.jpg").convert_alpha()

        self.FontTemperature = pygame.font.Font("Fonts/HelveticaNeue-Medium.ttf", 80)
        self.FontTemperatureMini = pygame.font.Font("Fonts/HelveticaNeue-UltraLight.ttf", 40)
        self.FontHumidite = pygame.font.Font("Fonts/HelveticaNeue-Medium.ttf", 80)
        self.FontRainProb = pygame.font.Font("Fonts/HelveticaNeue-Medium.ttf", 80)
        
        self.barre_icon = pygame.Surface((113,100)).convert_alpha()

        self.barre_icon.fill((255,255,255,100))
            
        self.currentday = 0

        self.DayFont = pygame.font.Font("Fonts/HelveticaNeue-UltraLight.ttf",30)


    def Update(self, InputEvents):
        for event in InputEvents:
            if "TOUCH" in event:
                    mousepos = Helpers.get_message_x_y(event)
                    if Helpers.is_in_rect(mousepos, [1.5, 380, 113, 100]): #x, y, longueur cote x, longueur cote y
                       self.currentday = 0
                  
                    if Helpers.is_in_rect(mousepos, [115.5, 380, 113, 100]): #x, y, longueur cote x, longueur cote y
                       self.currentday = 1
                   
                    if Helpers.is_in_rect(mousepos, [229.5, 380, 113, 100]): #x, y, longueur cote x, longueur cote y
                       self.currentday = 2
                   
                    if Helpers.is_in_rect(mousepos, [343.5, 380, 113, 100]): #x, y, longueur cote x, longueur cote y
                       self.currentday = 3
                   
                    if Helpers.is_in_rect(mousepos, [457.5, 380, 113, 100]): #x, y, longueur cote x, longueur cote y
                       self.currentday = 4
                   
                    if Helpers.is_in_rect(mousepos, [571.5, 380, 113, 100]): #x, y, longueur cote x, longueur cote y
                       self.currentday = 5
                   
                    if Helpers.is_in_rect(mousepos, [685.5, 380, 113, 100]): #x, y, longueur cote x, longueur cote y
                       self.currentday = 6
                   
    def Draw(self, gameDisplay):

        if self.infos_meteo.DailyWeather.Icons[self.currentday] == "sun":
             gameDisplay.blit(self.WallPaperSun,(0,0))
             gameDisplay.blit(self.sunny_icon, (20, 20))

        if self.infos_meteo.DailyWeather.Icons[self.currentday] == "sun_cloud":
            gameDisplay.blit(self.WallPaperCloudandsun,(0,0))
            gameDisplay.blit(self.sunny_cloud_icon, (20, 20))

        if self.infos_meteo.DailyWeather.Icons[self.currentday] == "cloud":
            gameDisplay.blit(self.WallPaperCloud,(0,0))
            gameDisplay.blit(self.cloud_icon, (20, 20))

        if self.infos_meteo.DailyWeather.Icons[self.currentday] == "light_rain":
            gameDisplay.blit(self.WallPaperLightrain,(0,0))
            gameDisplay.blit(self.light_rain_icon, (20,20))

        if self.infos_meteo.DailyWeather.Icons[self.currentday] == "heavy_rain":
            gameDisplay.blit(self.WallPaperHeavyrain,(0,0))
            gameDisplay.blit(self.heavy_rain_icon, (20, 20))

        if self.infos_meteo.DailyWeather.Icons[self.currentday] == "storm":
            gameDisplay.blit(self.WallPaperStorm,(0,0))
            gameDisplay.blit(self.storm_icon, (20, 20))

        if self.infos_meteo.DailyWeather.Icons[self.currentday] == "snow":
            gameDisplay.blit(self.WallPaperSnow,(0,0))
            gameDisplay.blit(self.snow_icon, (20, 20))



        gameDisplay.blit(self.thermometre_icon, (220, 20))

        gameDisplay.blit(self.RainProb_icon, (420, 20))

        gameDisplay.blit(self.humidite_icon, (620, 20))

        self.Temperature = self.FontTemperature.render(str(self.infos_meteo.DailyWeather.Temperatures[self.currentday])+" C", True, (0,0,0,100))
        gameDisplay.blit(self.Temperature, (221, 251))
        self.Temperature = self.FontTemperature.render(str(self.infos_meteo.DailyWeather.Temperatures[self.currentday])+" C", True, (255,255,255))
        gameDisplay.blit(self.Temperature, (220, 250))
        

        self.Humidite = self.FontHumidite.render(str(self.infos_meteo.DailyWeather.Humidities[self.currentday])+"%", True, (0,0,0,100))
        gameDisplay.blit(self.Humidite, (621, 251))
        self.Humidite = self.FontHumidite.render(str(self.infos_meteo.DailyWeather.Humidities[self.currentday])+"%", True, (255,255,255))
        gameDisplay.blit(self.Humidite, (620, 250))

        self.RainProb = self.FontRainProb.render(str(self.infos_meteo.DailyWeather.RainProbs[self.currentday])+"%", True, (0,0,0,100))
        gameDisplay.blit(self.RainProb, (421, 251))
        self.RainProb = self.FontRainProb.render(str(self.infos_meteo.DailyWeather.RainProbs[self.currentday])+"%", True, (255,255,255))
        gameDisplay.blit(self.RainProb, (420, 250))

        gameDisplay.blit(self.barre_icon, (1.5,380))
        gameDisplay.blit(self.barre_icon, (115.5,380))
        gameDisplay.blit(self.barre_icon, (229.5,380))
        gameDisplay.blit(self.barre_icon, (343.5,380))
        gameDisplay.blit(self.barre_icon, (457.5,380))
        gameDisplay.blit(self.barre_icon, (571.5,380))
        gameDisplay.blit(self.barre_icon, (685.5,380))

        self.DayoneText = self.DayFont.render("Day 1", True, (0,0,0))
        gameDisplay.blit(self.DayoneText, (1.5+30,380+60))

        self.DaytwoText = self.DayFont.render("Day 2", True, (0,0,0))
        gameDisplay.blit(self.DaytwoText, (115.5+30,380+60))

        self.DaythreeText = self.DayFont.render("Day 3", True, (0,0,0))
        gameDisplay.blit(self.DaythreeText, (229.5+30,380+60))

        self.DayfourText = self.DayFont.render("Day 4", True, (0,0,0))
        gameDisplay.blit(self.DayfourText, (343.5+30,380+60))

        self.DayfiveText = self.DayFont.render("Day 5", True, (0,0,0))
        gameDisplay.blit(self.DayfiveText, (457.5+30,380+60))

        self.DaysixText = self.DayFont.render("Day 6", True, (0,0,0))
        gameDisplay.blit(self.DaysixText, (571.5+30,380+60))

        self.DaysevenText = self.DayFont.render("Day 7", True, (0,0,0))
        gameDisplay.blit(self.DaysevenText, (685.5+30,380+60))


        if self.infos_meteo.DailyWeather.Icons[0] == "sun":
             gameDisplay.blit(self.sunny_mini_icon,(1.5,380))    
        if self.infos_meteo.DailyWeather.Icons[0] == "sun_cloud":
            gameDisplay.blit(self.sunny_cloud_mini_icon, (1.5, 380))
        if self.infos_meteo.DailyWeather.Icons[0] == "cloud":
            gameDisplay.blit(self.cloud_mini_icon, (1.5, 380))
        if self.infos_meteo.DailyWeather.Icons[0] == "light_rain":
            gameDisplay.blit(self.light_rain_mini_icon, (1.5,380))
        if self.infos_meteo.DailyWeather.Icons[0] == "heavy_rain":
            gameDisplay.blit(self.heavy_rain_mini_icon, (1.5, 380))
        if self.infos_meteo.DailyWeather.Icons[0] == "storm":
            gameDisplay.blit(self.storm_mini_icon, (1.5, 380))
        if self.infos_meteo.DailyWeather.Icons[0] == "snow":
            gameDisplay.blit(self.snow_mini_icon, (1.5, 380))

        if self.infos_meteo.DailyWeather.Icons[1] == "sun":
             gameDisplay.blit(self.sunny_mini_icon,(115.5,380))           
        if self.infos_meteo.DailyWeather.Icons[1] == "sun_cloud":
            gameDisplay.blit(self.sunny_cloud_mini_icon, (115.5, 380))
        if self.infos_meteo.DailyWeather.Icons[1] == "cloud":
            gameDisplay.blit(self.cloud_mini_icon, (115.5, 380))
        if self.infos_meteo.DailyWeather.Icons[1] == "light_rain":
            gameDisplay.blit(self.light_rain_mini_icon, (115.5,380))
        if self.infos_meteo.DailyWeather.Icons[1] == "heavy_rain":
            gameDisplay.blit(self.heavy_rain_mini_icon, (115.5, 380))
        if self.infos_meteo.DailyWeather.Icons[1] == "storm":
            gameDisplay.blit(self.storm_mini_icon, (115.5, 380))
        if self.infos_meteo.DailyWeather.Icons[1] == "snow":
            gameDisplay.blit(self.snow_mini_icon, (115.5, 380))

        if self.infos_meteo.DailyWeather.Icons[2] == "sun":
             gameDisplay.blit(self.sunny_mini_icon,(229.5,380))            
        if self.infos_meteo.DailyWeather.Icons[2] == "sun_cloud":
            gameDisplay.blit(self.sunny_cloud_mini_icon, (229.5, 380))
        if self.infos_meteo.DailyWeather.Icons[2] == "cloud":
            gameDisplay.blit(self.cloud_mini_icon, (229.5, 380))
        if self.infos_meteo.DailyWeather.Icons[2] == "light_rain":
            gameDisplay.blit(self.light_rain_mini_icon, (229.5,380))
        if self.infos_meteo.DailyWeather.Icons[2] == "heavy_rain":
            gameDisplay.blit(self.heavy_rain_mini_icon, (229.5, 380))
        if self.infos_meteo.DailyWeather.Icons[2] == "storm":
            gameDisplay.blit(self.storm_mini_icon, (229.5, 380))
        if self.infos_meteo.DailyWeather.Icons[2] == "snow":
            gameDisplay.blit(self.snow_mini_icon, (229.5, 380))

        if self.infos_meteo.DailyWeather.Icons[3] == "sun":
             gameDisplay.blit(self.sunny_mini_icon,(343.5,380))            
        if self.infos_meteo.DailyWeather.Icons[3] == "sun_cloud":
            gameDisplay.blit(self.sunny_cloud_mini_icon, (343.5, 380))
        if self.infos_meteo.DailyWeather.Icons[3] == "cloud":
            gameDisplay.blit(self.cloud_mini_icon, (343.5, 380))
        if self.infos_meteo.DailyWeather.Icons[3] == "light_rain":
            gameDisplay.blit(self.light_rain_mini_icon, (343.5,380))
        if self.infos_meteo.DailyWeather.Icons[3] == "heavy_rain":
            gameDisplay.blit(self.heavy_rain_mini_icon, (343.5, 380))
        if self.infos_meteo.DailyWeather.Icons[3] == "storm":
            gameDisplay.blit(self.storm_mini_icon, (343.5, 380))
        if self.infos_meteo.DailyWeather.Icons[3] == "snow":
            gameDisplay.blit(self.snow_mini_icon, (343.5, 380))

        if self.infos_meteo.DailyWeather.Icons[4] == "sun":
             gameDisplay.blit(self.sunny_mini_icon,(457.5,380))            
        if self.infos_meteo.DailyWeather.Icons[4] == "sun_cloud":
            gameDisplay.blit(self.sunny_cloud_mini_icon, (457.5, 380))
        if self.infos_meteo.DailyWeather.Icons[4] == "cloud":
            gameDisplay.blit(self.cloud_mini_icon, (457.5, 380))
        if self.infos_meteo.DailyWeather.Icons[4] == "light_rain":
            gameDisplay.blit(self.light_rain_mini_icon, (457.5,380))
        if self.infos_meteo.DailyWeather.Icons[4] == "heavy_rain":
            gameDisplay.blit(self.heavy_rain_mini_icon, (457.5, 380))
        if self.infos_meteo.DailyWeather.Icons[4] == "storm":
            gameDisplay.blit(self.storm_mini_icon, (457.5, 380))
        if self.infos_meteo.DailyWeather.Icons[4] == "snow":
            gameDisplay.blit(self.snow_mini_icon, (457.5, 380))

        if self.infos_meteo.DailyWeather.Icons[5] == "sun":
             gameDisplay.blit(self.sunny_mini_icon,(571.5,380))            
        if self.infos_meteo.DailyWeather.Icons[5] == "sun_cloud":
            gameDisplay.blit(self.sunny_cloud_mini_icon, (571.5, 380))
        if self.infos_meteo.DailyWeather.Icons[5] == "cloud":
            gameDisplay.blit(self.cloud_mini_icon, (571.5, 380))
        if self.infos_meteo.DailyWeather.Icons[5] == "light_rain":
            gameDisplay.blit(self.light_rain_mini_icon, (571.5,380))
        if self.infos_meteo.DailyWeather.Icons[5] == "heavy_rain":
            gameDisplay.blit(self.heavy_rain_mini_icon, (571.5, 380))
        if self.infos_meteo.DailyWeather.Icons[5] == "storm":
            gameDisplay.blit(self.storm_mini_icon, (571.5, 380))
        if self.infos_meteo.DailyWeather.Icons[5] == "snow":
            gameDisplay.blit(self.snow_mini_icon, (571.5, 380))

        if self.infos_meteo.DailyWeather.Icons[6] == "sun":
             gameDisplay.blit(self.sunny_mini_icon,(685.5,380))            
        if self.infos_meteo.DailyWeather.Icons[6] == "sun_cloud":
            gameDisplay.blit(self.sunny_cloud_mini_icon, (685.5, 380))
        if self.infos_meteo.DailyWeather.Icons[6] == "cloud":
            gameDisplay.blit(self.cloud_mini_icon, (685.5, 380))
        if self.infos_meteo.DailyWeather.Icons[6] == "light_rain":
            gameDisplay.blit(self.light_rain_mini_icon, (685.5,380))
        if self.infos_meteo.DailyWeather.Icons[6] == "heavy_rain":
            gameDisplay.blit(self.heavy_rain_mini_icon, (685.5, 380))
        if self.infos_meteo.DailyWeather.Icons[6] == "storm":
            gameDisplay.blit(self.storm_mini_icon, (685.5, 380))
        if self.infos_meteo.DailyWeather.Icons[6] == "snow":
            gameDisplay.blit(self.snow_mini_icon, (685.5, 380))

        self.TemperatureMini = self.FontTemperatureMini.render(str(self.infos_meteo.DailyWeather.Temperatures[0]), True, (0,0,0))
        gameDisplay.blit(self.TemperatureMini, (62, 380))
        self.TemperatureMini = self.FontTemperatureMini.render(str(self.infos_meteo.DailyWeather.Temperatures[1]), True, (0,0,0))
        gameDisplay.blit(self.TemperatureMini, (176, 380))
        self.TemperatureMini = self.FontTemperatureMini.render(str(self.infos_meteo.DailyWeather.Temperatures[2]), True, (0,0,0))
        gameDisplay.blit(self.TemperatureMini, (290, 380))
        self.TemperatureMini = self.FontTemperatureMini.render(str(self.infos_meteo.DailyWeather.Temperatures[3]), True, (0,0,0))
        gameDisplay.blit(self.TemperatureMini, (403, 380))
        self.TemperatureMini = self.FontTemperatureMini.render(str(self.infos_meteo.DailyWeather.Temperatures[4]), True, (0,0,0))
        gameDisplay.blit(self.TemperatureMini, (517, 380))
        self.TemperatureMini = self.FontTemperatureMini.render(str(self.infos_meteo.DailyWeather.Temperatures[5]), True, (0,0,0))
        gameDisplay.blit(self.TemperatureMini, (631, 380))
        self.TemperatureMini = self.FontTemperatureMini.render(str(self.infos_meteo.DailyWeather.Temperatures[6]), True, (0,0,0))
        gameDisplay.blit(self.TemperatureMini, (745, 380))

        
            

            

    def Quit(self):
        pass
    
    def __str__(self):
        return "WEATHERSCREEN"