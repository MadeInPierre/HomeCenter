import pygame
from Helpers import *
from time import strftime

class TimeScreen():
    def __init__(self, windowres):
        self.WindowRes = windowres # NE PAS TOUCHER
        self.ScreenStatus = "NONE" # NE PAS TOUCHER

        '''
        On initialise tous les ecrans, comme ca ca sera fait et peu importe lequel on choisit il sera deja charge.
        '''
        self.timeScreen_init()
        self.minuteurScreen_init()
        self.chronoScreen_init()
        self.alarmesScreen_init()

        '''
        Cette variable enregistre lequel des quatre ecrans est actif. On met 1 (soit le premier) par defaut/choix.
        '''
        self.ecran = 1
        self.LeTempsDuChrono = 0.0

    def timeScreen_init(self):
    #ON CHARGE LES IMAGES#
        '''
        On charge l'image de fond
        '''
        self.bigben_image = pygame.image.load("Images/bigben.png") # charger une image

        # creation des surfaces correspondant aux horloges
        self.Paris = pygame.Surface((305, 195)).convert_alpha()
        self.Paris.fill((255, 255, 255, 60))
        self.Londres = pygame.Surface((305, 195)).convert_alpha()
        self.Londres.fill((255, 255, 255, 60))
        self.Sao_paulo = pygame.Surface((305, 195)).convert_alpha()
        self.Sao_paulo.fill((255, 255, 255, 60))
        self.Sidney = pygame.Surface((305, 195)).convert_alpha()
        self.Sidney.fill((255, 255, 255, 60))


        '''
        On cree la barre laterale blanche qui permet de selectionner l'ecran actif, on l'affichera dans le draw.
        '''
        self.barre_laterale = pygame.Surface((100, 480)).convert_alpha()
        self.barre_laterale.fill((255, 255, 255, 120))

        # creation de la Surface qui mettra en evidence le bouton selectionné dans la barre laterale
        self.selection_surface = pygame.Surface((100, 30)).convert_alpha()
        self.selection_surface.fill((255, 255, 255, 50))

    #ON CHARGE LES POLICES#
        self.PostTitleFont = pygame.font.Font("Fonts/HelveticaNeue-Medium.ttf", 17, bold=False)
        self.TitleFont2 = pygame.font.Font("Fonts/HelveticaNeue-UltraLight.ttf", 100)
        self.TitleFont = pygame.font.Font("Fonts/HelveticaNeue-Light.ttf", 50)

    #ON CREE LES VARIABLES QUI CONTIENDRONT LES HEURES
        self.heure_sao     = ""
        self.heure_londres = ""
        self.heure_sidney  = ""
        self.heure_paris   = ""


    def minuteurScreen_init(self):

    #ON CHARGE LES IMAGES#
        self.fleche1 = pygame.image.load("Images/fleche_minuteur.png").convert_alpha()
        self.fleche2 = pygame.image.load("Images/fleche2_minuteur.png").convert_alpha()
        self.bouton_start = pygame.image.load("Images/bouton_start.png").convert_alpha()
        self.tempsdonne = pygame.Surface((350, 120)).convert_alpha()
        self.tempsdonne.fill((255, 255, 255, 60))
        self.Start_surface = pygame.Surface((230, 79)).convert_alpha()
        self.Start_surface.fill((255, 255, 255, 60))

    #ON CHARGE LES POLICES#
        self.PostTitleFont = pygame.font.Font("Fonts/HelveticaNeue-Medium.ttf", 17, bold  = False)
        self.PostTitleFont2 = pygame.font.Font("Fonts/HelveticaNeue-Medium.ttf", 50, bold = False)
        self.TitleFont3 = pygame.font.Font("Fonts/HelveticaNeue-Light.ttf", 60)
        self.TitleFont5 = pygame.font.Font("Fonts/HelveticaNeue-UltraLight.ttf", 50)
        self.TitleFont4 = pygame.font.Font("Fonts/HelveticaNeue-UltraLight.ttf", 100)

    #ON DEFINI LES VARIABLES#
        self.chrono2 = AnimationManager() #On cree un chrono qui va compter le temps
        self.TempsDuMinuteur = 0
        self.minuteur = 0
        self.redcolor = 0
        self.TempsSecondes = 0
        self.TempsHeures = 0
        self.TempsMin = 0
        self.HeuresRestantes = 0
        self.MinutesRestantes = 0
        self.SecondesRestantes = 0


    def chronoScreen_init(self):

    #ON CHARGE LES IMAGES#
        self.bouton_reset_image = pygame.image.load("Images/bouton_reset.png")
        self.bouton_start_image = pygame.image.load("Images/bouton_start.png")
        self.Start_surface = pygame.Surface((230, 79)).convert_alpha()
        self.Start_surface.fill((255, 255, 255, 60))

    #ON CHARGE LES POLICES#
        self.PostTitleFont = pygame.font.Font("Fonts/HelveticaNeue-Medium.ttf", 17, bold=False)
        self.PostTitleFont2 = pygame.font.Font("Fonts/HelveticaNeue-Medium.ttf", 50, bold=False)
        self.PostTitleFont3 = pygame.font.Font("Fonts/HelveticaNeue-Medium.ttf", 60, bold=False)
        self.PostTitleFont4 = pygame.font.Font("Fonts/HelveticaNeue-Light.ttf", 60)
        self.PostTitleFont5 = pygame.font.Font("Fonts/HelveticaNeue-UltraLight.ttf", 100)
        self.PostTitleFont6 = pygame.font.Font("Fonts/HelveticaNeue-UltraLight.ttf", 50)


    #ON DEFINI LES VARIABLES#
        self.pause_start = "START"
        self.chrono_start = 0
        self.chrono = AnimationManager() #On cree un chrono qui va compter le temps


    def alarmesScreen_init(self):
    #ON CHARGE LES POLICES#
        self.ultralight = pygame.font.Font("Fonts/HelveticaNeue-UltraLight.ttf", 40)


    #########################################################################################################################
    ##############################################  PARTIE UPDATE
    ##############################################  ##########################################################
    #########################################################################################################################
    def Update(self, InputEvents):
        #ON DEFINI LE UPDATE COMMUN#

        for event in InputEvents:
            if "TOUCH" in event:
                mousepos = Helpers.get_message_x_y(event) # recupere la position ou la personne a clique
                if Helpers.is_in_rect(mousepos, [700,  30, 100, 100]): #Coordonne x du coin en haut a gauche, coordonnee y, longueur, hauteur
                    self.ecran = 1
                if Helpers.is_in_rect(mousepos, [700, 130, 100, 100]):
                    self.ecran = 2
                if Helpers.is_in_rect(mousepos, [700, 230, 100, 100]):
                    self.ecran = 3
                if Helpers.is_in_rect(mousepos, [700, 330, 100, 100]):
                    self.ecran = 4

        if self.ecran == 1 :
            self.timeScreen_update(InputEvents) #On attribut a chaque clic dans la barre laterale le update correspondant
        if self.ecran == 2 :
            self.alarmesScreen_update(InputEvents)
        if self.ecran == 3 :
            self.chronoScreen_update(InputEvents)
        if self.ecran == 4 :
            self.minuteurScreen_update(InputEvents)


    def timeScreen_update(self, InputEvents):
        self.heure_sao = int(strftime("%H")) - 5 #On retire ou ajoute les heures du decalage horaire
        self.heure_londres = int(strftime("%H")) - 1
        self.heure_sidney = int(strftime("%H")) + 8
        self.heure_paris = int(strftime("%H")) #le strftime permet de recuperer lheure du reseau

        #ON EFFECTUE LES ARRANGEMENTS#
        if self.heure_paris < 10:                               #on affiche un 0 devant les heures a 1 chiffre
            self.heure_paris = '0' + str(self.heure_paris)      #par soucis esthetique
        if self.heure_sao < 10:
            self.heure_sao = '0' + str(self.heure_sao)
        if self.heure_sao < 0:                             #on evite en ajoutant 24h les heures négatives
            self.heure_sao += 24
        if self.heure_sao > 24:                             #on evite en ajoutant 24h les heures négatives
            self.heure_sao -= 24
        if self.heure_londres < 10:
            self.heure_londres = '0' + str(self.heure_londres)
        if self.heure_londres < 0:
            self.heure_londres += 24
        if self.heure_londres > 24:
            self.heure_londres -= 24
        if self.heure_sidney < 10:
            self.heure_sidney = '0' + str(self.heure_sidney)
        if self.heure_sidney < 0:
            self.heure_sidney += 24
        if self.heure_sidney > 24:
            self.heure_sidney -= 24


    def alarmesScreen_update(self, InputEvents):
        pass

    def minuteurScreen_update(self, InputEvents):
        self.chrono2.Update()
        # REMARQUE le jamais oublier les "self." des qu'on utilise des
        # variables ou des fonctions.
        if self.minuteur == 0:
            for event in InputEvents:
                if "TOUCH" in event:
                    mousepos = Helpers.get_message_x_y(event)
                    if Helpers.is_in_rect(mousepos, [325, 60, 50, 50]): #chaque variable heure, minute, seconde prend
                        self.TempsMin += 1                             #la valeur choisie par les clics de l'utilisateur
                    if Helpers.is_in_rect(mousepos, [325, 260, 50, 50]):
                        self.TempsMin -= 1
                    if Helpers.is_in_rect(mousepos, [125, 60, 50, 50]):
                        self.TempsHeures += 1
                    if Helpers.is_in_rect(mousepos, [125, 260, 50, 50]):
                        self.TempsHeures -= 1
                    if Helpers.is_in_rect(mousepos, [525, 60, 50, 50]):
                        self.TempsSecondes += 1
                    if Helpers.is_in_rect(mousepos, [525, 260, 50, 50]):
                        self.TempsSecondes -= 1
                    if Helpers.is_in_rect(mousepos, [200, 330, 230, 79]):
                        self.minuteur = 1

            #on ajoute ces 3 variables dans une seule qui a un temps en secondes
            self.TempsDuMinuteur = self.TempsSecondes + 60*self.TempsMin + 3600*self.TempsHeures

             #QUAND ON DEMARRE LE DECOMPTE#

        else:
            for event in InputEvents:
                if "TOUCH" in event:
                    mousepos = Helpers.get_message_x_y(event)
                    if Helpers.is_in_rect(mousepos, [235, 300, 230, 79]): #lorsqu'on appuit sur le bouton reset
                        self.minuteur = 0                                #on revient a la configuration de depart
                        self.TempsDuMinuteur = 0                  #on remet toutes les variables a 0
                        self.TempsSecondes = 0
                        self.TempsMin = 0
                        self.TempsHeures = 0
                        self.redcolor = 0


            self.TempsDuMinuteur -= self.chrono2.delta_elapsed_time() #on enleve au temps choisi par l'utilisateur le chrono
                                                                        # créé dans une autre classe

            self.HeuresRestantes = int(self.TempsDuMinuteur / 3600)    #on recupere seulement la partie entiere du temps divisé par 3600
                                                                        #ce qui revient a recuperer le nombre d'heures restantes
                                                                        #ce qui est plus pratique pour l'utilisateur


            self.MinutesRestantes = int(self.TempsDuMinuteur / 60) - (self.HeuresRestantes * 60) #pour obtenir le nombre de minutes restantes on reproduit
                                                                                                #le meme principe que pour les heures mais en retirant le nombre d'heures
                                                                                                #restantes transfere en minutes

            self.SecondesRestantes = self.TempsDuMinuteur - (self.HeuresRestantes * 3600) - (self.MinutesRestantes * 60) #meme chose en retirant les heures et minutes restantes
                                                                                                                          #converties en secondes
            if self.TempsDuMinuteur < 0:         #lorsque le temps passe au negatif le texte passe au rouge
                self.redcolor = 1




    def chronoScreen_update(self, InputEvents):
        # REMARQUE le jamais oublier les "self." des qu'on utilise des
        # variables ou des fonctions.
        self.chrono.Update()
        self.HeuresRestantes = int(self.LeTempsDuChrono / 3600)    #on recupere seulement la partie entiere du temps divisé par 3600
                                                                    #ce qui revient a recuperer le nombre d'heures restantes
                                                                    #ce qui est plus pratique pour l'utilisateur


        self.MinutesRestantes = int(self.LeTempsDuChrono / 60) - (self.HeuresRestantes * 60) #pour obtenir le nombre de minutes restantes on reproduit
                                                                                            #le meme principe que pour les heures mais en retirant le nombre d'heures
                                                                                            #restantes transfere en minutes

        self.SecondesRestantes = self.LeTempsDuChrono - (self.HeuresRestantes * 3600) - (self.MinutesRestantes * 60)

        for event in InputEvents:
            if "TOUCH" in event:
               mousepos = Helpers.get_message_x_y(event) # recupere la position ou la personne a clique
               if Helpers.is_in_rect(mousepos, [60, 300, 230, 79]):
                   if self.chrono_start == 2 :
                       self.chrono_start = 3  #le chrono est sur pause
                       self.pause_start = "START" #le bouton start pause devient start
                   else :
                       self.chrono_start = 2 #le chrono est en marche
                       self.pause_start = "PAUSE" #le bouton devient stop
                       self.chrono.reset() #le temps a ajouter repart a 0
               if Helpers.is_in_rect(mousepos, [390, 300, 230, 79]):
                   self.chrono.reset() #le temps a ajouter repart a 0
                   self.LeTempsDuChrono = 0 #le temps du chrono est a 0


        if self.chrono_start == 2 :
           self.LeTempsDuChrono += self.chrono.delta_elapsed_time()
           #on rajoute le temps qu'on a "sauvegardé" a une fonction
           #qui va continuer de faire tourner le temps


    #########################################################################################################################
    ################################################  PARTIE DRAW  ##########################################################
    #########################################################################################################################
    def Draw(self, gameDisplay):
        # on affiche le fond d'ecran.  On le met dans le Draw principal
        # puisqu'il s'affiche peu importe l'ecran
        Helpers.blit_alpha(gameDisplay, self.bigben_image, (0, -20), 200) # afficher une image avec un peu de transparence
                                                                          # pour
                                                                                                                                                   # qu'elle
                                                                                                                                                   # soit
                                                                                                                                                   # plus
                                                                                                                                                   # foncee
        gameDisplay.blit(self.barre_laterale, (700, 0)) #affichage barre laterale


        if self.ecran == 1:
            self.timeScreen_draw(gameDisplay)
            gameDisplay.blit(self.selection_surface, (700, 76))
        if self.ecran == 2:
            self.alarmesScreen_draw(gameDisplay)
            gameDisplay.blit(self.selection_surface, (700, 176))
        if self.ecran == 3:
            self.chronoScreen_draw(gameDisplay)
            gameDisplay.blit(self.selection_surface, (700, 276))
        if self.ecran == 4:
            self.minuteurScreen_draw(gameDisplay)
            gameDisplay.blit(self.selection_surface, (700, 376))


        self.AlarmeText = self.PostTitleFont.render("Horloges", True, (0, 0, 0))
        gameDisplay.blit(self.AlarmeText, (750 - self.AlarmeText.get_rect().width / 2, 80)) #on affiche tous les textes de la barre laterale

        self.HorlogesText = self.PostTitleFont.render("Alarmes", True, (0, 0, 0))
        gameDisplay.blit(self.HorlogesText, (750 - self.HorlogesText.get_rect().width / 2, 180))

        self.ChronoText = self.PostTitleFont.render("Chrono", True, (0, 0, 0))
        gameDisplay.blit(self.ChronoText, (750 - self.ChronoText.get_rect().width / 2, 280))

        self.MinuteurText = self.PostTitleFont.render("Minuteur", True, (0, 0, 0))
        gameDisplay.blit(self.MinuteurText, (750 - self.MinuteurText.get_rect().width / 2, 380))

    def timeScreen_draw(self, gameDisplay):
        # positions des differentes horloges
        gameDisplay.blit(self.Paris, (30, 30)) #surface blanche transparente

        self.paris_text = self.TitleFont.render("PARIS", True, (250, 250, 250)) #affichage du nom de chaque ville
        gameDisplay.blit(self.paris_text, ((30+(305/2)) -(self.paris_text.get_rect().width/2), 150))

        gameDisplay.blit(self.Londres, (365, 30))

        self.londres_text = self.TitleFont.render("LONDRES", True, (250, 250, 250))
        gameDisplay.blit(self.londres_text, ((365 + 305/2) -(self.londres_text.get_rect().width/2), 150))

        gameDisplay.blit(self.Sao_paulo, (30, 255))

        self.sao_paulo_text = self.TitleFont.render("SAO PAULO", True, (250, 250, 250))
        gameDisplay.blit(self.sao_paulo_text, ((30 + 305/2) -(self.sao_paulo_text.get_rect().width/2), 375))

        gameDisplay.blit(self.Sidney, (365, 255))

        self.sidney_text = self.TitleFont.render("SIDNEY", True, (250, 250, 250))
        gameDisplay.blit(self.sidney_text, ((365 + 305/2) -(self.sidney_text.get_rect().width/2), 375))

        self.timeSurface = self.TitleFont2.render (str(self.heure_paris)+strftime(":%M"), True, (250, 250, 250)) #affichage de l'heure regler dans le update et
        gameDisplay.blit(self.timeSurface, ((30 + 305/2) -(self.timeSurface.get_rect().width/2), 40))             #les minutes du reseau

        self.timeSurface2 = self.TitleFont2.render (str(self.heure_londres)+strftime(":%M"), True, (250, 250, 250))
        gameDisplay.blit(self.timeSurface2, ((365 + 305/2) -(self.timeSurface2.get_rect().width/2), 40))

        self.timeSurface3 = self.TitleFont2.render (str(self.heure_sao)+strftime(":%M"), True, (250, 250, 250))
        gameDisplay.blit(self.timeSurface3, ((30 + 305/2) -(self.timeSurface3.get_rect().width/2), 265))

        self.timeSurface4 = self.TitleFont2.render (str(self.heure_sidney)+strftime(":%M"), True, (250, 250, 250))
        gameDisplay.blit(self.timeSurface4, ((365 + 305/2) -(self.timeSurface4.get_rect().width/2), 265))


    def alarmesScreen_draw(self, gameDisplay):
        self.message = self.ultralight.render ("Prochainement disponible.", True, (250, 250, 250))
        gameDisplay.blit(self.message, (350-(self.message.get_rect().width/2), 200)) #les alarmes restent encore a developper


    def minuteurScreen_draw(self, gameDisplay):
        if self.minuteur == 0 :  #aspect du debut ou l'on peut regler le temps que l'on souhaite
            gameDisplay.blit(self.Start_surface, (350-((self.Start_surface.get_rect().width)/2), 330)) #surface transparente blanche bouton start

            #on defini toutes les fleches
            gameDisplay.blit(self.fleche1, (325, 60))
            gameDisplay.blit(self.fleche2, (325, 260))
            gameDisplay.blit(self.fleche1, (125, 60))
            gameDisplay.blit(self.fleche2, (125, 260))
            gameDisplay.blit(self.fleche1, (525, 60))
            gameDisplay.blit(self.fleche2, (525, 260))

            #affichage des textes h min s start
            self.heure_text = self.TitleFont5.render("h", True, (255, 255, 255))
            gameDisplay.blit(self.heure_text, (227-((self.heure_text.get_rect().width)/2), 163))
            self.minute_text = self.TitleFont5.render("min", True, (255, 255, 255))
            gameDisplay.blit(self.minute_text, (445-((self.minute_text.get_rect().width)/2), 163))
            self.minute_text = self.TitleFont5.render("s", True, (255, 255, 255))
            gameDisplay.blit(self.minute_text, (630-((self.minute_text.get_rect().width)/2), 163))
            self.start_text = self.TitleFont3.render("START", True, (255, 255, 255))

            #affichage des temps choisis definis par le update
            gameDisplay.blit(self.start_text, (350-((self.start_text.get_rect().width)/2), 330))
            self.Minutes_text = self.TitleFont4.render(str(self.TempsMin), True, (255, 255, 255))
            gameDisplay.blit(self.Minutes_text, (350-((self.Minutes_text.get_rect().width)/2), 120))
            self.Heures_text = self.TitleFont4.render(str(self.TempsHeures), True, (255, 255, 255))
            gameDisplay.blit(self.Heures_text, (150-((self.Heures_text.get_rect().width)/2), 120))
            self.Secondes_text = self.TitleFont4.render(str(self.TempsSecondes), True, (255, 255, 255))
            gameDisplay.blit(self.Secondes_text, (550-((self.Secondes_text.get_rect().width)/2), 120))

        if self.minuteur == 1: #lorsque le minuteur est en marche
            if self.redcolor == 0: #le texte devient rouge lorsque cette variable est egale a 1
                self.heure_text = self.TitleFont5.render("h", True, (255, 255, 255))
                gameDisplay.blit(self.heure_text, (227-((self.heure_text.get_rect().width)/2), 163))
                self.minute_text = self.TitleFont5.render("min", True, (255, 255, 255))
                gameDisplay.blit(self.minute_text, (445-((self.minute_text.get_rect().width)/2), 163))
                self.minute_text = self.TitleFont5.render("s", True, (255, 255, 255))
                gameDisplay.blit(self.minute_text, (630-((self.minute_text.get_rect().width)/2), 163))
                self.Heures_text = self.TitleFont4.render(str(int(self.HeuresRestantes)), True, (255, 255, 255))
                gameDisplay.blit(self.Heures_text, (150-((self.Heures_text.get_rect().width)/2), 120))
                self.Minutes_text = self.TitleFont4.render(str(int(self.MinutesRestantes)), True, (255, 255, 255))
                gameDisplay.blit(self.Minutes_text, (350-((self.Minutes_text.get_rect().width)/2), 120))
                self.Secondes_text = self.TitleFont4.render(str(int(self.SecondesRestantes)), True, (255, 255, 255))
                gameDisplay.blit(self.Secondes_text, (550-((self.Secondes_text.get_rect().width)/2), 120))
                self.reset_text = self.PostTitleFont4.render("RESET", True, (255, 255, 255))
            else: #le texte devient rouge car le minuteur va dans les negatifs
                self.heure_text = self.TitleFont5.render("h", True, (255, 0, 0))
                gameDisplay.blit(self.heure_text, (227-((self.heure_text.get_rect().width)/2), 163))
                self.minute_text = self.TitleFont5.render("min", True, (255, 0, 0))
                gameDisplay.blit(self.minute_text, (445-((self.minute_text.get_rect().width)/2), 163))
                self.minute_text = self.TitleFont5.render("s", True, (255, 0, 0))
                gameDisplay.blit(self.minute_text, (630-((self.minute_text.get_rect().width)/2), 163))
                self.Heures_text = self.TitleFont4.render(str(int(self.HeuresRestantes)), True, (255, 0, 0))
                gameDisplay.blit(self.Heures_text, (150-((self.Heures_text.get_rect().width)/2), 120))
                self.Minutes_text = self.TitleFont4.render(str(int(self.MinutesRestantes)), True, (255, 0, 0))
                gameDisplay.blit(self.Minutes_text, (350-((self.Minutes_text.get_rect().width)/2), 120))
                self.Secondes_text = self.TitleFont4.render(str(int(self.SecondesRestantes)), True, (255, 0, 0))
                gameDisplay.blit(self.Secondes_text, (550-((self.Secondes_text.get_rect().width)/2), 120))


            gameDisplay.blit(self.reset_text, (350-((self.reset_text.get_rect().width) / 2), 302))
            gameDisplay.blit(self.Start_surface, (350-((self.Start_surface.get_rect().width)/2), 300))



    def chronoScreen_draw(self, gameDisplay):


        self.heure_text = self.TitleFont5.render("h", True, (255, 255, 255))
        gameDisplay.blit(self.heure_text, (210-((self.heure_text.get_rect().width)/2), 163))
        self.minute_text = self.TitleFont5.render("min", True, (255, 255, 255))
        gameDisplay.blit(self.minute_text, (440-((self.minute_text.get_rect().width)/2), 163))
        self.minute_text = self.TitleFont5.render("s", True, (255, 255, 255))
        gameDisplay.blit(self.minute_text, (635-((self.minute_text.get_rect().width)/2), 163))

        gameDisplay.blit(self.Start_surface, (80, 300))
        gameDisplay.blit(self.Start_surface, (390, 300))

        self.start_text = self.PostTitleFont4.render(str(self.pause_start), True, (255, 255, 255))
        gameDisplay.blit(self.start_text, ((81 + (self.bouton_start_image.get_rect().width)/2) - ((self.start_text.get_rect().width) / 2), 302))

        self.reset_text = self.PostTitleFont4.render("RESET", True, (255, 255, 255))
        gameDisplay.blit(self.reset_text, ((391 + (self.bouton_reset_image.get_rect().width)/2) - ((self.start_text.get_rect().width) / 2), 302))


        self.Heures_text = self.TitleFont4.render(str(int(self.HeuresRestantes)), True, (255, 255, 255))
        gameDisplay.blit(self.Heures_text, (150-((self.Heures_text.get_rect().width)/2), 120))
        self.Minutes_text = self.TitleFont4.render(str(int(self.MinutesRestantes)), True, (255, 255, 255))
        gameDisplay.blit(self.Minutes_text, (350-((self.Minutes_text.get_rect().width)/2), 120))
        self.Secondes_text = self.TitleFont4.render(str(int(self.SecondesRestantes)), True, (255, 255, 255))
        gameDisplay.blit(self.Secondes_text, (550-((self.Secondes_text.get_rect().width)/2), 120))



    def Quit(self):
        pass

    def __str__(self):
        return "SCREEN"
