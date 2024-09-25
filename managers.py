import pygame

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

    process = []
    draw = [[],[],[]] # the draw function have 2 layers, the thing on the botton have to be in layer 0, the things on top on layer 1
    event = []
    

    def start_game():
        '''Run the game'''
        
        Game_Manager.game_started = True

    def update_screen_size():
        '''Catch the current screen size'''

        info = pygame.display.Info()
        Game_Manager.screen_width = info.current_w
        Game_Manager.screen_height = info.current_h