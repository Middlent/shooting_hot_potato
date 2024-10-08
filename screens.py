from managers import Game_Manager
import game_entities as ent
import pygame

from color import WHITE, BLUE


class Screen():
    def __init__(self):
        self.process = []
        self.draw = [[],[],[]] # the draw function have 2 layers, the thing on the botton have to be in layer 0, the things on top on layer 1
        self.event = []

    def add_item(self, item, layer):
        self.process.append(item.process)
        self.draw[layer].append(item.draw)
        self.event.append(item.event)

    def remove_item(self, item, layer):
        try:
            self.process.remove(item.process)
        except:
            print("Process that is not here tried to me removed")
        try:
            self.draw[layer].remove(item.draw)
        except:
            print("Draw that is not here tried to me removed")
        try:
            self.event.remove(item.event)
        except:
            print("Event that is not here tried to me removed")


    def clear_screen(self):
        self.process.clear()
        for layer in self.draw:
            layer.clear()
        self.event.clear()

    def populate(self):
        pass

class Game_Screen(Screen):
    def __init__(self):
        super().__init__()
    
    def populate(self):
        ent.Background()

        Game_Manager.player_1 = ent.Player(
            0.05 * Game_Manager.screen_width, 
            0.5 * Game_Manager.screen_height, {
            "UP_MOVEMENT":pygame.K_w,
            "DOWN_MOVEMENT":pygame.K_s,
            "LEFT_MOVEMENT":pygame.K_a,
            "RIGHT_MOVEMENT":pygame.K_d,
            "UP_GUN":pygame.K_b,
            "DOWN_GUN":pygame.K_c,
            "SHOOT":pygame.K_v
            },
            WHITE,
            0,
            gun_angle = 0)

        Game_Manager.player_2 = ent.Player(
            0.95 * Game_Manager.screen_width, 
            0.5 * Game_Manager.screen_height, {
            "UP_MOVEMENT":pygame.K_UP,
            "DOWN_MOVEMENT":pygame.K_DOWN,
            "LEFT_MOVEMENT":pygame.K_LEFT,
            "RIGHT_MOVEMENT":pygame.K_RIGHT,
            "UP_GUN":pygame.K_p,
            "DOWN_GUN":pygame.K_i,
            "SHOOT":pygame.K_o
            },
            BLUE, 
            1,
            gun_angle = 180)

        Game_Manager.bomb = ent.Bomb()

        ent.Game_Music()

class End_Screen(Screen):

    def __init__(self):
        super().__init__()

    def populate(self, winner):
        ent.Background()
        ent.Win_Text(winner)


class Start_Screen(Screen):

    def __init__(self):
        super().__init__()

    def populate(self):
        ent.Start_Text()
        ent.Start_Music()
        