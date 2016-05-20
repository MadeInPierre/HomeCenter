﻿import pygame
import datetime
import time
from AnimationManager import *
from WeatherCollector import *
from InputManager import *
from Helpers import *

class WeatherScreen():
    def __init__(self, WindowRes):
        self.windowres = WindowRes
        self.infos_meteo = WeatherCollector()

        self.ScreenStatus = "RUNNING"

#Icones meteo de la grande fenetre

        self.sunny_icon = pygame.image.load("Images/Icones_Meteo/weather-clear-2.png").convert_alpha()
        self.sunny_cloud_icon = pygame.image.load("Images/Icones_Meteo/weather-few-clouds-2.png").convert_alpha()
        self.cloud_icon = pygame.image.load("Images/Icones_Meteo/weather-overcast-2.png").convert_alpha()
        self.light_rain_icon = pygame.image.load("Images/Icones_Meteo/weather-showers-scattered-2.png").convert_alpha()
        self.heavy_rain_icon = pygame.image.load("Images/Icones_Meteo/weather-showers-2.png").convert_alpha()
        self.storm_icon = pygame.image.load("Images/Icones_Meteo/weather-storm-2.png").convert_alpha()
        self.snow_icon = pygame.image.load("Images/Icones_Meteo/weather-snow-2.png").convert_alpha()


#Icones meteo des petites fenetres

        self.sunny_mini_icon = pygame.image.load("Images/Icones_Meteo/weather-clear-2-mini.png").convert_alpha()
        self.sunny_cloud_mini_icon = pygame.image.load("Images/Icones_Meteo/weather-few-clouds-2-mini.png").convert_alpha()
        self.cloud_mini_icon = pygame.image.load("Images/Icones_Meteo/weather-overcast-2-mini.png").convert_alpha()
        self.light_rain_mini_icon = pygame.image.load("Images/Icones_Meteo/weather-showers-scattered-2-mini.png").convert_alpha()
        self.heavy_rain_mini_icon = pygame.image.load("Images/Icones_Meteo/weather-showers-2-mini.png").convert_alpha()
        self.storm_mini_icon = pygame.image.load("Images/Icones_Meteo/weather-storm-2-mini.png").convert_alpha()
        self.snow_mini_icon = pygame.image.load("Images/Icones_Meteo/weather-snow-2-mini.png").convert_alpha()
       
#Icones des parametres du temps de la grande fenetre (vent, temperature...)

        self.thermometremax_icon = pygame.image.load("Images/Icones_Meteo/ThermometreMax.png").convert_alpha()
        self.thermometremin_icon = pygame.image.load("Images/Icones_Meteo/ThermometreMin.png").convert_alpha()
        self.humidite_icon = pygame.image.load("Images/Icones_Meteo/Goutte.png").convert_alpha()
        self.RainProb_icon = pygame.image.load("Images/Icones_Meteo/probapluie.png").convert_alpha()
        self.wind_icon = pygame.image.load("Images/Icones_Meteo/Vent.png").convert_alpha() 
        self.sunrise_icon = pygame.image.load("Images/Icones_Meteo/sunrise.png").convert_alpha() 
        self.sunset_icon = pygame.image.load("Images/Icones_Meteo/sunset.png").convert_alpha() 
        self.switch_icon = pygame.image.load("Images/Icones_Meteo/switch.png").convert_alpha()


#Fonds d'ecran en fonction du temps

        self.WallPaperSun = pygame.image.load("Images/Icones_Meteo/sun_sky.jpg").convert_alpha()
        self.WallPaperCloudandsun = pygame.image.load("Images/Icones_Meteo/cloudandsun_sky.jpg").convert_alpha()
        self.WallPaperCloud = pygame.image.load("Images/Icones_Meteo/cloud_sky.jpg").convert_alpha()
        self.WallPaperLightrain = pygame.image.load("Images/Icones_Meteo/lightrain_sky.jpg").convert_alpha()
        self.WallPaperHeavyrain = pygame.image.load("Images/Icones_Meteo/heavyrain_sky.jpg").convert_alpha()
        self.WallPaperStorm = pygame.image.load("Images/Icones_Meteo/storm_sky.jpg").convert_alpha()
        self.WallPaperSnow = pygame.image.load("Images/Icones_Meteo/snow_sky.jpg").convert_alpha()

