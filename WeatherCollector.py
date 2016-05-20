import pygame
from pyowm import OWM # module meteo-internet

class WeatherCollector():
    def __init__(self):
      
        API = 'd71c3a62822470f2ecd05e06f214ecf5'
        CITY = 'Saint-Gely-du-Fesc'

        '''
        Pour avoir les conditions actuelles
        '''
        owm = OWM(API, language = 'fr')

        '''
        Pour avoir les prochains jours
        '''
        fc = owm.daily_forecast('Saint-Gely-du-Fesc')
        f = fc.get_forecast()
        
#Listes qui recuperent les infos de la semaine

        self.Week = []
        self.Time = []
        self.Meteo = []
        self.Wind = []
        self.Hum = []
        self.TempMax = []
        self.TempMin = []
        self.Temp2 = []
        self.Rain = []
        self.Sunrise = []
        self.Sunset = []


        for w in f:

            print "TIME : "   + str(w.get_reference_time(timeformat='iso'))
            print self.Time
            print self.Week
            print "    meteo :  " + str(w.get_status()) + " (img = " + str(w.get_weather_icon_name()) + ")"
            print "    rain :   " + str(w.get_rain())
            print "    wind :   "  + str(w.get_wind())
            print "    hum :    "  + str(w.get_humidity())
            print "    temp :   "  + str(w.get_temperature(unit='celsius'))
            print "    sunrise: "  + str(w.get_sunrise_time('iso')[11:16])
            print "    sunset: "  + str(w.get_sunset_time('iso')[11:16])


#Quand il y a un "if" avec un '== "." ', cela veut dire qu l'on ne veut que la partie entiere de la donnee (on enleve les decimales)


            self.Day = (str(w.get_reference_time(timeformat='iso'))[8:10])

            self.Month = (str(w.get_reference_time(timeformat='iso'))[5:7])

            self.Year = (str(w.get_reference_time(timeformat='iso'))[0:4])

            self.Time.append(self.Day + "-" + self.Month + "-" + self.Year) #Date "a la francaise"

            self.Week.append(self.Day + "/" + self.Month) #Date "reduite" pour cases du bas

            self.Meteo.append(str(w.get_weather_icon_name()))           

#Si aucune info concernant la proba de pluie n'est donnee alors il y aura 0% de proba de pluie
            try:
                if str(w.get_rain()['all'])[2:3] == ".":
                    self.Rain.append(str(w.get_rain()['all'])[0:2])
                else:
                    self.Rain.append(str(w.get_rain()['all']))
            except:
                self.Rain.append("0")

            if str(w.get_wind()['speed']*3.6)[2:3] == "." :
                self.Wind.append(str(w.get_wind()['speed']*3.6)[0:2])
            else:
                self.Wind.append(str(w.get_wind()['speed']*3.6)[0:3])

            self.Hum.append(str(w.get_humidity()))

            if str((w.get_temperature(unit='celsius')['max']))[1:2] == ".":
                self.TempMax.append(str((w.get_temperature(unit='celsius')['max']))[0:1])
            else:
                self.TempMax.append(str((w.get_temperature(unit='celsius')['max']))[0:2])

            if str((w.get_temperature(unit='celsius')['min']))[1:2] == ".":
                self.TempMin.append(str((w.get_temperature(unit='celsius')['min']))[0:1])
            else:
                self.TempMin.append(str((w.get_temperature(unit='celsius')['min']))[0:2])
            
            if str((w.get_temperature(unit='celsius')['day']))[1:2] == ".":
                self.Temp2.append(str((w.get_temperature(unit='celsius')['day']))[0:1])
            else:
                self.Temp2.append(str((w.get_temperature(unit='celsius')['day']))[0:2])
            
            self.Sunrise.append(str(w.get_sunrise_time('iso')[11:16]))

            self.Sunset.append(str(w.get_sunset_time('iso')[11:16]))
         
     
        
        self.DailyWeather   = daily_weather  (self.Meteo,
                                              self.TempMax,
                                              self.TempMin,
                                              self.Hum,
                                              self.Rain,
                                              self.Wind,
                                              self.Sunrise,
                                              self.Sunset,
                                              self.Time,
                                              self.Week,
                                              self.Temp2) #Temperatures des cases du bas (moyenne du jour)

#On associe chaque liste a une variable du WeatherScreen

class daily_weather():
    def __init__(self, icons, tempmax, tempmin, hums, rain_probs, wind_strength, sunrises, sunsets, time, week, temp2):
        self.Icons        = icons
        self.TemperaturesMax = tempmax
        self.TemperaturesMin = tempmin
        self.Humidities   = hums
        self.RainProbs    = rain_probs
        self.Sunrise     = sunrises
        self.Sunset     = sunsets
        self.WindStrength  = wind_strength
        self.Time = time
        self.Week = week
        self.TemperaturesBas = temp2