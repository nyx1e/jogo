import pygame

width,heigth = 900,500
FPS = 60
tamanho_bloco = 32

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surf = pygame.Surface((tamanho_bloco,tamanho_bloco))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect
        if sprite_type == 'visible':
            self.hitbox = self.rect.inflate(0,-10)