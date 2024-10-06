import managers
from color import *
import screens

import pygame
import math
import random
import numpy

class Base():
    def __init__(self, layer):
        self.layer = layer
        managers.Game_Manager.main_screen.add_item(self, layer)

    def event(self, event):
        pass
    
    def destroy(self):
        managers.Game_Manager.main_screen.remove_item(self, self.layer)

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
    def __init__(self, x, y, controls_dict: dict, color, player_num, life = 3, gun_angle = 0):
        super().__init__(layer = 1)
        
        self.controls = controls_dict
        self.color = color
        self.player_num = player_num

        self.life = life
        self.lives_text = Lives_Text(x, 0.1 * managers.Game_Manager.screen_height, player_num)
        self.lives_text.update_text(str(self.life))
        

        self.size = 0.05 * managers.Game_Manager.screen_height
        self.speed = 0.01 * managers.Game_Manager.screen_height

        if player_num == 0:
            self.player_image = pygame.image.load("assets\Art\Player_1.png")
        if player_num == 1:
            self.player_image = pygame.image.load("assets\Art\Player_2.png")

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
                       self.size * 2,
                       gun_angle,
                       player_num)

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
                self.gun.shoot()
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


    def process(self):
        # Movement Code
        gun_movement = [self.rect.x, self.rect.y]
        if self.moving_up and not self.moving_down:
            self.rect.y -= self.speed
            if self.rect.y <= 0:
                self.rect.y = 0
        if self.moving_down and not self.moving_up:
            self.rect.y += self.speed
            if self.rect.bottom >= managers.Game_Manager.screen_height:
                self.rect.bottom = managers.Game_Manager.screen_height
        if self.moving_left and not self.moving_right:
            self.rect.x -= self.speed
            if self.rect.x <= 0:
                self.rect.x = 0
        if self.moving_right and not self.moving_left:
            self.rect.x += self.speed
            if self.rect.right >= managers.Game_Manager.screen_width:
                self.rect.right = managers.Game_Manager.screen_width

        gun_movement[0] = self.rect.x - gun_movement[0]
        gun_movement[1] = self.rect.y - gun_movement[1]

        self.gun.move(gun_movement)

        if self.aiming_down and not self.aiming_up:
            self.gun.rotate(Gun.CLOCKWISE)
        if self.aiming_up and not self.aiming_down:
            self.gun.rotate(Gun.COUNTER_CLOCKWISE)


        if self.rect.colliderect(managers.Game_Manager.bomb.rect):
            self.life -= 1
            self.lives_text.update_text(str(self.life))
            pygame.mixer.Channel(2).play(pygame.mixer.Sound('assets\SFX\Explosion.mp3'), maxtime=600)
            managers.Game_Manager.bomb.destroy()
            if self.life == 0:
                players = [1,2]
                players.remove(self.player_num + 1)
                winner = players[0]
                managers.Game_Manager.game_over(winner)
            else:
                managers.Game_Manager.bomb = Bomb()
                managers.Game_Manager.reset_players_pos()

    def set_pos(self, position):
        gun_movement = [self.rect.x, self.rect.y]

        self.rect.x = position[0]
        self.rect.y = position[1]

        gun_movement[0] = self.rect.x - gun_movement[0]
        gun_movement[1] = self.rect.y - gun_movement[1]

        self.gun.move(gun_movement)
        

    def draw(self, screen: pygame.Surface):
        screen.blit(source = self.player_image, 
                    dest = (self.rect.x, self.rect.y))


