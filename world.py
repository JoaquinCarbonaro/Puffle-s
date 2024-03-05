import pygame
from constants import *
from enemy import Enemy
from lava import Lava
from door import Door
from coin import Coin
from platform_move import Platform

class World():
	def __init__(self, word_data, blob_group, lava_group, door_group, coin_group, platform_group) -> None:
		self.tile_list = [] #creo lista de mosaicos
		self.blob_group = blob_group  # asigno blob_group como atributo de la clase
		self.lava_group = lava_group
		self.door_group = door_group
		self.coin_group = coin_group
		self.platform_group = platform_group

		#load images
		dirt_img = pygame.image.load('img/dirt.png') #imagen tierra
		grass_img = pygame.image.load('img/grass.png') #imagen pasto

		row_count = 0 #contador de filas
		for row in word_data:
			col_count = 0 #contador de columnas
			for tile in row:
				if tile == 1:
					img = pygame.transform.scale(dirt_img, (TILE_SIZE, TILE_SIZE)) #esacala de imagen(mosaico) = escala de mosaico
					img_rect = img.get_rect() #rectangulo de imagen
					img_rect.x = col_count * TILE_SIZE #contador de columna * tamño de mosaico
					img_rect.y = row_count * TILE_SIZE
					tile = (img, img_rect) #guardo como tupla la pos x=img, y=rect
					self.tile_list.append(tile) #agrego a la lista la tupla que representa ese mosaico
				if tile == 2:
					img = pygame.transform.scale(grass_img, (TILE_SIZE, TILE_SIZE))
					img_rect = img.get_rect()
					img_rect.x = col_count * TILE_SIZE
					img_rect.y = row_count * TILE_SIZE
					tile = (img, img_rect) #imagen(png)-rectangulo de la imagen(rect de colision)
					self.tile_list.append(tile)
				if tile == 3:
					blob = Enemy(col_count * TILE_SIZE, row_count * TILE_SIZE + 15) #argumentos (x,y)
					#(x=contador de columnas * tamaño de mosaico)
					#(y=contador de filas * tamaño de mosaico + 15 (desplazamiento hacia abajo para ajustar al enemigo al piso))
					self.blob_group.add(blob) #agrego al enemigo a la "lista" de sprite
				if tile == 4:
					platform = Platform(col_count * TILE_SIZE, row_count * TILE_SIZE, 1, 0)
					self.platform_group.add(platform)
				if tile == 5:
					platform = Platform(col_count * TILE_SIZE, row_count * TILE_SIZE, 0, 1)
					self.platform_group.add(platform)
				if tile == 6:
					lava = Lava(col_count * TILE_SIZE, row_count * TILE_SIZE + (TILE_SIZE // 2)) #misma logica que el title == 3
					self.lava_group.add(lava)
				if tile == 7:
					coin = Coin(col_count * TILE_SIZE + (TILE_SIZE // 2), row_count * TILE_SIZE + (TILE_SIZE // 2))
					self.coin_group.add(coin)
				if tile == 8:
					exit = Door(col_count * TILE_SIZE, row_count * TILE_SIZE - (TILE_SIZE // 2))
					self.door_group.add(exit)
				col_count += 1
			row_count += 1

	def draw(self,surface):
		for tile in self.tile_list:
			surface.blit(tile[0], tile[1]) #tile[0]=imagen, tile[1]=rect.de la imagen
			if DEBUG:
				pygame.draw.rect(surface, WHITE, tile[1], 2)
