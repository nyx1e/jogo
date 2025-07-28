import pygame
from spritesheet import *

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()

    def move(self,speed): #multiplica vetores pela velocidade
        if self.direction.magnitude() != 0: self.direction = self.direction.normalize() #iguala a velocidade nas diagonais
        self.hitbox.x += self.direction.x *speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y *speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self,direction):
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if direction == 'horizontal': #checa direção do movimento e se há colisão
                    if self.direction.x > 0: self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: self.hitbox.left = sprite.hitbox.right
                if direction == 'vertical':
                    if self.direction.y > 0: self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: self.hitbox.top = sprite.hitbox.bottom

class Inimigos(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.sprite_type = 'enemy'
        #gráficos
        self.load_images(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]
        #movimento
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.obstacle_sprites = obstacle_sprites
        #stats
        self.monster_name = monster_name
        monster_data = enemies_data[self.monster_name]
        self.health = monster_data['health']
        self.exp = monster_data['exp']
        self.speed = monster_data['speed']
        self.attack_damage = monster_data['damage']
        self.resistance = monster_data['resistance']
        self.attack_radius = monster_data['attack_radius']
        self.notice_radius = monster_data['notice_radius']
        self.attack_type = monster_data['attack_type']

        #interação c/ player
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400

    def load_images(self, name):
        path = f'assets/enemies/{name}/'
        self.animations = {'move': [], 'idle': [], 'attack': []}
        for sprite in self.animations.keys():
            full_path = path + sprite + '.png'
            self.spritesheet = Spritesheet(full_path)
            for animation in range(8):
                if name == 'canines': 
                    color = '#00f800'
                    scale = 1.2
                else: 
                    color = 'black'
                    scale = 1.4
                self.animations[sprite].append(self.spritesheet.get_image(animation, 60, 34, scale, color))

    def get_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude() #resulta num novo vetor
        if distance > 0:    
            direction = (player_vec - enemy_vec).normalize() #impede o vetor de passar do player
        else: 
            direction = pygame.math.Vector2()
        return (distance,direction)

    def get_status(self, player):
        distance = self.get_distance_direction(player)[0]
        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else: self.status = 'idle'

    def actions(self, player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            print('attack')
        elif self.status == 'move':
            self.direction = self.get_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2() #

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation) - 1:
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0
        self.image = animation[int(self.frame_index)] 
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def cooldown(self):
        if not self.can_attack:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

    def update(self):
        self.move(self.speed)
        self.animate()
        self.cooldown()

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)