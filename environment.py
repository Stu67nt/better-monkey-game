import pygame
import math
import time

class Environment:
	def __init__(self):
		self.time_font = pygame.font.SysFont('Arial', 30)
		self.bg = pygame.image.load("img/grass.png")
		self.start_time = 0

		pygame.font.init()

	def time_progressed(self) -> int:
		return math.floor(time.time() - self.start_time)

	def get_time_text(self, screen):
		return self.time_font.render(f"Time survived: {self.time_progressed()}", True, (0, 0, 0))

	def tileBackground(self, screen, image):
		# Shamelessly stolen from stack overflow
		screenWidth, screenHeight = screen.get_size()
		imageWidth, imageHeight = image.get_size()

		# Calculate how many tiles we need to draw in x axis and y axis
		tilesX = math.ceil(screenWidth / imageWidth)
		tilesY = math.ceil(screenHeight / imageHeight)

		# Loop over both and blit accordingly
		for x in range(tilesX):
			for y in range(tilesY):
				screen.blit(image, (x * imageWidth, y * imageHeight))

