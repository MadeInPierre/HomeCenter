import pygame

class TimeScreen():

    def __init__(self, windowres):
        self.WindowRes = windowres # NE PAS TOUCHER
        self.ScreenStatus = "NONE" # NE PAS TOUCHER

        self.bigben_image = pygame.image.load("Images/bigben.png") # charger une image
        self.barre_laterale = pygame.Surface((100, 480)).convert_alpha()
        self.barre_laterale.fill((255, 255, 255, 120))
        self.PostTitleFont = pygame.font.Font("Fonts/HelveticaNeue-Medium.ttf", 17, bold=False)

		# chargement des images correspondant aux horloges
        self.Paris = pygame.Surface((305, 195)).convert_alpha()
        self.Paris.fill((255, 255, 255, 60))

        self.Londres = pygame.Surface((305, 195)).convert_alpha()
        self.Londres.fill((255, 255, 255, 60))

        self.Sao_paulo = pygame.Surface((305, 195)).convert_alpha()
        self.Sao_paulo.fill((255, 255, 255, 60))

        self.Sidney = pygame.Surface((305, 195)).convert_alpha()
        self.Sidney.fill((255, 255, 255, 60))

    def Update(self, InputEvents):
        pass

    def Draw(self, gameDisplay):
        gameDisplay.blit(self.bigben_image, (0, -20)) # afficher une image
        gameDisplay.blit(self.barre_laterale, (700, 0))

		# positions des differentes horloges
        gameDisplay.blit(self.Paris, (30, 30))

        gameDisplay.blit(self.Londres, (365, 30))

        gameDisplay.blit(self.Sao_paulo, (30, 255))

        gameDisplay.blit(self.Sidney, (365, 255))

		# positions des fonctionnalites
        self.AlarmeText = self.PostTitleFont.render("Alarme", True, (0, 0, 0))
        gameDisplay.blit(self.AlarmeText, (750 - self.AlarmeText.get_rect().width/ 2, 80))

        self.HorlogesText = self.PostTitleFont.render("Horloges", True, (0, 0, 0))
        gameDisplay.blit(self.HorlogesText, (750 - self.HorlogesText.get_rect().width/ 2, 180))

        self.ChronoText = self.PostTitleFont.render("Chrono", True, (0, 0, 0))
        gameDisplay.blit(self.ChronoText, (750 - self.ChronoText.get_rect().width/ 2, 280))

        self.MinuteurText = self.PostTitleFont.render("Minuteur", True, (0, 0, 0))
        gameDisplay.blit(self.MinuteurText, (750 - self.MinuteurText.get_rect().width/ 2, 380))


    def Quit(self):
        pass

    def __str__(self):
        return "SCREEN"
