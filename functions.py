import json
from constants import *
from level_1 import Level_1
from level_2 import Level_2
from level_3 import Level_3
from level_4 import Level_4
from level_5 import Level_5
from world import World
from player import Player
from coin import Coin

#Funcion para escribir texto
def draw_text(text, font, text_col, x, y,screen):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


#funcion para guardar ranking
def read_data(archivo: str) -> list:
    with open(archivo, "r", encoding='utf-8') as file: # bloque with, que garantiza que el archivo se cierre correctamente después de su uso.
        data = json.load(file) #Esto convierte el JSON en un diccionario de Python

    list_score = data.get("ranking", [])
    list_score.sort(key=lambda x: x["score"], reverse=True) #orden descendente

    return list_score[:10]

def save_data(ranking:list,name:str,time_ranking:int,score:int):
    ranking.append({"name": name, "time": time_ranking, "score": score})    
    with open("data_juego.json", 'w', encoding='utf-8') as file:
        json.dump({"ranking": ranking}, file, indent=4)


#Función para reiniciar el nivel
def reset_level(level, jump_fx, game_over_fx, blob_group, platform_group, coin_group, lava_group, door_group):
    #Limpiar los grupos de sprites
    blob_group.empty()
    platform_group.empty()
    coin_group.empty()
    lava_group.empty()
    door_group.empty()
    
    # Instanciar la clase del nivel correspondiente
    if level == 1:
        level_class = Level_1 # Crear una instancia de la clase
    elif level == 2:
        level_class = Level_2
    elif level == 3:
        level_class = Level_3
    elif level == 4:
        level_class = Level_4
    elif level == 5:
        level_class = Level_5

    # Crear una instancia del nivel y obtener los datos del mundo
    current_level = level_class()
    world_data = current_level.get_world_data() # Acceder a world_data a través de la instancia
    world = World(world_data, blob_group, lava_group, door_group, coin_group, platform_group)

    # Create an instance of Player
    player = Player(100, SCREEN_HEIGHT - 130, world, jump_fx, game_over_fx, platform_group)  # -130 = 50(mosaico) + 80(player)

    #create dummy coin for showing the score
    score_coin = Coin(TILE_SIZE // 2, TILE_SIZE // 2)
    coin_group.add(score_coin)

    return world, player