#Styles d'ecriture

        self.FontDatum = pygame.font.Font("Fonts/HelveticaNeue-Light.ttf", 55)
        self.FontTemperatureMini = pygame.font.Font("Fonts/HelveticaNeue-UltraLight.ttf", 40)
        self.FontDate = pygame.font.Font("Fonts/HelveticaNeue-Light.ttf", 45)
        self.DayFont = pygame.font.Font("Fonts/HelveticaNeue-UltraLight.ttf",30)

#Barres transparentes

        self.barre_icon = pygame.Surface((113,100)).convert_alpha() 
        self.barre_icon.fill((255,255,255,150)) #Case des jours non choisis plus transparentes (150)
        self.barre2_icon = pygame.Surface((113,100)).convert_alpha() 
        self.barre2_icon.fill((255,255,255,225)) #Case du jour choisi qui est plus claire (225)
        self.barre_switch = pygame.Surface((59,37)).convert_alpha()
        self.barre_switch.fill((255,255,255,210))
        self.barre2_switch = pygame.Surface((59,37)).convert_alpha()
        self.barre2_switch.fill((255,255,255,150))

#!!!!!!VARIABLES!!!!!!:
            
#Variable qui correspond à l'ecran qui EST affiche / EST apparu

        self.currentday = 0

#Variable qui correspond à l'ecran que l'on VEUT faire apparaitre

        self.NewDay = 0

#Variables qui appellent des chronos

        self.chrono = AnimationManager() #Chrono de la majeur partie  des animations
        self.chrono2 = AnimationManager() #Chrono de l'icone meteo de l'ecran principal
        self.chrono1screen = AnimationManager() #Chrono du 1er ecran (quand on lance l'application)

#Variables qui donnent la transparence (Permet un ordre d'apparition)

        self.Transparence = 0  #Transparence de la date, de l'icone meteo et du fond d'ecran
        self.Transparence2 = 0 #Transparence de la temperature, de son icone associe et du bouton "switch"
        self.Transparence3 = 0 #Transparence du vent et de son icone associe
        self.Transparence4 = 0 #Transparence du la proba de pluie et de son icone associe
        self.Transparence5 = 0 #Transparence de l'humidite et de son icone associe
        self.Transparence6 = 0 #Transparence du lever de soleil et de son icone associe
        self.Transparence7 = 0 #Transparence du coucher de soleil et de son icone associe

#Variable qui donne la position Y (Utilisee dans des formules pour faire "planer" textes/images...)

        self.PosY_Icone = 100

#Variable qui sert a donner la temperature max ou min (Pair = Max / Impair = Min)

        self.tempswitch = 0

    def Update(self, InputEvents):

#Ci-dessous: Si le clic est dans le carre delimite par les valeurs alors affiche l'ecran lie a la variable NewDay (La valeur du NewDay prendra ensuite la forme de currentday, cad )

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

#Permet de passer de la temperature max a min et inversement quand on clique sur le bouton "switch"

                    if Helpers.is_in_rect(mousepos, [205, 75, 65, 65]):
                        self.tempswitch = self.tempswitch + 1


#Aniamation -> Fondu "apparaissant" du 1er écran (currentscreen0) quand on lance l'application 
#L'ecran apparait des que l'application est lancee

        if self.chrono1screen.elapsed_time() > 0 and self.chrono1screen < 1:
            self.Transparence=int(255 / (1 + math.exp(-(self.chrono1screen.elapsed_time() - 2.5/2 ) / 0.05)))
                            
#Animation -> Fondu "apparaissant" des ecrans (Apres le 1er). La condition avec le chrono1screen est necessaire pour ne pas engendrer un conflit entre les animations 
#L'ecran apparait 1sec apres qu'on ait decide de changer d'ecran (il faut 1sec a l'ecran d'avant pour disparaitre)

        if self.chrono1screen.elapsed_time() > 1:
            if self.chrono.elapsed_time() > 1 and self.chrono.elapsed_time() < 3  :
                self.currentday = self.NewDay #Le jour que l'on a selectionne va apparaitre
                self.Transparence=int(255 / (1 + math.exp(-(self.chrono.elapsed_time() - 2 ) / 0.1)))

