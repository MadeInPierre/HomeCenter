import pygame, time, math
from time import strftime
from AnimationManager import *

class SwipeArrow():

    def __init__(self, size = 40):
        self.arrow_img = pygame.image.load("Images/arrow-UltraLight.png").convert_alpha()
        if size is not 40:
            self.arrow_img = pygame.transform.scale(self.arrow_img, (size, size))

        self.left_image  = Helpers.rotate(self.arrow_img, 0)
        self.right_image = Helpers.rotate(self.arrow_img, 180)
        self.up_image    = Helpers.rotate(self.arrow_img, 270)
        self.down_image  = Helpers.rotate(self.arrow_img, 90)

    def Update(self):
        pass

    def Draw(self, gameDisplay, position, angle, opacity=255):
        if angle is "LEFT":
            Helpers.blit_alpha(gameDisplay, self.left_image, position, opacity)
            # gameDisplay.blit(self.left_image, position)
        if angle is "RIGHT":
            Helpers.blit_alpha(gameDisplay, self.right_image, position, opacity)
            # gameDisplay.blit(self.right_image, position)
        if angle is "UP":
            Helpers.blit_alpha(gameDisplay, self.up_image, position, opacity)
            # gameDisplay.blit(self.up_image, position)
        if angle is "DOWN":
            Helpers.blit_alpha(gameDisplay, self.down_image, position, opacity)
            # gameDisplay.blit(self.down_image, position)


class Helpers():

    @staticmethod
    def rotate(image, angle):
        '''
        Redonne une image tournee selon l'angle donne.
        L'image reste centree, pas besoin de toucher a la position.
        '''
        # orig_rect = image.get_rect()
        # rot_image = pygame.transform.rotate(image, angle)
        # rot_rect = orig_rect.copy()
        # rot_rect.center = rot_image.get_rect().center
        # rot_image = rot_image.subsurface(rot_rect).copy()
        # return rot_image

        rot_image = pygame.transform.rotate(image, angle)
        return rot_image

    @staticmethod
    def blit_alpha(gameDisplay, image, position, opacity):
        '''
        Fonction qui permet de changer l'opacite des images (par exemple, rendre un texte plus ou moins visible
        pour des animations)

        MODE D'EMPLOI :
            - Importer la classe Helpers en debut de fichier avec "from Helpers import Helpers"

            - Au moment de dessiner, au lieu d'utiliser "gameDisplay.blit(<image>, (<positionX>, <positionY>))",
            utiliser "Helpers.blit_alpha(gameDisplay, <image>, (<positionX>, <positionY>), <opacite 0 a 255>)"

            - Regler l'opacite entre 0 et 255, 0 etant totalement transparent et 255 totalement visible.
        '''
        x = position[0]
        y = position[1]
        temp = pygame.Surface((image.get_width(), image.get_height())).convert()
        temp.blit(gameDisplay, (-x, -y))
        temp.blit(image, (0, 0))
        temp.set_alpha(opacity)
        gameDisplay.blit(temp, position)

    @staticmethod
    def is_in_rect(pos_to_check, rect):
        '''
        On donne une position et une zone (rect).
        La fonction redonne True si la position est dans la zone, et False si c'est le contraire.

        C'est utile pour savoir si, quand l'utilisateur clique quelque part, a bien clique sur tel ou tel bouton/icone.
        '''
        px, py = pos_to_check

        x, y, width, height = rect
        if (px >= x and px <= x + width) and (py >= y and py <= y + height):
            return True

        return False

    @staticmethod
    def get_message_x_y(message):
        args = message.split()
        return [int(args[1]), int(args[2])]

    @staticmethod
    def mathlerp(origine, destination, speed):
        value = (speed * origine) + ((1 - speed) * destination)
        return value