import time

class AnimationManager():

	def __init__(self):
		self.start_time = time.time()

	def elapsed_time(self):
		return time.time() - self.start_time

	def reset(self):
		self.start_time = time.time()
