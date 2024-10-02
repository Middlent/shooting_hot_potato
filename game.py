# library imports
import pygame


# local imports
from color import BLACK, WHITE, BLUE
from managers import Game_Manager
from entities import Player, Bomb

pygame.init()

# setting the game screen to the size of the computer screen
# every size and position have to be a value from 0 to 1 multiplied by screen heigth or width
info_object = pygame.display.Info()
screen = pygame.display.set_mode((0.9 * info_object.current_w, 0.9 * info_object.current_h))
Game_Manager.update_screen_size()

Game_Manager.player_1 = Player(
    0.05 * Game_Manager.screen_width, 
    0.5 * Game_Manager.screen_height, {
    "UP_MOVEMENT":pygame.K_w,
    "DOWN_MOVEMENT":pygame.K_s,
    "LEFT_MOVEMENT":pygame.K_a,
    "RIGHT_MOVEMENT":pygame.K_d,
    "UP_GUN":pygame.K_c,
    "DOWN_GUN":pygame.K_v,
    "SHOOT":pygame.K_b
    },
    WHITE,
    gun_angle = 0)

Game_Manager.player_2 = Player(
    0.95 * Game_Manager.screen_width, 
    0.5 * Game_Manager.screen_height, {
    "UP_MOVEMENT":pygame.K_UP,
    "DOWN_MOVEMENT":pygame.K_DOWN,
    "LEFT_MOVEMENT":pygame.K_LEFT,
    "RIGHT_MOVEMENT":pygame.K_RIGHT,
    "UP_GUN":pygame.K_i,
    "DOWN_GUN":pygame.K_o,
    "SHOOT":pygame.K_p
    },
    BLUE, 
    gun_angle = 180)

Game_Manager.bomb = Bomb()


# game loop
game_loop = True
game_clock = pygame.time.Clock()

while game_loop:
    screen.fill(BLACK)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop = False
                
        for event_func in Game_Manager.event:
            event_func(event)

    for layer in Game_Manager.draw:
        for draw in layer:
            draw(screen)

    for process in Game_Manager.process:
        process()

    pygame.display.flip()
    game_clock.tick(60)

    


pygame.quit()