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

	def smooth_move(self, target_pos, speed, dt=1):
		target_x = target_pos.centerx - self.half_width
		target_y = target_pos.centery - self.half_height

		self.offset.x += (target_x - self.offset.x) * speed * dt
		self.offset.y += (target_y - self.offset.y) * speed * dt

	def new_draw(self, player_pos, dt):
		self.smooth_move(player_pos, 2, dt)

		for sprite in self.sprites():
			offset_pos = sprite.rect.topleft - self.offset
			self.screen.blit(sprite.image, offset_pos)