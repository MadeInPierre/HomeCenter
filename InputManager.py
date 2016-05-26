import pygame
from Helpers import *
from TouchManager import TouchGesturesManager

class InputManager():
    '''
    Classe qui s'occupe de recuperer, trier, classer, transforme et distribuer toutes
    les entrees utilisateur : clavier, souris, tactile, Leap Motion (qui n'est plus utilise aujourd'hui).
    '''
    def __init__(self, use_leapmotion = True, mouse_visible = False):
        self.events = []

        '''
        Code qui n'est plus utilise : avant, on pouvait utiliser un Leap Montion comme entree utilisateur.
        Nous avons cependant plus tard choisi le tactile : le code est toujours la, mais nous ne
        l'utilisons plus.
        '''
        self.use_leapmotion = use_leapmotion
        if use_leapmotion == True:
            from LeapCardinalGestures import LeapManager
            self.leapManager = LeapManager()
            self.leapManager.initialize()

        pygame.mouse.set_visible(mouse_visible)

        '''
        Classe qui s'occupe exclusivement du tactile : reconnait les clics, les glissers, les scrolls.
        Les met en forme (transformation en messages distribuables a tous les ecrans du systeme), et
        les passe a cette classe pour que celle-ci les donne au MainSC.
        '''
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

        '''
        Recuperation des evenements du clavier et mise en forme pour les messages systeme.
        '''
        for event in pyevents:
            if event.type == pygame.QUIT:
                self.events.append("QUIT")
            if event.type == pygame.KEYUP:
                print "Key Up"

                if event.key == pygame.K_ESCAPE:
                    self.events.append("QUIT")
                if event.key == pygame.K_h:
                    self.events.append("HOME")

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
        A la fin de chaque boucle, le MainSC appelle cette fonction. Celle ci vide les evenements qui ont
        eu lieu durant cette boucle pour preparer la prochaine.
        '''
        if len(self.events) > 0:
            self.events = []

    def quit(self):
        '''
        Extinction du systeme necessite la fermeture du service Leap Motion.
        '''
        if self.use_leapmotion:
            self.leapManager.quit()
