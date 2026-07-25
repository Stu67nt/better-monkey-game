import pygame

class Camera(pygame.sprite.Group):
	def __init__(self, screen):
		super().__init__()
		self.screen = screen
		self.offset = pygame.math.Vector2()
		self.half_width = self.screen.get_width() // 2
		self.half_height = self.screen.get_height() // 2

	def center_camera(self, player_pos):
		self.offset.x = player_pos.centerx - self.half_width
		self.offset.y = player_pos.centery - self.half_height

	def new_draw(self, player_pos):
		self.center_camera(player_pos)

		for sprite in self.sprites():
			offset_pos = sprite.rect.topleft - self.offset
			self.screen.blit(sprite.image, offset_pos)