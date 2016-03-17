'''
InputManager.py

'''
import pygame
from Helpers import *
from TouchManager import TouchGesturesManager

class InputManager():

    def __init__(self, use_leapmotion = True, mouse_visible = False):
        self.events = []

        self.use_leapmotion = use_leapmotion
        if use_leapmotion == True:
            from LeapCardinalGestures import LeapManager
            self.leapManager = LeapManager()
            self.leapManager.initialize()

        pygame.mouse.set_visible(mouse_visible)

        self.TGM = TouchGesturesManager()


    def Update(self, pyevents):
        if self.use_leapmotion:
            self.events += self.leapManager.listener.events

        '''
        Touch gestures (swipes)
        '''
        touch_gestures = self.TGM.Update(pyevents)
        if len(touch_gestures) > 0:
            for gesture in touch_gestures:
                self.events.append(gesture)

        for event in pyevents:
            if event.type == pygame.QUIT:
                self.events.append("QUIT")
            if event.type == pygame.KEYUP:
                print "Key Up"

                if event.key == pygame.K_ESCAPE:
                    self.events.append("QUIT")

                if event.key == pygame.K_LEFT:
                    self.events.append("LEFT")
                if event.key == pygame.K_RIGHT:
                    self.events.append("RIGHT")
                if event.key == pygame.K_UP:
                    self.events.append("UP")
                if event.key == pygame.K_DOWN:
                    self.events.append("DOWN")
            if event.type == pygame.MOUSEBUTTONUP:
                mousepos = pygame.mouse.get_pos()
                # if touch_gesture is None: #TODO  touch points aren't recognized anymor because of the touch gestures
                # 	if Helpers.is_in_rect(mousepos, (200, 0, 400, 100)): #touched in the upward part
                # 		print "touch UP"
                # 		self.events.append("UP")
                # 	if Helpers.is_in_rect(mousepos, (150, 380, 500, 100)): #touched in the upward part
                # 		print "touch DOWN"
                # 		self.events.append("DOWN")
                # 	if Helpers.is_in_rect(mousepos, (0,  40, 100, 400)): #touched in the upward part
                # 		print "touch LEFT"
                # 		self.events.append("LEFT")
                # 	if Helpers.is_in_rect(mousepos, (700, 40, 100, 400)): #touched in the upward part
                # 		print "touch RIGHT"
                # 		self.events.append("RIGHT")

    def EndUpdate(self):
        '''
        Cleans the Input and LeapMotion events after letting the screens use them.
        '''
        if len(self.events) > 0:
            self.events = []

    def quit(self):
        if self.use_leapmotion:
            self.leapManager.quit()
