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
from TimeScreen import *
from Screen import *
from TestScreen import *

'''
Initialize : starts the important stuff (pygame, timer)
'''
pygame.init()
clock = pygame.time.Clock()

'''
Window initialize : prepares the window (resolution, fullscreen)
'''
WindowRes = (800, 450)
gameDisplay = pygame.display.set_mode(WindowRes)#, pygame.FULLSCREEN)
pygame.display.set_caption('HomeCenter')

'''
Input initialize : Lets the program prepare to catch inputs (keyboard, mouse, leap motion, pygame events)
'''
Input = InputManager(use_leapmotion = False, mouse_visible = True)

'''
Uses 
'''
global currentScreen
currentScreen = StartScreen(WindowRes)
fadingScreen = Screen(WindowRes)

gameRunning = True
while gameRunning:
        '''
        Handles pygame events such as quitting events.
        '''
        Input.Update(pygame.event.get())
        if "QUIT" in Input.events:
            gameRunning = False

        

        '''
        Updates the screens (current for the main screen and fading for the 
        fading out animation still occuring)
        '''
        currentScreen.Update(Input.events)
        fadingScreen.Update(Input.events)



        '''
        ScreenManager : Handles the loading and unloading of screens, and gives them to the Render Zone.
        '''
        status = currentScreen.ScreenStatus
        if "FADING_OUT" in status :
            fadingScreen = currentScreen
            currentScreen = Screen(WindowRes)        

        status = fadingScreen.ScreenStatus
        if status is not "RUNNING":
            if "GOTO" in status:
                if "GOTO_HOMESCREEN" in status:
                    currentScreen = HomeScreen(WindowRes, "UP")
                if "GOTO_STARTSCREEN" in status:
                    currentScreen = StartScreen(WindowRes)
                if "GOTO_NEWSSCREEN" in status:
                    currentScreen = NewsScreen(WindowRes)
                if "GOTO_TIMESCREEN" in status:
                    currentScreen = TimeScreen(WindowRes)

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

        Input.EndUpdate()



        '''
        Render Zone : renders the active screens.
        '''
        gameDisplay.fill((0, 0, 0))

        if "FADING_OUT" in fadingScreen.ScreenStatus:
            fadingScreen.Draw(gameDisplay)

        currentScreen.Draw(gameDisplay)

        pygame.display.update()
        # print str(currentScreen) + "  " + str(fadingScreen)
        clock.tick(30)

'''
Exit : Unloads everything and closes the window.
'''
pygame.quit()
Input.quit()
currentScreen.Quit()
fadingScreen.Quit()
quit()