#Animation -> Fondu "disparaissant" des ecrans. La condition avec le chrono1screen est necessaire pour ne pas engendrer un conflit entre les animations 

            if self.chrono.elapsed_time() > 0 and self.chrono.elapsed_time() < 1 : 
                self.Transparence=int(255 / (1 + math.exp(-(0.5 - self.chrono.elapsed_time()) / 0.1)))

#Animation -> Fondu "apparaissant" des Icones et de leur valeur associee
#Voir a quel element les transparences correspondent dans le init

            if self.chrono.elapsed_time() > 3 and  self.chrono.elapsed_time() < 4 :
                self.Transparence2=int(255 / (1 + math.exp(-(self.chrono.elapsed_time() - 6.5/2) / 0.05)))

            if self.chrono.elapsed_time() > 4 and  self.chrono.elapsed_time() < 5:
                self.Transparence3=int(255 / (1 + math.exp(-(self.chrono.elapsed_time() - 8.5/2) / 0.05)))

            if self.chrono.elapsed_time() > 5 and  self.chrono.elapsed_time() < 6:
                self.Transparence4=int(255 / (1 + math.exp(-(self.chrono.elapsed_time() - 10.5/2) / 0.05)))

            if self.chrono.elapsed_time() > 6 and  self.chrono.elapsed_time() < 7:
                self.Transparence5=int(255 / (1 + math.exp(-(self.chrono.elapsed_time() - 12.5/2) / 0.05)))

            if self.chrono.elapsed_time() > 7 and  self.chrono.elapsed_time() < 8:
                self.Transparence6=int(255 / (1 + math.exp(-(self.chrono.elapsed_time() - 14.5/2) / 0.05)))

            if self.chrono.elapsed_time() > 8 and  self.chrono.elapsed_time() < 9:
                self.Transparence7=int(255 / (1 + math.exp(-(self.chrono.elapsed_time() - 16.5/2) / 0.05)))

#Animation -> Fondu "disparraissant"  des Icones et de leur valeur associee

            if self.chrono.elapsed_time() > 0 and self.chrono.elapsed_time() < 1: 
                self.Transparence2=int(255 / (1 + math.exp(-(0.5 - self.chrono.elapsed_time()) / 0.1)))

            if self.chrono.elapsed_time() > 0 and self.chrono.elapsed_time() < 1 : 
                self.Transparence3=int(255 / (1 + math.exp(-(0.5 - self.chrono.elapsed_time()) / 0.1)))

            if self.chrono.elapsed_time() > 0 and self.chrono.elapsed_time() < 1 : 
                self.Transparence4=int(255 / (1 + math.exp(-(0.5 - self.chrono.elapsed_time()) / 0.1)))

            if self.chrono.elapsed_time() > 0 and self.chrono.elapsed_time() < 1 : 
                self.Transparence5=int(255 / (1 + math.exp(-(0.5 - self.chrono.elapsed_time()) / 0.1)))

            if self.chrono.elapsed_time() > 0 and self.chrono.elapsed_time() < 1 : 
                self.Transparence6=int(255 / (1 + math.exp(-(0.5 - self.chrono.elapsed_time()) / 0.1)))

            if self.chrono.elapsed_time() > 0 and self.chrono.elapsed_time() < 1 : 
                self.Transparence7=int(255 / (1 + math.exp(-(0.5 - self.chrono.elapsed_time()) / 0.1)))


#Varaible PosY_Icone est placee dans fonction sinusoidale pour faire "planer" textes/images
#fct sinus: Amplitude*math.sin(2*math.pi/Periode*t)
      
        if self.chrono2.elapsed_time() > 0:
            self.PosY_Icone = 100 + 5*math.sin(2*math.pi/3*self.chrono2.elapsed_time())
            

    def Draw(self, gameDisplay):

