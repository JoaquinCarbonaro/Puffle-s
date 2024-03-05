import pygame
from constants import *
pygame.init()
pygame.font.init()

#Configuración de la ventana del juego
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PUFFLE' S")

#define font
font = pygame.font.SysFont('Bauhaus 93', 70)
font_data = pygame.font.SysFont('Bauhaus 93', 30)
font_input = pygame.font.SysFont("Arial",30)

#Carga de imágenes
title = pygame.image.load('img/title.png')
bg_img = pygame.image.load('img/sky.png')  # imagen fondo
bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
start_img = pygame.image.load('img/start_btn.png')
ranking_back_img = pygame.image.load('img/ranking_back.png')
ranking_img = pygame.image.load('img/ranking_btn.png')
exit_img = pygame.image.load('img/exit_btn.png')
menu_img = pygame.image.load('img/menu_btn.png')
restart_img = pygame.image.load('img/restart_btn.png')  # boton restart
save_img = pygame.image.load('img/save_btn.png')

#load sounds
pygame.mixer.music.load('music/music.wav')
pygame.mixer.music.play(-1, 0.0, 5000) #loop infinito y arranca de a poco la musica
coin_fx = pygame.mixer.Sound('music/coin.wav')
coin_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound('music/jump.wav')
jump_fx.set_volume(0.5)
game_over_fx = pygame.mixer.Sound('music/game_over.wav')
game_over_fx.set_volume(0.5)

#TEMPORIZADOR
start_time = pygame.time.get_ticks()  # Tiempo en milisegundos
