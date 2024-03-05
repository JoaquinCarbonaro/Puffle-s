import pygame
from constants import *
from button import Button
from functions import *
from data import *

#Inicialización de Pygame
pygame.init()

# se crea "listas" de sprite
blob_group = pygame.sprite.Group()  
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()

# Creación de instancias del juego
world, player = reset_level(level, jump_fx, game_over_fx, blob_group, platform_group, coin_group, lava_group, door_group) 

#Creación de botones
start_button = Button(SCREEN_WIDTH // 2 - 200, 610, start_img, screen)
ranking_button = Button(SCREEN_WIDTH // 2 - 200, 610 + (120 + 15), ranking_img, screen)
exit_button = Button(SCREEN_WIDTH // 2 - 200, 610 + ((120*2) + (15*2)), exit_img, screen)
menu_button = Button(50,50, menu_img, screen)
save_button = Button(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + (125 + 41.5), save_img, screen)
restart_button = Button(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + ((125*2) + (41.5*2)), restart_img, screen)

#read ranking
ranking = read_data("data_juego.json")

#Bucle principal del juego
run = True
while run:
    clock.tick(FPS)
    screen.blit(bg_img, (0, 0))  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                ingreso = ingreso[0:-1]
            elif event.key == pygame.K_RETURN:
                name = ingreso
            else:
                ingreso += event.unicode #devuelve la tecla presionada en str 

    ###MENU###
    if main_menu:
        screen.blit(title, (SCREEN_WIDTH // 2 - 350, 200))

        mensaje_img = font_input.render(mensaje,True,WHITE)
        screen.blit(mensaje_img,(105,500))
        
        pygame.draw.rect(screen,WHITE, pygame.Rect(300,540,400,50), 4)
        font_input_surface = font_input.render(ingreso,True,WHITE)
        screen.blit(font_input_surface,(307,547))

        if exit_button.draw():  # devuelve (y entra) true cuando es presionado
            run = False  # deja de entrar al while del juego
        if ranking_button.draw():
            main_menu = False
            mostrar_ranking = True
        if start_button.draw():
            level = 1
            main_menu = False
            mostrar_juego = True
                
    ###RANKING###
    elif mostrar_ranking:
        screen.blit(ranking_back_img,(130,200))
        for i in range(len(ranking)):
            texto_name = font_data.render(ranking[i]["name"], True, WHITE)
            screen.blit(texto_name, (200, 320 + i * 60))

            texto_time = font_data.render(str(ranking[i]["time"]), True, WHITE)
            screen.blit(texto_time, (455, 320 + i * 60))

            texto_score = font_data.render(str(ranking[i]["score"]), True, WHITE)
            screen.blit(texto_score, (670, 320 + i * 60))
        if menu_button.draw():
            mostrar_ranking = False
            main_menu = True

    ###JUEGO###
    elif mostrar_juego:  #  se dibuja el mundo y se actualizan y dibujan los sprites 
        world.draw(surface=screen)

        #TEMPORIZADOR
        tiempo = font_data.render("TIME: {0}".format(elapsed_time),True,WHITE)
        screen.blit(tiempo,(850,10))
        
        blob_group.draw(screen)
        platform_group.draw(screen)
        lava_group.draw(screen)
        door_group.draw(screen)
        coin_group.draw(screen)

        game_over = player.update(screen, game_over)  # player return game_over (-1=perdio, 0=jugando, 1=paso nivel)

        #PLAY#
        if game_over == 0: 
            #TEMPORIZADOR
            elapsed_time = 0
            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # Convertir a segundos

            blob_group.update()
            platform_group.update()

            #check if a coin has been collected
            if pygame.sprite.spritecollide(player, coin_group, True):
                score += 10
                coin_fx.play()
            draw_text('X ' + str(score), font_data, WHITE, TILE_SIZE - 10, 10, screen)

        #GAME OVER#
        if game_over == -1: 
            draw_text('GAME OVER!', font, WHITE, (SCREEN_WIDTH // 2) - 200, SCREEN_HEIGHT // 2,screen)
            
            if save_button.draw():
                try:
                    time_ranking =  int(elapsed_time)
                    save_data(ranking,name,elapsed_time,score)
                    mostrar_juego = False
                    main_menu = True
                except:
                    mostrar_juego = False
                    main_menu = True
            
            if restart_button.draw():  # devuelve (y entra) true cuando es presionado
                world, player = reset_level(level, jump_fx, game_over_fx, blob_group, platform_group, coin_group, lava_group, door_group) #restablecer valores
                game_over = 0  # indicando que el juego ha vuelto a estar en curso.
                score = 0
            
            if menu_button.draw():
                mostrar_juego = False
                main_menu = True

        #PASO NIVEL# -> pasa a estado jugando
        if game_over == 1: 
            # reset game and go to next level
            level += 1
            if level <= max_levels:
                world, player = reset_level(level, jump_fx, game_over_fx, blob_group, platform_group, coin_group, lava_group, door_group) # reset level
                game_over = 0
            else:
                draw_text('YOU WIN!', font, WHITE, (SCREEN_WIDTH // 2) - 100, SCREEN_HEIGHT // 2,screen)
                if save_button.draw():
                    try:
                        time_ranking =  int(elapsed_time)
                        save_data(ranking,name,elapsed_time,score)
                        mostrar_juego = False
                        main_menu = True
                    except:
                        mostrar_juego = False
                        main_menu = True
                if restart_button.draw(): # reset level
                    level = 1
                    world, player = reset_level(level, jump_fx, game_over_fx, blob_group, platform_group, coin_group, lava_group, door_group)
                    game_over = 0
                    score = 0
                if menu_button.draw():
                    mostrar_juego = False
                    main_menu = True

    #dibujar lineas de mosaicos, ayuda a tener en cuenta las dimensiones
    if DEBUG:
        for line in range(0, 20):
            pygame.draw.line(screen, WHITE, (0, line * TILE_SIZE), (SCREEN_WIDTH, line * TILE_SIZE)) #superfice,color,pos.inicial(x,y),pos.final(x,y)
            pygame.draw.line(screen, WHITE, (line * TILE_SIZE, 0), (line * TILE_SIZE, SCREEN_HEIGHT))

    pygame.display.update()

pygame.quit()
