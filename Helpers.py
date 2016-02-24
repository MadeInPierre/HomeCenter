import pygame, time, math
from time import strftime
from AnimationManager import *

class SwipeArrow():
    
    def __init__(self, orientation, is_animated, size = 40):
        self.orientation = orientation
        self.is_animated = is_animated

        self.arrow_img = pygame.image.load("Images/arrow-UltraLight.png").convert_alpha()
        if size is not 40:
            self.arrow_img = pygame.transform.scale(self.arrow_img, (size, size))

        self.left_image  = Helpers.rotate(self.arrow_img, 0)
        self.right_image = Helpers.rotate(self.arrow_img, 180)
        self.up_image    = Helpers.rotate(self.arrow_img, 270)
        self.down_image  = Helpers.rotate(self.arrow_img, 90)

    def Update(self):
        if self.is_animated:
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
        """rotate an image while keeping its center and size"""
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
        x = position[0]
        y = position[1]
        temp = pygame.Surface((image.get_width(), image.get_height())).convert()
        temp.blit(gameDisplay, (-x, -y))
        temp.blit(image, (0, 0))
        temp.set_alpha(opacity)        
        gameDisplay.blit(temp, position)

    @staticmethod
    def is_in_rect(pos_to_check, rect):
        px, py = pos_to_check

        x, y, width, height = rect
        if (px >= x and px <= x + width) and \
           (py >= y and py <= y + height):
                return True

        return False