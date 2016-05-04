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
        if self.lock_screen.ScreenStatus is not "OUT":
            self.lock_screen.Update(InputEvents)

        for event in InputEvents:
            if "TOUCH" in event or "SCROLL" in event:
                self.chrono.reset()


        if self.chrono.elapsed_time() > 2 and self.lock_screen.ScreenStatus is "OUT":
            self.launch_lockscreen()
        else:
            self.unlock_lockscreen()

        if "RESET" in self.lock_screen.ScreenStatus:
            self.lock_screen = LockScreen(self.WindowRes)
            self.chrono.reset()
            self.lockscreen_activated = False


    def launch_lockscreen(self):
        if self.lockscreen_activated == False:
            self.lock_screen = LockScreen(self.WindowRes)
            self.lock_screen.Activate()
        self.lockscreen_activated = True

    def unlock_lockscreen(self):
        if self.lockscreen_activated == True:
            pass#self.lock_screen.Deactivate()
        self.lockscreen_activated = False

    def Draw(self, gameDisplay):
        if self.lock_screen.ScreenStatus != "OUT":
            self.lock_screen.Draw(gameDisplay)




'''--------------------------------------------------------------------------------------------------------------------------------------'''
'''--------------------------------------------------------------------------------------------------------------------------------------'''
'''--------------------------------------------------------------------------------------------------------------------------------------'''
'''------------------------------------------------------- LOCK SCREEN APPLICATION ------------------------------------------------------'''
'''--------------------------------------------------------------------------------------------------------------------------------------'''
'''--------------------------------------------------------------------------------------------------------------------------------------'''


