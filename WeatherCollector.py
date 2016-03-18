'''
WeatherCollector : Classe qui recupere les previsions meteo sur internet, et les range plus un acces facile plus tard.

MODE D'EMPLOI :
    - Importer la classe avec "from WeatherCollector import *"
    - Creer dans le __init__ une variable qui gardera les infos avec "self.infos_meteo = WeatherCollector()". Ceci va creer la classe WeatherCollector, qui va immediatement
        et stocker les infos sur internet, des qu'on la cree.

    - Pour recuperer une info actuelle (ex temperature actuelle), utiliser         "  self.infos_meteo.CurrentWeather.Temperature  "
                                                                                                                     .Icon
                                                                                                                     .Humidity
                                                                                                                     .RainProb
    - Pour recuperer toutes les infos des 12 prochaines heures, utiliser           "   self.infos_meteo.HourlyWeather.Temperatures[i]  "   avec i de 0 a 11, 0 etant l'heure
                                                                                                                     .Icons[i]             suivante et les i suivant etant
                                                                                                                     .Humidities[i]        les heures qui suivent.
                                                                                                                     .RainProbs[i]
    - Pour recuperer toutes les infos des 12 prochaines heures, utiliser           "    self.infos_meteo.DailyWeather.Temperatures[i]  "   avec i de 0 a 11, 0 etant le jour
                                                                                                                     .Icons[i]             suivant et les i suivant etant
                                                                                                                     .Humidities[i]        les jours qui suivent.
                                                                                                                     .RainProbs[i]

'''
import pygame

class WeatherCollector():
    def __init__(self):
        '''
        A FAIRE : Tout le code qui recupere les infos d'internet et les range dans les classes 'current weather', 'daily weather' et 'hourly weather'
        '''


        '''
        Imaginons qu'on a les infos. On les range ensuite dans les classes respectives pour organiser et rendre l'acces plus facile plus tard.
        A FAIRE : INFORMATIONS ALEATOIRES TEMPORAIRES
        '''
        self.CurrentWeather = current_weather("heavy_rain",   # Icone
                                              19,      # Temperature
                                              68,      # Humidite
                                              12)      # Chances de pleuvoir

        self.HourlyWeather  = hourly_weather (["sun", "sun", "sun_cloud", "sun_cloud", "cloud", "light_rain", "light_rain", "light_rain", "heavy_rain", "storm", "snow", "snow"],
                                              [19   , 19   , 18         , 17         , 17     , 15          , 12          , 8           , 4           , 2      , -1    , -4    ],
                                              [9    , 17   , 32         , 43         , 57     , 68          , 76          , 85          , 100         , 100    , 100   , 100   ],
                                              [0    , 0    , 5          , 13         , 39     , 60          , 70          , 78          , 90          , 100    , 90    , 80    ])

        self.DailyWeather   = daily_weather  (["storm", "sun", "sun_cloud", "snow", "cloud", "light_rain", "heavy_rain", "light_rain", "heavy_rain", "storm", "snow", "snow"],
                                              [19   , 19   , 18         , 17         , 17     , 15          , 12          , 8           , 4           , 2      , -1    , -4    ],
                                              [9    , 17   , 32         , 43         , 57     , 68          , 76          , 85          , 100         , 100    , 100   , 100   ],
                                              [0    , 0    , 5          , 13         , 39     , 60          , 70          , 78          , 90          , 100    , 90    , 80    ])


class current_weather():
    def __init__(self, icon, temp, hum, rain_prob):
        self.Icon         = icon
        self.Temperature  = temp
        self.Humidity     = hum
        self.RainProb     = rain_prob

class hourly_weather():
    def __init__(self, icons, temps, hums, rain_probs):
        self.Icons        = icons
        self.Temperatures = temps
        self.Humidities   = hums
        self.RainProbs    = rain_probs


class daily_weather():
    def __init__(self, icons, temps, hums, rain_probs):
        self.Icons        = icons
        self.Temperatures = temps
        self.Humidities   = hums
        self.RainProbs    = rain_probs
        #self.Sunrises     = sunrises
        #self.Sunsets      = sunsets
