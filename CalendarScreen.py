import pygame, math
import calendar, datetime
import unicodedata
from CalendarCollector import *
from Helpers import *

class CalendarScreen():
    def __init__(self, WindowRes):
        self.windowres = WindowRes
        self.ScreenStatus = "RUNNING"
        self.MonthsTitleFont = pygame.font.Font("Fonts/HelveticaNeue-Light.ttf",  24)
        self.DaysTitleFont   = pygame.font.Font("Fonts/HelveticaNeue-Medium.ttf", 15)
        self.EventsTitleFont   = pygame.font.Font("Fonts/HelveticaNeue-Medium.ttf", 14)
        self.now = datetime.datetime.now()
        self.arrow = SwipeArrow(40)

        self.selected_month = int(self.now.month)
        self.selected_year = int(self.now.year)
        self.selected_day = [0, 0]
        self.MonthNames =["Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin", "Juillet", "Aout", "Septembre", "Octobre", "Novembre", "Decembre"]

        self.reset_calendars()


        self.calendar_events = CalendarCollector().get_events(2015, 10, 1)
        for list in self.calendar_events:
            print list[0]
            for event in list[1]:
                print event
            print "\n"
        self.test = self.calendar_events[2][1][0][0] # 1=CT AR TR DI MA, 2=1, 3=event_number, 4=TITRE DATE



    def Update(self, InputEvents):
        for event in InputEvents:
            if "TOUCH" in event:
                mousepos = pygame.mouse.get_pos()

                '''
                Si l'utilisateur clique sur les fleches pour changer le mois
                '''
                if Helpers.is_in_rect(mousepos, [30 + 550/2 - self.monthTitleSurface.get_rect().width / 2 - 40, 24, 40, 40]):
                    self.selected_month -= 1
                    if self.selected_month < 0:
                        self.selected_month = 11
                        self.selected_year -= 1
                    self.reset_calendars()
                if Helpers.is_in_rect(mousepos, [30 + 550/2 + self.monthTitleSurface.get_rect().width / 2 + 20, 24, 40, 40]):
                    self.selected_month += 1
                    if self.selected_month > 11:
                        self.selected_month = 0
                        self.selected_year += 1
                    self.reset_calendars()

                '''
                Si l'utilisateur clique sur un autre jour
                '''
                for week in range(0, 5):
                    for day in range(0, 7):
                        if Helpers.is_in_rect(mousepos, [30 + 530/7 * day, 60 + 390/5 * week, 530 / 7, 390 / 5]):
                            self.selected_day = [day, week]

    def Draw(self, gameDisplay):
        gameDisplay.fill((30, 30, 30))

        self.monthTitleSurface = self.MonthsTitleFont.render(self.MonthNames[self.selected_month] + " " + str(self.selected_year), True, (255, 255, 255))
        gameDisplay.blit(self.monthTitleSurface, (30 + 550/2 - self.monthTitleSurface.get_rect().width / 2, 16))
        self.arrow.Draw(gameDisplay, (30 + 550/2 - self.monthTitleSurface.get_rect().width / 2 - 40, 24), "LEFT")
        self.arrow.Draw(gameDisplay, (30 + 550/2 + self.monthTitleSurface.get_rect().width / 2 + 20, 24), "RIGHT")

        self.monthTitleSurface = self.EventsTitleFont.render("Bonjour", True, (30, 255, 30))
        #gameDisplay.blit(self.monthTitleSurface, (40, 80))
        #gameDisplay.blit(self.monthTitleSurface, (40, 100))
        #gameDisplay.blit(self.monthTitleSurface, (40, 120))

        '''
        On dessine les numeros des jours et les pastilles de couleur d'evenements
        de chaque case dans le panneau mensuel
        '''
        for week in range(0, 5):
            for day in range(0, 7):
                '''
                On trouve le numero du jour correspondant
                '''
                day_value = self.actual_month[week][day]
                is_from_actual_month = True
                if day_value == 0 and week == 0:
                    day_value = self.prev_month[len(self.prev_month) - 1][day]
                    is_from_actual_month = False
                if day_value == 0 and week == 4:
                    day_value = self.next_month[0][day]
                    is_from_actual_month = False

                '''
                On le dessine
                '''
                if is_from_actual_month == True:
                    self.daySurface = self.DaysTitleFont.render(str(day_value), True, (255, 255, 255))
                if is_from_actual_month == False:
                    self.daySurface = self.DaysTitleFont.render(str(day_value), True, (180, 180, 180))
                gameDisplay.blit(self.daySurface, (35 + 530/7 * day, 60+ 390/5 * week))

                '''
                On dessine les pastilles de chaque jour
                '''
                cell_year = str(self.selected_year)
                cell_month = str(self.selected_month + 1)
                cell_day = str(day_value)

                for event in self.calendar_events[0][1]:
                    event_date_parsed = unicodedata.normalize('NFKD', event[1]).encode('ascii','ignore').split("-")
                    if  (int(event_date_parsed[0]) == int(cell_year)  ) and \
                        (int(event_date_parsed[1]) == int(cell_month) ) and \
                        (int(event_date_parsed[2]) == int(cell_day)   ):
                        s = pygame.Surface((5, 5))
                        s.fill((255, 0, 0))
                        gameDisplay.blit(s, (35 + 530/7 * day + 5, 60+ 390/5 * week + 25))

                for event in self.calendar_events[1][1]:
                    event_date_parsed = unicodedata.normalize('NFKD', event[1]).encode('ascii','ignore').split("-")
                    if  (int(event_date_parsed[0]) == int(cell_year)  ) and \
                        (int(event_date_parsed[1]) == int(cell_month) ) and \
                        (int(event_date_parsed[2]) == int(cell_day)   ):
                        s = pygame.Surface((5, 5))
                        s.fill((255, 145, 0))
                        gameDisplay.blit(s, (35 + 530/7 * day + 5, 60+ 390/5 * week + 35))

                for event in self.calendar_events[2][1]:
                    event_date_parsed = unicodedata.normalize('NFKD', event[1]).encode('ascii','ignore').split("-")
                    if  (int(event_date_parsed[0]) == int(cell_year)  ) and \
                        (int(event_date_parsed[1]) == int(cell_month) ) and \
                        (int(event_date_parsed[2]) == int(cell_day)   ):
                        s = pygame.Surface((5, 5))
                        s.fill((0, 98, 255))
                        gameDisplay.blit(s, (35 + 530/7 * day + 5, 60+ 390/5 * week + 45))

                for event in self.calendar_events[3][1]:
                    event_date_parsed = unicodedata.normalize('NFKD', event[1]).encode('ascii','ignore').split("-")
                    if  (int(event_date_parsed[0]) == int(cell_year)  ) and \
                        (int(event_date_parsed[1]) == int(cell_month) ) and \
                        (int(event_date_parsed[2]) == int(cell_day)   ):
                        s = pygame.Surface((5, 5))
                        s.fill((115, 255, 0))
                        gameDisplay.blit(s, (35 + 530/7 * day + 5, 60+ 390/5 * week + 55))

                for event in self.calendar_events[4][1]:
                    event_date_parsed = unicodedata.normalize('NFKD', event[1]).encode('ascii','ignore').split("-")
                    if  (int(event_date_parsed[0]) == int(cell_year)  ) and \
                        (int(event_date_parsed[1]) == int(cell_month) ) and \
                        (int(event_date_parsed[2]) == int(cell_day)   ):
                        s = pygame.Surface((5, 5))
                        s.fill((255, 0, 255))
                        gameDisplay.blit(s, (35 + 530/7 * day + 5, 60+ 390/5 * week + 65))

                '''
                On rend la case selectionnee un peu plus claire
                '''
                if self.selected_day[0] == day and self.selected_day[1] == week:
                    s = pygame.Surface((530 / 7, 390 / 5)).convert_alpha()
                    s.fill((255, 255, 255, 100))
                    gameDisplay.blit(s, (30 + (530/7) * day, 60 + (390/5) * week))

                '''
                La case d'aujourd'hui devient plus claire.
                '''
                if self.now.day == day_value and self.now.month == self.selected_month and self.now.year == self.selected_year:
                    s = pygame.Surface((530 / 7, 390 / 5)).convert_alpha()
                    s.fill((45, 45, 255, 100))
                    gameDisplay.blit(s, (30 + (530/7) * day, 60 + (390/5) * week))


        '''
        On dessine le cadre externe du panneau mensuel
        '''
        self.draw_line(gameDisplay, 30 , 60                    , 530, 1  , (255, 255, 255))
        self.draw_line(gameDisplay, 30 , self.windowres[1] - 31, 530, 1  , (255, 255, 255))
        self.draw_line(gameDisplay, 30 , 60                    , 1  , 390, (255, 255, 255))
        self.draw_line(gameDisplay, 560, 60                    , 1  , 390, (255, 255, 255))

        '''
        On dessine les lignes separant les jours dans le panneau mensuel
        '''
        self.draw_line(gameDisplay, 30 , 60 + 390/5 * 1        , 530, 1  , (255, 255, 255))
        self.draw_line(gameDisplay, 30 , 60 + 390/5 * 2        , 530, 1  , (255, 255, 255))
        self.draw_line(gameDisplay, 30 , 60 + 390/5 * 3        , 530, 1  , (255, 255, 255))
        self.draw_line(gameDisplay, 30 , 60 + 390/5 * 4        , 530, 1  , (255, 255, 255))

        self.draw_line(gameDisplay, 30 + 530/7 * 1, 60         , 1  , 390, (255, 255, 255))
        self.draw_line(gameDisplay, 30 + 530/7 * 2, 60         , 1  , 390, (255, 255, 255))
        self.draw_line(gameDisplay, 30 + 530/7 * 3, 60         , 1  , 390, (255, 255, 255))
        self.draw_line(gameDisplay, 30 + 530/7 * 4, 60         , 1  , 390, (255, 255, 255))
        self.draw_line(gameDisplay, 30 + 530/7 * 5, 60         , 1  , 390, (255, 255, 255))
        self.draw_line(gameDisplay, 30 + 530/7 * 6, 60         , 1  , 390, (255, 255, 255))

        '''
        On dessine le cadre externe du panneau journalier
        '''
        self.draw_line(gameDisplay, 590, 60                    , 180, 1  , (255, 255, 255))
        self.draw_line(gameDisplay, 590, self.windowres[1] - 31, 180, 1  , (255, 255, 255))
        self.draw_line(gameDisplay, 590, 60                    , 1  , 390, (255, 255, 255))
        self.draw_line(gameDisplay, 770, 60                    , 1  , 390, (255, 255, 255))

        '''
        Ligne separatrice sous le titre/jour du panneau journalier
        '''
        self.draw_line(gameDisplay, 605, 90                    , 150, 1  , (255, 255, 255))

    def draw_line(self, gameDisplay, pX, pY, width, height, color):
        ligne = pygame.Surface((width, height))
        ligne.fill(color)
        gameDisplay.blit(ligne, (pX, pY))

    def reset_calendars(self):
        prev_y = self.selected_year
        prev_m = self.selected_month
        if prev_m == 0:
            prev_m = 12
            prev_y -= 1
        self.prev_month   = calendar.monthcalendar(prev_y, prev_m)

        self.actual_month = calendar.monthcalendar(self.selected_year, self.selected_month + 1)

        next_y = self.selected_year
        next_m = self.selected_month + 2
        if next_m > 12:
            next_m = 1
            next_y += 1
        self.next_month   = calendar.monthcalendar(next_y, next_m)

    def Quit(self):
        pass

    def __str__(self):
        return "CALENDARSCREEN"
