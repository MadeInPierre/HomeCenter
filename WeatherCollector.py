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
from pyowm import OWM # module meteo-internet

class WeatherCollector():
    def __init__(self):
        '''
        A FAIRE : Tout le code qui recupere les infos d'internet et les range dans les classes 'current weather', 'daily weather' et 'hourly weather'
        '''
        API = 'd71c3a62822470f2ecd05e06f214ecf5'
        CITY = 'Saint-Gely-du-Fesc'

        '''
        Pour avoir les conditions actuelles
        '''
        owm = OWM(API, language = 'fr')
        obs = owm.weather_at_id(2980033) # St Gely
        w = obs.get_weather()
        print "CONDITIONS EN CE MOMENT : "   + str(w.get_reference_time(timeformat='iso'))
        print "    meteo :  " + str(w.get_status()) + " (img = " + str(w.get_weather_icon_name()) + ")"
        print "    clouds : " + str(w.get_clouds())
        print "    rain :   " + str(w.get_rain())
        print "    wind :   "  + str(w.get_wind())
        print "    hum :    "  + str(w.get_humidity())
        print "    temp :   "  + str(w.get_temperature(unit='celsius'))

        '''
        Pour avoir les prochains jours
        '''
        fc = owm.daily_forecast('Saint-Gely-du-Fesc')
        f = fc.get_forecast()

        for w in f:
            print "TIME : "   + str(w.get_reference_time(timeformat='iso'))
            print "    meteo :  " + str(w.get_status()) + " (img = " + str(w.get_weather_icon_name()) + ")"
            print "    clouds : " + str(w.get_clouds())
            print "    rain :   " + str(w.get_rain())
            print "    wind :   "  + str(w.get_wind())
            print "    hum :    "  + str(w.get_humidity())
            print "    temp :   "  + str(w.get_temperature(unit='celsius'))
            


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

        self.DailyWeather   = daily_weather  (["sun", "storm", "sun_cloud", "snow", "heavy_rain", "light_rain", "cloud", "light_rain", "heavy_rain", "storm", "snow", "snow"],
                                              [19   , 19   , 18         , 17         , 17     , 15          , 12          , 8           , 4           , 2      , -1    , -4    ],
                                              [9    , 17   , 32         , 43         , 57     , 68          , 76          , 85          , 100         , 100    , 100   , 100   ],
                                              [0    , 0    , 5          , 13         , 39     , 60          , 70          , 78          , 90          , 100    , 90    , 80    ],
                                              [20   , 120  , 100        , 80         , 60     , 70          , 0           , 140         , 40          , 75     , 55    , 0     ],
                                              ["N-E","O"   , "E"        , "S"        , "N"    ,"S-O"        , "O"         ,""           ,""           , ""     , ""    , ""    ],
                                              ["7h02","7h03","7h04"     ,"7h05"      ,"7h06"  ,"7h10"       ,"7h12"       ,"7h15"       ,""           , ""     ,""     ,""     ],
                                              ["17h02","17h03","17h04"     ,"17h05"      ,"17h06"  ,"17h10"       ,"17h12"       ,"17h15"       ,""           , ""     ,""     ,""     ])

class current_weather():
    def __init__(self, icon, temp, hum, rain_prob,):
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
    def __init__(self, icons, temps, hums, rain_probs, wind_strength, wind_direction, sunrises, sunsets):
        self.Icons        = icons
        self.Temperatures = temps
        self.Humidities   = hums
        self.RainProbs    = rain_probs
        self.Sunrise     = sunrises
        self.Sunset     = sunsets
        self.WindStrength  = wind_strength
        self.WindDirection= wind_direction
