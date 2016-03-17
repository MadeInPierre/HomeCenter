import pygame
from AnimationManager import *

class TimerScreen():

    def __init__(self, windowres):
        self.WindowRes = windowres
        self.ScreenStatus = "NONE"

        self.bigben_image = pygame.image.load("Images/bigben.png") # charger une image
        self.barre_laterale = pygame.Surface((100, 480)).convert_alpha()
        self.barre_laterale.fill((255, 255, 255, 120))
        self.PostTitleFont = pygame.font.Font("Fonts/HelveticaNeue-Medium.ttf", 17, bold=False)
        self.PostTitleFont2 = pygame.font.Font("Fonts/HelveticaNeue-Medium.ttf", 50, bold=False)
        self.chrono = AnimationManager() #On cree un chrono qui va compter le temps


    def Update(self, ImputEvents):
        # REMARQUE le jamais oublier les "self." des qu'on utilise des variables ou des fonctions.
        self.LeTempsDuChrono = self.chrono.elapsed_time() # on demande au chrono combien de temps s'est ecoule
                                                          # et on l'enregistre dans LeTempsDuChrono
        self.TempsRestant = 30 - self.LeTempsDuChrono # On calcule, pour le timer, combien de temps il reste si on avait 30
                                                 # secondes.

    def Draw(self, gameDisplay):
        gameDisplay.blit(self.bigben_image, (0, -20)) # afficher une image
        gameDisplay.blit(self.barre_laterale, (700, 0))


        self.AlarmeText = self.PostTitleFont.render("Alarme", True, (0, 0, 0))
        gameDisplay.blit(self.AlarmeText, (750 - self.AlarmeText.get_rect().width/ 2, 80))

        self.HorlogesText = self.PostTitleFont.render("Horloges", True, (0, 0, 0))
        gameDisplay.blit(self.HorlogesText, (750 - self.HorlogesText.get_rect().width/ 2, 180))

        self.ChronoText = self.PostTitleFont.render("Chrono", True, (0, 0, 0))
        gameDisplay.blit(self.ChronoText, (750 - self.ChronoText.get_rect().width/ 2, 280))

        self.MinuteurText = self.PostTitleFont.render("Minuteur", True, (0, 0, 0))
        gameDisplay.blit(self.MinuteurText, (750 - self.MinuteurText.get_rect().width/ 2, 380))


        self.temps_restant_text = self.PostTitleFont2.render(str(self.TempsRestant), True, (0, 0, 0))
                                    # on met des guillemets quand on veut mettre manuellement du texte,
                                    # et on  n'en met pas quand le texte vient d'une variable, comme ici
        gameDisplay.blit(self.temps_restant_text, (200, 200)) # on affiche le texte une fois qu'il a ete cree (a la ligne au dessus)


    def Quit(self):
        pass

    def __str__(self):
        return "SCREEN"
