import pygame
import math
import time
import util


class Environment:
	def __init__(self):
		self.time_font = pygame.font.SysFont('Arial', 30)
		self.bg = pygame.image.load("assets/img/grass.png")
		self.start_time = 0
		self.bg = pygame.transform.scale_by(self.bg, 5)
		pygame.mixer.init()
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

	def deathscreen(self, screen, score, old_high):
		screen.fill("black")
		win = pygame.image.load("assets/img/deathscreens/death.png")
		win_rect = win.get_rect(topleft=(0, 0))
		screen.blit(win, win_rect)
		if old_high < self.time_progressed():
			win_msg = self.time_font.render(f"You beat your high score!", True, (255, 255, 255))
			win_msg_score = self.time_font.render(f"New score: {max(util.read_highscores("scores.txt"))}", True, (255, 255, 255))
			restart_msg = self.time_font.render(f"Press space to restart", True, (255, 255, 255))
			screen.blit(win_msg, (500, 500))
			screen.blit(win_msg_score, (500, 550))
			screen.blit(restart_msg, (500, 600))
		else:
			win_msg = self.time_font.render(f"You didn't beat your high score!", True, (255, 255, 255))
			win_msg_score = self.time_font.render(f"Your score: {score}", True,
												  (255, 255, 255))
			restart_msg = self.time_font.render(f"Press space to restart", True, (255, 255, 255))
			screen.blit(win_msg, (500, 500))
			screen.blit(win_msg_score, (500, 550))
			screen.blit(restart_msg, (500, 600))