#Afficher le fond d'ecran et l'icone correspondant a la case selectionnne et en lien avec les infos du WeatherCollector ("01d"... sont les informations recuperees du site internet)
#Permet aussi de gerer la transparence et la position des elements a afficher

        if str(self.infos_meteo.DailyWeather.Icons[self.currentday]) == "01d" : 
            Helpers.blit_alpha(gameDisplay, self.WallPaperSun,(0,0), self.Transparence)
            Helpers.blit_alpha(gameDisplay, self.sunny_icon, (20, self.PosY_Icone), self.Transparence)

        if str(self.infos_meteo.DailyWeather.Icons[self.currentday]) == "02d" : 
            Helpers.blit_alpha(gameDisplay, self.WallPaperCloudandsun,(0,0), self.Transparence)
            Helpers.blit_alpha(gameDisplay, self.sunny_cloud_icon, (20, self.PosY_Icone), self.Transparence)

        if str(self.infos_meteo.DailyWeather.Icons[self.currentday]) == "03d" : 
            Helpers.blit_alpha(gameDisplay, self.WallPaperCloud,(0,0), self.Transparence)
            Helpers.blit_alpha(gameDisplay, self.cloud_icon, (20, self.PosY_Icone), self.Transparence)

        if str(self.infos_meteo.DailyWeather.Icons[self.currentday]) == "04d" : 
            Helpers.blit_alpha(gameDisplay, self.WallPaperCloud,(0,0), self.Transparence)
            Helpers.blit_alpha(gameDisplay, self.cloud_icon, (20, self.PosY_Icone), self.Transparence)

        if str(self.infos_meteo.DailyWeather.Icons[self.currentday]) == "10d" : 
            Helpers.blit_alpha(gameDisplay, self.WallPaperLightrain,(0,0), self.Transparence)
            Helpers.blit_alpha(gameDisplay, self.light_rain_icon, (20, self.PosY_Icone), self.Transparence)

        if str(self.infos_meteo.DailyWeather.Icons[self.currentday]) == "09d" :
            Helpers.blit_alpha(gameDisplay, self.WallPaperHeavyrain,(0,0), self.Transparence)
            Helpers.blit_alpha(gameDisplay, self.heavy_rain_icon, (20, self.PosY_Icone), self.Transparence)

        if str(self.infos_meteo.DailyWeather.Icons[self.currentday]) == "11d" :
            Helpers.blit_alpha(gameDisplay, self.WallPaperStorm,(0,0), self.Transparence)
            Helpers.blit_alpha(gameDisplay, self.storm_icon, (20, self.PosY_Icone), self.Transparence)

        if str(self.infos_meteo.DailyWeather.Icons[self.currentday]) == "13d": 
            Helpers.blit_alpha(gameDisplay, self.WallPaperSnow,(0,0), self.Transparence)
            Helpers.blit_alpha(gameDisplay, self.snow_icon, (20, self.PosY_Icone), self.Transparence)

#Affiche les icones lies aux caracteristiques du temps

        Helpers.blit_alpha(gameDisplay, self.RainProb_icon, (250, 175), self.Transparence4)
        Helpers.blit_alpha(gameDisplay, self.humidite_icon, (510, 175), self.Transparence5)
        Helpers.blit_alpha(gameDisplay, self.wind_icon, (515, 70), self.Transparence3)
        Helpers.blit_alpha(gameDisplay, self.sunrise_icon, (250, 280), self.Transparence6)
        Helpers.blit_alpha(gameDisplay, self.sunset_icon, (510, 280), self.Transparence7)

