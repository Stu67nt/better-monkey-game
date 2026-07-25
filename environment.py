import pygame

class Environment:
	def __init__(self, clock, fps):
		self.clock = clock
		self.fps = fps
		self.frame_count = 0
		self.time_font = pygame.font.SysFont('Arial', 30)

		pygame.font.init()

	def time_progressed(self):
		return self.frame_count//self.fps

	def get_time_text(self, screen):
		return self.time_font.render(f"Time survived: {self.time_progressed()}", True, (0, 0, 0))


