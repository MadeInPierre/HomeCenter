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
        self.DayPannelTitleFont   = pygame.font.Font("Fonts/HelveticaNeue-Medium.ttf", 16)
        self.SyncFont   = pygame.font.Font("Fonts/HelveticaNeue-Light.ttf", 17, bold=True)

        self.bg_img = pygame.image.load("Images/calendar2.jpg")
        self.sync_img = pygame.image.load("Images/cloud_sync.png")

        self.now = datetime.datetime.now()
        self.arrow = SwipeArrow(40)

        self.selected_month = int(self.now.month - 1)
        self.selected_year = int(self.now.year)
        self.selected_day = [0, 0]
        self.MonthNames = ["Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin", "Juillet", "Aout", "Septembre", "Octobre", "Novembre", "Decembre"]
        self.DayNames =   ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

        self.reset_calendars()

        self.syncing = False
        self.synced = False
        self.calendar_events = [("CONTROLES", []), ("ARENDRE",   []), ("TRAVAIL",   []), ("DIVERS",    []), ("MAIN",      [])] # evenements vides au demarrage
        for list in self.calendar_events:
            print list[0]
            for event in list[1]:
                print event
            print "\n"



    def Update(self, InputEvents):
        if self.syncing == True:
            self.calendar_events = CalendarCollector().get_events(2015, 10, 1)
            self.syncing = False
            self.synced = True

        '''
        Si on n'a pas encore synchronise, le faire a la prochaine frame.
        On le fait pour que l'appli demarre rapidement (sans synchroniser) et qu'elle synchronise juste
        apres avoir demarre. Le meilleur des deux mondes : demarrage rapide et les evenements apparaissent rapidement apres.
        '''
        if not self.synced:
            self.syncing = True

        for event in InputEvents:
            if "TOUCH" in event:
                mousepos = pygame.mouse.get_pos()

                '''
                Si l'utilisateur clique sur les fleches pour changer le mois
                '''
                if Helpers.is_in_rect(mousepos, [30 + 530/2 - self.monthTitleSurface.get_rect().width / 2 - 80, 19, 160, 50]):
                    self.selected_month -= 1
                    if self.selected_month < 0:
                        self.selected_month = 11
                        self.selected_year -= 1
                    self.reset_calendars()
                if Helpers.is_in_rect(mousepos, [30 + 530/2 + self.monthTitleSurface.get_rect().width / 2 + 20, 24, 40, 40]):
                    self.selected_month += 1
                    if self.selected_month > 11:
                        self.selected_month = 0
                        self.selected_year += 1
                    self.reset_calendars()

                '''
                Si l'utilisateur clique sur le bouton de synchronisation, initier la recherche d'evenements sur internet 
                et changer l'icone sur l'interface pour prevenir (question de design et intuitivite)
                '''
                if Helpers.is_in_rect(mousepos, [685, 8, 90, 30]):
                    self.syncing = True

                '''
                Si l'utilisateur clique sur un autre jour
                '''
                for week in range(0, 5):
                    for day in range(0, 7):
                        if Helpers.is_in_rect(mousepos, [30 + 530/7 * day, 60 + 390/5 * week, 530 / 7, 390 / 5]):
                            self.selected_day = [week, day]
            if "LEFT" in event:
                self.selected_month += 1
                if self.selected_month > 11:
                    self.selected_month = 0
                    self.selected_year += 1
                self.reset_calendars()
            if "RIGHT" in event:
                self.selected_month -= 1
                if self.selected_month < 0:
                    self.selected_month = 11
                    self.selected_year -= 1
                self.reset_calendars()

    def Draw(self, gameDisplay):
        Helpers.blit_alpha(gameDisplay, self.bg_img, (0, 0), 120)

        self.monthTitleSurface = self.MonthsTitleFont.render(self.MonthNames[self.selected_month] + " " + str(self.selected_year), True, (255, 255, 255))
        gameDisplay.blit(self.monthTitleSurface, (30 + 550/2 - self.monthTitleSurface.get_rect().width / 2, 6))

        self.arrow.Draw(gameDisplay, (30 + 550/2 - self.monthTitleSurface.get_rect().width / 2 - 40, 14), "LEFT")
        self.arrow.Draw(gameDisplay, (30 + 550/2 + self.monthTitleSurface.get_rect().width / 2 + 20, 14), "RIGHT")

        '''
        On dessine les numeros des jours et les pastilles de couleur d'evenements
        de chaque case dans le panneau mensuel
        '''
        for week in range(0, 5):
            for day in range(0, 7):
                '''
                On trouve le numero du jour correspondant... (on en a besoin dans tous nos calculs)
                '''
                day_value, is_from_actual_month = self.get_day_number_at_pos(week, day)



                '''
                On rend la case selectionnee un peu plus claire
                '''
                if self.selected_day[1] == day and self.selected_day[0] == week:
                    s = pygame.Surface((530 / 7 + 1, 390 / 5 + 1)).convert_alpha()
                    s.fill((255, 255, 255, 100))
                    gameDisplay.blit(s, (30 + day * 530/7, 60 + week * 390/5))

                '''
                La case d'aujourd'hui devient plus claire.
                '''
                if self.now.day == day_value and self.now.month == self.selected_month + 1 and self.now.year == self.selected_year:
                    s = pygame.Surface((530 / 7, 390 / 5)).convert_alpha()
                    s.fill((0, 0, 255, 200))
                    gameDisplay.blit(s, (30 + day * 530/7, 60 + week * 390/5))
                
                
                '''
                ... et on le dessine.
                '''
                if is_from_actual_month == True:
                    self.daySurface = self.DaysTitleFont.render(str(day_value), True, (255, 255, 255))
                if is_from_actual_month == False:
                    self.daySurface = self.DaysTitleFont.render(str(day_value), True, (180, 180, 180))
                gameDisplay.blit(self.daySurface, (36 + day * 530/7, 62 + week * 390/5))

                
                '''
                On scanne tous les evenements pour voir s'il y en a qui correspondent a la case actuelle.
                '''
                cell_year  = str(self.selected_year)

                #on trouve le bon mois correspondant a la case selectionnee
                if is_from_actual_month:
                    cell_month = str(self.selected_month + 1)
                else: 
                    if day_value > 20:
                        cell_month = str(self.selected_month)
                    else: 
                        cell_month = str(self.selected_month + 2)

                cell_day   = str(day_value)

                for i in range(0, 5):
                    for event in self.calendar_events[i][1]:
                        '''
                        on separe lannee, mois et jour de l'evenement pour le comparer ensuite
                        '''
                        date = unicodedata.normalize('NFKD', event[1][:10]).encode('ascii','ignore').split("-") 

                        '''
                        Si l'evenement a bien lieu au jour de la case actuelle, on dessine pastille de couleur et position correspondantes a 
                        la categorie de l'evenement (controle, a rendre, travail...)
                        '''
                        if  (int(date[0]) == int(cell_year)  ) and \
                            (int(date[1]) == int(cell_month) ) and \
                            (int(date[2]) == int(cell_day)   ):
                            s = pygame.Surface((530/7 + 1, 11))
                            if i == 0: color = (255,   0,   0)
                            if i == 1: color = (255, 145,   0)
                            if i == 2: color = (  0,  98, 255)
                            if i == 3: color = (115, 255,   0)
                            if i == 4: color = (255,   0, 255) 
                            s.fill(color)
                            gameDisplay.blit(s, (30 + day * 530/7, 60 + week * 390/5 + 24 + 11 * i))

                

        '''
        On dessine les lignes horizontales de la grille mensuelle, puis les verticales.
        '''
        self.draw_line(gameDisplay, 30 , 60 + 0 * 390/5        , 530, 1  , (255, 255, 255))
        self.draw_line(gameDisplay, 30 , 60 + 1 * 390/5        , 530, 1  , (255, 255, 255))
        self.draw_line(gameDisplay, 30 , 60 + 2 * 390/5        , 530, 1  , (255, 255, 255))
        self.draw_line(gameDisplay, 30 , 60 + 3 * 390/5        , 530, 1  , (255, 255, 255))
        self.draw_line(gameDisplay, 30 , 60 + 4 * 390/5        , 530, 1  , (255, 255, 255))
        self.draw_line(gameDisplay, 30 , 60 + 5 * 390/5        , 530, 1  , (255, 255, 255))

        self.draw_line(gameDisplay, 30 + 0 * 530/7, 60         , 1  , 390, (255, 255, 255))
        self.draw_line(gameDisplay, 30 + 1 * 530/7, 60         , 1  , 390, (255, 255, 255))
        self.draw_line(gameDisplay, 30 + 2 * 530/7, 60         , 1  , 390, (255, 255, 255))
        self.draw_line(gameDisplay, 30 + 3 * 530/7, 60         , 1  , 390, (255, 255, 255))
        self.draw_line(gameDisplay, 30 + 4 * 530/7, 60         , 1  , 390, (255, 255, 255))
        self.draw_line(gameDisplay, 30 + 5 * 530/7, 60         , 1  , 390, (255, 255, 255))
        self.draw_line(gameDisplay, 30 + 6 * 530/7, 60         , 1  , 390, (255, 255, 255))
        self.draw_line(gameDisplay, 30 + 7 * 530/7, 60         , 1  , 390, (255, 255, 255))

        s = pygame.Surface((530, 390)).convert_alpha()
        s.fill((255, 255, 255, 35))
        gameDisplay.blit(s, (30, 60))

        s = pygame.Surface((180, 390)).convert_alpha()
        s.fill((255, 255, 255, 35))
        gameDisplay.blit(s, (590, 60))

        '''
        On dessine les titres des colonnes du panneau mensuel (lundi, mardi...)
        '''
        for i in range(0, 7):
            text = self.EventsTitleFont.render(self.DayNames[i], True, (255, 255, 255))
            gameDisplay.blit(text, (30 + 530/7/2 + i * 530/7 - text.get_rect().width / 2, 40))

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

        '''
        Titre du panneau journalier, qui reporte le jour selectionne (par exemple "Mercredi 29 Janvier")
        '''
        day, i = self.get_day_number_at_pos(self.selected_day[0], self.selected_day[1])
        dayPannelTitleSurface = self.DayPannelTitleFont.render(str(self.DayNames[self.selected_day[1]]) + " " + str(day) + " " + self.MonthNames[self.selected_month], True, (255, 255, 255))
        gameDisplay.blit(dayPannelTitleSurface, (680 - dayPannelTitleSurface.get_rect().width / 2, 66))

        '''
        AFFICHAGE DES DETAILS DES EVENEMENTS (l'interieur du panneau journalier)
        '''
        y_offset = 0
        for i in range(0, 5):
            for event in self.calendar_events[i][1]:
                '''
                on separe lannee, mois et jour de l'evenement pour le comparer ensuite
                '''
                date = unicodedata.normalize('NFKD', event[1][:10]).encode('ascii','ignore').split("-") 
                day, z = self.get_day_number_at_pos(self.selected_day[0], self.selected_day[1]) # z inutile

                month = self.selected_month + 1
                if not z:
                    if day < 10:
                        month += 1
                    elif day > 20:
                        month -= 1

                '''
                Si l'evenement a bien lieu au jour de la case actuelle, on dessine le titre puis la description
                de l'evenement.
                '''
                if  (int(date[0]) == int(self.selected_year)      ) and \
                    (int(date[1]) == int(month) ) and \
                    (int(date[2]) == int(day)):
                    if i == 0: color = (255,   0,   0)
                    if i == 1: color = (255, 145,   0)
                    if i == 2: color = (  0,  98, 255)
                    if i == 3: color = (115, 255,   0)
                    if i == 4: color = (255,   0, 255)
                    
                    title_offset = self.render_text_in_zone(gameDisplay, event[0], self.EventsTitleFont, color, (600, 110 + y_offset), 760)
                    
                    rect = pygame.Surface((179, title_offset + 10)).convert_alpha()
                    rect.fill(color)
                    gameDisplay.blit(rect, (591, 110 + y_offset - 5))

                    self.render_text_in_zone(gameDisplay, event[0], self.EventsTitleFont, (255, 255, 255), (600, 110 + y_offset), 760) # A OPTIMISER
                    
                    y_offset += title_offset + 20

        if self.syncing == False:
            text = self.SyncFont.render("SYNC", True, (255, 255, 255))
            gameDisplay.blit(text, (690, 12))
        else:
            text = self.SyncFont.render("SYNCING...", True, (255, 255, 255))
            gameDisplay.blit(text, (650, 12))
        
        gameDisplay.blit(self.sync_img, (740, 8))






    def get_day_number_at_pos(self, week, day):
        day_value = self.actual_month[week][day]

        is_from_actual_month = True
        
        
        if day_value == 0 and week == 0:
            day_value = self.prev_month[len(self.prev_month) - 1][day]
            is_from_actual_month = False
        if day_value == 0 and week == 4:
            day_value = self.next_month[0][day]
            is_from_actual_month = False

        return day_value, is_from_actual_month

    def draw_line(self, gameDisplay, pX, pY, width, height, color):
        ligne = pygame.Surface((width, height))
        ligne.fill(color)
        gameDisplay.blit(ligne, (pX, pY))

    def render_text_in_zone(self, gameDisplay, text, font, color, startpos, horizontal_size_limit): # parametres necessaires pour dessiner le texte multiligneS
        s = font.render(text, True, color) # on dessine le texte une première fois pour avoir sa longueur
        h_size = horizontal_size_limit - startpos[0] # la limite en longueur que le texte ne doit pas depasser
        vertical_size = 0 # voir return en derniere ligne

        '''
        Si le texte est trop long, on le coupe jusqu'a ce qu'il reste dans l'espace delimite
        '''
        if s.get_rect().width > h_size:
            splitted_text = text.split() # On separe la phrase entre chaque mot
            final_lines = []

            cropped_size = 0
            done = False
            for i in range(len(splitted_text) - 1, -1, -1): # on scanne toues les mots en partant du dernier
                if not done:
                    word_image = font.render(splitted_text[i], True, color) # on dessine le mot pour avoir 
                
                    cropped_size += word_image.get_rect().width + 4 # on compte ce mot en plus dans la largeur du texte qu'on est en train de couper
                                                                    # on ajoute 4 pixels pour compter l'espace qui vient juste apres le mot dans la phrase

                    if s.get_rect().width - cropped_size < h_size: # on teste si le bout coupe est suffisant pour que le titre ne depasse pas la limite
                        '''
                        On prepare le dessin en dessinant la premier ligne...
                        '''
                        first_line_text = ""
                        for word in splitted_text[0:i]:
                            first_line_text += " " + word
                        first_line = font.render(first_line_text, True, color)
                        final_lines.append(first_line)
                        
                        '''
                        ... separement a la deuxieme (le bout de la premiere coupee) 
                        '''
                        line_text = ""
                        for word in range(i, len(splitted_text)):
                            line_text += " " + splitted_text[word]
                    
                        final_line = font.render(line_text, True, color)
                        final_lines.append(final_line)

                        done = True

            '''
            On dessine les lignes sur l'ecran, avec la bonne position
            '''
            for linenumber in range(0, len(final_lines)):
                gameDisplay.blit(final_lines[linenumber], (startpos[0], startpos[1] + 17 * linenumber))
            vertical_size = 17 * len(final_lines) # on enregistre l'espace vertical qui a ete utilise pour afficher le texte (voir return en derniere ligne)
            
        else:
            gameDisplay.blit(s, startpos) # si le titre n'est pas trop long, on le dessine simplement.
            vertical_size = s.get_rect().height
        return vertical_size # redonne la taille verticale qui a ete utilisee pour afficher ce texte (utile pour afficher les prochains titres en dessous).


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
