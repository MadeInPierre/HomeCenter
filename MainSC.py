'''
This is the entry point to the SmartClock interface.
It initializes the window and manages the screens.
It also updates the main modules, like the Leap Motion module, and distributes the data to the screens.

Interface developped by Julien REBOUL, Priscille Valla and Pierre LACLAU.
'''

import pygame
from InputManager import InputManager
from HomeScreen import *
from StartScreen import *
from NewsScreen import *
from Screen import *
from TestScreen import *
from WeatherScreen import *
from AutomationScreen import *
from TimeScreen import *
from CalendarScreen import *
from LockScreen import *

'''
Initialisations principales : demarrage de pygame et du chrono qui limite le systeme a 30 FPS.
'''
pygame.init()
clock = pygame.time.Clock()

'''
Initialisation de la fenetre : definit la resolution, mode plein ecran, et titre du logiciel.
'''
WindowRes = (800, 480)
gameDisplay = pygame.display.set_mode(WindowRes)#, pygame.FULLSCREEN)
pygame.display.set_caption('HomeCenter')

'''
....
Initialisation de l'ecouteur d'entrees : prepare la classe a capturer les entrees utilisateur
(clavier, souris, leap motion, evenements pygame)
'''
Input = InputManager(use_leapmotion = False, mouse_visible = True)
home_icon = pygame.image.load("Images/home.png")

'''
Creation de deux slots qui contiendront les ecrans a afficher.
Initialisation du premier ecran (StartScreen) et d'un ecran vide (Screen) pour l'instant.
'''
global currentScreen
LockScreen = SleepManager(WindowRes)
currentScreen = HomeScreen(WindowRes) # ECRAN DE DEMARRAGE ICI
fadingScreen = Screen(WindowRes)


chrono = AnimationManager() #DEBUG FPS

gameRunning = True
while gameRunning:
        chrono.Update()
        '''
        Handles pygame events such as quitting events.
        '''
        Input.Update(pygame.event.get())
        if "QUIT" in Input.events:
            gameRunning = False
        if "HOME" in Input.events:
            currentScreen = HomeScreen(WindowRes)
        '''
        Update des ecrans actifs (currentScreen pour l'ecran actif et fadingScreen pour l'eventuel ecran qui est en
        train de faire sa transition sortante).
        '''
        #LockScreen.Update(Input.events)
        currentScreen.Update(Input.events)
        fadingScreen.Update(Input.events)


        '''
        ScreenManager : Gere la creation, destruction et organisation des ecrans, et les prepare pour la Render Zone.
        '''
        status = currentScreen.ScreenStatus
        if "FADING_OUT" in status :
            fadingScreen = currentScreen
            currentScreen = Screen(WindowRes)

        status = fadingScreen.ScreenStatus
        if status is not "RUNNING":
            if "GOTO" in status:
                if "GOTO_HOMESCREEN"  in status:
                    currentScreen = HomeScreen(WindowRes, str(fadingScreen))
                if "GOTO_STARTSCREEN" in status:
                    currentScreen = StartScreen(WindowRes)
                if "GOTO_NEWSSCREEN"  in status:
                    currentScreen = NewsScreen(WindowRes)
                if "GOTO_TIMESCREEN"  in status:
                    currentScreen = TimeScreen(WindowRes)
                if "GOTO_CALENDARSCREEN" in status:
                    currentScreen = CalendarScreen(WindowRes)
                if "GOTO_WEATHERSCREEN" in status:
                    currentScreen = WeatherScreen(WindowRes)
                if "GOTO_AUTOMATIONSCREEN" in status:
                    currentScreen = AutomationScreen(WindowRes)


                if "DEAD" in fadingScreen.ScreenStatus:
                    print "killing " + str(fadingScreen)
                    fadingScreen.Quit()
                    fadingScreen = Screen(WindowRes)
                else:
                    fadingScreen.ScreenStatus = "FADING_OUT"

        if "DEAD" in fadingScreen.ScreenStatus:
            print "killing " + str(fadingScreen)
            fadingScreen.Quit()
            fadingScreen = Screen(WindowRes)



        '''
        Render Zone : dessine tous les ecrans actifs.
        '''
        gameDisplay.fill((0, 0, 0))

        if "FADING_OUT" in fadingScreen.ScreenStatus:
            fadingScreen.Draw(gameDisplay)
        currentScreen.Draw(gameDisplay)
        #LockScreen.Draw(gameDisplay)

        if str(currentScreen) is not "HOMESCREEN":
            if str(currentScreen) is not "NEWSSCREEN": # petite exception pour NewsScreen
                gameDisplay.blit(home_icon, (0, 0))

            for event in Input.events:
                if Helpers.is_in_rect(pygame.mouse.get_pos(), [0, 0, 30, 30]):
                    currentScreen = HomeScreen(WindowRes)


        Input.EndUpdate()

        '''
        Envoie les dessins a pygame qui les affiche.
        Limite le systeme a 30 FPS pour economiser les ressources de l'ordinateur.
        '''
        pygame.display.update()
        clock.tick(30)

        #print "FPS : " + str(1/ chrono.delta_elapsed_time()) #DEBUG FPS

'''
Sortie du systeme : desinitialise pygame, les ecrans actifs et l'ecouteur d'entrees avant de quitter totalement.
'''
pygame.quit()
Input.quit()
currentScreen.Quit()
fadingScreen.Quit()
quit()
