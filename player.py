import pygame
from os.path import join
from os import walk
from spritesheet import *
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
        self.hitbox = self.rect.inflate(0,-40)
        self.obstacle_sprites = obstacle_sprites
        
        #animação
        self.load_images()
        self.status = 'down'
        
        #espada
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        # self.damage = 20
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
    
        #mágica
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.switch_magic = True
        self.switch_time = None
        self.switch_duration_cooldown = 200

        #stats
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 5}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 100
        self.speed = self.stats['speed']
    
    def load_images(self):
        path = 'assets/player/'
        self.animations = {'left': [], 'right': [], 'left_attack': [], 'right_attack': [], 'left_idle':[], 'right_idle': [], 
            'down': [], 'down_attack': [], 'down_idle': [], 'up': [], 'up_attack': [], 'up_idle': []}
        for sprite in self.animations.keys():
            full_path = path + sprite + '.png'
            self.spritesheet = Spritesheet(full_path)
            for animation in range(8):
                self.animations[sprite].append(self.spritesheet.get_image(animation, 86.375, 80, 1.4, 'black'))

    def input(self): #pega vetores
        if not self.attacking: #previne o player de atacar e fazer outros movimentos ao msm tempo 
            keys = pygame.key.get_pressed()
            #movimento
            self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])     
            self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
            #ataque
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']
                self.create_magic(style, strength, cost)    

            if keys[pygame.K_e] and self.switch_magic:   
                self.switch_magic = False
                self.switch_time = pygame.time.get_ticks()
                if self.magic_index < len(list(magic_data.keys())) - 1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0
                self.magic = list(magic_data.keys())[self.magic_index]

    def get_status(self):
        #status
        if self.direction.x > 0: self.status = 'right'
        elif self.direction.x < 0: self.status = 'left'
        elif self.direction.y > 0: self.status = 'down'
        else: self.status = 'up' 
        
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle' 
        if self.attacking:
            self.direction.x, self.direction.x = 0, 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:    
                    self.status = self.status + ('_attack')
        else: 
            if 'attack' in self.status:
                self.status = self.status.replace('_attack','')

    def cooldowns(self):
        current_time = pygame.time.get_ticks() 
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()
        
        if not self.switch_magic:
            if current_time - self.switch_time >= self.switch_duration_cooldown:
                self.switch_magic = True
    
    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        #define a imagem
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center) #evita q imagens de tamanhos diferentes tenham centros diferentes

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)