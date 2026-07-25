import pygame
import math
import time

class Environment:
	def __init__(self):
		self.time_font = pygame.font.SysFont('Arial', 30)
		self.bg = pygame.image.load("assets/img/grass.png")
		self.start_time = 0
		self.bg = pygame.transform.scale_by(self.bg, 5)

		pygame.font.init()

	def time_progressed(self) -> int:
		return math.floor(time.time() - self.start_time)

	def get_time_text(self, screen):
		return self.time_font.render(f"Time survived: {self.time_progressed()}", True, (0, 0, 0))

	def tileBackground(self, screen, image, offset):
		# Shamelessly stolen from stack overflow
		screenWidth, screenHeight = screen.get_size()
		imageWidth, imageHeight = image.get_size()

		xTileOffset, yTileOffset = (offset[0]%imageWidth, offset[1]%imageHeight)

		# Calculate how many tiles we need to draw in x axis and y axis
		tilesX = math.ceil(screenWidth / imageWidth)+1
		tilesY = math.ceil(screenHeight / imageHeight)+1

		# Loop over both and blit accordingly
		for x in range(tilesX):
			for y in range(tilesY):
				screen.blit(image, (x * imageWidth - xTileOffset, y * imageHeight - yTileOffset))

	def healthbar(self, screen, player_health):
		pygame.draw.rect(screen, (0, 0 ,0), (0, screen.get_height() - 50, screen.get_width(), 50))
		pygame.draw.rect(screen, (255, 0 ,0), (0, screen.get_height() - 50, round(screen.get_width()*(player_health/100)), 50))