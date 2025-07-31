import pygame
from biblioteca import magic_data

width,heigth = 900,500
FPS = 60
tamanho_bloco = 32

barra_height = 20
health_width, energy_width = 200, 140
UI_font = 'assets/fonte/Eight-Bit Madness.ttf'
UI_size = 18

class UI: #tds atributos do player 
    def __init__(self):
        #geral
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_font, UI_size)
        #setup da barra
        self.health_bar_rect = pygame.Rect(10,10, health_width, barra_height)
        self.energy_bar_rect = pygame.Rect(10,35, energy_width, barra_height)
        #pegando graficos da magia
        self.magic_graphics = []
        for magic in magic_data.values():
            image = pygame.image.load(magic['grafico']).convert_alpha()
            magic = pygame.transform.scale(image, (35,35))
            self.magic_graphics.append(magic)

    def show_bar(self, current, max, bg_rect, color):
        #fundo da barra
        pygame.draw.rect(self.display_surface, 'black', bg_rect)
        #conversão pixel/stats
        ratio = current/max
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width
        #barra real
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, '#111111', bg_rect, 2)

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False,'#EEEEEE')
        text_rect = text_surf.get_rect(bottomright = (880, 480))
        pygame.draw.rect(self.display_surface, '#111111', text_rect.inflate(10,10))
        self.display_surface.blit(text_surf,text_rect)
        pygame.draw.rect(self.display_surface, '#5C5C5C', text_rect.inflate(10,10),2)

    def show_health(self, health):
        text_surf = self.font.render(str(int(health)), False,'#EEEEEE')
        text_rect = text_surf.get_rect(bottomright = (243, 26))
        pygame.draw.rect(self.display_surface, "#F55D5D", text_rect.inflate(10,10))
        self.display_surface.blit(text_surf,text_rect)
        pygame.draw.rect(self.display_surface, 'black', text_rect.inflate(10,10),2)
    
    def show_energy(self, energy):
        text_surf = self.font.render(str(int(energy)), False,'#EEEEEE')
        text_rect = text_surf.get_rect(bottomright = (175, 50))
        pygame.draw.rect(self.display_surface, "#727AEB", text_rect.inflate(10,10))
        self.display_surface.blit(text_surf,text_rect)
        pygame.draw.rect(self.display_surface, 'black', text_rect.inflate(10,10),2)

    def selection_box(self, left, top, has_switched):
        bg_rect = pygame.Rect(left, top, 60, 60)
        pygame.draw.rect(self.display_surface, "#111111", bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface, 'gold', bg_rect, 3)
        else: pygame.draw.rect(self.display_surface, '#5C5C5C', bg_rect, 3)
        return bg_rect

    def magic_overlay(self, magic_index, has_switched):
        bg_rect = self.selection_box(10,430,has_switched)
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center = bg_rect.center)
        self.display_surface.blit(magic_surf, magic_rect)

    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, 'red')
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, 'blue')
        self.show_exp(player.exp)
        self.show_health(player.health)
        self.show_energy(player.energy)
        self.magic_overlay(player.magic_index, not player.switch_magic)