import time

class AnimationManager():

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
        return self.time - self.prev_time

    def reset(self):
        self.start_time = time.time()
        self.time = 0.0
        self.prev_time = 0.0