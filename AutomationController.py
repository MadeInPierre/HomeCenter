import pygame

class AutomationController():
    def __init__(self):
        self.lamp_status = 0
        self.window_status = 0
        pass

    def Update(self):
        '''
        Lamp, window
        '''
        pass

    def setLampStatus(self, status):
        self.lamp_status = status
        '''
        Set GPIO commands
        '''
    def getLampStatus(self, status):
        return self.lamp_status

    def setWindowStatus(self, status):
        self.lamp_status = status
        '''
        Set GPIO commands
        '''
    def getWindowStatus(self, status):
        return self.window_status
