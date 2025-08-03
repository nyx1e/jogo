import pygame
from player import Player
from objetos import *
from pytmx.util_pygame import load_pygame
from os.path import join
from ui import UI
from inimigos import Inimigos
from particulas import AnimationPlayer
from magica import MagicPlayer
from upgrade import Upgrade

width,heigth = 900,500
FPS = 60
tamanho_bloco = 32

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('assets/fonte/Eight-Bit Madness.ttf', 25)
        self.game_paused = False
        self.gameover = False
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.enemy = []
        self.create_map()
        #interface jogador
        self.ui = UI()
        self.upgrade = Upgrade(self.player)
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)
        #gameover
        self.gameover_image = pygame.image.load('assets/gameover.png').convert_alpha()
        self.gameover_rect = self.gameover_image.get_rect(center = (width/2,heigth/2))
        self.over_text = self.font.render(f'Press SPACE to restart', False, 'black')
        self.over_rect = self.over_text.get_rect(center = (width/2, 400))
        #victory
        self.victory_image = pygame.image.load('assets/victory.png').convert_alpha()
        self.victory_image = pygame.transform.scale(self.victory_image, (350, 300))
        self.victory_rect = self.victory_image.get_rect(center = (width/2,heigth/2 - 25))
        self.victory_text = self.font.render(f'Press SPACE to restart', False, 'black')
        self.victory_text_rect = self.victory_text.get_rect(center = (width/2, 400))
        #trilha
        self.trilha_sonora = pygame.mixer.Sound('assets/sons/A Carousing Consort - La Volte du Roy.mp3')
        self.trilha_sonora.play(loops = -1)
        self.trilha_sonora.set_volume(0.05)

    def create_map(self):
        self.mapa = load_pygame(join('assets', 'mapa', 'mundo.tmx'))
        
        for x, y, image in self.mapa.get_layer_by_name('solo').tiles():
            Sprite((x * tamanho_bloco, y * tamanho_bloco), image, self.visible_sprites)
        for x, y, image in self.mapa.get_layer_by_name('relevo').tiles():
            Sprite((x * tamanho_bloco, y * tamanho_bloco), image, self.visible_sprites)
        for obj in self.mapa.get_layer_by_name('objetos'):
            if obj.name == 'arbusto':
                ColisaoCenario((obj.x, obj.y), [self.visible_sprites], 'objeto', obj.image)
            else:
                ColisaoCenario((obj.x, obj.y), [self.visible_sprites, self.obstacle_sprites], 'objeto', obj.image)
        for obj in self.mapa.get_layer_by_name('limites'):
            ColisaoCenario((obj.x, obj.y),  self.obstacle_sprites, 'limite', pygame.Surface((obj.width, obj.height)))
        for persona in self.mapa.get_layer_by_name('personagens'):
            if persona.name == 'jogador':
                self.player = Player((persona.x,persona.y), [self.visible_sprites], 
                    self.obstacle_sprites, self.create_attack, self.destroy_attack, self.create_magic)
            if persona.name == 'slime':
                self.slime = Inimigos('slime', (persona.x, persona.y), [self.visible_sprites, self.attackable_sprites], 
                    self.obstacle_sprites, self.damage_player, self.ativar_particulas_morte, self.add_exp)
                self.enemy.append(self.slime)
            if persona.name == 'goblin':
                self.canines = Inimigos('canines', (persona.x, persona.y), [self.visible_sprites, self.attackable_sprites], 
                    self.obstacle_sprites, self.damage_player, self.ativar_particulas_morte, self.add_exp)
                self.enemy.append(self.canines)
            # if persona.name == 'boss':
            #     self.enemie = Inimigos('boss', (persona.x, persona.y), [self.visible_sprites, self.attackable_sprites],
            #  self.obstacle_sprites, self.damage_player, self.ativar_particulas_morte, self.add_exp)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.attack_sprites])
    
    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])
        if style == 'flame':
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])
        if style == 'raio':
            self.magic_player.raio(self.player, cost, [self.visible_sprites, self.attack_sprites])
        
    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None
    
    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()

    def ativar_particulas_morte(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, self.visible_sprites)      

    def add_exp(self, amount):
        self.player.exp += amount

    def menu_pausa(self):
        self.game_paused = not self.game_paused

    def create_gameover(self):
        if self.player.health <= 0:
            self.gameover = True

    def restart(self):
        self.gameover = False
        self.player.health = 100
        self.player.energy = 60
        self.player.exp = 100
        self.player.speed = 5
        self.player.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 5}
        self.player.max_stats = {'health': 300, 'energy': 140, 'attack': 20, 'magic': 10, 'speed': 10}
        self.player.upgrade_cost = {'health': 100, 'energy': 100, 'attack': 100, 'magic': 100, 'speed': 100}
        for i in range(len(self.enemy)):
            self.enemy[i].kill()
        for persona in self.mapa.get_layer_by_name('personagens'):
            if persona.name == 'jogador':
                self.player = Player((persona.x,persona.y), [self.visible_sprites], 
                    self.obstacle_sprites, self.create_attack, self.destroy_attack, self.create_magic)
                self.upgrade = Upgrade(self.player)
            if persona.name == 'slime':
                self.slime = Inimigos('slime', (persona.x, persona.y), [self.visible_sprites, self.attackable_sprites], 
                    self.obstacle_sprites, self.damage_player, self.ativar_particulas_morte, self.add_exp)
                self.enemy.append(self.slime)
            if persona.name == 'goblin':
                self.canines = Inimigos('canines', (persona.x, persona.y), [self.visible_sprites, self.attackable_sprites], 
                    self.obstacle_sprites, self.damage_player, self.ativar_particulas_morte, self.add_exp)
                self.enemy.append(self.canines)
  

    def run(self):
        #update/draw jogo
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)
        if self.gameover:
            self.display_surface.blit(self.gameover_image, self.gameover_rect)
            self.display_surface.blit(self.over_text, self.over_rect)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.restart()
        elif self.game_paused:
            self.upgrade.display()
        elif all(enemy.health <= 0 for enemy in self.enemy): #ambos fazem a msm coisa
            self.display_surface.blit(self.victory_image, self.victory_rect)
            self.display_surface.blit(self.victory_text, self.victory_text_rect)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.restart()
        else:  
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()
            self.create_gameover()
        
class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        #desenha o chão sem atrapalhar a lógica do ysort
        # self.floor_surf = pygame.image.load('assets/mapa/mundo.png').convert()
        # self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

    def custom_draw(self, player): #camera e ordem de desenho dos sprites
        self.offset.x = -(player.rect.centerx - width//2) #pega o centro do player e o centro da tela 
        self.offset.y = -(player.rect.centery - heigth//2)
        sprites_chao = [sprite for sprite in self if hasattr(sprite, 'chao')] #chao tem q ser desenhado antes dos objetos
        sprite_objetos = [sprite for sprite in self if not hasattr(sprite, 'chao')]
        for camada in [sprites_chao, sprite_objetos]:           #ordena draw sprites
            for sprite in sorted(camada, key= lambda sprite: sprite.rect.centery): #compara a localização dos centros dos sprites
                self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)

    def enemy_update(self, player): #p/ atualizar só inimigos
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)