class Bomb(Base):
    COLLISION_MODE_SIDES = 0
    COLLISION_MODE_UPDOWN = 1
    
    def __init__(self):
        super().__init__(layer = 1)

        self.size = 0.1 * managers.Game_Manager.screen_height
        self.rect = pygame.rect.Rect(0.5 * managers.Game_Manager.screen_width,
                            0.5 * managers.Game_Manager.screen_height, 
                            self.size, 
                            self.size)
        
        self.image = pygame.image.load("assets\Art\Potato.png")

        self.speed = 0.006 * managers.Game_Manager.screen_height
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

        if not (0 < self.rect.y < managers.Game_Manager.screen_height - self.size):
            if 0 > self.rect.y:
                self.rect.y = 0
            if self.rect.y > managers.Game_Manager.screen_height - self.size:
                self.rect.y = managers.Game_Manager.screen_height - self.size
            self.bounce(Bomb.COLLISION_MODE_UPDOWN)
        elif not (0 < self.rect.x < managers.Game_Manager.screen_width - self.size):
            if 0 > self.rect.x:
                self.rect.x = 0
            if self.rect.x > managers.Game_Manager.screen_width - self.size:
                self.rect.x = managers.Game_Manager.screen_width - self.size
            self.bounce(Bomb.COLLISION_MODE_SIDES)
        
    def charge(self):
        self.speed += 0.001 * managers.Game_Manager.screen_height
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('assets\SFX\Wall.mp3'), maxtime=600)
    
    def bounce(self, collision_mode):
        if collision_mode == Bomb.COLLISION_MODE_SIDES:
            self.quadrant = (self.quadrant + (numpy.sign(self.speed_v) * numpy.sign(self.speed_h))) % 4
        elif collision_mode == Bomb.COLLISION_MODE_UPDOWN:
            self.quadrant = (self.quadrant - (numpy.sign(self.speed_v) * numpy.sign(self.speed_h))) % 4
        self.angle = self.quadrant * 90 + random.randint(30,60)
        
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('assets\SFX\Wall.mp3'), maxtime=600)

        self.speed += 0.0001 * managers.Game_Manager.screen_height
                

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Gun(Base):
    CLOCKWISE = 1
    COUNTER_CLOCKWISE = -1

    def __init__(self, x ,y, size, distance, angle, player_num):
        super().__init__(layer = 1)
        self.player_num = player_num

        self.base_gun = pygame.image.load("assets\Art\Gun.png")
        self.gun = self.base_gun

        self.angle = 0

        self.base_x = x
        self.base_y = y

        self.x = x
        self.y = y 

        self.size = size
        self.distance = distance

        self.point_x = self.base_x + self.distance * math.cos(math.radians(self.angle))
        self.point_y = self.base_y - self.distance * math.sin(math.radians(self.angle))

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
        self.point_x = self.base_x + self.distance * math.cos(math.radians(self.angle))
        self.point_y = self.base_y - self.distance * math.sin(math.radians(self.angle))

        self.x = self.point_x + self.gun.get_rect().width * ((-math.cos(math.radians(self.angle))/2) -1/2) 
        self.y = self.point_y + self.gun.get_rect().height * ((math.sin(math.radians(self.angle))/2) -1/2) 

    def shoot(self):
        managers.Game_Manager.bullets[self.player_num].append(Bullet(self.angle, self.point_x, self.point_y, self.player_num))

    def draw(self, screen):
        screen.blit(self.gun, (self.x, self.y))


class Bullet(Base):
    def __init__(self, angle, x, y, player_num):
        super().__init__(layer = 1)

        pygame.mixer.Channel(0).play(pygame.mixer.Sound('assets\SFX\Shoot.mp3'), maxtime=600)
        self.player_num = player_num

        self.bullet = pygame.image.load("assets/placeholders/bullet.png")

        self.collision_rect = pygame.rect.Rect(x, y, self.bullet.get_rect().width, self.bullet.get_rect().height)

        self.angle = angle

        pygame.transform.rotate(self.bullet,self.angle)

        self.x = x
        self.y = y 

        self.size = 0.01 * managers.Game_Manager.screen_height
        self.speed = 0.02 * managers.Game_Manager.screen_height

    def destroy(self):
        super().destroy()
        managers.Game_Manager.bullets[self.player_num].remove(self)

    def process(self):
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y -= math.sin(math.radians(self.angle)) * self.speed
        
        self.collision_rect.x = self.x
        self.collision_rect.y = self.y
        
        if 0 > self.x > managers.Game_Manager.screen_width:
            self.destroy()
        if 0 > self.y > managers.Game_Manager.screen_height:
            self.destroy()

        if self.collision_rect.colliderect(managers.Game_Manager.bomb.rect):
            self.destroy()
            managers.Game_Manager.bomb.charge()

    def draw(self, screen):
        screen.blit(self.bullet, (self.x, self.y))



class Background(Base):
    def __init__(self):
        super().__init__(layer = 0)
        self.image = pygame.image.load("assets\Art\BG.png")
        self.image = pygame.transform.scale(self.image, (managers.Game_Manager.screen_width, managers.Game_Manager.screen_height))

    def draw(self, screen):
        screen.blit(self.image, (0,0))    

