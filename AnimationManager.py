import time

class AnimationManager():
    '''
    Classe qui sert de chronometre au systeme entier.
    On l'utilise partout : animations, chronometre dans TimeScreen, changements d'états après un certain temps...

    Cette classe peut donner :
        - Le temps ecoule depuis sa creation
        - Le temps ecoule depuis la derniere fois qu'on a appele la fonction reset()
        - Le temps ecoule depuis la derniere boucle qui a tourne dans le systeme
    '''
    def __init__(self):
        self.start_time = time.time()
        self.prev_time = 0.0
        self.time = 0.0

    def Update(self):
        self.prev_time = self.time
        self.time = self.elapsed_time()

    def elapsed_time(self):
        return time.time() - self.start_time

    def delta_elapsed_time(self):
        if self.time - self.prev_time != 0:
            return self.time - self.prev_time
        else:
            return 1

    def reset(self):
        self.start_time = time.time()
        self.time = 0.0
        self.prev_time = 0.0
