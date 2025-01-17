import pygame
from constants import *

class Lava(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/lava.png')
		self.image = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE // 2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y