class LockScreen():
    def __init__(self, windowres):
        self.WindowRes = windowres
        self.ScreenStatus = "OUT"
        self.chrono = AnimationManager()

        self.Locked = True
        self.InputCode = ""
        self.SecretCode = "1234"

        self.PannelsStatus = "SLEEP" # SLEEP pour afficher l'ecran noir, LOCK pour le deverrouillage

        self.TitleFont       = pygame.font.Font("Fonts/HelveticaNeue-UltraLight.ttf", 88)
        self.TimeFont        = pygame.font.Font("Fonts/HelveticaNeue-UltraLight.ttf", 180)
        self.SecondsFont     = pygame.font.Font("Fonts/HelveticaNeue-UltraLight.ttf", 80 )
        self.DateFont        = pygame.font.Font("Fonts/HelveticaNeue-Light.ttf",      25 )
        self.SwipeFont       = pygame.font.Font("Fonts/HelveticaNeue-Light.ttf",      20 )
        self.WarningFont     = pygame.font.Font("Fonts/HelveticaNeue-Medium.ttf",      12 )

        self.bg          = pygame.image.load("Images/lock_bg1.png")
        self.numbers_imgs = [   pygame.image.load("Images/Numbers/zero.png" ),
                                pygame.image.load("Images/Numbers/one.png"  ),
                                pygame.image.load("Images/Numbers/two.png"  ),
                                pygame.image.load("Images/Numbers/three.png"),
                                pygame.image.load("Images/Numbers/four.png" ),
                                pygame.image.load("Images/Numbers/five.png" ),
                                pygame.image.load("Images/Numbers/six.png"  ),
                                pygame.image.load("Images/Numbers/seven.png"),
                                pygame.image.load("Images/Numbers/eight.png"),
                                pygame.image.load("Images/Numbers/nine.png" ),
                                pygame.image.load("Images/Numbers/back.png" )  ]

        self.chrono_warningbanner = AnimationManager()
        self.show_warningbanner = False

        self.general_transp = 0.0
        self.time_color = 0.0
        self.date_color = 0.0
        self.swipe_color = 0.0
        self.bg_transp = 0.0
        self.keypad_transp = 0.0
        self.warning_transp = 0.0

    def Update(self, InputEvents):
        print self.ScreenStatus + "   " + self.PannelsStatus
        for event in InputEvents:
            if "TOUCH" in event:
                mousepos = pygame.mouse.get_pos()
                if self.PannelsStatus is "SLEEP":
                    self.PannelsStatus = "SLEEPTOLOCK"
                    self.chrono.reset()
                if self.PannelsStatus is "LOCK":
                    '''
                    On regarde si on a clique sur une des touches. Si oui on verifie si le nouveau code est bon, etc.
                    '''
                    for line in range(3):
                        for column in range(3):
                            if Helpers.is_in_rect(mousepos, [self.WindowRes[0] / 2 - 200 / 2 + column * 80,
                                                             self.WindowRes[1] / 2 - 280 / 2 + line * 80 + 50, 40, 40]): # touche 0
                                i = column + line * 3 + 1
                                print "TOUCHE : " + str(i) # DEBUG


                                self.InputCode += str(i)
                                if self.InputCode == self.SecretCode:
                                    self.Locked = False
                                elif self.InputCode != self.SecretCode and len(self.InputCode) == 4:
                                    self.InputCode = ""
                                    self.show_warningbanner = True
                                    self.chrono_warningbanner.reset()
                    '''
                    Meme chose si on clique sur la touche 0
                    '''
                    if Helpers.is_in_rect(mousepos, [self.WindowRes[0] / 2 - 200 / 2 + 1 * 80,
                                                     self.WindowRes[1] / 2 - 280 / 2 + 3 * 80 + 50, 40, 40]): # touche 1
                        self.InputCode += '0'

                        if self.InputCode == self.SecretCode:
                            self.Locked = False
                        elif self.InputCode != self.SecretCode and len(self.InputCode) == 4:
                            self.InputCode = ""
                            self.show_warningbanner = True
                            self.chrono_warningbanner.reset()


                    '''
                    Si on clique sur le bouton pour supprimer le dernier chiffre qu'on vient d'entrer,
                    on enleve le dernier chiffre du code qui est en train d'etre entre.
                    '''
                    if Helpers.is_in_rect(mousepos, [500, 73, 20, 20]):
                        try:
                            self.InputCode = self.InputCode[0: len(self.InputCode) - 1]
                        except:
                            self.InputCode = "" # si l'utilisateur demande d'effacer alors que rien n'est entre encore, on gere l'erreur.


        if self.ScreenStatus == "RUNNING":
            self.swipe_color = 120 + 40 * math.sin(1 * self.chrono.elapsed_time())

        if self.ScreenStatus == "FADING_IN":
            if self.chrono.elapsed_time() > 0 and self.chrono.elapsed_time() < 2:
                self.general_transp = 255 / (1 + math.exp(-(self.chrono.elapsed_time() - 1) / 0.2))
            if self.chrono.elapsed_time() > 2 and self.chrono.elapsed_time() < 10:
                self.time_color = 160 / (1 + math.exp(-(self.chrono.elapsed_time() - 4.5) / 0.5))
                self.date_color = 160 / (1 + math.exp(-(self.chrono.elapsed_time() - 7) / 0.3))
            if self.chrono.elapsed_time() > 6 and self.chrono.elapsed_time() < 10:
                self.swipe_color = 130 / (1 + math.exp(-(self.chrono.elapsed_time() - 8) / 0.4))

            if self.chrono.elapsed_time() > 10:
                self.ScreenStatus = "RUNNING"
                self.chrono.reset()

        if self.ScreenStatus == "FADING_OUT":
            if self.chrono.elapsed_time() > 0:
                self.ScreenStatus = "OUT"
                self.date_color  = 0
                self.swipe_color = 0
                self.time_color  = 0

        if self.PannelsStatus == "SLEEPTOLOCK":
            if self.chrono.elapsed_time() > 0 and self.chrono.elapsed_time() < 2:
                self.general_transp = 255 / (1 + math.exp(-(1 - self.chrono.elapsed_time()) / 0.2))
                self.time_color     = 160 / (1 + math.exp(-(1 - self.chrono.elapsed_time()) / 0.2))
                self.date_color     = 160 / (1 + math.exp(-(1 - self.chrono.elapsed_time()) / 0.2))
                self.swipe_color    = 130 / (1 + math.exp(-(1 - self.chrono.elapsed_time()) / 0.2))
                self.bg_transp      = 100 / (1 + math.exp(-(self.chrono.elapsed_time() - 1) / 0.2))

            if self.chrono.elapsed_time() > 2:
                self.PannelsStatus = "LOCK_FADING_IN"
                self.chrono.reset()

        if self.PannelsStatus == "LOCK_FADING_IN":
            self.keypad_transp  = 255 / (1 + math.exp(-(self.chrono.elapsed_time() - 1) / 0.2))
            self.warning_transp = 255 / (1 + math.exp(-(self.chrono.elapsed_time() - 1) / 0.2))

            if self.chrono.elapsed_time() > 3:
                self.PannelsStatus = "LOCK"
                self.chrono.reset()



        if self.PannelsStatus == "LOCK":
            if self.Locked == False:
                self.Deactivate()


    def Activate(self):
        self.chrono.reset()
        self.ScreenStatus = "FADING_IN"

    def Deactivate(self):
        self.chrono.reset()
        self.ScreenStatus = "RESET"
        self.PannelsStatus = "INACTIVE"

    def Reset(self):
        self.ScreenStatus = "OUT"
        self.PannelsStatus = "SLEEP"

    def Draw(self, gameDisplay):
        '''
        On cree une surface d'affichage temporaire.
        Ceci permet de mettre de l'opacite sur toute la surface, pour obscurcir tout l'ecran
        progressivement.
        '''
        black = pygame.Surface(self.WindowRes).convert_alpha()
        if self.PannelsStatus == "SLEEP":
            black.fill((0, 0, 0, self.general_transp))
            gameDisplay.blit(black, (0, 0))
        else:
            black.fill((0, 0, 0))
            gameDisplay.blit(black, (0, 0))
            Helpers.blit_alpha(gameDisplay, self.bg, (0, 0), self.bg_transp)

        '''
        --------------------------------------------------- PARTIE SLEEP -------------------------------------------------------
        '''
        if self.PannelsStatus == "SLEEP":
            '''
            Renders the Date and Time (date, Hours+Minutes, Seconds)
            '''
            timeSurface    = self.TimeFont.render   (strftime("%H:%M"), True, (255, 255, 255))
            secondsSurface = self.SecondsFont.render(strftime(":%S"), True, (255, 255, 255))
            dateSurface    = self.DateFont.render   ("Today is " + strftime("%A %d, %B %Y"), True, (255, 255, 255))

            '''
            Rendu du texte qui demande de cliquer.
            '''
            swipeSurface = self.SwipeFont.render(u"Tapez pour déverrouiller", True, (255, 255, 255))

            '''
            Calculs de positions pour simplifier les blit() en bas
            '''
            secondsWidth = self.SecondsFont.render(strftime(":00"), True, (255, 255, 255)).get_rect().width
            timePos = self.WindowRes[0] / 2 - (timeSurface.get_rect().width + secondsWidth) / 2

            '''
            On dessine tout, avec transparence
            '''
            # on dessine l'heure
            Helpers.blit_alpha(gameDisplay, timeSurface,    (timePos,
                                                             self.WindowRes[1] / 2 - timeSurface.get_rect().height/2 - 60),
                                                             self.time_color)

            # on dessine les secondes
            Helpers.blit_alpha(gameDisplay, secondsSurface, (timePos + timeSurface.get_rect().width,
                                                             timeSurface.get_rect().bottom - timeSurface.get_rect().height * 1/5 + 5),
                                                             self.time_color)

            # on dessine la date situee sous l'heure
            Helpers.blit_alpha(gameDisplay, dateSurface,    (self.WindowRes[0] / 2 - dateSurface.get_rect().width/2,
                                                             self.WindowRes[1] / 2 - dateSurface.get_rect().height/2 + 28),
                                                             self.time_color)

            # on dessine la ligne qui demande de cliquer pour deverrouiller
            Helpers.blit_alpha(gameDisplay, swipeSurface,   (self.WindowRes[0] / 2 - swipeSurface.get_rect().width / 2,
                                                             self.WindowRes[1] - 70),
                                                             self.swipe_color)

        '''
        ---------------------------------------------------- PARTIE LOCK -------------------------------------------------------
        '''
        if self.PannelsStatus == "LOCK" or self.PannelsStatus == "LOCK_FADING_IN":
            s = pygame.Surface((40, 40))
            s.fill((255, 255, 255))

            count = 1
            for line in range(3):
                for column in range(3):
                    Helpers.blit_alpha(gameDisplay, self.numbers_imgs[count], (self.WindowRes[0] / 2 - 200 / 2 + column * 80,
                                                                               self.WindowRes[1] / 2 - 280 / 2 + line * 80 + 50), self.keypad_transp)

                    count += 1

            Helpers.blit_alpha(gameDisplay, self.numbers_imgs[0],  (self.WindowRes[0] / 2 - 200 / 2 + 1 * 80, # touche 0
                                                                    self.WindowRes[1] / 2 - 280 / 2 + 3 * 80 + 50), self.keypad_transp)
            Helpers.blit_alpha(gameDisplay, self.numbers_imgs[10], (self.WindowRes[0] / 2 - 200 / 2 + 2 * 80, # touche backspace
                                                                    self.WindowRes[1] / 2 - 280 / 2 + 3 * 80 + 50), self.keypad_transp)

            s = pygame.Surface((15, 15))
            for i in range(4):
                if len(self.InputCode) > i:
                    s.fill((255, 255, 255))
                else:
                    s.fill((60, 60, 60))
                Helpers.blit_alpha(gameDisplay, s, (self.WindowRes[0] / 2 - 15 / 2 - 68 + i * 45, 76), self.keypad_transp)

            self.WarningBanner_Update(gameDisplay)

    def WarningBanner_Update(self, gameDisplay):
        if self.show_warningbanner:
            text = self.WarningFont.render(u"Code erroné. Veuillez Réessayer.", True, (255, 0, 0))
            Helpers.blit_alpha(gameDisplay, text, (self.WindowRes[0] / 2 - text.get_rect().width / 2, 45), self.warning_transp)

            if self.chrono_warningbanner.elapsed_time() > 2.5:
                self.show_warningbanner = False
        else:
            text = self.WarningFont.render(u"Entrez votre code pour déverrouiller.", True, (255, 255, 255))
            Helpers.blit_alpha(gameDisplay, text, (self.WindowRes[0] / 2 - text.get_rect().width / 2, 45), self.warning_transp)


    def Quit(self):
        pass

    def __str__(self):
        return "LOCKSCREEN"