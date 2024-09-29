from managers import Game_Manager
from color import RED

import pygame
import math
import random
import numpy

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
    def __init__(self, x, y, controls_dict: dict, color, life = 3):
        super().__init__(layer = 1)
        self.controls = controls_dict
        self.color = color
        self.life = life

        self.size = 0.05 * Game_Manager.screen_height
        self.speed = 0.01 * Game_Manager.screen_height

        self.spawn_x = x - self.size/2
        self.spawn_y = y - self.size/2

        self.rect = pygame.rect.Rect(
            self.spawn_x,
            self.spawn_y,
            self.size,
            self.size,
        )

        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False
        self.aiming_up = False
        self.aiming_down = False
        self.shoot = False

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.controls["UP_MOVEMENT"]:
                self.moving_up = True
            if event.key == self.controls["DOWN_MOVEMENT"]:
                self.moving_down = True
            if event.key == self.controls["LEFT_MOVEMENT"]:
                self.moving_left = True
            if event.key == self.controls["RIGHT_MOVEMENT"]:
                self.moving_right = True
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
            if event.key == self.controls["LEFT_MOVEMENT"]:
                self.moving_left = False
            if event.key == self.controls["RIGHT_MOVEMENT"]:
                self.moving_right = False
            if event.key == self.controls["UP_GUN"]:
                self.aiming_up = False
            if event.key == self.controls["DOWN_GUN"]:
                self.aiming_down = False
            if event.key == self.controls["SHOOT"]:
                self.shoot = False

    def process(self):
        # Movement Code
        if self.moving_up and not self.moving_down:
            self.rect.y -= self.speed
            if self.rect.y <= 0:
                self.rect.y = 0
        if self.moving_down and not self.moving_up:
            self.rect.y += self.speed
            if self.rect.bottom >= Game_Manager.screen_height:
                self.rect.bottom = Game_Manager.screen_height
        if self.moving_left and not self.moving_right:
            self.rect.x -= self.speed
            if self.rect.x <= 0:
                self.rect.x = 0
        if self.moving_right and not self.moving_left:
            self.rect.x += self.speed
            if self.rect.right >= Game_Manager.screen_width:
                self.rect.right = Game_Manager.screen_width

        if self.rect.colliderect(Game_Manager.bomb.rect):
            self.life -= 1
            Game_Manager.bomb.destroy()
            if self.life == 0:
                self.destroy()
            else:
                Game_Manager.bomb = Bomb()
                Game_Manager.reset_players_pos()


    def draw(self, screen):
        pygame.draw.rect(surface = screen,color = self.color,rect = self.rect)


class Bomb(Base):
    COLLISION_MODE_SIDES = 0
    COLLISION_MODE_UPDOWN = 1
    
    def __init__(self):
        super().__init__(layer = 1)

        self.size = 0.1 * Game_Manager.screen_height
        self.rect = pygame.rect.Rect(0.5 * Game_Manager.screen_width,
                            0.5 * Game_Manager.screen_height, 
                            self.size, 
                            self.size)
        

        self.speed = 0.003 * Game_Manager.screen_height
        self.quadrant = random.randint(0,1)
        self.angle = self.quadrant * 90 + random.randint(30,60)

        self.speed_h = 0
        self.speed_v = 0

        self.returning = False


    def process(self):
        self.speed_v = math.sin(math.radians(self.angle)) * self.speed
        self.speed_h = math.cos(math.radians(self.angle)) * self.speed

        self.rect.y += self.speed_v
        self.rect.x += self.speed_h

        if not (0 < self.rect.y < Game_Manager.screen_height - self.size):
            if 0 > self.rect.y:
                self.rect.y = 0
            if self.rect.y > Game_Manager.screen_height - self.size:
                self.rect.y = Game_Manager.screen_height - self.size
            self.bounce(Bomb.COLLISION_MODE_UPDOWN)
        elif not (0 < self.rect.x < Game_Manager.screen_width - self.size):
            if 0 > self.rect.x:
                self.rect.x = 0
            if self.rect.x > Game_Manager.screen_width - self.size:
                self.rect.x = Game_Manager.screen_width - self.size
            self.bounce(Bomb.COLLISION_MODE_SIDES)
        

    
    def bounce(self, collision_mode):
        print("oldq",self.quadrant)
        print("v",self.speed_v)
        print("h",self.speed_h)
        
        
        if collision_mode == Bomb.COLLISION_MODE_SIDES:
            self.quadrant = (self.quadrant + (numpy.sign(self.speed_v) * numpy.sign(self.speed_h))) % 4
        elif collision_mode == Bomb.COLLISION_MODE_UPDOWN:
            self.quadrant = (self.quadrant - (numpy.sign(self.speed_v) * numpy.sign(self.speed_h))) % 4
        self.angle = self.quadrant * 90 + random.randint(30,60)
        
        self.speed += 0.0001 * Game_Manager.screen_height
        print("newq",self.quadrant)
                

    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect)


class Walls(Base):
    def __init__(self):
        super().__init__(layer = 1)


class Bullet(Base):
    def __init__(self):
        super().__init__(layer = 1)


class Lives_Text(Base):
    def __init__(self):
        super().__init__(layer = 2)

