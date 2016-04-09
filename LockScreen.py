import pygame
from AnimationManager import *
from Helpers import *

class SleepManager():
    def __init__(self, WindowRes):
        self.WindowRes = WindowRes
        self.chrono = AnimationManager()
        self.lock_screen = LockScreen(WindowRes)

        self.lockscreen_activated = False

    def Update(self, InputEvents):
        self.chrono.Update()

        for event in InputEvents:
            if "TOUCH" in event or "SCROLL" in event:
                self.chrono.reset()

        if self.chrono.elapsed_time() > 5:
            self.launch_lockscreen()
        else:
            self.unlock_lockscreen()

    def launch_lockscreen(self):
        if self.lockscreen_activated == False:
            self.lock_screen.Activate()
        self.lockscreen_activated = True

    def unlock_lockscreen(self):
        if self.lockscreen_activated == True:
            self.lock_screen.Deactivate()
        self.lockscreen_activated = False

    def Draw(self, gameDisplay):
        if self.lockscreen_activated:
            self.lock_screen.Draw(gameDisplay)








class LockScreen():
    def __init__(self, windowres):
        self.WindowRes = windowres
        self.ScreenStatus = "RUNNING"
        self.chrono = AnimationManager()

        self.TitleFont = pygame.font.Font("Fonts/HelveticaNeue-UltraLight.ttf", 88)

        self.general_transp = 0.0

    def Update(self, InputEvents):
        for event in InputEvents:
            if "TOUCH" in event:
                mousepos = pygame.mouse.get_pos()
                if Helpers.is_in_rect(mousepos, [0, 0, self.WindowRes[0] / 2, self.WindowRes[1]]):
                    pass

                if Helpers.is_in_rect(mousepos, [self.WindowRes[0], 0, self.WindowRes[0] / 2, self.WindowRes[1]]):
                    pass

        if self.ScreenStatus == "FADING_IN":
            self.general_transp = 0.0
        if self.ScreenStatus == "FADING_OUT":
            pass

    def Activate(self):
        self.chrono.reset()
        self.ScreenStatus = "FADING_IN"

    def Deactivate(self):
        self.chrono.reset()
        self.ScreenStatus = "FADING_OUT"

    def Draw(self, gameDisplay):
        '''
        On cree une surface d'affichage temporaire.
        Ceci permet de mettre de l'opacite sur toute la surface, pour obscurcir tout l'ecran
        progressivement.
        '''
        lockDisplay = pygame.Surface(self.WindowRes).convert_alpha()
        lockDisplay.blit((0, 0, 0, self.general_transp))


        f = self.TitleFont.render("Lock Screen", True, (255, 255, 255))
        lockDisplay.blit(f, (self.WindowRes[0] / 2 - f.get_rect().width / 2, self.WindowRes[1] / 2 - f.get_rect().height / 2))


        '''
        On dessine la surface temporaire sur l'ecran general pour finaliser le rendu.
        '''
        gameDisplay.blit(lockDisplay, (0, 0))



    def Quit(self):
        pass

    def __str__(self):
        return "LOCKSCREEN"
