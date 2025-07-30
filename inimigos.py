import pygame
from math import sin
from biblioteca import *

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

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0: return 255
        else: return 0

class Inimigos(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player, ativar_particulas_morte, add_exp):
        super().__init__(groups)
        self.sprite_type = 'enemy'
        #gráficos
        self.load_images(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        #movimento
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
        self.damage_player = damage_player
        self.ativar_particulas_morte = ativar_particulas_morte
        self.add_exp = add_exp
        self.contador_inimigos = 0

        #invulnerabilidade
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300

    def load_images(self, name):
        main_path = f'assets/enemies/{name}/'
        self.animations = {'move':[], 'idle': [], 'attack': []}
        for animation in self.animations.keys():
            full_path = main_path + animation
            self.animations[animation] = import_folder(full_path)

    def get_distance_direction(self, player): #define o espaço e direção q o inimigo deve andar p/ seguir o player
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
            self.damage_player(self.attack_damage, self.attack_type)
        elif self.status == 'move':
            self.direction = self.get_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2() 

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation) - 1:
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0
        self.image = animation[int(self.frame_index)] 
        self.rect = self.image.get_rect(center = self.hitbox.center)
        if not self.vulnerable: # "animação" de hit
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else: #s/ transparência
            self.image.set_alpha(255)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack: #evita q o inimigo ataque multiplas vezes
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_damage(self, player, attack_type):
        if self.vulnerable:
            self.direction = self.get_distance_direction(player)[1]
            if attack_type == 'weapon':
                self.health -= player.get_weapon_damage() 
            else: 
                self.health -= player.get_magic_damage()
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            self.kill()
            self.ativar_particulas_morte(self.rect.center, self.monster_name)
            self.add_exp(self.exp)
            self.contador_inimigos += 1

    def hit_reaction(self):
        if not self.vulnerable: #atacar e 
            self.direction *= -self.resistance

    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.check_death()

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)