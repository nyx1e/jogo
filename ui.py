import pygame

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
        pygame.draw.rect(self.display_surface, 'black', text_rect.inflate(10,10),2)

    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, 'red')
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, 'blue')
        self.show_exp(player.exp)