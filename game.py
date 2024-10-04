# library imports
import pygame


# local imports
from color import BLACK
import screens
from managers import Game_Manager

pygame.init()

# setting the game screen to the size of the computer screen
# every size and position have to be a value from 0 to 1 multiplied by screen heigth or width
info_object = pygame.display.Info()
screen = pygame.display.set_mode((0.9 * info_object.current_w, 0.9 * info_object.current_h))
Game_Manager.update_screen_size()

Game_Manager.change_screen(screens.Start_Screen())

# game loop
game_loop = True
game_clock = pygame.time.Clock()

while game_loop:
    screen.fill(BLACK)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop = False
                
        for event_func in Game_Manager.main_screen.event:
            event_func(event)

    for layer in Game_Manager.main_screen.draw:
        for draw in layer:
            draw(screen)

    for process in Game_Manager.main_screen.process:
        process()

    pygame.display.flip()
    game_clock.tick(60)

    


pygame.quit()