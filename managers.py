import pygame

import screens

class Game_Manager():
    '''
    Class that manage everything that happens in game scope

    Attributes
    ----------
    game_started : bool
        True if the game is running, False otherwise
    screen_width : float
        Width of the game screen
    screen_height : float
        Height of the game screen
    process : list
        A list of Callables that run game logic
    draw : list
        A list of layers, each one being a list
        of Callables that put things on screen
    event : list
        A list of Callables that receive game
        input and run code acordingly

    Methods
    -------
    start_game()
        Run the game
    update_screen_size()
        Catch the current screen size
    '''
    game_started = False

    screen_width = 0
    screen_height = 0

    start_screen = None
    game_screen = None
    ending_screen = None

    main_screen = None
    
    bomb = None
    player_1 = None
    player_2 = None
    bullets = [[],[]]

    def change_screen(screen):
        Game_Manager.main_screen = screen
        Game_Manager.main_screen.populate()

    def start_game():
        '''Run the game'''
        Game_Manager.change_screen(screens.Game_Screen())
        
        Game_Manager.game_started = True
    
    def game_over(winner):
        Game_Manager.main_screen = screens.End_Screen()
        Game_Manager.main_screen.populate(winner)
        Game_Manager.game_started = False

    def update_screen_size():
        '''Catch the current screen size'''

        info = pygame.display.Info()
        Game_Manager.screen_width = info.current_w
        Game_Manager.screen_height = info.current_h

    def reset_players_pos():
        Game_Manager.player_1.set_pos((Game_Manager.player_1.spawn_x, Game_Manager.player_1.spawn_y))
        Game_Manager.player_2.set_pos((Game_Manager.player_2.spawn_x, Game_Manager.player_2.spawn_y))

    def convert_to_relative_height(number):
        n_per_pixel = number / 1080
        return n_per_pixel * Game_Manager.screen_height
    
    def convert_to_relative_width(number):
        n_per_pixel = number / 1920
        return n_per_pixel * Game_Manager.screen_width
    