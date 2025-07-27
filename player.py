import pygame
from os.path import join
from os import walk
from spritesheet import Spritesheet

width,heigth = 900,500
FPS = 60
tamanho_bloco = 32

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack):
        super().__init__(groups)
        #base
        self.spritesheet = Spritesheet('assets/player/IDLE/idle_down.png')
        self.image = self.spritesheet.get_image(37, 24 , 19, 34, 1, (0,0,0))
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-15)
        #movimento
        self.direction = pygame.math.Vector2()
        self.speed = 5
        #atributos
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        #stats
        
        # self.load_assets()
        # self.state, self.frame_index = 'idle_dir', 0

    # def load_assets(self,state):
    #     self.animations = {'direita':[], 'esquerda': [], 'idle_dir':[], 'idle_esq':[], 'ataque_esq':[], 'ataque_esq':[], 'magica_esq':[], 'magica_dir':[]}

    #     for animation in self.animations.keys():
    #         for folder_path, sub_folder, file_name in walk(join('assets','player', state)):
    #             if file_name:
    #                 for pasta in sorted(file_name, key= lambda nome: int(nome.split('.')[0])):
    #                     full_path = join(folder_path, pasta)
    #                     surf = pygame.image.load(full_path).convert_alpha()
    #                     self.animations[state].append(surf)

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
                print('magic')
                

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

    def cooldowns(self):
        current_time = pygame.time.get_ticks() 
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()
            
    def update(self):
        self.input()
        self.cooldowns()
        self.move(self.speed)