#Affiche les donnees liees a la temperature/humidite/pluie
#Exception pour la temperature -> Affiche aussi LES icones de la temperature (Temp Max et Min)

        if self.tempswitch % 2 == 0:
                self.Temperature = self.FontDatum.render(str(self.infos_meteo.DailyWeather.TemperaturesMax[self.currentday])+chr(176)+"C", True, (0,0,0,100))
                Helpers.blit_alpha(gameDisplay, self.Temperature, (341, 71), self.Transparence2)
                self.Temperature = self.FontDatum.render(str(self.infos_meteo.DailyWeather.TemperaturesMax[self.currentday])+chr(176)+"C", True, (255,255,255))
                Helpers.blit_alpha(gameDisplay, self.Temperature, (340, 70), self.Transparence2)
                Helpers.blit_alpha(gameDisplay, self.thermometremax_icon, (250, 70), self.Transparence2)

        else:
                self.Temperature = self.FontDatum.render(str(self.infos_meteo.DailyWeather.TemperaturesMin[self.currentday])+chr(176)+"C", True, (0,0,0,100))
                Helpers.blit_alpha(gameDisplay, self.Temperature, (341, 71), self.Transparence2)
                self.Temperature = self.FontDatum.render(str(self.infos_meteo.DailyWeather.TemperaturesMin[self.currentday])+chr(176)+"C", True, (255,255,255))
                Helpers.blit_alpha(gameDisplay, self.Temperature, (340, 70), self.Transparence2)
                Helpers.blit_alpha(gameDisplay, self.thermometremin_icon, (250, 70), self.Transparence2)

        
        self.WindStrength = self.FontDatum.render(str(self.infos_meteo.DailyWeather.WindStrength[self.currentday])+"km/h", True, (0,0,0,100))
        Helpers.blit_alpha(gameDisplay, self.WindStrength, (601, 71), self.Transparence3)
        self.WindStrength = self.FontDatum.render(str(self.infos_meteo.DailyWeather.WindStrength[self.currentday])+"km/h", True, (255,255,255))
        Helpers.blit_alpha(gameDisplay, self.WindStrength, (600, 70), self.Transparence3)

        self.Sunset = self.FontDatum.render(str(self.infos_meteo.DailyWeather.Sunset[self.currentday]), True, (0,0,0,100))
        Helpers.blit_alpha(gameDisplay, self.Sunset, (601, 281), self.Transparence7)
        self.Sunset = self.FontDatum.render(str(self.infos_meteo.DailyWeather.Sunset[self.currentday]), True, (255,255,255))
        Helpers.blit_alpha(gameDisplay, self.Sunset, (600, 280), self.Transparence7)

        self.Sunrise = self.FontDatum.render(str(self.infos_meteo.DailyWeather.Sunrise[self.currentday]), True, (0,0,0,100))
        Helpers.blit_alpha(gameDisplay, self.Sunrise, (341, 281), self.Transparence6)
        self.Sunrise = self.FontDatum.render(str(self.infos_meteo.DailyWeather.Sunrise[self.currentday]), True, (255,255,255))
        Helpers.blit_alpha(gameDisplay, self.Sunrise, (340, 280), self.Transparence6)

#Le site duquel on recupere les infos meteo ne donne plus d'info concernant la proba de l'humidite a partir du 6e jour, d'ou ce "if", pour ne pas faire apparaitre "0%" pour le 5e et 6e jour

        if self.currentday == 5 or self.currentday == 6 : 
            self.Humidite = self.FontDatum.render("N/A %", True, (0,0,0,100))
            Helpers.blit_alpha(gameDisplay, self.Humidite, (601, 176), self.Transparence5)
            self.Humidite = self.FontDatum.render("N/A %", True, (255,255,255))
            Helpers.blit_alpha(gameDisplay, self.Humidite, (600, 175), self.Transparence5)

            self.RainProb = self.FontDatum.render(str(self.infos_meteo.DailyWeather.RainProbs[self.currentday])+"%", True, (0,0,0,100))
            Helpers.blit_alpha(gameDisplay, self.RainProb, (341, 176), self.Transparence4)
            self.RainProb = self.FontDatum.render(str(self.infos_meteo.DailyWeather.RainProbs[self.currentday])+"%", True, (255,255,255))
            Helpers.blit_alpha(gameDisplay, self.RainProb, (340, 175), self.Transparence4)

          
        else:
            self.Humidite = self.FontDatum.render(str(self.infos_meteo.DailyWeather.Humidities[self.currentday])+"%", True, (0,0,0,100))
            Helpers.blit_alpha(gameDisplay, self.Humidite, (601, 176), self.Transparence5)
            self.Humidite = self.FontDatum.render(str(self.infos_meteo.DailyWeather.Humidities[self.currentday])+"%", True, (255,255,255))
            Helpers.blit_alpha(gameDisplay, self.Humidite, (600, 175), self.Transparence5)

            self.RainProb = self.FontDatum.render(str(self.infos_meteo.DailyWeather.RainProbs[self.currentday])+"%", True, (0,0,0,100))
            Helpers.blit_alpha(gameDisplay, self.RainProb, (341, 176), self.Transparence4)
            self.RainProb = self.FontDatum.render(str(self.infos_meteo.DailyWeather.RainProbs[self.currentday])+"%", True, (255,255,255))
            Helpers.blit_alpha(gameDisplay, self.RainProb, (340, 175), self.Transparence4)

