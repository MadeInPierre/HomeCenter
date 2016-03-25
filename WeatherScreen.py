import pygame
from AnimationManager import *
from WeatherCollector import *
from InputManager import *
from Helpers import *

class WeatherScreen():
    def __init__(self, WindowRes):
        self.windowres = WindowRes
        self.infos_meteo = WeatherCollector()

        self.ScreenStatus = "RUNNING"

#Icones du temps de la grande fenetre

        self.sunny_icon = pygame.image.load("Images/Icones_Meteo/weather-clear-2.png").convert_alpha()
        self.sunny_cloud_icon = pygame.image.load("Images/Icones_Meteo/weather-few-clouds-2.png").convert_alpha()
        self.cloud_icon = pygame.image.load("Images/Icones_Meteo/weather-overcast-2.png").convert_alpha()
        self.light_rain_icon = pygame.image.load("Images/Icones_Meteo/weather-showers-scattered-2.png").convert_alpha()
        self.heavy_rain_icon = pygame.image.load("Images/Icones_Meteo/weather-showers-2.png").convert_alpha()
        self.storm_icon = pygame.image.load("Images/Icones_Meteo/weather-storm-2.png").convert_alpha()
        self.snow_icon = pygame.image.load("Images/Icones_Meteo/weather-snow-2.png").convert_alpha()


#Icones du temps des petites fenetres

        self.sunny_mini_icon = pygame.image.load("Images/Icones_Meteo/weather-clear-2-mini.png").convert_alpha()
        self.sunny_cloud_mini_icon = pygame.image.load("Images/Icones_Meteo/weather-few-clouds-2-mini.png").convert_alpha()
        self.cloud_mini_icon = pygame.image.load("Images/Icones_Meteo/weather-overcast-2-mini.png").convert_alpha()
        self.light_rain_mini_icon = pygame.image.load("Images/Icones_Meteo/weather-showers-scattered-2-mini.png").convert_alpha()
        self.heavy_rain_mini_icon = pygame.image.load("Images/Icones_Meteo/weather-showers-2-mini.png").convert_alpha()
        self.storm_mini_icon = pygame.image.load("Images/Icones_Meteo/weather-storm-2-mini.png").convert_alpha()
        self.snow_mini_icon = pygame.image.load("Images/Icones_Meteo/weather-snow-2-mini.png").convert_alpha()
       
#Icones des parametres du temps de la grande fenetre

        self.thermometre_icon = pygame.image.load("Images/Icones_Meteo/thermometre.png").convert_alpha()
        self.humidite_icon = pygame.image.load("Images/Icones_Meteo/Goutte.png").convert_alpha()
        self.RainProb_icon = pygame.image.load("Images/Icones_Meteo/probapluie.png").convert_alpha()

#Fonds d'ecran en fonction du temps

        self.WallPaperSun = pygame.image.load("Images/Icones_Meteo/sun_sky.jpg").convert_alpha()
        self.WallPaperCloudandsun = pygame.image.load("Images/Icones_Meteo/cloudandsun_sky.jpg").convert_alpha()
        self.WallPaperCloud = pygame.image.load("Images/Icones_Meteo/cloud_sky.jpg").convert_alpha()
        self.WallPaperLightrain = pygame.image.load("Images/Icones_Meteo/lightrain_sky.jpg").convert_alpha()
        self.WallPaperHeavyrain = pygame.image.load("Images/Icones_Meteo/heavyrain_sky.jpg").convert_alpha()
        self.WallPaperStorm = pygame.image.load("Images/Icones_Meteo/storm_sky.jpg").convert_alpha()
        self.WallPaperSnow = pygame.image.load("Images/Icones_Meteo/snow_sky.jpg").convert_alpha()

#Styles d'ecriture

        self.FontTemperature = pygame.font.Font("Fonts/HelveticaNeue-Medium.ttf", 80)
        self.FontTemperatureMini = pygame.font.Font("Fonts/HelveticaNeue-UltraLight.ttf", 40)
        self.FontHumidite = pygame.font.Font("Fonts/HelveticaNeue-Medium.ttf", 80)
        self.FontRainProb = pygame.font.Font("Fonts/HelveticaNeue-Medium.ttf", 80)
        self.FontDate = pygame.font.Font("Fonts/HelveticaNeue-Medium.ttf", 40)
        self.DayFont = pygame.font.Font("Fonts/HelveticaNeue-UltraLight.ttf",30)

