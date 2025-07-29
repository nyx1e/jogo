import pygame

width,heigth = 900,500
FPS = 60
tamanho_bloco = 32

class MagicPlayer:
    def __init__(self, animation_player):
        self.animation_player = animation_player
    
    def heal(self, player, strength, cost, groups):
        if player.energy >= cost:
            player.health += strength
            player.energy -= cost
            if player.health >= player.stats['health']:
                player.health = player.stats['health']
            self.animation_player.create_particles('heal', player.rect.center, groups)

    def flame(self, player, cost, groups):
        if player.energy >= cost:
            player.energy -= cost
            if player.status.split('_')[0] == 'right': direction = pygame.math.Vector2(1,0)
            elif player.status.split('_')[0] == 'left': direction = pygame.math.Vector2(-1,0)
            elif player.status.split('_')[0] == 'down': direction = pygame.math.Vector2(0,1)
            else: direction = pygame.math.Vector2(0,-1)

            for i in range(1,6):
                if direction.x :
                    offset_x = (direction.x * i)* tamanho_bloco
                    x = player.rect.centerx + offset_x
                    y = player.rect.centery
                    self.animation_player.create_particles('flame', (x,y), groups)
                else:
                    offset_y = (direction.y * i)* tamanho_bloco
                    y = player.rect.centery + offset_y
                    x = player.rect.centerx
                    self.animation_player.create_particles('flame', (x,y), groups)

    def raio(self, player, cost, groups):
        if player.energy >= cost:
            player.energy -= cost
            if player.status.split('_')[0] == 'right': direction = pygame.math.Vector2(1,0)
            elif player.status.split('_')[0] == 'left': direction = pygame.math.Vector2(-1,0)
            elif player.status.split('_')[0] == 'down': direction = pygame.math.Vector2(0,1)
            else: direction = pygame.math.Vector2(0,-1)

            for i in range(1,6):
                if direction.x :
                    offset_x = (direction.x * i)* tamanho_bloco
                    x = player.rect.centerx + offset_x
                    y = player.rect.centery
                    self.animation_player.create_particles('horizontal', (x,y), groups)
                else:
                    offset_y = (direction.y * i)* tamanho_bloco
                    y = player.rect.centery + offset_y
                    x = player.rect.centerx
                    self.animation_player.create_particles('vertical', (x,y), groups)