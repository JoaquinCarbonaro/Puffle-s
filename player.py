import pygame
from constants import *

class Player():
    def __init__(self, x, y, world, jump_fx, game_over_fx, platform_group):
        #constructor
        self.reset(x, y) 
        self.world = world
        self.jump_fx = jump_fx
        self.game_over_fx = game_over_fx
        self.platform_group = platform_group
        
    def update(self, surface, game_over):
        dx = 0  # (Delta x) se utiliza para saber cuál será la próxima posición horizontal del personaje
        dy = 0  # (Delta y) se utiliza para saber cuál será la próxima posición vertical del personaje
        col_thresh = 20 #colisión umbral
        walk_cooldown = 5  # Cada cuántas veces toco para moverse, se iteran las imágenes de animación

        if game_over == 0:  # NO perdió
            # Obtener teclas presionadas
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                self.jump_fx.play()
                self.vel_y = -15
                self.jumped = True
            if not key[pygame.K_SPACE]:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1  # Dirección = izquierda (animación)
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1  # Dirección = derecha (animación)
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                # Cuando no se toca tecla dirección, queda mirando para el último lado (animación)
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                elif self.direction == -1:
                    self.image = self.images_left[self.index]

            # Manejar animación
            if self.counter > walk_cooldown:  # Cada X veces que se toca la tecla se hace la animación de caminar
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):  # Si el nro de imagen que se debería mostrar es mayor a la cantidad que existen
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]  # Guarda la imagen (de mov.) según el index (nro de imagen que se muestra)
                elif self.direction == -1:
                    self.image = self.images_left[self.index]  # Guarda la imagen (de mov.) según el index (nro de imagen que se muestra)

            # Agregar gravedad
            '''
            Si utilizáramos una constante para la velocidad vertical, el movimiento del personaje sería constante y lineal, lo que no se sentiría tan realista. 
			Al incrementar la velocidad vertical en cada iteración del bucle, logramos una aceleración constante hacia abajo, como en la vida real. 
			Esto significa que cuanto más tiempo el personaje está en el aire, más rápido caerá, lo que crea una sensación más natural de gravedad.
            '''
            self.vel_y += 1  # Aumenta en 1 la gravedad
            if self.vel_y > 10:  # Límite velocidad vertical. Si supera 10, se limita a 10.
                self.vel_y = 10
            dy += self.vel_y  # Actualizas la posición vertical del personaje de acuerdo con la velocidad vertical.

            # Verificar colisiones
            self.in_air = True
            for tile in self.world.tile_list:
                # Verificar colisión en dirección x
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0  # Significa que el jugador no puede moverse más en esa dirección
                # Verificar colisión en dirección y
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # Verificar si está debajo del suelo (saltando)
                    '''
                    #.top: Este atributo se refiere a la coordenada vertical del borde superior del rectángulo.
					#.bottom: Este atributo se refiere a la coordenada vertical del borde inferior del rectángulo.
                    '''
                    if self.vel_y < 0:  #moviendo hacia arriba (velocidad vertical self.vel_y es negativa)
                        dy = tile[1].bottom - self.rect.top  # Ajusta la posición vertical dy para que el jugador choque en la parte inferior del mosaico
                        self.vel_y = 0  # El jugador ha dejado de saltar.
                    # Verificar si está encima del suelo (cayendo)
                    elif self.vel_y >= 0:  #si se mueve hacia abajo o esta quieto
                        dy = tile[1].top - self.rect.bottom  # Ajusta la posición vertical dy para que el jugador esté justo por encima del mosaico
                        self.vel_y = 0  # Establece la velocidad vertical en 0. Evita que el jugador continúe cayendo a través del mosaico.
                        self.in_air = False

            # Verificar colisión con enemigos
            if pygame.sprite.spritecollide(self, self.world.blob_group, False):
                game_over = -1
                self.game_over_fx.play()

            # Verificar colisión con lava
            if pygame.sprite.spritecollide(self, self.world.lava_group, False):
                game_over = -1
                self.game_over_fx.play()

            #check for collision with door
            if pygame.sprite.spritecollide(self, self.world.door_group, False):
                game_over = 1

            #check for collision with platforms
            for platform in self.platform_group:
				#collision in the x direction
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
				#collision in the y direction
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					#check if below platform
                    if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top
					#check if above platform
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
                        self.rect.bottom = platform.rect.top - 1
                        self.in_air = False
                        dy = 0
					#move sideways with the platform
                    if platform.move_x != 0:
                        self.rect.x += platform.move_direction

            # Actualizar coordenadas del jugador
            self.rect.x += dx  # Se pasa el valor delta de movimiento en x al movimiento real del rectángulo
            self.rect.y += dy  # Se pasa el valor delta de movimiento en y al movimiento real del rectángulo

        elif game_over == -1:  # Perdió
            self.image = self.dead_image
            if self.rect.y > 50:  # Sube el fantasma hasta arriba de la pantalla
                self.rect.y -= 5

        # Dibujar jugador en la pantalla
        surface.blit(self.image, self.rect)
        if DEBUG:
            pygame.draw.rect(surface, WHITE, self.rect, 2)  # Rectángulo de "colisión" de la imagen (2=grosor del marco del rectángulo)
        
        return game_over

    def reset(self, x, y):
        # Variables
        self.images_right = []
        self.images_left = []
        self.index = 0  # Nro de imagen que se muestra (animacion)
        self.counter = 0  # Contador de veces se mueve hacia algún lado (sirve para animación)

        # Constructores
        for num in range(1, 9):  # Son 8 imágenes (este for solo se itera una vez por estar en el constructor)
            img_right = pygame.image.load(f'img/player/{num}.png')  # f'{num}= hace que varíe según la iteración
            img_right = pygame.transform.scale(img_right, (50, 50))  # Tamaño del player
            img_left = pygame.transform.flip(img_right, True, False)  # Doy vuelta la imagen (camina hacia izquierda)
            self.images_right.append(img_right)  # Guardo cada imagen en la lista
            self.images_left.append(img_left)
        
        self.dead_image = pygame.image.load('img/ghost.png')
        self.image = self.images_right[self.index]  # Guarda la imagen (de la lista) según el index (nro de imagen que se muestra)
        self.rect = self.image.get_rect()  # Rect del player (imagen)
        self.rect.x = x  # Manejo del eje x del rect
        self.rect.y = y  # Manejo del eje y del rect
        self.width = self.image.get_width()  # Obtengo el ancho de la imagen
        self.height = self.image.get_height()  # Obtengo el alto de la imagen
        self.vel_y = 0  # Variable que representa la velocidad vertical del personaje
        self.jumped = False
        self.direction = 0  # Dirección que mira el personaje (-1=izquierda)(1=derecha)
        self.in_air = True