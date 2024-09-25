import pygame

class Game_Manager():
    game_started = False

    screen_width = 0
    screen_height = 0

    process = []
    draw = [[],[]] # the draw function have 2 layers, the thing on the botton have to be in layer 0, the things on top on layer 1
    event = []
    

    def start_game():
        Game_Manager.game_started = True

    def update_screen_size():
        info = pygame.display.Info()
        Game_Manager.screen_width = info.current_w
        Game_Manager.screen_height = info.current_h