import pygame
from player import Player
from objetos import *
from pytmx.util_pygame import load_pygame
from os.path import join
from ui import UI

width,heigth = 900,500
FPS = 60
tamanho_bloco = 32

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.create_map()
        self.current_attack = None
        #interface jogador
        self.ui = UI()

    def create_map(self):
        mapa = load_pygame(join('assets', 'mapa', 'mundo3.tmx'))
        
        for obj in mapa.get_layer_by_name('objetos'):
            Tile((obj.x, obj.y), [self.visible_sprites, self.obstacle_sprites], 'visible', obj.image)
        for obj in mapa.get_layer_by_name('limites'):
            Tile((obj.x, obj.y), [self.obstacle_sprites], 'invisible', pygame.Surface((obj.width, obj.height)))
        for persona in mapa.get_layer_by_name('personagens'):
            if persona.name == 'jogador':
                self.player = Player((persona.x,persona.y), [self.visible_sprites], self.obstacle_sprites, self.create_attack, self.destroy_attack)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites])
    
    # def create_magic(self, style, strength, cost):
    #     print(style, strength, cost)

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None
    
    def run(self):
        #update/draw jogo
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.ui.display(self.player)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        #chao
        self.floor_surf = pygame.image.load('assets/mapa/chao.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

    def custom_draw(self, player): #camera e ordem de desenho dos sprites
        self.offset.x = -(player.rect.centerx - width//2) #pega o centro do player e o centro da tela 
        self.offset.y = -(player.rect.centery - heigth//2)
        self.display_surface.blit(self.floor_surf, self.floor_rect.topleft + self.offset)
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery): #compara centro sprites/player
            self.display_surface.blit(sprite.image,sprite.rect.topleft + self.offset)