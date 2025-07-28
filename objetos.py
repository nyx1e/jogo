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

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        direction = player.direction
        self.image = pygame.Surface((25,25))
        if direction.x > 0:     #ataca em relação a direção q o player estava andando
            self.rect = self.image.get_rect(midleft = player.rect.midright)
        elif direction.x < 0:
            self.rect = self.image.get_rect(midright = player.rect.midleft)
        elif direction.y < 0:
            self.rect = self.image.get_rect(midbottom = player.rect.midtop)
        else: 
            self.rect = self.image.get_rect(midtop = player.rect.midbottom)