import pygame

class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('img/blob.png')
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.move_direction = 1  # 1= der / -1=izq
		self.move_counter = 0

	def update(self):
		self.rect.x += self.move_direction #Incrementa la posición en el eje x del rectángulo segun la direccion
		self.move_counter += 1 #Incrementa el contador de movimiento en 1 (ya sea en +1 o -1) en cada actualización
		#Este contador se utiliza para controlar cuánto tiempo el enemigo se ha movido en una dirección antes de cambiar de dirección.
		if abs(self.move_counter) > 50: #verifica si el enemigo ha estado moviéndose en una dirección durante más de 50 actualizaciones.
			self.move_direction *= -1 #invierte la dirección
			self.move_counter *= -1 #invierte el valor del contador de movimiento