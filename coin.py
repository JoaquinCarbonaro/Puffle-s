import pygame
from constants import *

class Coin(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/coin.png')
		self.image = pygame.transform.scale(img, (TILE_SIZE // 2, TILE_SIZE // 2))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)