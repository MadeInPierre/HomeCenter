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
        # creation des images correspondant aux horloges
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

    #ON CHARGE LES POLICES#
        self.PostTitleFont = pygame.font.Font("Fonts/HelveticaNeue-Medium.ttf", 17, bold=False)
        self.TitleFont2 = pygame.font.Font("Fonts/HelveticaNeue-UltraLight.ttf", 100)
        self.TitleFont = pygame.font.Font("Fonts/HelveticaNeue-Light.ttf", 50)


    def minuteurScreen_init(self):

    #ON CHARGE LES IMAGES#
        self.fleche1 = pygame.image.load("Images/fleche_minuteur.png").convert_alpha()
        self.fleche2 = pygame.image.load("Images/fleche2_minuteur.png").convert_alpha()
        self.bouton_start = pygame.image.load("Images/bouton_start.png").convert_alpha()
        self.tempsdonne = pygame.Surface((350, 120)).convert_alpha()
        self.tempsdonne.fill((255, 255, 255, 60))

    #ON CHARGE LES POLICES#
        self.PostTitleFont = pygame.font.Font("Fonts/HelveticaNeue-Medium.ttf", 17, bold  = False)
        self.PostTitleFont2 = pygame.font.Font("Fonts/HelveticaNeue-Medium.ttf", 50, bold = False)
        self.TitleFont3 = pygame.font.Font("Fonts/HelveticaNeue-UltraLight.ttf", 50)
       
    #ON DEFINI LES VARIABLES#
        self.chrono2 = AnimationManager() #On cree un chrono qui va compter le temps
        self.TempsDuMinuteur = 0
        self.minuteur = 0
        

    def chronoScreen_init(self):

    #ON CHARGE LES IMAGES#
        self.chrono_image = pygame.image.load("Images/chrono.png") # charger une image
        self.bouton_reset_image = pygame.image.load("Images/bouton_reset.png")
        self.bouton_start_image = pygame.image.load("Images/bouton_start.png")

    #ON CHARGE LES POLICES#
        self.PostTitleFont = pygame.font.Font("Fonts/HelveticaNeue-Medium.ttf", 17, bold=False)
        self.PostTitleFont2 = pygame.font.Font("Fonts/HelveticaNeue-Medium.ttf", 50, bold=False)
        self.PostTitleFont3 = pygame.font.Font("Fonts/HelveticaNeue-Medium.ttf", 60, bold=False)

    #ON DEFINI LES VARIABLES#
        self.pause_start = "START"
        self.chrono_start = 0
        self.chrono = AnimationManager() #On cree un chrono qui va compter le temps


    def alarmesScreen_init(self):
        pass


    #########################################################################################################################
    ##############################################  PARTIE UPDATE
    ##############################################  ##########################################################
    #########################################################################################################################
    def Update(self, InputEvents):
        
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
            self.timeScreen_update(InputEvents)
        if self.ecran == 2 :
            self.alarmesScreen_update(InputEvents)
        if self.ecran == 3 :
            self.chronoScreen_update(InputEvents)
        if self.ecran == 4 :
            self.minuteurScreen_update(InputEvents)


    def timeScreen_update(self, InputEvents):
        pass
    
    def alarmesScreen_update(self, InputEvents):
        pass
    
    def minuteurScreen_update(self, InputEvents):
        self.chrono2.Update()
        # REMARQUE le jamais oublier les "self." des qu'on utilise des
        # variables ou des fonctions.
        
        for event in InputEvents:
            if "TOUCH" in event:
                mousepos = Helpers.get_message_x_y(event)
                if Helpers.is_in_rect(mousepos, [315, 60, 50, 50]):
                    self.TempsDuMinuteur += 1
                if Helpers.is_in_rect(mousepos, [315, 260, 50, 50]):
                    self.TempsDuMinuteur -= 1
                if Helpers.is_in_rect(mousepos, [220, 330, 230, 79]):
                    self.minuteur = 1

             #QUAND ON DEMARRE LE DECOMPTE#
                   
        if self.minuteur == 1:
            self.TempsDuMinuteur = self.TempsDuMinuteur - self.chrono2.elapsed_time()

                    

    def chronoScreen_update(self, InputEvents):
        # REMARQUE le jamais oublier les "self." des qu'on utilise des
        # variables ou des fonctions.
        self.chrono.Update()
        for event in InputEvents:
            if "TOUCH" in event:
               mousepos = Helpers.get_message_x_y(event) # recupere la position ou la personne a clique
               if Helpers.is_in_rect(mousepos, [60, 300, 230, 79]):
                   if self.chrono_start == 2 :
                       self.chrono_start = 3
                       self.pause_start = "START"
                   else :
                       self.chrono_start = 2
                       self.pause_start = "PAUSE"
                       self.chrono.reset()
               if Helpers.is_in_rect(mousepos, [390, 300, 230, 79]):
                   self.chrono.reset()
                   self.LeTempsDuChrono = 0


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
        gameDisplay.blit(self.barre_laterale, (700, 0))

        if self.ecran == 1:
            self.timeScreen_draw(gameDisplay)
        if self.ecran == 2:
            self.alarmesScreen_draw(gameDisplay)
        if self.ecran == 3:
            self.chronoScreen_draw(gameDisplay)
        if self.ecran == 4:
            self.minuteurScreen_draw(gameDisplay)

        # position de la barre laterale.  On le met dans le Draw principal
        # parce que on l'affiche dans tous les ecrans de toutes
        # facons, pas besoin de le repeter 4 fois dans les sous-draws.
        self.AlarmeText = self.PostTitleFont.render("Horloges", True, (0, 0, 0))
        gameDisplay.blit(self.AlarmeText, (750 - self.AlarmeText.get_rect().width / 2, 80))

        self.HorlogesText = self.PostTitleFont.render("Alarmes", True, (0, 0, 0))
        gameDisplay.blit(self.HorlogesText, (750 - self.HorlogesText.get_rect().width / 2, 180))

        self.ChronoText = self.PostTitleFont.render("Chrono", True, (0, 0, 0))
        gameDisplay.blit(self.ChronoText, (750 - self.ChronoText.get_rect().width / 2, 280))

        self.MinuteurText = self.PostTitleFont.render("Minuteur", True, (0, 0, 0))
        gameDisplay.blit(self.MinuteurText, (750 - self.MinuteurText.get_rect().width / 2, 380))

    def timeScreen_draw(self, gameDisplay):
        # positions des differentes horloges
        gameDisplay.blit(self.Paris, (30, 30))
        
        self.paris_text = self.TitleFont.render("PARIS", True, (250, 250, 250))
        gameDisplay.blit(self.paris_text, ((30 + 305/2) -(self.paris_text.get_rect().width/2), 150)) 

        gameDisplay.blit(self.Londres, (365, 30))

        self.londres_text = self.TitleFont.render("LONDRES", True, (250, 250, 250))
        gameDisplay.blit(self.londres_text, ((365 + 305/2) -(self.londres_text.get_rect().width/2), 150))
     
        gameDisplay.blit(self.Sao_paulo, (30, 255))

        self.sao_paulo_text = self.TitleFont.render("SAO PAULO", True, (250, 250, 250))
        gameDisplay.blit(self.sao_paulo_text, ((30 + 305/2) -(self.sao_paulo_text.get_rect().width/2), 375))

        gameDisplay.blit(self.Sidney, (365, 255))

        self.sidney_text = self.TitleFont.render("SIDNEY", True, (250, 250, 250))
        gameDisplay.blit(self.sidney_text, ((365 + 305/2) -(self.sidney_text.get_rect().width/2), 375))

        self.timeSurface = self.TitleFont2.render (strftime("%H:%M"), True, (250, 250, 250))
        gameDisplay.blit(self.timeSurface, ((30 + 305/2) -(self.timeSurface.get_rect().width/2), 40))

        self.timeSurface2 = self.TitleFont2.render (strftime("%H:%M"), True, (250, 250, 250))
        gameDisplay.blit(self.timeSurface2, ((365 + 305/2) -(self.timeSurface.get_rect().width/2), 40))

        self.timeSurface3 = self.TitleFont2.render (strftime("%H:%M"), True, (250, 250, 250))
        gameDisplay.blit(self.timeSurface3, ((30 + 305/2) -(self.timeSurface.get_rect().width/2), 270))

        self.timeSurface4 = self.TitleFont2.render (strftime("%H:%M"), True, (250, 250, 250))
        gameDisplay.blit(self.timeSurface4, ((365 + 305/2) -(self.timeSurface.get_rect().width/2), 270))



    def alarmesScreen_draw(self, gameDisplay):
        pass

    def minuteurScreen_draw(self, gameDisplay):
        if self.minuteur == 0 :
            
            gameDisplay.blit(self.fleche1, (315, 60))
            gameDisplay.blit(self.fleche2, (315, 260))
            gameDisplay.blit(self.fleche1, (140, 60))
            gameDisplay.blit(self.fleche2, (140, 260))
            gameDisplay.blit(self.fleche1, (490, 60))
            gameDisplay.blit(self.fleche2, (490, 260))
            gameDisplay.blit(self.bouton_start, (220, 330))
            self.heure_text = self.TitleFont3.render("h", True, (0, 0, 0))
            gameDisplay.blit(self.heure_text, (227-((self.heure_text.get_rect().width)/2), 150))
            self.minute_text = self.TitleFont3.render("min", True, (0, 0, 0))
            gameDisplay.blit(self.minute_text, (425-((self.minute_text.get_rect().width)/2), 150))
            self.start_text = self.PostTitleFont3.render("START", True, (0, 0, 0))
            gameDisplay.blit(self.start_text, (235, 330))
            self.TempsDeDepart_text = self.PostTitleFont2.render(str(self.TempsDuMinuteur), True, (0, 0, 0))
            gameDisplay.blit(self.TempsDeDepart_text, (340-((self.TempsDeDepart_text.get_rect().width)/2), 160))

        if self.minuteur == 1 :
            self.temps_du_minuteur_text = self.PostTitleFont2.render(str(self.TempsDuMinuteur), True, (0, 0, 0))
                                    # on met des guillemets quand on veut
                                    # mettre manuellement du texte,
                                    # et on n'en met pas quand le texte vient
                                    # d'une variable, comme ici
            gameDisplay.blit(self.temps_du_minuteur_text, (200, 200))
                  # on affiche le texte une fois qu'il a ete cree (a la ligne au dessus)
            

    def chronoScreen_draw(self, gameDisplay):
        gameDisplay.blit(self.chrono_image, (275, 50))

        self.temps_text = self.PostTitleFont2.render(str(self.LeTempsDuChrono), True, (0, 0, 0))
                                    # on met des guillemets quand on veut
                                    # mettre manuellement du texte,
                                    # et on n'en met pas quand le texte vient
                                    # d'une variable, comme ici
        gameDisplay.blit(self.temps_text, (200, 200)) # on affiche le texte une fois qu'il a ete cree (a la ligne au dessus)

        gameDisplay.blit(self.bouton_start_image, (80, 300))
        gameDisplay.blit(self.bouton_reset_image, (390, 300))
        
        #self.start_text = self.PostTitleFont3.render(str(self.pause_start), True, (0, 0, 0))#
        #gameDisplay.blit(self.start_text, (270, 301))#

        self.start_text = self.PostTitleFont3.render(str(self.pause_start), True, (0, 0, 0))
        gameDisplay.blit(self.start_text, ((80 + (self.bouton_start_image.get_rect().width)/2) - ((self.start_text.get_rect().width) / 2), 301))

        self.reset_text = self.PostTitleFont3.render("RESET", True, (0, 0, 0))
        gameDisplay.blit(self.reset_text, ((390 + (self.bouton_reset_image.get_rect().width)/2) - ((self.start_text.get_rect().width) / 2), 301))

    def Quit(self):
        pass

    def __str__(self):
        return "SCREEN"
