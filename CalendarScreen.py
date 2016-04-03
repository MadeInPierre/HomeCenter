import pygame
import math
import calendar
import datetime
import unicodedata
from CalendarCollector import *
from Helpers import *

class CalendarScreen():
    def __init__(self, WindowRes):
        self.windowres = WindowRes
        self.ScreenStatus = "RUNNING"

        self.MonthsTitleFont = pygame.font.Font("Fonts/HelveticaNeue-Light.ttf",  24)
        self.DaysTitleFont = pygame.font.Font("Fonts/HelveticaNeue-Medium.ttf", 15)
        self.EventsTitleFont = pygame.font.Font("Fonts/HelveticaNeue-Medium.ttf", 14)
        self.EventsDescriptionFont = pygame.font.Font("Fonts/HelveticaNeue-Medium.ttf", 10)
        self.DayPannelTitleFont = pygame.font.Font("Fonts/HelveticaNeue-Medium.ttf", 16)
        self.SyncFont = pygame.font.Font("Fonts/HelveticaNeue-Light.ttf", 17, bold=True)

        self.bg_img = pygame.image.load("Images/calendar2.jpg")
        self.sync_img = pygame.image.load("Images/cloud_sync.png")
        self.arrow = SwipeArrow(40)
        
        self.now = datetime.datetime.now()

        self.selected_month = int(self.now.month - 1)
        self.selected_year = int(self.now.year)
        self.selected_day = [0, 0]
        self.MonthNames = ["Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin", "Juillet", "Aout", "Septembre", "Octobre", "Novembre", "Decembre"]
        self.DayNames = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

        self.reset_calendars()

        self.syncing = False
        self.synced = False
        self.calendar_events = [("CONTROLES", []), ("ARENDRE", []), ("TRAVAIL", []), ("DIVERS", []), ("MAIN", [])] # evenements vides au demarrage

        self.MonthGridSurface = pygame.Surface((WindowRes[0], WindowRes[1])).convert_alpha()
        self.updateGrid = True

        '''
        Chronometre qui aidera dans les animations (quand on clique sur un evenement dans le panneau journalier,
        la case s'ouvre joliment pour afficher la description de l'evenement.)
        '''
        self.daypannel_click = False #quand on clique dans le panneau journalier, le Draw s'occupe de voir s'il faut activer une animation
        self.evenements = []



    def Update(self, InputEvents):
        '''
        MISE A ZERO On remet tout a zero niveau evenements...
        '''
        self.daypannel_click = False

        if self.syncing == True:
            self.calendar_events = CalendarCollector().get_events(2015, 10, 1)
            self.syncing = False
            self.synced = True
            self.updateGrid = True

        '''
        Si on n'a pas encore synchronise, le faire a la prochaine frame.
        On le fait pour que l'appli demarre rapidement (sans synchroniser) et qu'elle synchronise juste
        apres avoir demarre. Le meilleur des deux mondes : demarrage rapide et les evenements apparaissent quelque temps apres.
        '''
        if not self.synced:
            self.syncing = True

        '''
        EVENEMENTS
        '''
        for event in InputEvents:
            if "TOUCH" in event:
                mousepos = pygame.mouse.get_pos()

                '''
                Si l'utilisateur clique sur les fleches pour changer le mois
                '''
                if Helpers.is_in_rect(mousepos, [30 + 530 / 2 - self.monthTitleSurface.get_rect().width / 2 - 80, 19, 160, 50]):
                    self.selected_month -= 1
                    if self.selected_month < 0:
                        self.selected_month = 11
                        self.selected_year -= 1
                    self.reset_calendars()
                    self.updateGrid = True
                if Helpers.is_in_rect(mousepos, [30 + 530 / 2 + self.monthTitleSurface.get_rect().width / 2 + 20, 24, 40, 40]):
                    self.selected_month += 1
                    if self.selected_month > 11:
                        self.selected_month = 0
                        self.selected_year += 1
                    self.reset_calendars()
                    self.updateGrid = True

                '''
                Si l'utilisateur clique sur le bouton de synchronisation, initier la recherche d'evenements sur internet
                et changer l'icone sur l'interface pour prevenir (question de design et intuitivite)
                '''
                if Helpers.is_in_rect(mousepos, [685, 8, 90, 30]):
                    self.syncing = True
                    self.updateGrid = True

                if Helpers.is_in_rect(mousepos, [590, 60, 180, 390]):
                    self.daypannel_click = True

                    '''
                    On regarde si l'utilisateur a clique sur un des evenements...
                    '''
                    y_offset = 0
                    for cal_event in self.evenements:
                        if Helpers.is_in_rect(mousepos, [591, 110 + y_offset - 5, 179, cal_event.vertical_space_used - 10]):
                            '''
                            ... si oui : on active l'animation d'ouverture et on ferme tous les autres.
                            '''
                            cal_event.Revert()
                        else:
                            cal_event.Close()

                        y_offset += cal_event.vertical_space_used

                '''
                Si l'utilisateur clique sur un autre jour
                '''
                for week in range(0, 5):
                    for day in range(0, 7):
                        if Helpers.is_in_rect(mousepos, [30 + 530 / 7 * day, 60 + 390 / 5 * week, 530 / 7, 390 / 5]):
                            '''
                            On enregistre le jour selectionne pour plus tard (eclaircir la case du jour selectionne...)
                            '''
                            self.selected_day = [week, day]

                            '''
                            On rafraichit la liste d'evenements dans le panneau journalier.
                            '''
                            self.update_evenements_list()


            if "LEFT" in event:
                self.selected_month += 1
                if self.selected_month > 11:
                    self.selected_month = 0
                    self.selected_year += 1
                self.reset_calendars()
                self.update_evenements_list()
                self.updateGrid = True
            if "RIGHT" in event:
                self.selected_month -= 1
                if self.selected_month < 0:
                    self.selected_month = 11
                    self.selected_year -= 1
                self.reset_calendars()
                self.update_evenements_list()
                self.updateGrid = True


        for event in self.evenements:
            event.Update()


    '''---------------------------------------------------------------------------------------------------------------------------------
    ----------------------------------------------------------   PARTIE DRAW   ---------------------------------------------------------
    ------------------------------------------------------------------------------------------------------------------------------------'''


    def Draw(self, gameDisplay):
        Helpers.blit_alpha(gameDisplay, self.bg_img, (0, 0), 120)

        self.monthTitleSurface = self.MonthsTitleFont.render(self.MonthNames[self.selected_month] + " " + str(self.selected_year), True, (255, 255, 255))
        gameDisplay.blit(self.monthTitleSurface, (30 + 550 / 2 - self.monthTitleSurface.get_rect().width / 2, 6))

        self.arrow.Draw(gameDisplay, (30 + 550 / 2 - self.monthTitleSurface.get_rect().width / 2 - 40, 14), "LEFT")
        self.arrow.Draw(gameDisplay, (30 + 550 / 2 + self.monthTitleSurface.get_rect().width / 2 + 20, 14), "RIGHT")

        '''
        On redessine le panneau mensuel seulement si le système en a besoin (le Update() decide : changement de mois, nouvelle synchronisation...).
        '''
        if self.updateGrid == True:
            self.MonthGridSurface.fill((0, 0, 0, 0))
            self.draw_monthGrid(self.MonthGridSurface)
            self.updateGrid = False
        '''
        On rend le jour selectionne plus clair que les autres cases
        '''
        s = pygame.Surface((530 / 7 + 1, 390 / 5 + 1)).convert_alpha()
        s.fill((255, 255, 255, 100))
        gameDisplay.blit(s, (30 + self.selected_day[1] * 530 / 7, 60 + self.selected_day[0] * 390 / 5))

        '''
        On dessine le panneau mensuel
        '''
        gameDisplay.blit(self.MonthGridSurface, (0, 0))


        '''
        ------------------------------------ PANNEAU JOURNALIER -----------------------------
        '''

        '''
        On rend le panneau un peu plus clair en rajoutent bu blance transparent.
        '''
        s = pygame.Surface((180, 390)).convert_alpha()
        s.fill((255, 255, 255, 35))
        gameDisplay.blit(s, (590, 60))

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
        month = self.selected_month
        if not i:
            if day < 10:
                month += 1
                if month > 10:
                    month = 0
            elif day > 20:
                month -= 1

        dayPannelTitleSurface = self.DayPannelTitleFont.render(str(self.DayNames[self.selected_day[1]]) + " " + str(day) + " " + self.MonthNames[month], True, (255, 255, 255))
        gameDisplay.blit(dayPannelTitleSurface, (680 - dayPannelTitleSurface.get_rect().width / 2, 66))

        '''
        AFFICHAGE DES DETAILS DES EVENEMENTS (l'interieur du panneau journalier)
        '''
        y_offset = 0
        for event in self.evenements:
            event.Draw(gameDisplay, y_offset)

            y_offset += event.vertical_space_used

        '''
        Autres elements graphiques dans l'interface
        '''
        if self.syncing == False:
            text = self.SyncFont.render("SYNC", True, (255, 255, 255))
            gameDisplay.blit(text, (690, 12))
        else:
            text = self.SyncFont.render("SYNCING...", True, (255, 255, 255))
            gameDisplay.blit(text, (650, 12))

        gameDisplay.blit(self.sync_img, (740, 8))







    '''--------------------------------------------------------------------------------------------------------------------------------------------------------'''







    def draw_monthGrid(self, gameDisplay):
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
                '''if self.selected_day[1] == day and self.selected_day[0] == week:
                    s = pygame.Surface((530 / 7 + 1, 390 / 5 + 1)).convert_alpha()
                    s.fill((255, 255, 255, 100))
                    gameDisplay.blit(s, (30 + day * 530 / 7, 60 + week * 390 / 5))'''

                '''
                La case d'aujourd'hui devient plus claire.
                '''
                if self.now.day == day_value and self.now.month == self.selected_month + 1 and self.now.year == self.selected_year:
                    s = pygame.Surface((530 / 7, 390 / 5)).convert_alpha()
                    s.fill((0, 0, 255, 200))
                    gameDisplay.blit(s, (30 + day * 530 / 7, 60 + week * 390 / 5))


                '''
                ... et on le dessine.
                '''
                if is_from_actual_month == True:
                    self.daySurface = self.DaysTitleFont.render(str(day_value), True, (255, 255, 255))
                if is_from_actual_month == False:
                    self.daySurface = self.DaysTitleFont.render(str(day_value), True, (180, 180, 180))
                gameDisplay.blit(self.daySurface, (36 + day * 530 / 7, 62 + week * 390 / 5))


                '''
                On scanne tous les evenements pour voir s'il y en a qui correspondent a la case actuelle.
                '''
                cell_year = str(self.selected_year)

                #on trouve le bon mois correspondant a la case selectionnee
                if is_from_actual_month:
                    cell_month = str(self.selected_month + 1)
                else:
                    if day_value > 20:
                        cell_month = str(self.selected_month)
                    else:
                        cell_month = str(self.selected_month + 2)

                cell_day = str(day_value)

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
                        if  (int(date[0]) == int(cell_year)) and \
                            (int(date[1]) == int(cell_month)) and \
                            (int(date[2]) == int(cell_day)):
                            s = pygame.Surface((530 / 7 + 1, 11))
                            if i == 0: color = (255,   0,   0)
                            if i == 1: color = (255, 145,   0)
                            if i == 2: color = (0,  98, 255)
                            if i == 3: color = (115, 255,   0)
                            if i == 4: color = (255,   0, 255)
                            s.fill(color)
                            gameDisplay.blit(s, (30 + day * 530 / 7, 60 + week * 390 / 5 + 24 + 11 * i))



        '''
        On dessine les lignes horizontales de la grille mensuelle, puis les verticales.
        '''
        self.draw_line(gameDisplay, 30 , 60 + 0 * 390 / 5        , 530, 1  , (255, 255, 255))
        self.draw_line(gameDisplay, 30 , 60 + 1 * 390 / 5        , 530, 1  , (255, 255, 255))
        self.draw_line(gameDisplay, 30 , 60 + 2 * 390 / 5        , 530, 1  , (255, 255, 255))
        self.draw_line(gameDisplay, 30 , 60 + 3 * 390 / 5        , 530, 1  , (255, 255, 255))
        self.draw_line(gameDisplay, 30 , 60 + 4 * 390 / 5        , 530, 1  , (255, 255, 255))
        self.draw_line(gameDisplay, 30 , 60 + 5 * 390 / 5        , 530, 1  , (255, 255, 255))

        self.draw_line(gameDisplay, 30 + 0 * 530 / 7, 60         , 1  , 390, (255, 255, 255))
        self.draw_line(gameDisplay, 30 + 1 * 530 / 7, 60         , 1  , 390, (255, 255, 255))
        self.draw_line(gameDisplay, 30 + 2 * 530 / 7, 60         , 1  , 390, (255, 255, 255))
        self.draw_line(gameDisplay, 30 + 3 * 530 / 7, 60         , 1  , 390, (255, 255, 255))
        self.draw_line(gameDisplay, 30 + 4 * 530 / 7, 60         , 1  , 390, (255, 255, 255))
        self.draw_line(gameDisplay, 30 + 5 * 530 / 7, 60         , 1  , 390, (255, 255, 255))
        self.draw_line(gameDisplay, 30 + 6 * 530 / 7, 60         , 1  , 390, (255, 255, 255))
        self.draw_line(gameDisplay, 30 + 7 * 530 / 7, 60         , 1  , 390, (255, 255, 255))

        '''
        On rend la grille un peu plus claire que le fond en rajoutant du blanc transparent.
        '''
        s = pygame.Surface((530, 390)).convert_alpha()
        s.fill((255, 255, 255, 35))
        gameDisplay.blit(s, (30, 60))

        '''
        On dessine les titres des colonnes du panneau mensuel (lundi, mardi...)
        '''
        for i in range(0, 7):
            text = self.EventsTitleFont.render(self.DayNames[i], True, (255, 255, 255))
            gameDisplay.blit(text, (30 + 530 / 7 / 2 + i * 530 / 7 - text.get_rect().width / 2, 40))

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

                    cropped_size += word_image.get_rect().width + 4 # on compte ce mot en plus dans la largeur du texte qu'on est en train de
                                                                    # couper
                                                                    # on ajoute
                                                                                                                                       # 4 pixels
                                                                                                                                       # pour
                                                                                                                                       # compter
                                                                                                                                       # l'espace
                                                                                                                                       # qui vient
                                                                                                                                       # juste
                                                                                                                                       # apres le
                                                                                                                                       # mot dans
                                                                                                                                       # la phrase

                    if s.get_rect().width - cropped_size < h_size: # on teste si le bout coupe est suffisant pour que le titre ne depasse pas la
                                                                   # limite
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
            vertical_size = 17 * len(final_lines) # on enregistre l'espace vertical qui a ete utilise pour afficher le texte
                                                  # (voir return en derniere ligne)

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
        self.prev_month = calendar.monthcalendar(prev_y, prev_m)

        self.actual_month = calendar.monthcalendar(self.selected_year, self.selected_month + 1)

        next_y = self.selected_year
        next_m = self.selected_month + 2
        if next_m > 12:
            next_m = 1
            next_y += 1
        self.next_month = calendar.monthcalendar(next_y, next_m)

    def update_evenements_list(self):
        '''
        On remplit une liste d'evenements correspondant a ce jour ci.
        '''
        self.evenements = []
                            
        day, z = self.get_day_number_at_pos(self.selected_day[0], self.selected_day[1])
        month = self.selected_month + 1
        if not z:
            if day < 10:
                month += 1
            elif day > 20:
                month -= 1

        for i in range(0, 5):
            for event in self.calendar_events[i][1]:
                '''
                on separe lannee, mois et jour de l'evenement pour le comparer ensuite
                '''
                date = unicodedata.normalize('NFKD', event[1][:10]).encode('ascii','ignore').split("-")
                '''
                Si l'evenement a bien lieu au jour de la case actuelle, on dessine le titre puis la description
                de l'evenement.
                '''
                if (int(date[0]) == int(self.selected_year)) and (int(date[1]) == int(month)) and (int(date[2]) == int(day)):
                    self.evenements.append(Event(event + [i], self.EventsTitleFont, self.EventsDescriptionFont))

    def Quit(self):
        pass

    def __str__(self):
        return "CALENDARSCREEN"





