from managers import Game_Manager
from color import RED, WHITE, BLACK

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
    def __init__(self, x, y, controls_dict: dict, color, life = 3, gun_angle = 0):
        super().__init__(layer = 1)
        self.controls = controls_dict
        self.color = color

        self.life = life
        self.lives_text = Lives_Text(x, 0.1 * Game_Manager.screen_height )
        self.lives_text.update_text(str(self.life))
        

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

        self.gun = Gun(self.spawn_x + self.size/2,
                       self.spawn_y + self.size/2,
                       self.size,
                       self.size * 3,
                       gun_angle)

        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False
        self.aiming_up = False
        self.aiming_down = False
        self.shoot = False

    def destroy(self):
        super().destroy()
        self.gun.destroy()

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
        gun_movement = [self.rect.x, self.rect.y]
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

        gun_movement[0] = self.rect.x - gun_movement[0]
        gun_movement[1] = self.rect.y - gun_movement[1]

        self.gun.move(gun_movement)

        if self.aiming_down and not self.aiming_up:
            self.gun.rotate(Gun.CLOCKWISE)
        if self.aiming_up and not self.aiming_down:
            self.gun.rotate(Gun.COUNTER_CLOCKWISE)

        if self.rect.colliderect(Game_Manager.bomb.rect):
            self.life -= 1
            self.lives_text.update_text(str(self.life))
            Game_Manager.bomb.destroy()
            if self.life == 0:
                self.destroy()
            else:
                Game_Manager.bomb = Bomb()
                Game_Manager.reset_players_pos()

    def set_pos(self, position):
        gun_movement = [self.rect.x, self.rect.y]

        self.rect.x = position[0]
        self.rect.y = position[1]

        gun_movement[0] = self.rect.x - gun_movement[0]
        gun_movement[1] = self.rect.y - gun_movement[1]

        self.gun.move(gun_movement)
        

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
        

        self.speed = 0.006 * Game_Manager.screen_height
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
        if collision_mode == Bomb.COLLISION_MODE_SIDES:
            self.quadrant = (self.quadrant + (numpy.sign(self.speed_v) * numpy.sign(self.speed_h))) % 4
        elif collision_mode == Bomb.COLLISION_MODE_UPDOWN:
            self.quadrant = (self.quadrant - (numpy.sign(self.speed_v) * numpy.sign(self.speed_h))) % 4
        self.angle = self.quadrant * 90 + random.randint(30,60)
        
        self.speed += 0.0001 * Game_Manager.screen_height
                

    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect)


class Walls(Base):
    def __init__(self):
        super().__init__(layer = 1)

class Gun(Base):
    CLOCKWISE = 1
    COUNTER_CLOCKWISE = -1

    def __init__(self, x ,y, size, distance, angle):
        super().__init__(layer = 1)

        self.base_gun = pygame.image.load("assets/placeholders/gun.png")
        self.gun = self.base_gun

        self.angle = 0

        self.base_x = x# + size
        self.base_y = y# + size/2

        self.x = x
        self.y = y 

        self.size = size
        self.distance = distance

        self.rotate(angle)

    def move(self, movement):
        self.base_x += movement[0]
        self.base_y += movement[1]

        self.update_position()

    def rotate(self, direction):
        self.angle = (self.angle + direction * 5) % 360
        self.gun = pygame.transform.rotate(self.base_gun, self.angle)

        self.update_position()

    def update_position(self):
        new_base_x = self.base_x + self.distance * math.cos(math.radians(self.angle))
        new_base_y = self.base_y - self.distance * math.sin(math.radians(self.angle))

        self.x = new_base_x + self.gun.get_rect().width * ((-math.cos(math.radians(self.angle))/2) -1/2) 
        self.y = new_base_y + self.gun.get_rect().height * ((math.sin(math.radians(self.angle))/2) -1/2) 



    def draw(self, screen):
        screen.blit(self.gun, (self.x, self.y))


class Bullet(Base):
    def __init__(self):
        super().__init__(layer = 1)


class Lives_Text(Base):
    def __init__(self, x, y):
        super().__init__(layer = 0)
        self.font = pygame.font.Font('assets/PressStart2P.ttf', 44)

        self.x = x
        self.y = y

    def update_text(self, new_text):
        self.text = self.font.render(new_text, True, WHITE, BLACK)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.text, self.text_rect)       