class Lives_Text(Base):
    def __init__(self, x, y, player_num):
        super().__init__(layer = 0)
        self.font = pygame.font.Font('assets/PressStart2P.ttf', 44)
        self.small_font = pygame.font.Font('assets/PressStart2P.ttf', 33)

        self.x = x
        self.y = y

        if player_num == 0:
            self.move = self.small_font.render("W,A,S,D to move", True, BLACK)
            self.move_rect = self.move.get_rect()
            self.move_rect.topleft = (self.x, managers.Game_Manager.screen_height * 0.85)
            
            self.aim = self.small_font.render("C and B to aim", True, BLACK)
            self.aim_rect = self.aim.get_rect()
            self.aim_rect.topleft = (self.x, managers.Game_Manager.screen_height * 0.90)

            self.shoot = self.small_font.render("V to shoot", True, BLACK)
            self.shoot_rect = self.shoot.get_rect()
            self.shoot_rect.topleft = (self.x, managers.Game_Manager.screen_height * 0.95)

        if player_num == 1:
            self.move = self.small_font.render("Arrows to move", True, BLACK)
            self.move_rect = self.move.get_rect()
            self.move_rect.topright = (self.x, managers.Game_Manager.screen_height * 0.85)
            
            self.aim = self.small_font.render("I and P to aim", True, BLACK)
            self.aim_rect = self.aim.get_rect()
            self.aim_rect.topright = (self.x, managers.Game_Manager.screen_height * 0.90)

            self.shoot = self.small_font.render("O to shoot", True, BLACK)
            self.shoot_rect = self.shoot.get_rect()
            self.shoot_rect.topright = (self.x, managers.Game_Manager.screen_height * 0.95)

    def update_text(self, new_text):
        self.text = self.font.render(new_text, True, BLACK)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.text, self.text_rect)  
        screen.blit(self.move, self.move_rect)    
        screen.blit(self.aim, self.aim_rect)   
        screen.blit(self.shoot, self.shoot_rect)       

class Start_Text(Base):
    def __init__(self):
        super().__init__(layer = 0)
        self.image = pygame.image.load("assets\Art\Start.png")
        self.image = pygame.transform.scale(self.image, (managers.Game_Manager.screen_width, managers.Game_Manager.screen_height))
        self.font = pygame.font.Font('assets/PressStart2P.ttf', 55)

        self.target_x = managers.Game_Manager.screen_width * 0.5
        self.target_y = managers.Game_Manager.screen_height * 0.05

        self.title_x = self.target_x
        self.title_y = self.target_y

        self.x = managers.Game_Manager.screen_width * 0.5
        self.y = managers.Game_Manager.screen_height * 0.85

        self.title = self.font.render("SHOOTING HOT POTATO!!", True, POTATO)
        self.title_rect = self.title.get_rect()
        self.title_rect.center = (self.title_x, self.title_y)

        self.text = self.font.render("Press Space to Start Game", True, BLACK)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (self.x, self.y)

    def process(self):
        if int(self.title_rect.centerx) == int(self.target_x):
            self.target_x = random.randint(int(managers.Game_Manager.screen_width * 0.47), int(managers.Game_Manager.screen_width * 0.53))
        else:
            self.title_rect.centerx -= numpy.sign(self.title_rect.centerx - self.target_x)
        if int(self.title_rect.centery) == int(self.target_y):
            self.target_y = random.randint(int(managers.Game_Manager.screen_height * 0.05), int(managers.Game_Manager.screen_height * 0.15))
        else:
            self.title_rect.centery -= numpy.sign(self.title_rect.centery - self.target_y)

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                managers.Game_Manager.start_game()

    def draw(self, screen):
        screen.blit(self.image, (0,0))
        screen.blit(self.text, self.text_rect)    
        screen.blit(self.title, self.title_rect)    

class Start_Music(Base):
    def __init__(self):
        super().__init__(layer = 0)
        pygame.mixer_music.load('assets\Musica\Menu [START].ogg')
        pygame.mixer_music.queue('assets\Musica\Menu [LOOP].ogg')
        pygame.mixer_music.play()

class Game_Music(Base):
    def __init__(self):
        super().__init__(layer = 0)
        pygame.mixer_music.load('assets\Musica\Level [LOOP].ogg')
        pygame.mixer_music.play()

class Win_Text(Base):
    def __init__(self, winner):
        super().__init__(layer = 0)
        self.font = pygame.font.Font('assets/PressStart2P.ttf', 55)

        self.image = pygame.image.load('assets\Art\Win_'+str(winner)+'.png')

        self.x = managers.Game_Manager.screen_width * 0.5
        self.y = managers.Game_Manager.screen_height * 0.95

        self.text = self.font.render("Jogador "+str(winner)+" Venceu", True, BLACK)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (self.x, self.y)

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                managers.Game_Manager.change_screen(screens.Start_Screen())

    def draw(self, screen):
        screen.blit(self.image, (0,0))      
        screen.blit(self.text, self.text_rect)  