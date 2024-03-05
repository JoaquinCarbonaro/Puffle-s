import pygame

class Button():
	def __init__(self, x, y, image, surface):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.clicked = False #botón no ha sido clicado previamente 
		self.surface = surface

	def draw(self):
		action = False #indicar que el botón no esta siendo clickeado

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos): #verifica si el mouse está sobre el botón.
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: #(Comprueba si el botón izquierdo del mouse está siendo presionado) and (si el botón no ha sido clicado previamente) 
				action = True #indicando que se ha realizado alguna acción
				self.clicked = True #indicar que el botón ha sido clicado

		if pygame.mouse.get_pressed()[0] == 0: #Comprueba si el botón izquierdo del mouse no está siendo presionado
			self.clicked = False #indicar que el botón no esta siendo clickeado


		#draw button
		self.surface.blit(self.image, self.rect)

		return action