#Barres transparentes

        self.barre_icon = pygame.Surface((113,100)).convert_alpha()
        self.barre_icon.fill((255,255,255,100))

#VARIABLES:
            
#Variable qui sert à l'affichage du temps des jours selectionnes
        self.currentday = 0

#Variable qui appelle le chrono

        self.chrono = AnimationManager()

#Variable qui donne la transparence

        self.Transparence = 0

#Variable qui donne la position Y (Utilisee dans des formules)

        self.PosY_Icone = 80

#Variable qui correspond à l'ecran a faire apparaitre

        self.NewDay = 0

    def Update(self, InputEvents):

#Ci-dessous: Si le clic est dans le carre delimite par les valeurs alors affiche l'ecran lie a la variable currentday
        for event in InputEvents:
            if "TOUCH" in event:
                    mousepos = Helpers.get_message_x_y(event)
                    
                    if Helpers.is_in_rect(mousepos, [1.5, 380, 797, 100]):
                                            
                        if Helpers.is_in_rect(mousepos, [1.5, 380, 113, 100]): #x, y, longueur cote x, longueur cote y
                            self.chrono.reset()                            
                            self.NewDay = 0
                            
                        if Helpers.is_in_rect(mousepos, [115.5, 380, 113, 100]): 
                            self.chrono.reset()
                            self.NewDay = 1
                                              
                        if Helpers.is_in_rect(mousepos, [229.5, 380, 113, 100]):
                            self.chrono.reset()
                            self.NewDay = 2
                            
                        if Helpers.is_in_rect(mousepos, [343.5, 380, 113, 100]): 
                            self.NewDay = 3
                            self.chrono.reset()
                           
                        if Helpers.is_in_rect(mousepos, [457.5, 380, 113, 100]): 
                            self.NewDay = 4
                            self.chrono.reset()
                           
                        if Helpers.is_in_rect(mousepos, [571.5, 380, 113, 100]): 
                            self.NewDay = 5
                            self.chrono.reset()
                            
                        if Helpers.is_in_rect(mousepos, [685.5, 380, 113, 100]): 
                            self.NewDay = 6
                            self.chrono.reset()
                            
#Animation -> Fondu "apparaissant" des ecrans

        if self.chrono.elapsed_time() > 1 and self.chrono.elapsed_time() < 3  :
           self.currentday = self.NewDay
           self.Transparence=int(255 / (1 + math.exp(-(self.chrono.elapsed_time() - 2 ) / 0.1)))

#Animation -> Fondu "disparaissant" des ecrans

        if self.chrono.elapsed_time() > 0 and self.chrono.elapsed_time() < 1 : 
           self.Transparence=int(255 / (1 + math.exp(-(0.5 - self.chrono.elapsed_time()) / 0.1)))

#Varaible PosY_Icone est placee dans fonction sinusoidale pour faire "planer" textes/images
      
        if self.chrono.elapsed_time() > 0:
            self.PosY_Icone = 80 + 5*math.sin(2*math.pi/3*self.chrono.elapsed_time())
#fct sinus: Amplitude*math.sin(2*math.pi/Periode*t)

    def Draw(self, gameDisplay):