class Event():
    def __init__(self, event, titleFont, descriptionFont):
        self.Title       = event[0]
        self.Date        = event[1]
        self.Description = event[2]
        self.Type        = event[3]

        if event[3] == 0: self.color = (255,   0,   0)
        if event[3] == 1: self.color = (255, 145,   0)
        if event[3] == 2: self.color = (0,    98, 255)
        if event[3] == 3: self.color = (115, 255,   0)
        if event[3] == 4: self.color = (255,   0, 255)

        self.EventsTitleFont = titleFont
        self.EventsDescriptionFont = descriptionFont

        if self.Description is not '':
            self.print_description = True
        else:
            self.print_description = False

        self.animation_state = "CLOSED"
        self.animation_progress = 0.0
        self.chrono = AnimationManager()

        self.vertical_space_used = 0
        self.arrow = SwipeArrow(size = 10)
        self.arrowtransp_progress = 255
        self.arrow_direction = "DOWN"

        self.pre_rendered = False

    def Update(self):
        if "OPENING" in self.animation_state:
            if self.chrono.elapsed_time() > 0 and self.chrono.elapsed_time() < 0.6:
                self.animation_progress = self.total_offset / (1 + math.exp(-(self.chrono.elapsed_time() - 0.2) / 0.06))

                if self.animation_progress > self.total_offset - 1:
                    self.animation_progress = self.total_offset

            if self.chrono.elapsed_time() > 0 and self.chrono.elapsed_time() < 0.2:
                self.arrowtransp_progress = 255 / (1 + math.exp(-(0.1 - self.chrono.elapsed_time()) / 0.02))
                self.arrow_direction = "DOWN"
            if self.chrono.elapsed_time() > 0.6 and self.chrono.elapsed_time() < 0.8:
                self.arrowtransp_progress = 255 / (1 + math.exp(-(self.chrono.elapsed_time() - 0.7) / 0.02))
                self.arrow_direction = "UP"

            if self.chrono.elapsed_time() > 0.8:
                self.animation_state = "OPENED"

        if "CLOSING" in self.animation_state:
            if self.chrono.elapsed_time() > 0 and self.chrono.elapsed_time() < 0.6:
                self.animation_progress = self.total_offset / (1 + math.exp(-(0.2 - self.chrono.elapsed_time()) / 0.06))

                if self.animation_progress < 1:
                    self.animation_progress = 0

            if self.chrono.elapsed_time() > 0 and self.chrono.elapsed_time() < 0.2:
                self.arrowtransp_progress = 255 / (1 + math.exp(-(0.1 - self.chrono.elapsed_time()) / 0.02))
                self.arrow_direction = "UP"
            if self.chrono.elapsed_time() > 0.6 and self.chrono.elapsed_time() < 0.8:
                self.arrowtransp_progress = 255 / (1 + math.exp(-(self.chrono.elapsed_time() - 0.7) / 0.02))
                self.arrow_direction = "DOWN"

            if self.chrono.elapsed_time() > 0.8:
                self.animation_state = "CLOSED"


    def Close(self):
        if self.print_description is True:
            if self.animation_state is not "CLOSED":
                self.animation_state = "CLOSING"
                self.chrono.reset()

    def Open(self):
        if self.print_description is True:
            if self.animation_state is not "OPENED":
                self.animation_state = "OPENING"
                self.chrono.reset()

    def Revert(self):
        if self.print_description is True:
            if self.animation_state is "CLOSED":
                self.Open()
            if self.animation_state is "OPENED":
                self.Close()

    def pre_render(self, gameDisplay, y_offset):
        s = pygame.Surface((1, 1))
        self.title_offset       = self.render_text_in_zone(s, self.Title,       self.EventsTitleFont,       17, self.color,      (600, 110 + y_offset),       760)
        self.description_offset = self.render_text_in_zone(s, self.Description, self.EventsDescriptionFont, 12, (255, 255, 255), (18, self.title_offset + 12), 160)
        self.total_offset = self.description_offset + 10

    def Draw(self, gameDisplay, y_offset):
        if not self.pre_rendered:
            self.pre_render(gameDisplay, y_offset)
            self.pre_rendered = True

        rect = pygame.Surface((179, self.title_offset + 10 + self.animation_progress)).convert_alpha()
        rect.fill(self.color)

        if self.print_description is True:
            self.render_text_in_zone(rect, self.Description, self.EventsDescriptionFont, 12, (255, 255, 255), (18, self.title_offset + 12), 160)
            self.arrow.Draw(rect, (rect.get_rect().width - 15, rect.get_rect().height - 12), self.arrow_direction, self.arrowtransp_progress)

        gameDisplay.blit(rect, (591, 110 + y_offset - 5))



        self.render_text_in_zone(gameDisplay, self.Title, self.EventsTitleFont, 17, (255, 255, 255), (600, 110 + y_offset), 760) # A OPTIMISER

        self.vertical_space_used = self.title_offset + 20 + self.animation_progress



    def render_text_in_zone(self, gameDisplay, text, font, line_spacing, color, startpos, horizontal_size_limit): # parametres necessaires pour dessiner le texte multiligneS
        s = font.render(text, True, color) # on dessine le texte une première fois pour avoir sa longueur
        h_size = horizontal_size_limit - startpos[0] # la limite en longueur que le texte ne doit pas depasser
        vertical_size = 0 # voir return en derniere ligne

        '''
        Si le texte est trop long, on le coupe jusqu'a ce qu'il reste dans l'espace delimite
        '''
        if s.get_rect().width > h_size:
            splitted_text = text.split() # On separe la phrase entre chaque mot

            cropped_size = 0
            for i in range(len(splitted_text) - 1, -1, -1): # on scanne toues les mots en partant du dernier
                word_image = font.render(splitted_text[i], True, color) # on dessine le mot pour avoir

                cropped_size += word_image.get_rect().width + 4 

                if s.get_rect().width - cropped_size < h_size: # on teste si le bout coupe est suffisant pour que le titre ne depasse pas la limite
                    first_line_text = ""
                    for word in splitted_text[0:i]:
                        first_line_text += " " + word
                    first_line = font.render(first_line_text, True, color)
                    gameDisplay.blit(first_line, startpos)

                    
                    line_text = ""
                    for word in range(i, len(splitted_text)):
                        line_text += " " + splitted_text[word]

                    line = self.render_text_in_zone(gameDisplay, line_text, font, line_spacing, color, (startpos[0], startpos[1] + line_spacing), horizontal_size_limit)
                    return line + line_spacing

        else:
            gameDisplay.blit(s, startpos) # si le titre n'est pas trop long, on le dessine directement sans transformations.
            vertical_size = s.get_rect().height
        return vertical_size # redonne la taille verticale qui a ete utilisee pour afficher ce texte (utile pour afficher les prochains titres en dessous).