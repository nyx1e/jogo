import pygame
from os.path import join
from os import walk
from biblioteca import *
from inimigos import Entity

width,heigth = 900,500
FPS = 60
tamanho_bloco = 32

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic):
        super().__init__(groups)
        #base
        self.image = pygame.image.load('assets/player/player.png')
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-60,-60)
        self.obstacle_sprites = obstacle_sprites
        
        #animação
        self.load_images()
        self.status = 'down'
        
        #espada
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.damage = 20
        self.attacking = False
        self.attack_cooldown = 300
        self.attack_time = None
        self.weapon_cooldown = 100
    
        #mágica
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.switch_magic = True
        self.switch_time = None
        self.switch_duration_cooldown = 200

        #stats
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 5}
        self.max_stats = {'health': 300, 'energy': 140, 'attack': 20, 'magic': 10, 'speed': 10}
        self.upgrade_cost = {'health': 100, 'energy': 100, 'attack': 100, 'magic': 100, 'speed': 100}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 100
        self.speed = self.stats['speed']

        #timer de dano
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500
    
    def load_images(self):
        path = 'assets/player/'
        self.animations = {'left': [], 'right': [], 'left_attack': [], 'right_attack': [], 'left_idle':[], 'right_idle': [], 
            'down': [], 'down_attack': [], 'down_idle': [], 'up': [], 'up_attack': [], 'up_idle': []}
        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = import_folder(full_path)           

    def input(self): #pega vetores
        if not self.attacking: #previne o player de atacar e fazer outros movimentos ao msm tempo 
            keys = pygame.key.get_pressed()
            #movimento
            # self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])     
            # self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
            if keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            elif keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            else:
                self.direction.y = 0
            if keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            #status
            # if self.direction.x > 0: self.status = 'right'
            # elif self.direction.x < 0: self.status = 'left'
            # elif self.direction.y > 0: self.status = 'down'
            # else: self.status = 'up' 
            #ataque
            if keys[pygame.K_q]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
            if keys[pygame.K_e]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']
                self.create_magic(style, strength, cost)    

            if keys[pygame.K_f] and self.switch_magic:   
                self.switch_magic = False
                self.switch_time = pygame.time.get_ticks()
                if self.magic_index < len(list(magic_data.keys())) - 1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0
                self.magic = list(magic_data.keys())[self.magic_index]

    def get_status(self):        
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle' 
        if self.attacking:
            self.direction.x, self.direction.y = 0, 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:    
                    self.status = self.status + '_attack'
        else: 
            if 'attack' in self.status:
                self.status = self.status.replace('_attack','')

    def cooldowns(self):
        current_time = pygame.time.get_ticks() 
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + self.weapon_cooldown:
                self.attacking = False
                self.destroy_attack()
        
        if not self.switch_magic:
            if current_time - self.switch_time >= self.switch_duration_cooldown:
                self.switch_magic = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True
    
    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        #define a imagem
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center) #evita q imagens de tamanhos diferentes tenham centros diferentes
        if not self.vulnerable: # "animação" de hit
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else: #s/ transparência
            self.image.set_alpha(255)

    def get_weapon_damage(self):
        base_damage = self.stats['attack']
        return base_damage + self.damage

    def get_magic_damage(self):
        base_damage = self.stats['magic']
        spell_damage = magic_data[self.magic]['strength']
        return base_damage + spell_damage

    def get_value_index(self, index):
        return list(self.stats.values())[index]

    def get_cost_index(self, index):
        return list(self.upgrade_cost.values())[index]

    def recover_energy(self):
        if self.energy < self.stats['energy']:
            self.energy += 0.01 * self.stats['magic']
        else:
            self.energy = self.stats['energy']

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.stats['speed'])
        self.recover_energy()