#Afficher le fond d'ecran et l'icone correspondant a la case selectionnne et en lien avec les infos du WeatherCollector
#Permet aussi de gerer la transparence et la position des elements a afficher

        if self.infos_meteo.DailyWeather.Icons[self.currentday] == "sun":
            Helpers.blit_alpha(gameDisplay, self.WallPaperSun,(0,0), self.Transparence)
            Helpers.blit_alpha(gameDisplay, self.sunny_icon, (20, self.PosY_Icone), self.Transparence)

        if self.infos_meteo.DailyWeather.Icons[self.currentday] == "sun_cloud":
            Helpers.blit_alpha(gameDisplay, self.WallPaperCloudandsun,(0,0), self.Transparence)
            Helpers.blit_alpha(gameDisplay, self.sunny_cloud_icon, (20, self.PosY_Icone), self.Transparence)

        if self.infos_meteo.DailyWeather.Icons[self.currentday] == "cloud":
            Helpers.blit_alpha(gameDisplay, self.WallPaperCloud,(0,0), self.Transparence)
            Helpers.blit_alpha(gameDisplay, self.cloud_icon, (20, self.PosY_Icone), self.Transparence)

        if self.infos_meteo.DailyWeather.Icons[self.currentday] == "light_rain":
            Helpers.blit_alpha(gameDisplay, self.WallPaperLightrain,(0,0), self.Transparence)
            Helpers.blit_alpha(gameDisplay, self.light_rain_icon, (20, self.PosY_Icone), self.Transparence)

        if self.infos_meteo.DailyWeather.Icons[self.currentday] == "heavy_rain":
            Helpers.blit_alpha(gameDisplay, self.WallPaperHeavyrain,(0,0), self.Transparence)
            Helpers.blit_alpha(gameDisplay, self.heavy_rain_icon, (20, self.PosY_Icone), self.Transparence)

        if self.infos_meteo.DailyWeather.Icons[self.currentday] == "storm":
            Helpers.blit_alpha(gameDisplay, self.WallPaperStorm,(0,0), self.Transparence)
            Helpers.blit_alpha(gameDisplay, self.storm_icon, (20, self.PosY_Icone), self.Transparence)

        if self.infos_meteo.DailyWeather.Icons[self.currentday] == "snow":
            Helpers.blit_alpha(gameDisplay, self.WallPaperSnow,(0,0), self.Transparence)
            Helpers.blit_alpha(gameDisplay, self.snow_icon, (20, self.PosY_Icone), self.Transparence)

#Affiche les icones lies aux caracteristiques du temps

        gameDisplay.blit(self.thermometre_icon, (450, 20))
        gameDisplay.blit(self.RainProb_icon, (450, 140))
        gameDisplay.blit(self.humidite_icon, (450, 260))

#Affiche les donnees liees a la temperature/humidite/pluie

        self.Temperature = self.FontTemperature.render(str(self.infos_meteo.DailyWeather.Temperatures[self.currentday])+" C", True, (0,0,0,100))
        gameDisplay.blit(self.Temperature, (601, 21))
        self.Temperature = self.FontTemperature.render(str(self.infos_meteo.DailyWeather.Temperatures[self.currentday])+" C", True, (255,255,255))
        gameDisplay.blit(self.Temperature, (600, 20))
        

        self.Humidite = self.FontHumidite.render(str(self.infos_meteo.DailyWeather.Humidities[self.currentday])+"%", True, (0,0,0,100))
        gameDisplay.blit(self.Humidite, (601, 141))
        self.Humidite = self.FontHumidite.render(str(self.infos_meteo.DailyWeather.Humidities[self.currentday])+"%", True, (255,255,255))
        gameDisplay.blit(self.Humidite, (600, 140))

        self.RainProb = self.FontRainProb.render(str(self.infos_meteo.DailyWeather.RainProbs[self.currentday])+"%", True, (0,0,0,100))
        gameDisplay.blit(self.RainProb, (601, 261))
        self.RainProb = self.FontRainProb.render(str(self.infos_meteo.DailyWeather.RainProbs[self.currentday])+"%", True, (255,255,255))
        gameDisplay.blit(self.RainProb, (600, 260))

#Definie les cases de la barre du bas

        gameDisplay.blit(self.barre_icon, (1.5,380))
        gameDisplay.blit(self.barre_icon, (115.5,380))
        gameDisplay.blit(self.barre_icon, (229.5,380))
        gameDisplay.blit(self.barre_icon, (343.5,380))
        gameDisplay.blit(self.barre_icon, (457.5,380))
        gameDisplay.blit(self.barre_icon, (571.5,380))
        gameDisplay.blit(self.barre_icon, (685.5,380))

#Affiche le texte dans les cases de la barre du bas

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

#faire boucle for pour tous les blocs ci-dessous (en garder un)

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

#Affiche la temperature dans les cases du bas

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

#Affiche la date

        self.Date = self.FontDate.render("Lundi 21 Mars 2016", True, (255,255,255))
        gameDisplay.blit(self.Date, (40, 20))
        
            
    def Quit(self):
        pass
    def __str__(self):
        return "WEATHERSCREEN"