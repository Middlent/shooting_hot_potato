from managers import Game_Manager
from color import WHITE

import pygame

class Base():
    def __init__(self, layer):
        self.layer = layer
        Game_Manager.draw[self.layer].append(self.draw)
        Game_Manager.event.append(self.event)
        Game_Manager.process.append(self.process)

    def event(self, event):
        pass
    
    def destroy(self):
        Game_Manager.draw[self.layer].remove(self.draw)
        Game_Manager.event.remove(self.event)
        Game_Manager.process.remove(self.process)

    def process(self):
        pass
    
    def draw(self, screen):
        pass

class Player(Base):
    '''
    Class for the controlable players
    
    Parameters
    ----------
    controls_dict : dict
        A dictionary with strings with the command
        name as keys and keyboard keys as values

    Notes
    -----
    Available command names are:
        UP_MOVEMENT - Player upward movement button
        DOWN_MOVEMENT - Player downward movement button
        LEFT_MOVEMENT - Player left movement button
        RIGHT_MOVEMENT - Player right movement button
        UP_GUN - Gun upward movement button
        DOWN_GUN - Gun downward movement button
        SHOOT - Shooting button
    '''
    def __init__(self, x, y, controls_dict: dict):
        super().__init__(layer = 1)
        self.controls = controls_dict

        self.size = 0.05 * Game_Manager.screen_height

        self.rect = pygame.rect.Rect(
            x - self.size/2,
            y - self.size/2,
            self.size,
            self.size,
        )

        self.moving_up = False
        self.moving_down = False
        self.aiming_up = False
        self.aiming_down = False
        self.shoot = False
    
    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.controls["UP_MOVEMENT"]:
                self.moving_up = True
            if event.key == self.controls["DOWN_MOVEMENT"]:
                self.moving_down = True
            if event.key == self.controls["UP_GUN"]:
                self.aiming_up = True
            if event.key == self.controls["DOWN_GUN"]:
                self.aiming_down = True
            if event.key == self.controls["SHOOT"]:
                self.shoot = True
        if event.type == pygame.KEYUP:
            if event.key == self.controls["UP_MOVEMENT"]:
                self.moving_up = False
            if event.key == self.controls["DOWN_MOVEMENT"]:
                self.moving_down = False
            if event.key == self.controls["UP_GUN"]:
                self.aiming_up = False
            if event.key == self.controls["DOWN_GUN"]:
                self.aiming_down = False
            if event.key == self.controls["SHOOT"]:
                self.shoot = False

    def process(self):
        if self.moving_up and not self.moving_down:
            self.rect.y -= 10
            if self.rect.y <= 0:
                self.rect.y = 0
        if self.moving_down and not self.moving_up:
            self.rect.y += 10
            if self.rect.bottom >= Game_Manager.screen_height:
                self.rect.bottom = Game_Manager.screen_height

    def draw(self, screen):
        pygame.draw.rect(surface = screen,color = WHITE,rect = self.rect)


class Bomb(Base):
    def __init__(self):
        super().__init__(layer = 1)


class Walls(Base):
    def __init__(self):
        super().__init__(layer = 1)


class Bullet(Base):
    def __init__(self):
        super().__init__(layer = 1)


class Lives_Text(Base):
    def __init__(self):
        super().__init__(layer = 2)