#Definie les cases de la barre du bas
#La case selectionnee est plus claire 

        for i in range (0,7):
            if self.NewDay == i:
                gameDisplay.blit(self.barre2_icon, (115.5+(i-1)*114,380))
            if self.NewDay != i:
                gameDisplay.blit(self.barre_icon, (115.5+(i-1)*114,380))

#Affiche le texte dans les cases de la barre du bas
        
            self.DayText = self.DayFont.render(str(self.infos_meteo.DailyWeather.Week[i]), True, (0,0,0))
            gameDisplay.blit(self.DayText, (115.5+(i-1)*114+20,380+60))
       
#Boucle (voir au-dessus) qui identifie quel icone de temps a afficher suivant le jour selectionne et les informations qui l'accompagnent

            if self.infos_meteo.DailyWeather.Icons[i] == "01d":
                gameDisplay.blit(self.sunny_mini_icon,(115.5+(i-1)*114,380))           
            if self.infos_meteo.DailyWeather.Icons[i] == "02d":
                gameDisplay.blit(self.sunny_cloud_mini_icon,(115.5+(i-1)*114,380))                    
            if self.infos_meteo.DailyWeather.Icons[i] == "03d":
                gameDisplay.blit(self.cloud_mini_icon,(115.5+(i-1)*114,380))              
            if self.infos_meteo.DailyWeather.Icons[i] == "04d":               
                gameDisplay.blit(self.cloud_mini_icon,(115.5+(i-1)*114,380))                   
            if self.infos_meteo.DailyWeather.Icons[i] == "10d":   
                gameDisplay.blit(self.light_rain_mini_icon,(115.5+(i-1)*114,380))                     
            if self.infos_meteo.DailyWeather.Icons[i] == "09d":
                gameDisplay.blit(self.heavy_rain_mini_icon,(115.5+(i-1)*114,380))                    
            if self.infos_meteo.DailyWeather.Icons[i] == "11d":
                gameDisplay.blit(self.storm_mini_icon,(115.5+(i-1)*114,380))                     
            if self.infos_meteo.DailyWeather.Icons[i] == "13d":
                gameDisplay.blit(self.snow_mini_icon,(115.5+(i-1)*114,380))
                         
#Affiche la temperature dans les cases du bas
#La position de la temperature n'est pas la meme suivant si elle est a 1 ou 2 chiffres

            if len(str(self.infos_meteo.DailyWeather.TemperaturesBas[i])) == 1:
                self.TemperatureMini = self.FontTemperatureMini.render(str(self.infos_meteo.DailyWeather.TemperaturesBas[i])+chr(176), True, (0,0,0))
                gameDisplay.blit(self.TemperatureMini, (178+(i-1)*114, 380))
            if len(str(self.infos_meteo.DailyWeather.TemperaturesBas[i])) > 1:
                self.TemperatureMini = self.FontTemperatureMini.render(str(self.infos_meteo.DailyWeather.TemperaturesBas[i])+chr(176), True, (0,0,0))
                gameDisplay.blit(self.TemperatureMini, (169+(i-1)*114, 380))
           
#Affiche date en haut de l'écran
  
        self.Date = self.FontDate.render(self.infos_meteo.DailyWeather.Time[self.currentday], True, (0,0,0,100))
        Helpers.blit_alpha(gameDisplay, self.Date, (41, 21), self.Transparence)
        self.Date = self.FontDate.render(self.infos_meteo.DailyWeather.Time[self.currentday], True, (255,255,255))
        Helpers.blit_alpha(gameDisplay, self.Date, (40, 20), self.Transparence)      

#Fond du bouton switch

        if self.tempswitch % 2 == 0:
           Helpers.blit_alpha(gameDisplay, self.barre2_switch, (213, 95), self.Transparence2)
        if self.tempswitch % 2 == 1:
           Helpers.blit_alpha(gameDisplay, self.barre_switch, (213, 95), self.Transparence2)    

#Bouton switch

        Helpers.blit_alpha(gameDisplay, self.switch_icon, (205, 75), self.Transparence2)

   
                   
    def Quit(self):
        pass
    def __str__(self):
        return "WEATHERSCREEN"